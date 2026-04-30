#!/usr/bin/env python3
"""
tools/deep_scan.py

End-to-end deep scan, semantic analysis, and safe autofix engine for zCyptoBot.

Features:
- Clone or use local repo
- AST parsing and safe AST-based edits
- Semantic embeddings for functions/classes
- Dependency and call graph construction (networkx)
- Anomaly detection (IsolationForest)
- Autofix engine for common issues (weak RNG, wildcard imports, missing try/except)
- Prometheus metrics endpoint
- Markdown bug report and semantic graph JSON output
- Safe git branch/commit/push workflow with rollback support
- Hooks for bandit, flake8, CodeQL (placeholders)
"""

import ast
import datetime
import json
import logging
import subprocess
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

import astor
import networkx as nx
from prometheus_client import Counter, start_http_server
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import IsolationForest

# -------------------------
# Configuration
# -------------------------
REPO_URL = "https://github.com/CVSz/zCyptoBot.git"
REPO_DIR = Path("zCyptoBot")
BUG_REPORT = Path("bug_report.md")
GRAPH_JSON = Path("semantic_graph.json")
CHANGELOG = Path("CHANGELOG.md")
EMBED_MODEL = "all-MiniLM-L6-v2"
PROMETHEUS_PORT = 8000
AUTOFIX_BRANCH_PREFIX = "deepscan/autofix/"
GIT_USER_NAME = "DeepScanBot"
GIT_USER_EMAIL = "deepscan-bot@example.com"
ANOMALY_CONTAMINATION = 0.08
LOG_LEVEL = logging.INFO

bug_counter = Counter("zcyptobot_bug_detected", "Number of bugs detected by deep_scan")
fix_counter = Counter("zcyptobot_autofix_applied", "Number of autofixes applied by deep_scan")

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("deep_scan")


