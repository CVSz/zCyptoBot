import numpy as np


class FeatureBuilder:
    def build(self, prices: list[float], oi: float, sentiment: float) -> dict[str, float]:
        returns = np.diff(prices) / prices[:-1]
        return {
            "vol": float(np.std(returns)),
            "momentum": float(prices[-1] - prices[0]),
            "oi": oi,
            "sentiment": sentiment,
        }
