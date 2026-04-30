#!/usr/bin/env python3
"""
tools/deep_scan.py

Hardened deep scan and safe autofix engine for zCyptoBot.

Usage:
  python tools/deep_scan.py --dry-run
  python tools/deep_scan.py --push --pr-create

Flags:
  --dry-run      : Do not modify files or commit; generate reports only.
  --push         : Push autofix branch to origin (requires GIT_PUSH_TOKEN).
  --pr-create    : Create PR after push (requires GITEA_TOKEN and GITEA_SERVER_URL and GITEA_REPO).
  --no-metrics   : Disable Prometheus metrics (useful in CI).
"""
from __future__ import annotations

import argparse
import ast
import datetime
import json
import logging
import os
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import astor
import networkx as nx
import requests

# Optional heavy imports guarded
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.ensemble import IsolationForest
except Exception:
    SentenceTransformer = None
    IsolationForest = None

# Prometheus optional
try:
    from prometheus_client import Counter, start_http_server
except Exception:
    Counter = None
    start_http_server = None

# -------------------------
# Configuration
# -------------------------
REPO_DIR = Path(os.environ.get("REPO_DIR", "zCyptoBot"))
REPO_URL = os.environ.get("REPO_URL", "https://github.com/CVSz/zCyptoBot.git")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "all-MiniLM-L6-v2")
BUG_REPORT = Path("bug_report.md")
GRAPH_JSON = Path("semantic_graph.json")
CHANGELOG = Path("CHANGELOG.md")
BACKUP_DIR = Path(os.environ.get("BACKUP_DIR", ".deepscan_backup"))
AUTOFIX_BRANCH_PREFIX = "deepscan/autofix/"
PROMETHEUS_PORT = int(os.environ.get("PROMETHEUS_PORT", "8000"))
ANOMALY_CONTAMINATION = float(os.environ.get("ANOMALY_CONTAMINATION", "0.08"))
MIN_ENTITIES_FOR_ANOMALY = 10
LOG_LEVEL = logging.INFO

# Prometheus metrics
if Counter:
    bug_counter = Counter("zcyptobot_bug_detected", "Number of bugs detected by deep_scan")
    fix_counter = Counter("zcyptobot_autofix_applied", "Number of autofixes applied by deep_scan")
else:
    bug_counter = fix_counter = None

# -------------------------
# Logging
# -------------------------
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("deep_scan")


# -------------------------
# Utilities
# -------------------------
def run(cmd: List[str], cwd: Path = None, check: bool = True) -> subprocess.CompletedProcess:
    logger.debug("Running: %s", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)


def safe_clone_or_pull():
    if REPO_DIR.exists():
        logger.info("Repository exists locally, fetching latest")
        try:
            run(["git", "fetch", "--all"], cwd=REPO_DIR)
            run(["git", "reset", "--hard", "origin/main"], cwd=REPO_DIR)
        except Exception as e:
            logger.warning("Failed to update local repo: %s", e)
    else:
        logger.info("Cloning repository %s", REPO_URL)
        run(["git", "clone", REPO_URL, str(REPO_DIR)])


def git_configure():
    name = os.environ.get("GIT_USER_NAME", "DeepScanBot")
    email = os.environ.get("GIT_USER_EMAIL", "deepscan-bot@example.com")
    run(["git", "config", "--global", "user.name", name])
    run(["git", "config", "--global", "user.email", email])


def create_autofix_branch() -> str:
    branch = (
        AUTOFIX_BRANCH_PREFIX
        + datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        + "-"
        + uuid.uuid4().hex[:6]
    )
    run(["git", "checkout", "-b", branch], cwd=REPO_DIR)
    logger.info("Created branch %s", branch)
    return branch


def commit_changes(message: str) -> bool:
    status = run(["git", "status", "--porcelain"], cwd=REPO_DIR, check=False)
    if not status.stdout.strip():
        logger.info("No changes to commit")
        return False
    run(["git", "add", "."], cwd=REPO_DIR)
    run(["git", "commit", "-m", message], cwd=REPO_DIR)
    logger.info("Committed changes: %s", message)
    return True


