#!/usr/bin/env python3
"""
tools/deep_scan.py

Hardened deep scan and safe autofix engine for zCyptoBot.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from datetime import UTC, datetime
import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
from typing import Any, Dict, List, Tuple
from urllib import error as urllib_error
from urllib import request as urllib_request
import uuid

import networkx as nx

try:
    import astor
except Exception:
    astor = None

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.ensemble import IsolationForest
except Exception:
    SentenceTransformer = None
    IsolationForest = None

try:
    from prometheus_client import Counter, start_http_server
except Exception:
    Counter = None
    start_http_server = None

REPO_URL = os.environ.get("REPO_URL", "https://github.com/CVSz/zCyptoBot.git")
REPO_DIR = Path(os.environ.get("REPO_DIR", "zCyptoBot"))
BUG_REPORT = Path("bug_report.md")
GRAPH_JSON = Path("semantic_graph.json")
CHANGELOG = Path("CHANGELOG.md")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "all-MiniLM-L6-v2")
PROMETHEUS_PORT = int(os.environ.get("PROMETHEUS_PORT", "8000"))
AUTOFIX_BRANCH_PREFIX = "deepscan/autofix/"
ANOMALY_CONTAMINATION = float(os.environ.get("ANOMALY_CONTAMINATION", "0.08"))
MIN_ENTITIES_FOR_ANOMALY = int(os.environ.get("MIN_ENTITIES_FOR_ANOMALY", "10"))
BACKUP_DIR = Path(os.environ.get("BACKUP_DIR", ".deepscan_backup"))

if Counter:
    bug_counter = Counter("zcyptobot_bug_detected", "Number of bugs detected by deep_scan")
    fix_counter = Counter("zcyptobot_autofix_applied", "Number of autofixes applied by deep_scan")
else:
    bug_counter = None
    fix_counter = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("deep_scan")


def run(cmd: List[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)


def safe_clone_or_pull() -> None:
    if REPO_DIR.exists():
        try:
            run(["git", "fetch", "--all"], cwd=REPO_DIR)
            run(["git", "reset", "--hard", "origin/main"], cwd=REPO_DIR)
        except Exception as exc:
            logger.warning("Failed to update local repo: %s", exc)
    else:
        run(["git", "clone", REPO_URL, str(REPO_DIR)])


def git_configure() -> None:
    run(["git", "config", "--global", "user.name", os.environ.get("GIT_USER_NAME", "DeepScanBot")])
    run(["git", "config", "--global", "user.email", os.environ.get("GIT_USER_EMAIL", "deepscan-bot@example.com")])


def create_autofix_branch() -> str:
    branch = AUTOFIX_BRANCH_PREFIX + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    run(["git", "checkout", "-b", branch], cwd=REPO_DIR)
    return branch


def commit_changes(message: str) -> bool:
    status = run(["git", "status", "--porcelain"], cwd=REPO_DIR, check=False)
    if not status.stdout.strip():
        logger.info("No changes to commit")
        return False
    run(["git", "add", "."], cwd=REPO_DIR)
    run(["git", "commit", "-m", message], cwd=REPO_DIR)
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
    return True


def create_gitea_pr(server_url: str, repo_full: str, branch: str, title: str, body: str, token: str, assignee: str | None = None, labels: List[str] | None = None) -> dict[str, Any] | None:
    api = f"{server_url.rstrip('/')}/api/v1/repos/{repo_full}/pulls"
    payload: dict[str, Any] = {"head": branch, "base": "main", "title": title, "body": body}
    if assignee:
        payload["assignee"] = assignee
    if labels:
        payload["labels"] = labels
    headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib_request.Request(api, data=data, headers=headers, method="POST")
    try:
        with urllib_request.urlopen(req, timeout=30) as response:
            status = response.getcode()
            raw = response.read().decode("utf-8")
            if status not in (200, 201):
                logger.error("Failed to create PR: %s %s", status, raw)
                return None
            return json.loads(raw) if raw else {}
    except urllib_error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        logger.error("Failed to create PR: %s %s", exc.code, err_body)
    except urllib_error.URLError as exc:
        logger.error("Failed to create PR request: %s", exc.reason)
    return None


@dataclass
class CodeEntity:
    path: Path
    node: ast.AST
    name: str
    lineno: int
    source_line: str


def collect_python_entities(repo_path: Path) -> Tuple[List[CodeEntity], Dict[Path, str]]:
    entities: List[CodeEntity] = []
    file_contents: Dict[Path, str] = {}
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
        except Exception as exc:
            logger.warning("Failed to parse %s: %s", py, exc)
    return entities, file_contents


def safe_backup_file(path: Path) -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    rel = path.relative_to(REPO_DIR)
    dest = BACKUP_DIR / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dest)


def ast_autofix_file(path: Path) -> List[str]:
    if astor is None:
        return []
    applied: List[str] = []
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    modified = False

    class Fixer(ast.NodeTransformer):
        def visit_ImportFrom(self, node: ast.ImportFrom):
            nonlocal modified
            if any(n.name == "*" for n in node.names):
                modified = True
                return ast.copy_location(
                    ast.Expr(value=ast.Constant(value=f"TODO: replace wildcard import from {node.module} with explicit names")),
                    node,
                )
            return node

        def visit_Call(self, node: ast.Call):
            nonlocal modified
            if isinstance(node.func, ast.Attribute):
                if getattr(node.func.value, "id", "") == "random" and node.func.attr in ("random", "randint", "choice"):
                    modified = True
                    return ast.copy_location(ast.parse("secrets.token_hex(16)").body[0].value, node)
            return self.generic_visit(node)

        def visit_FunctionDef(self, node: ast.FunctionDef):
            nonlocal modified
            has_yield = any(isinstance(n, (ast.Yield, ast.YieldFrom)) for n in ast.walk(node))
            has_try = any(isinstance(n, ast.Try) for n in node.body)
            if not has_yield and not has_try:
                modified = True
                node.body = [
                    ast.Try(
                        body=node.body,
                        handlers=[
                            ast.ExceptHandler(
                                type=ast.Name(id="Exception", ctx=ast.Load()),
                                name="e",
                                body=[ast.parse("import logging").body[0], ast.parse("logging.exception('DeepScan caught exception: %s', e)").body[0], ast.Raise()],
                            )
                        ],
                        orelse=[],
                        finalbody=[],
                    )
                ]
            return node

    new_tree = Fixer().visit(tree)
    ast.fix_missing_locations(new_tree)
    if modified:
        safe_backup_file(path)
        path.write_text(astor.to_source(new_tree), encoding="utf-8")
        applied.append(f"AST autofix applied to {path}")
    return applied


def build_embeddings(entities: List[CodeEntity]):
    if SentenceTransformer is None:
        return None
    model = SentenceTransformer(EMBED_MODEL)
    texts = [f"{e.path.name}:{e.name} {e.source_line}" for e in entities]
    embeddings = []
    for i in range(0, len(texts), 64):
        embeddings.extend(model.encode(texts[i : i + 64], show_progress_bar=False))
    return embeddings


def detect_anomalies(embeddings) -> List[int]:
    if embeddings is None or IsolationForest is None or len(embeddings) < MIN_ENTITIES_FOR_ANOMALY:
        return []
    clf = IsolationForest(contamination=ANOMALY_CONTAMINATION, random_state=42)
    return [i for i, p in enumerate(clf.fit_predict(embeddings)) if p == -1]


def write_bug_report(issues: List[Dict[str, Any]]) -> None:
    lines = ["| File | Line | Entity | Issue | Severity | Suggested Fix |", "|------|------|--------|-------|----------|---------------|"]
    for issue in issues:
        lines.append(f"| {issue['file']} | {issue['line']} | {issue['entity']} | {issue['message']} | {issue['severity']} | {issue.get('fix', 'manual review')} |")
    BUG_REPORT.write_text("\n".join(lines), encoding="utf-8")


def write_graph_json(graph: nx.DiGraph) -> None:
    GRAPH_JSON.write_text(json.dumps(nx.node_link_data(graph), indent=2), encoding="utf-8")


def append_changelog(entry: str) -> None:
    ts = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    block = f"## {ts} - DeepScan Autofix\n\n{entry}\n\n"
    if CHANGELOG.exists():
        CHANGELOG.write_text(CHANGELOG.read_text(encoding="utf-8") + "\n" + block, encoding="utf-8")
    else:
        CHANGELOG.write_text("# Changelog\n\n" + block, encoding="utf-8")


def main(dry_run: bool, push: bool, pr_create: bool, no_metrics: bool) -> int:
    if not no_metrics and start_http_server and Counter:
        start_http_server(PROMETHEUS_PORT)

    safe_clone_or_pull()
    git_configure()
    entities, file_contents = collect_python_entities(REPO_DIR)
    embeddings = build_embeddings(entities)

    graph = nx.DiGraph()
    for entity in entities:
        node_id = f"{entity.path.relative_to(REPO_DIR)}:{entity.name}:{entity.lineno}"
        graph.add_node(node_id, file=str(entity.path), name=entity.name, lineno=entity.lineno)
    write_graph_json(graph)

    issues: List[Dict[str, Any]] = []
    for entity in entities:
        line = entity.source_line
        if "random.random" in line or "random.randint(" in line or "random.choice(" in line:
            issues.append({"file": str(entity.path.relative_to(REPO_DIR)), "line": entity.lineno, "entity": entity.name, "message": "Weak RNG usage", "severity": "High", "fix": "Replace with secrets"})
        if "import *" in line:
            issues.append({"file": str(entity.path.relative_to(REPO_DIR)), "line": entity.lineno, "entity": entity.name, "message": "Wildcard import", "severity": "Medium", "fix": "Replace with explicit imports"})
        if "hashlib.md5" in line or "sha1" in line:
            issues.append({"file": str(entity.path.relative_to(REPO_DIR)), "line": entity.lineno, "entity": entity.name, "message": "Weak hash usage", "severity": "High", "fix": "Use SHA256+"})

    for idx in detect_anomalies(embeddings):
        e = entities[idx]
        issues.append({"file": str(e.path.relative_to(REPO_DIR)), "line": e.lineno, "entity": e.name, "message": "Semantic anomaly", "severity": "Medium", "fix": "Manual review"})

    write_bug_report(issues)
    if dry_run:
        return 0

    branch = create_autofix_branch()
    applied_fixes: List[str] = []
    for py in {e.path for e in entities}:
        applied_fixes.extend(ast_autofix_file(py))

    committed = commit_changes(f"DeepScan autofix: applied {len(applied_fixes)} fixes") if applied_fixes else False
    if committed and push:
        pushed = push_branch(branch)
        if pushed and pr_create:
            token = os.environ.get("GITEA_TOKEN")
            gitea_url = os.environ.get("GITEA_SERVER_URL")
            gitea_repo = os.environ.get("GITEA_REPO")
            if token and gitea_url and gitea_repo:
                create_gitea_pr(gitea_url, gitea_repo, branch, "DeepScan Autofix: automated fixes", "Automated fixes applied by DeepScan.", token, os.environ.get("AUTOFIX_ASSIGNEE"), os.environ.get("AUTOFIX_LABELS", "").split(",") if os.environ.get("AUTOFIX_LABELS") else None)

    append_changelog(f"- Issues found: {len(issues)}\n- Fixes applied: {len(applied_fixes)}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deep scan and safe autofix for zCyptoBot")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--pr-create", action="store_true")
    parser.add_argument("--no-metrics", action="store_true")
    args = parser.parse_args()
    raise SystemExit(main(args.dry_run, args.push, args.pr_create, args.no_metrics))
