class CostModel:
    COST = {
        "scale_api": 0.02,
        "restart_pods": 0.005,
        "rollback_deploy": 0.01,
        "scale_consumers": 0.02,
        "restart_kafka": 0.05,
    }

    def estimate(self, action, duration_min=5):
        return self.COST.get(action, 0.02) * duration_min

    def budget_penalty(self, budget_left_ratio: float):
        return (1.0 - budget_left_ratio) * 0.5
