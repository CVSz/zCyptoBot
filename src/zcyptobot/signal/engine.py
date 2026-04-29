from __future__ import annotations

import numpy as np


class SignalEngine:
    """Volatility breakout + OI divergence baseline."""

    def compute(self, prices: list[float], oi_now: float, oi_prev: float) -> str:
        vol = float(np.std(prices))
        momentum = prices[-1] - prices[0]

        if oi_now > oi_prev and vol > 0.5 and momentum > 0:
            return "LONG"
        if oi_now > oi_prev and vol > 0.5 and momentum < 0:
            return "SHORT"
        return "HOLD"
