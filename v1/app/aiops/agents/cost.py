from __future__ import annotations


class CostAgent:
    def __init__(self, min_budget_left: float = 0.2, expensive_actions: tuple[str, ...] = ("scale_api",)):
        self.min_budget_left = min_budget_left
        self.expensive_actions = set(expensive_actions)

    def allow(self, action: str, budget_left: float) -> bool:
        if action in self.expensive_actions and budget_left < self.min_budget_left:
            return False
        return True
