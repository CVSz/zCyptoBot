from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RLState:
    momentum: float
    volatility: float
    orderbook_imbalance: float


class RLV5Policy:
    """Lightweight RL policy scaffold for v5 upgrade.

    This deterministic policy is intentionally simple so it can be tested
    and replaced later by a learned checkpoint-backed model.
    """

    def __init__(self, long_threshold: float = 0.20, short_threshold: float = -0.20) -> None:
        self.long_threshold = long_threshold
        self.short_threshold = short_threshold

    def score(self, state: RLState) -> float:
        return (0.45 * state.momentum) - (0.25 * state.volatility) + (0.30 * state.orderbook_imbalance)

    def action(self, state: RLState) -> str:
        value = self.score(state)
        if value >= self.long_threshold:
            return "BUY"
        if value <= self.short_threshold:
            return "SELL"
        return "HOLD"
