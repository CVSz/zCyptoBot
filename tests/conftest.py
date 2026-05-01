import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1] / "zeaz-live" / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