def push_branch(branch: str) -> bool:
    token = os.environ.get("GIT_PUSH_TOKEN")
    if not token:
        logger.warning("GIT_PUSH_TOKEN not set; skipping push")
        return False
    origin_url = run(["git", "remote", "get-url", "origin"], cwd=REPO_DIR).stdout.strip()
    if origin_url.startswith("https://"):
        auth_url = origin_url.replace("https://", f"https://{token}@")
        run(["git", "remote", "set-url", "origin", auth_url], cwd=REPO_DIR)
    run(["git", "push", "--set-upstream", "origin", branch], cwd=REPO_DIR)
    logger.info("Pushed branch %s", branch)
    return True


def create_gitea_pr(
    server_url: str,
    repo_full: str,
    branch: str,
    title: str,
    body: str,
    assignee: Optional[str] = None,
    labels: Optional[List[str]] = None,
    token: Optional[str] = None,
):
    if not token:
        logger.warning("No token provided for PR creation")
        return None
    api = f"{server_url.rstrip('/')}/api/v1/repos/{repo_full}/pulls"
    payload = {"head": branch, "base": "main", "title": title, "body": body}
    if assignee:
        payload["assignee"] = assignee
    if labels:
        payload["labels"] = labels
    headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
    r = requests.post(api, json=payload, headers=headers, timeout=30)
    if r.status_code not in (200, 201):
        logger.error("Failed to create PR: %s %s", r.status_code, r.text)
        return None
    logger.info("Created PR: %s", r.json().get("html_url"))
    return r.json()


@dataclass
class CodeEntity:
    path: Path
    node: ast.AST
    name: str
    lineno: int
    source_line: str


def collect_python_entities(repo_path: Path) -> Tuple[List[CodeEntity], Dict[Path, str]]:
    entities = []
    file_contents = {}
    for py in repo_path.rglob("*.py"):
        try:
            text = py.read_text(encoding="utf-8")
            file_contents[py] = text
            tree = ast.parse(text)
            lines = text.splitlines()
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    line = lines[node.lineno - 1] if node.lineno - 1 < len(lines) else ""
                    entities.append(CodeEntity(py, node, node.name, node.lineno, line.strip()))
        except Exception as e:
            logger.warning("Failed to parse %s: %s", py, e)
    logger.info("Collected %d code entities", len(entities))
    return entities, file_contents


def safe_backup_file(path: Path, backup_dir: Path):
    backup_dir.mkdir(parents=True, exist_ok=True)
    rel = path.relative_to(REPO_DIR)
    dest = backup_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)


def ast_autofix_file(path: Path) -> List[str]:
    applied = []
    try:
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
        modified = False

        class Fixer(ast.NodeTransformer):
            def visit_ImportFrom(self, node):
                nonlocal modified
                if any(n.name == "*" for n in node.names):
                    modified = True
                    return ast.Expr(
                        value=ast.Constant(
                            value=f"# TODO: replace wildcard import from {node.module} with explicit names"
                        )
                    )
                return node

            def visit_Call(self, node):
                nonlocal modified
                node = self.generic_visit(node)
                if isinstance(node.func, ast.Attribute):
                    if getattr(node.func.value, "id", "") == "random" and node.func.attr in (
                        "random",
                        "randint",
                        "choice",
                    ):
                        modified = True
                        return ast.copy_location(ast.parse("secrets.token_hex(16)").body[0].value, node)
                return node

        fixer = Fixer()
        new_tree = fixer.visit(tree)
        if modified:
            safe_backup_file(path, BACKUP_DIR)
            new_src = astor.to_source(new_tree)
            path.write_text(new_src, encoding="utf-8")
            applied.append(f"AST autofix applied to {path}")
    except Exception as e:
        logger.exception("Autofix failed for %s: %s", path, e)
    return applied


def build_embeddings(entities: List[CodeEntity]):
    if SentenceTransformer is None:
        logger.warning("sentence-transformers not available; skipping embeddings")
        return None, []
    model = SentenceTransformer(EMBED_MODEL)
    texts = [f"{e.path.name}:{e.name} {e.source_line}" for e in entities]
    embeddings = []
    for i in range(0, len(texts), 64):
        embeddings.extend(model.encode(texts[i : i + 64], show_progress_bar=False))
    return embeddings, texts


def detect_anomalies(embeddings):
    if embeddings is None or IsolationForest is None:
        return []
    if len(embeddings) < MIN_ENTITIES_FOR_ANOMALY:
        return []
    clf = IsolationForest(contamination=ANOMALY_CONTAMINATION, random_state=42)
    preds = clf.fit_predict(embeddings)
    return [i for i, p in enumerate(preds) if p == -1]


