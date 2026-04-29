class PlannerAgent:
    def __init__(self, planner):
        self.planner = planner

    def propose(self, state):
        return self.planner.plan(state)


class SafetyAgent:
    def allow(self, state):
        return float(state[1]) < 0.05


class CostAgent:
    def allow(self, cost):
        return float(cost) < 1.0


class Router:
    def decide(self, action, safe, cost_ok):
        if not safe or not cost_ok:
            return "hold"
        return action
