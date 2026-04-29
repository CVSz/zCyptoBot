class RiskEngine:
    def __init__(self, risk, max_dd):
        self.risk = risk
        self.max_dd = max_dd
        self.equity = 10000
        self.peak = self.equity

    def size(self, price):
        return round((self.equity * self.risk) / price, 4)

    def check_drawdown(self):
        dd = (self.peak - self.equity) / self.peak
        return dd < self.max_dd
