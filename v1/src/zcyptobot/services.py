from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import random

from .models import MarketTick


class MarketDataService:
    """Synthetic market feed abstraction.

    In production this service would be backed by websocket ingestion.
    """

    def __init__(self, seed: int = 7):
        self._rng = random.Random(seed)

    def next_tick(self, ts: int, symbol: str, last_price: float, last_oi: float) -> MarketTick:
        drift = self._rng.uniform(-0.004, 0.006)
        noise = self._rng.uniform(-0.01, 0.01)
        price = max(0.01, last_price * (1 + drift + noise))
        oi = max(1.0, last_oi * (1 + self._rng.uniform(-0.01, 0.015)))
        sentiment = min(1.0, max(0.0, 0.5 + self._rng.uniform(-0.5, 0.5)))
        volume = self._rng.uniform(1_000, 20_000)
        return MarketTick(ts, symbol, price, volume, sentiment, oi)


class SocialSignalService:
    """Simple social source simulator with bot-noise filtering placeholder."""

    def __init__(self, seed: int = 11):
        self._rng = random.Random(seed)

    def trending_symbols(self, universe: Iterable[str], sample_size: int = 2) -> list[str]:
        symbols = list(universe)
        sample_size = min(max(1, sample_size), len(symbols))
        self._rng.shuffle(symbols)
        return symbols[:sample_size]


@dataclass(slots=True)
class CycleStats:
    ticks: int
    accepted: int
    fills: int
    equity: float
