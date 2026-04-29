from __future__ import annotations


class RiskEngine:
    def __init__(self, max_risk: float, max_dd: float, initial_equity: float = 10_000) -> None:
        self.max_risk = max_risk
        self.max_drawdown = max_dd
        self.equity = initial_equity
        self.peak = initial_equity

    def size(self, price: float) -> float:
        return (self.equity * self.max_risk) / max(price, 1e-9)

    def check_drawdown(self) -> bool:
        dd = (self.peak - self.equity) / max(self.peak, 1e-9)
        return dd < self.max_drawdown
