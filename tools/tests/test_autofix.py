from pathlib import Path
import shutil
import sys
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools"))
import deep_scan as ds  # noqa: E402

def setup_module(module):
    p = Path("zypto")
    if p.exists():
        shutil.rmtree(p)
    p.mkdir()

def teardown_module(module):
    for p in [Path("zypto"), Path(".deepscan_backup")]:
        if p.exists():
            shutil.rmtree(p)

def test_ast_autofix_replaces_random_and_backups():
    f = Path("zypto/test_random.py")
    f.write_text("import random\ndef foo():\n    return random.random()\n", encoding="utf-8")
    assert ds.ast_autofix_file(f)
