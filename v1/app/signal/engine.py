import numpy as np


class SignalEngine:
    def compute(self, prices, oi, oi_prev):
        vol = np.std(prices)
        momentum = prices[-1] - prices[0]

        if oi > oi_prev and vol > 0.5:
            if momentum > 0:
                return "LONG"
            return "SHORT"

        return "HOLD"
