import random

ACTIONS = ["scale", "hold", "shift"]


class Engine:
    def decide(self, state):
        if state["latency"] > 220:
            return "scale"
        if state["error"] > 0.05:
            return "restart"
        return random.choice(ACTIONS)