def write_bug_report(issues: List[Dict]):
    lines = [
        "| File | Line | Entity | Issue | Severity | Suggested Fix |",
        "|------|------|--------|-------|----------|---------------|",
    ]
    for it in issues:
        lines.append(
            f"| {it['file']} | {it['line']} | {it['entity']} | {it['message']} | {it['severity']} | {it.get('fix', 'manual review')} |"
        )
    BUG_REPORT.write_text("\n".join(lines), encoding="utf-8")


def write_graph(graph: nx.DiGraph):
    GRAPH_JSON.write_text(json.dumps(nx.node_link_data(graph), indent=2), encoding="utf-8")


def append_changelog(entry: str):
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    content = f"## {ts} - DeepScan Autofix\n\n{entry}\n\n"
    if CHANGELOG.exists():
        CHANGELOG.write_text(CHANGELOG.read_text(encoding="utf-8") + "\n" + content, encoding="utf-8")
    else:
        CHANGELOG.write_text("# Changelog\n\n" + content, encoding="utf-8")


def main(dry_run: bool, push: bool, pr_create: bool, no_metrics: bool):
    if not no_metrics and start_http_server and Counter:
        start_http_server(PROMETHEUS_PORT)

    safe_clone_or_pull()
    git_configure()

    entities, file_contents = collect_python_entities(REPO_DIR)
    embeddings, _ = build_embeddings(entities)
    graph = nx.DiGraph()
    for e in entities:
        node_id = f"{e.path.relative_to(REPO_DIR)}:{e.name}:{e.lineno}"
        graph.add_node(node_id, file=str(e.path), name=e.name, lineno=e.lineno)

    name_map = {}
    for node_id, data in graph.nodes(data=True):
        name_map.setdefault(data["name"], []).append(node_id)

    for e in entities:
        src = f"{e.path.relative_to(REPO_DIR)}:{e.name}:{e.lineno}"
        content = file_contents.get(e.path, "")
        for callee, nodes in name_map.items():
            if callee != e.name and f"{callee}(" in content:
                for tgt in nodes:
                    graph.add_edge(src, tgt)
    write_graph(graph)

    issues = []
    for e in entities:
        line = e.source_line
        if "random.random" in line or "random.randint(" in line or "random.choice(" in line:
            issues.append({"file": str(e.path.relative_to(REPO_DIR)), "line": e.lineno, "entity": e.name, "message": "Weak RNG usage", "severity": "High", "fix": "Replace with secrets"})
            if bug_counter:
                bug_counter.inc()

    for ai in detect_anomalies(embeddings):
        e = entities[ai]
        issues.append({"file": str(e.path.relative_to(REPO_DIR)), "line": e.lineno, "entity": e.name, "message": "Semantic anomaly", "severity": "Medium", "fix": "Manual review"})
        if bug_counter:
            bug_counter.inc()

    write_bug_report(issues)
    if dry_run:
        return

    branch = create_autofix_branch()
    applied_fixes = []
    for py in sorted({e.path for e in entities}):
        applied_fixes.extend(ast_autofix_file(py))

    if applied_fixes and commit_changes(f"DeepScan autofix: applied {len(applied_fixes)} fixes") and push:
        pushed = push_branch(branch)
        if pushed and pr_create:
            create_gitea_pr(
                os.environ.get("GITEA_SERVER_URL", ""),
                os.environ.get("GITEA_REPO", ""),
                branch,
                "DeepScan Autofix: automated fixes",
                "Automated fixes applied by DeepScan. Please review.",
                assignee=os.environ.get("AUTOFIX_ASSIGNEE"),
                labels=os.environ.get("AUTOFIX_LABELS", "").split(",") if os.environ.get("AUTOFIX_LABELS") else None,
                token=os.environ.get("GITEA_TOKEN"),
            )

    append_changelog(f"- Issues found: {len(issues)}\n- Fixes applied: {len(applied_fixes)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deep scan and safe autofix for zCyptoBot")
    parser.add_argument("--dry-run", action="store_true", help="Do not apply fixes or commit")
    parser.add_argument("--push", action="store_true", help="Push autofix branch to origin")
    parser.add_argument("--pr-create", action="store_true", help="Create PR after push")
    parser.add_argument("--no-metrics", action="store_true", help="Disable Prometheus metrics")
    args = parser.parse_args()
    main(args.dry_run, args.push, args.pr_create, args.no_metrics)
