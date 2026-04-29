import random


class SystemSimulator:
    def __init__(self):
        self.state = {
            "latency": 200.0,
            "error": 0.02,
            "load": 0.5,
        }

    def step(self, action: str):
        if action == "scale_api":
            self.state["latency"] *= 0.8
        elif action == "restart_pods":
            self.state["error"] *= 0.7
        elif action == "shift_traffic":
            self.state["load"] *= 0.7

        self.state["latency"] *= random.uniform(0.95, 1.05)
        self.state["error"] *= random.uniform(0.95, 1.05)

        return self.state
