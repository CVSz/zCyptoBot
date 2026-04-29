from __future__ import annotations


class Orchestrator:
    def __init__(self, planner, safety, cost, router):
        self.planner = planner
        self.safety = safety
        self.cost = cost
        self.router = router

    def step(self, z, metrics: dict) -> str:
        action = self.planner.act(z)
        ok_s = self.safety.allow(action, metrics)
        ok_c = self.cost.allow(action, metrics.get("budget_left", 0.0))
        return self.router.decide(action, ok_s, ok_c)
