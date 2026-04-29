from pathlib import Path
from typing import Dict

import yaml


class RewriteEngine:
    def propose_patch(self, policy_path: str, updates: Dict[str, float]) -> dict:
        with Path(policy_path).open("r", encoding="utf-8") as handle:
            policy = yaml.safe_load(handle) or {}

        rules = policy.setdefault("rules", {})
        for key, value in updates.items():
            rules[key] = value
        return policy
