import hashlib
import json
import time
from typing import Any, Dict


class AuditLogger:
    """Hash-chained append-only audit logger."""

    def __init__(self, genesis_hash: str = "GENESIS") -> None:
        self.prev_hash = genesis_hash

    def log(self, event: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "ts": time.time(),
            "event": event,
            "prev": self.prev_hash,
        }
        raw = json.dumps(payload, sort_keys=True)
        digest = hashlib.sha256(raw.encode()).hexdigest()
        payload["hash"] = digest
        self.prev_hash = digest

        print("AUDIT:", payload)  # replace with external sink
        return payload
