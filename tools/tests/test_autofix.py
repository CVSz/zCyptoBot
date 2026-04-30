from pathlib import Path
import shutil
import sys

ROOT = Path.cwd()
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import deep_scan as ds

def setup_module(module):
    test_repo = Path("zCyptoBot")
    if test_repo.exists():
        shutil.rmtree(test_repo)
    test_repo.mkdir()

def teardown_module(module):
    for p in [Path("zCyptoBot"), Path(".deepscan_backup")]:
        if p.exists():
            shutil.rmtree(p)

def test_ast_autofix_replaces_random_and_backups():
    test_file = Path("zCyptoBot/test_random.py")
    test_file.write_text("import random\ndef foo():\n    return random.random()\n", encoding="utf-8")
    applied = ds.ast_autofix_file(test_file)
    assert applied
    assert (Path(".deepscan_backup") / test_file).exists()
    assert "secrets.token_hex" in test_file.read_text(encoding="utf-8")
