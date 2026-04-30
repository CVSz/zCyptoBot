class Agent:
    def __init__(self, role):
        self.role = role

    def act(self, state):
        return f"{self.role} decision"


class Org:
    def __init__(self):
        self.agents = [
            Agent("product"),
            Agent("growth"),
            Agent("infra"),
            Agent("finance"),
        ]

    def run(self, state):
        decisions = [a.act(state) for a in self.agents]
        return decisions
