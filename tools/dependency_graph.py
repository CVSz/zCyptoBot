import ast
import os
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(__file__))
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}
edges = defaultdict(set)


def top(path: str) -> str:
    return path.split(os.sep)[0]


for root, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for file_name in files:
        if not file_name.endswith(".py"):
            continue
        fp = os.path.join(root, file_name)
        pkg = top(os.path.relpath(fp, ROOT))
        try:
            with open(fp, encoding="utf-8", errors="ignore") as f:
                tree = ast.parse(f.read())
        except Exception:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    edges[pkg].add(name.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                edges[pkg].add(node.module.split(".")[0])

print("digraph G {")
for src, tgts in edges.items():
    for tgt in tgts:
        print(f'  "{src}" -> "{tgt}";')
print("}")
