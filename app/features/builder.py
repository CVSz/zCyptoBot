import numpy as np


class FeatureBuilder:
    def build(self, prices: list[float], oi: float, oi_prev: float) -> np.ndarray:
        returns = np.diff(prices) / prices[:-1]
        volatility = np.std(returns)
        momentum = prices[-1] - prices[0]
        oi_delta = oi - oi_prev

        return np.array(
            [
                prices[-1],
                volatility,
                momentum,
                oi_delta,
            ],
            dtype=np.float32,
        )
