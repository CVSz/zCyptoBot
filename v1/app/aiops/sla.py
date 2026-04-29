class SLA:
    def __init__(self):
        self.rules = {
            "gold": {"latency": 150, "error": 0.01, "budget": 1.0},
            "silver": {"latency": 200, "error": 0.02, "budget": 0.6},
            "bronze": {"latency": 300, "error": 0.05, "budget": 0.3},
        }

    def get(self, tier: str):
        return self.rules.get(tier, self.rules["bronze"])


class CostCeiling:
    def allow(self, cost: float, budget_left: float) -> bool:
        return cost <= budget_left
