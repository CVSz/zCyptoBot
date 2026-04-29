class PricingAgent:
    def propose(self, state):
        return state["demand"] * 0.5


class CostAgent:
    def propose(self, state):
        return state["cost"]


class QoSAgent:
    def propose(self, state):
        return state["latency"] * 0.1


class Negotiator:
    def decide(self, proposals):
        return sum(proposals) / len(proposals)
