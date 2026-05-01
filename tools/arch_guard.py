import ast
import os
import sys
from typing import Dict, List, Tuple

import yaml

ROOT = os.path.dirname(os.path.dirname(__file__))
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}


def load_rules() -> Dict:
    with open(os.path.join(ROOT, "tools", "arch_rules.yml"), "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def top_package(path: str) -> str:
    rel = os.path.relpath(path, ROOT)
    parts = rel.split(os.sep)
    return parts[0] if parts else ""


def collect_imports(file_path: str) -> List[str]:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            return []
    imports: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def resolve_target_pkg(import_path: str) -> str:
    return import_path.split(".")[0]


def scan() -> Tuple[int, List[str]]:
    rules = load_rules()
    errors: List[str] = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for file_name in files:
            if not file_name.endswith(".py"):
                continue
            fp = os.path.join(root, file_name)
            src_pkg = top_package(fp)
            if src_pkg not in rules["layers"]:
                continue
            imports = collect_imports(fp)
            for imp in imports:
                tgt_pkg = resolve_target_pkg(imp)
                if tgt_pkg not in rules["layers"]:
                    continue
                for deny in rules.get("deny", []):
                    if deny["from"] == src_pkg and deny["to"] == tgt_pkg:
                        errors.append(f"{fp}: forbidden import {src_pkg} -> {tgt_pkg} ({imp})")
                allowed = rules["layers"][src_pkg].get("allow", [])
                if tgt_pkg != src_pkg and tgt_pkg not in allowed:
                    errors.append(f"{fp}: not allowed import {src_pkg} -> {tgt_pkg} ({imp})")
    return len(errors), errors


if __name__ == "__main__":
    count, errs = scan()
    for err in errs:
        print(err)
    if count > 0:
        print(f"\n[ARCH GUARD] violations: {count}")
        sys.exit(1)
    print("[ARCH GUARD] OK")
