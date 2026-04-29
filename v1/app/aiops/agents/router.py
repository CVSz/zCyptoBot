from __future__ import annotations


class Router:
    def decide(self, planner_action: str, ok_safety: bool, ok_cost: bool) -> str:
        if not ok_safety or not ok_cost:
            return "hold"
        return planner_action
