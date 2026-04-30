from pathlib import Path
import shutil
import sys
import ast

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import deep_scan as ds  # noqa: E402


def _reset_workspace(tmp_root: Path) -> Path:
    repo_root = tmp_root / "zCyptoBot"
    if repo_root.exists():
        shutil.rmtree(repo_root)
    repo_root.mkdir(parents=True)
    backup = tmp_root / ".deepscan_backup"
    if backup.exists():
        shutil.rmtree(backup)
    return repo_root


class _AstorShim:
    @staticmethod
    def to_source(tree):
        return ast.unparse(tree) + "\n"


def _ensure_astor(monkeypatch):
    if ds.astor is None:
        monkeypatch.setattr(ds, "astor", _AstorShim)


def test_random_rewrite_and_backup(tmp_path, monkeypatch):
    _ensure_astor(monkeypatch)
    repo_root = _reset_workspace(tmp_path)
    monkeypatch.setattr(ds, "REPO_DIR", repo_root)
    monkeypatch.setattr(ds, "BACKUP_DIR", tmp_path / ".deepscan_backup")

    py_file = repo_root / "sample.py"
    py_file.write_text(
        "import random\n\ndef f():\n    return random.random()\n",
        encoding="utf-8",
    )

    applied = ds.ast_autofix_file(py_file)
    assert applied
    rewritten = py_file.read_text(encoding="utf-8")
    assert ("secrets.token_hex" in rewritten) or ("try:" in rewritten)
    assert (tmp_path / ".deepscan_backup" / "sample.py").exists()


def test_return_semantics_preserved_after_wrap(tmp_path, monkeypatch):
    _ensure_astor(monkeypatch)
    repo_root = _reset_workspace(tmp_path)
    monkeypatch.setattr(ds, "REPO_DIR", repo_root)
    monkeypatch.setattr(ds, "BACKUP_DIR", tmp_path / ".deepscan_backup")

    py_file = repo_root / "maths.py"
    py_file.write_text(
        "def add(a, b):\n    return a + b\n",
        encoding="utf-8",
    )

    ds.ast_autofix_file(py_file)
    namespace = {}
    exec(py_file.read_text(encoding="utf-8"), namespace)
    assert namespace["add"](2, 3) == 5


def test_async_function_not_wrapped(tmp_path, monkeypatch):
    _ensure_astor(monkeypatch)
    repo_root = _reset_workspace(tmp_path)
    monkeypatch.setattr(ds, "REPO_DIR", repo_root)
    monkeypatch.setattr(ds, "BACKUP_DIR", tmp_path / ".deepscan_backup")

    py_file = repo_root / "async_mod.py"
    original = "async def work(x):\n    return x\n"
    py_file.write_text(original, encoding="utf-8")

    ds.ast_autofix_file(py_file)
    rewritten = py_file.read_text(encoding="utf-8")
    assert "async def work" in rewritten
    assert "try:" not in rewritten


def test_generator_function_not_wrapped(tmp_path, monkeypatch):
    _ensure_astor(monkeypatch)
    repo_root = _reset_workspace(tmp_path)
    monkeypatch.setattr(ds, "REPO_DIR", repo_root)
    monkeypatch.setattr(ds, "BACKUP_DIR", tmp_path / ".deepscan_backup")

    py_file = repo_root / "gen_mod.py"
    original = "def gen():\n    yield 1\n"
    py_file.write_text(original, encoding="utf-8")

    ds.ast_autofix_file(py_file)
    rewritten = py_file.read_text(encoding="utf-8")
    assert "yield 1" in rewritten
    assert "try:" not in rewritten


def test_decorated_function_still_executes(tmp_path, monkeypatch):
    _ensure_astor(monkeypatch)
    repo_root = _reset_workspace(tmp_path)
    monkeypatch.setattr(ds, "REPO_DIR", repo_root)
    monkeypatch.setattr(ds, "BACKUP_DIR", tmp_path / ".deepscan_backup")

    py_file = repo_root / "decorated.py"
    py_file.write_text(
        "def deco(fn):\n"
        "    def wrapper(*args, **kwargs):\n"
        "        return fn(*args, **kwargs)\n"
        "    return wrapper\n\n"
        "@deco\n"
        "def value(x):\n"
        "    return x + 10\n",
        encoding="utf-8",
    )

    ds.ast_autofix_file(py_file)
    namespace = {}
    exec(py_file.read_text(encoding="utf-8"), namespace)
    assert namespace["value"](5) == 15


def test_wildcard_import_replacement_preserves_runtime(tmp_path, monkeypatch):
    _ensure_astor(monkeypatch)
    repo_root = _reset_workspace(tmp_path)
    monkeypatch.setattr(ds, "REPO_DIR", repo_root)
    monkeypatch.setattr(ds, "BACKUP_DIR", tmp_path / ".deepscan_backup")

    helper = repo_root / "helper_mod.py"
    helper.write_text(
        "from math import sqrt\n\n"
        "def root_four():\n"
        "    return sqrt(4)\n",
        encoding="utf-8",
    )
    py_file = repo_root / "wildcard.py"
    py_file.write_text(
        "from helper_mod import *\n\n"
        "def use_helper():\n"
        "    return root_four()\n",
        encoding="utf-8",
    )

    ds.ast_autofix_file(py_file)
    rewritten = py_file.read_text(encoding="utf-8")
    assert "TODO: replace wildcard import from helper_mod" in rewritten
    namespace = {}
    exec(helper.read_text(encoding="utf-8"), namespace)
    exec(rewritten, namespace)
    assert namespace["use_helper"]() == 2.0
