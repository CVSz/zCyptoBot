from typing import Any, Dict


class Limits:
    def allow(self, tenant: Dict[str, Any], action: Dict[str, Any]) -> bool:
        _ = action
        return tenant["usage"] <= tenant["limit"]
