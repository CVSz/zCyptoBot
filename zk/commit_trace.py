import hashlib
import json
from typing import Any


def trace_commit(trace: dict[str, Any]) -> str:
    blob = json.dumps(trace, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()
