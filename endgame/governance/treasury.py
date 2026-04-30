class Treasury:
    def __init__(self):
        self.balance = 0

    def allocate(self, pct):
        if not (0 <= pct <= 1):
            raise ValueError("pct 0..1")
        return self.balance * pct
