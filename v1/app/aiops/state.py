class Incident:
    def __init__(self):
        self.state = "healthy"
        self.history = []

    def transition(self, state: str, info=None):
        self.state = state
        self.history.append((state, info))
