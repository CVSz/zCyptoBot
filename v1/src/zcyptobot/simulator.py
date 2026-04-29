from __future__ import annotations

import random
from dataclasses import dataclass

from .config import BotConfig
from .models import MarketTick
from .pipeline import QuantBot


@dataclass(slots=True)
class SimulationReport:
    final_equity: float
    total_fills: int
    accepted_ticks: int


def generate_ticks(symbol: str, n: int, seed: int = 42) -> list[MarketTick]:
    rng = random.Random(seed)
    price = 100.0
    oi = 1000.0
    ticks: list[MarketTick] = []
    for t in range(n):
        drift = 0.0005 if 30 < t < 120 else -0.0002
        shock = rng.uniform(-0.01, 0.01)
        price *= max(0.5, (1 + drift + shock))
        oi *= max(0.8, (1 + rng.uniform(-0.01, 0.02)))
        sentiment = min(1.0, max(0.0, 0.55 + rng.uniform(-0.4, 0.4)))
        ticks.append(MarketTick(t, symbol, price, rng.uniform(1000, 5000), sentiment, oi))
    return ticks


def run_simulation(config: BotConfig | None = None, ticks_per_symbol: int = 200) -> SimulationReport:
    cfg = config or BotConfig()
    bot = QuantBot(cfg)
    fills = 0
    accepted = 0
    for symbol in cfg.symbols:
        for tick in generate_ticks(symbol, ticks_per_symbol, seed=hash(symbol) % 10_000):
            result = bot.on_tick(tick)
            accepted += int(result.accepted)
            fills += int(result.fill is not None)
    return SimulationReport(bot.portfolio.market_value(bot.marks), fills, accepted)
