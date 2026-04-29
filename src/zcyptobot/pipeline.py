from __future__ import annotations

from dataclasses import dataclass

from .config import BotConfig
from .engines import DataFilter, ExecutionEngine, Portfolio, RiskEngine, SignalEngine
from .models import Fill, MarketTick, Side


@dataclass(slots=True)
class StepResult:
    accepted: bool
    fill: Fill | None
    equity: float


class QuantBot:
    def __init__(self, config: BotConfig | None = None):
        self.config = config or BotConfig()
        self.data_filter = DataFilter(self.config.symbols)
        self.signal_engine = SignalEngine(self.config)
        self.risk_engine = RiskEngine(self.config)
        self.exec_engine = ExecutionEngine(self.config)
        self.portfolio = Portfolio(self.config.initial_cash)
        self.marks: dict[str, float] = {}

    def _apply_fill(self, fill: Fill) -> None:
        pos = self.portfolio.positions[fill.symbol]
        gross = fill.qty * fill.price
        if fill.side == Side.BUY:
            new_qty = pos.qty + fill.qty
            pos.avg_price = (pos.avg_price * pos.qty + gross) / max(new_qty, 1e-9)
            pos.qty = new_qty
            self.portfolio.cash -= gross + fill.fee
        else:
            sell_qty = min(pos.qty, fill.qty)
            proceeds = sell_qty * fill.price
            pos.qty -= sell_qty
            if pos.qty == 0:
                pos.avg_price = 0.0
            self.portfolio.cash += proceeds - fill.fee

    def on_tick(self, tick: MarketTick) -> StepResult:
        if not self.data_filter.accept(tick):
            eq = self.portfolio.market_value(self.marks)
            return StepResult(False, None, eq)

        self.marks[tick.symbol] = tick.price
        signal = self.signal_engine.on_tick(tick)
        order = self.risk_engine.propose_order(signal, self.portfolio, self.marks)
        fill = self.exec_engine.execute(order, tick.price) if order else None
        if fill:
            self._apply_fill(fill)

        equity = self.portfolio.market_value(self.marks)
        self.portfolio.equity_peak = max(self.portfolio.equity_peak, equity)
        return StepResult(True, fill, equity)