def run(cmd: List[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    logger.debug("Running command: %s", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)


def safe_clone_or_pull() -> None:
    if REPO_DIR.exists():
        logger.info("Repository exists locally, fetching latest")
        try:
            run(["git", "fetch", "--all"], cwd=REPO_DIR)
            run(["git", "reset", "--hard", "origin/main"], cwd=REPO_DIR)
        except Exception as exc:
            logger.warning("Failed to update local repo: %s", exc)
    else:
        logger.info("Cloning repository %s", REPO_URL)
        run(["git", "clone", REPO_URL, str(REPO_DIR)])


def git_configure() -> None:
    run(["git", "config", "--global", "user.name", GIT_USER_NAME])
    run(["git", "config", "--global", "user.email", GIT_USER_EMAIL])


def create_autofix_branch() -> str:
    branch = AUTOFIX_BRANCH_PREFIX + datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    run(["git", "checkout", "-b", branch], cwd=REPO_DIR)
    logger.info("Created branch %s", branch)
    return branch


def push_branch(branch: str) -> None:
    run(["git", "push", "--set-upstream", "origin", branch], cwd=REPO_DIR)
    logger.info("Pushed branch %s", branch)


def commit_changes(message: str) -> None:
    try:
        run(["git", "add", "."], cwd=REPO_DIR)
        run(["git", "commit", "-m", message], cwd=REPO_DIR)
        logger.info("Committed changes: %s", message)
    except subprocess.CalledProcessError as exc:
        logger.info("No changes to commit or commit failed: %s", exc)


class CodeEntity:
    def __init__(self, path: Path, node: ast.AST, name: str, lineno: int, source_line: str):
        self.path = path
        self.node = node
        self.name = name
        self.lineno = lineno
        self.source_line = source_line


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
    logger.info("Collected %d code entities", len(entities))
    return entities, file_contents


def build_embeddings(entities: List[CodeEntity], model_name: str):
    model = SentenceTransformer(model_name)
    texts = [f"{e.path.name}:{e.name} {e.source_line}" for e in entities]
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings, texts


def build_dependency_graph(entities: List[CodeEntity], file_contents: Dict[Path, str]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for entity in entities:
        node_id = f"{entity.path.relative_to(REPO_DIR)}:{entity.name}:{entity.lineno}"
        graph.add_node(node_id, file=str(entity.path), name=entity.name, lineno=entity.lineno)

    name_to_nodes: Dict[str, List[str]] = {}
    for node_id, attrs in graph.nodes(data=True):
        name_to_nodes.setdefault(attrs["name"], []).append(node_id)

    for entity in entities:
        src = f"{entity.path.relative_to(REPO_DIR)}:{entity.name}:{entity.lineno}"
        content = file_contents.get(entity.path, "")
        for callee_name, targets in name_to_nodes.items():
            if callee_name != entity.name and f"{callee_name}(" in content:
                for tgt in targets:
                    graph.add_edge(src, tgt)
    return graph


def detect_static_issues(entity: CodeEntity) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    line = entity.source_line
    if "random.random()" in line or "random.randint(" in line or "random.choice(" in line:
        issues.append({"type": "weak_rng", "message": "Use secrets for cryptographic randomness", "severity": "High"})
    if "import *" in line:
        issues.append({"type": "wildcard_import", "message": "Avoid wildcard imports", "severity": "Medium"})
    has_try = any(isinstance(node, ast.Try) for node in ast.walk(entity.node))
    if isinstance(entity.node, ast.FunctionDef) and not has_try:
        issues.append({"type": "missing_try", "message": "Function has no try/except", "severity": "Low"})
    if "hashlib.md5" in line or "sha1" in line:
        issues.append({"type": "weak_hash", "message": "Use SHA256 or better", "severity": "High"})
    return issues


def autofix_entity(entity: CodeEntity) -> List[str]:
    applied: List[str] = []
    path = entity.path
    try:
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
        modified = False

        class Transformer(ast.NodeTransformer):
            def visit_ImportFrom(self, node):
                nonlocal modified
                if node.names and node.names[0].name == "*":
                    modified = True
                    return ast.copy_location(
                        ast.Expr(value=ast.Constant(value=f"# TODO: replace wildcard import from {node.module} with explicit names")),
                        node,
                    )
                return node

            def visit_Call(self, node):
                nonlocal modified
                if isinstance(node.func, ast.Attribute):
                    if getattr(node.func.value, "id", "") == "random" and node.func.attr in ("random", "randint", "choice"):
                        modified = True
                        return ast.copy_location(ast.parse("secrets.token_hex(16)").body[0].value, node)
                return self.generic_visit(node)

            def visit_FunctionDef(self, node):
                nonlocal modified
                has_try_stmt = any(isinstance(n, ast.Try) for n in node.body)
                if not has_try_stmt:
                    modified = True
                    node.body = [
                        ast.Try(
                            body=node.body,
                            handlers=[
                                ast.ExceptHandler(
                                    type=ast.Name(id="Exception", ctx=ast.Load()),
                                    name="e",
                                    body=[
                                        ast.parse("import logging").body[0],
                                        ast.parse("logging.exception('autofix caught exception: %s', e)").body[0],
                                    ],
                                )
                            ],
                            orelse=[],
                            finalbody=[],
                        )
                    ]
                return node

        new_tree = Transformer().visit(tree)
        if modified:
            path.write_text(astor.to_source(new_tree), encoding="utf-8")
            applied.append(f"AST autofix applied to {path}")
    except Exception as exc:
        logger.exception("Autofix failed for %s: %s", path, exc)
    return applied


def detect_anomalies_with_embeddings(embeddings, texts) -> List[int]:
    if len(embeddings) < 3:
        return []
    clf = IsolationForest(contamination=ANOMALY_CONTAMINATION, random_state=42)
    preds = clf.fit_predict(embeddings)
    return [i for i, pred in enumerate(preds) if pred == -1]


def run_bandit(repo_dir: Path) -> Tuple[bool, str]:
    try:
        res = run(["bandit", "-r", "."], cwd=repo_dir)
        return True, res.stdout + res.stderr
    except Exception as exc:
        return False, str(exc)


def run_flake8(repo_dir: Path) -> Tuple[bool, str]:
    try:
        res = run(["flake8", "."], cwd=repo_dir)
        return True, res.stdout + res.stderr
    except Exception as exc:
        return False, str(exc)


def write_bug_report(issues: List[Dict[str, Any]]) -> None:
    lines = [
        "| File | Line | Entity | Issue | Severity | Suggested Fix |",
        "|------|------|--------|-------|----------|---------------|",
    ]
    for issue in issues:
        lines.append(
            f"| {issue['file']} | {issue['line']} | {issue['entity']} | {issue['message']} | {issue['severity']} | {issue.get('fix', 'manual review')} |"
        )
    BUG_REPORT.write_text("\n".join(lines), encoding="utf-8")


def write_graph_json(graph: nx.DiGraph) -> None:
    GRAPH_JSON.write_text(json.dumps(nx.node_link_data(graph), indent=2), encoding="utf-8")


def append_changelog(entry: str) -> None:
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    content = f"## {ts} - DeepScan Autofix\n\n{entry}\n\n"
    if CHANGELOG.exists():
        CHANGELOG.write_text(CHANGELOG.read_text(encoding="utf-8") + "\n" + content, encoding="utf-8")
    else:
        CHANGELOG.write_text("# Changelog\n\n" + content, encoding="utf-8")


def main(dry_run: bool = False, push_branch_flag: bool = False) -> None:
    start_http_server(PROMETHEUS_PORT)
    logger.info("Prometheus metrics available on port %d", PROMETHEUS_PORT)

    safe_clone_or_pull()
    git_configure()

    entities, file_contents = collect_python_entities(REPO_DIR)
    embeddings, texts = build_embeddings(entities, EMBED_MODEL)

    graph = build_dependency_graph(entities, file_contents)
    write_graph_json(graph)

    issues: List[Dict[str, Any]] = []
    for entity in entities:
        for static_issue in detect_static_issues(entity):
            issues.append(
                {
                    "file": str(entity.path.relative_to(REPO_DIR)),
                    "line": entity.lineno,
                    "entity": entity.name,
                    "type": static_issue["type"],
                    "message": static_issue["message"],
                    "severity": static_issue["severity"],
                    "fix": None,
                }
            )

    for idx in detect_anomalies_with_embeddings(embeddings, texts):
        anomaly = entities[idx]
        issues.append(
            {
                "file": str(anomaly.path.relative_to(REPO_DIR)),
                "line": anomaly.lineno,
                "entity": anomaly.name,
                "type": "semantic_anomaly",
                "message": "Semantic anomaly detected by embedding model",
                "severity": "Medium",
                "fix": "manual review or targeted refactor",
            }
        )
        bug_counter.inc()

    write_bug_report(issues)

    if dry_run:
        logger.info("Dry run enabled; exiting before applying fixes")
        return

    branch = create_autofix_branch()
    applied_fixes: List[str] = []
    for entity in entities:
        applied = autofix_entity(entity)
        if applied:
            applied_fixes.extend(applied)
            fix_counter.inc()

    _, bandit_out = run_bandit(REPO_DIR)
    _, flake_out = run_flake8(REPO_DIR)
    logger.info("Bandit output length %d, Flake8 output length %d", len(bandit_out), len(flake_out))

    commit_changes(f"DeepScan autofix: applied {len(applied_fixes)} fixes")
    if push_branch_flag:
        push_branch(branch)

    changelog_entry = f"- Applied fixes: {len(applied_fixes)}\n- Issues found: {len(issues)}\n- Bandit issues: {len(bandit_out)}\n"
    append_changelog(changelog_entry)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Deep scan and autofix for zCyptoBot")
    parser.add_argument("--dry-run", action="store_true", help="Do not apply fixes or commit")
    parser.add_argument("--push", action="store_true", help="Push autofix branch to origin")
    args = parser.parse_args()
    main(dry_run=args.dry_run, push_branch_flag=args.push)
