class AIOps:
    def step(self, state):
        if state["error"] > 0.03:
            return "restart_pods"
        if state["latency"] > 220:
            return "scale_api"
        if state["load"] > 0.75:
            return "shift_traffic"
        return "observe"
