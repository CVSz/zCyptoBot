from typing import Dict, Any


class PolicyEngine:
    def __init__(self, pii_cross_border_allowed: bool = False):
        self.pii_cross_border_allowed = pii_cross_border_allowed

    def evaluate(self, claims: Dict[str, Any], resource_region: str, has_pii: bool) -> bool:
        if has_pii and not self.pii_cross_border_allowed:
            return claims.get("region") == resource_region
        return True
