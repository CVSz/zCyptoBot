from typing import Any, Dict, Iterable


class FairnessMonitor:
    def check_bias(self, decisions: Iterable[Dict[str, Any]]) -> bool:
        prices = [d["price"] for d in decisions]
        if not prices:
            return True
        if max(prices) / max(1e-6, min(prices)) > 3:
            return False
        return True
