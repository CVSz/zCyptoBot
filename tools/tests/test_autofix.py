from pathlib import Path
import shutil
import sys
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools"))
import deep_scan as ds

def setup_module(module):
    p = Path("zCyptoBot")
    if p.exists():
        shutil.rmtree(p)
    p.mkdir()

def teardown_module(module):
    for p in [Path("zCyptoBot"), Path(".deepscan_backup")]:
        if p.exists():
            shutil.rmtree(p)

def test_ast_autofix_replaces_random_and_backups():
    f = Path("zCyptoBot/test_random.py")
    f.write_text("import random\ndef foo():\n    return random.random()\n", encoding="utf-8")
    assert ds.ast_autofix_file(f)
