"""Policy checks for autonomous actions."""


class PolicyGuard:
    def __init__(self, max_cost: float = 1.0, kill_switch: bool = False) -> None:
        self.max_cost = max_cost
        self.kill_switch = kill_switch

    def allow(self, action: dict) -> bool:
        if self.kill_switch:
            return False
        if action.get("type") == "scale_cluster" and action.get("cost", 0.0) > self.max_cost:
            return False
        return True
