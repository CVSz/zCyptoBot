from typing import Any, Dict, Iterable


class AuditTrail:
    """Helpers to validate audit-chain integrity and iterate events."""

    def verify_chain(self, logs: Iterable[Dict[str, Any]]) -> bool:
        prev = "GENESIS"
        for entry in logs:
            if entry.get("prev") != prev:
                return False
            prev = entry.get("hash")
        return True
