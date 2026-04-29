from __future__ import annotations

from dataclasses import dataclass

from .config import BotConfig
from .pipeline import QuantBot
from .services import CycleStats, MarketDataService, SocialSignalService


@dataclass(slots=True)
class SymbolState:
    price: float = 100.0
    oi: float = 1_000.0


class Orchestrator:
    """Core async-friendly orchestrator.

    Designed so the run loop can be called from API/scheduler workers.
    """

    def __init__(self, config: BotConfig | None = None):
        self.config = config or BotConfig()
        self.bot = QuantBot(self.config)
        self.market = MarketDataService()
        self.social = SocialSignalService()
        self._state = {s: SymbolState() for s in self.config.symbols}
        self._ts = 0

    def run_cycle(self) -> CycleStats:
        candidates = self.social.trending_symbols(self.config.symbols, sample_size=min(2, len(self.config.symbols)))
        ticks = accepted = fills = 0

        for symbol in candidates:
            state = self._state[symbol]
            tick = self.market.next_tick(self._ts, symbol, state.price, state.oi)
            self._ts += 1
            ticks += 1
            state.price, state.oi = tick.price, tick.open_interest

            result = self.bot.on_tick(tick)
            accepted += int(result.accepted)
            fills += int(result.fill is not None)

        equity = self.bot.portfolio.market_value(self.bot.marks)
        return CycleStats(ticks=ticks, accepted=accepted, fills=fills, equity=equity)
