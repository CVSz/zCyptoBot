class CostOptimizer:
    """Budget-aware right-sizing helper for short-horizon scaling decisions."""

    def __init__(self):
        self.unit_cost = {
            "cpu": 0.02,  # per vCPU/min
            "mem": 0.01,  # per GB/min
        }

    def estimate(self, cpu, mem, minutes=5):
        return cpu * self.unit_cost["cpu"] * minutes + mem * self.unit_cost["mem"] * minutes

    def recommend(self, metrics):
        cpu = 0.5 if metrics["cpu_usage"] < 0.4 else 1.0
        mem = 256 if metrics["mem_usage"] < 0.5 else 512
        return cpu, mem

    def enforce_budget(self, cost, budget_left):
        return cost <= budget_left
