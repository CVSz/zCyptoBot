from pathlib import Path
from typing import Any, Dict, Tuple

import yaml


class ComplianceEngine:
    def __init__(self, path: str | None = None) -> None:
        rules_path = Path(path) if path else Path(__file__).with_name("rules.yaml")
        with rules_path.open("r", encoding="utf-8") as f:
            self.rules = yaml.safe_load(f)

    def check(self, decision: Dict[str, Any]) -> Tuple[bool, str]:
        if decision["price"] > self.rules["pricing"]["max_markup"]:
            return False, "price_violation"

        jurisdiction = decision.get("jurisdiction", "EU")
        max_latency = self.rules["jurisdiction"].get(jurisdiction, {}).get("max_latency")
        if max_latency is not None and decision["latency"] > max_latency:
            return False, "latency_violation"

        return True, "ok"
