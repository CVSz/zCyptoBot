import numpy as np


class SignalEngine:
    def generate(self, prices: list[float]) -> str:
        returns = np.diff(prices) / prices[:-1]
        vol = np.std(returns)
        momentum = prices[-1] - prices[0]

        if vol > 0.003 and momentum > 0:
            return "LONG"
        if vol > 0.003 and momentum < 0:
            return "SHORT"
        return "HOLD"
