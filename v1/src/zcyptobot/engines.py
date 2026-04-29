from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass

from .config import BotConfig
from .models import Fill, MarketTick, OrderRequest, Side, Signal


class DataFilter:
    def __init__(self, symbols: tuple[str, ...]):
        self.allowed = set(symbols)

    def accept(self, tick: MarketTick) -> bool:
        return (
            tick.symbol in self.allowed
            and tick.price > 0
            and tick.volume > 0
            and 0 <= tick.sentiment <= 1
            and tick.open_interest >= 0
        )


class SignalEngine:
    def __init__(self, config: BotConfig):
        self.config = config
        self.prices: dict[str, deque[float]] = defaultdict(
            lambda: deque(maxlen=config.signal.lookback)
        )
        self.oi: dict[str, deque[float]] = defaultdict(
            lambda: deque(maxlen=config.signal.lookback)
        )

    def on_tick(self, tick: MarketTick) -> Signal:
        pbuf = self.prices[tick.symbol]
        obuf = self.oi[tick.symbol]
        pbuf.append(tick.price)
        obuf.append(tick.open_interest)

        if len(pbuf) < max(3, self.config.signal.lookback // 2):
            return Signal(tick.ts, tick.symbol, Side.HOLD, 0.0, "insufficient history")

        pmin, pmax = min(pbuf), max(pbuf)
        volatility = (pmax - pmin) / max(pmin, 1e-9)
        oi_change = (obuf[-1] - obuf[0]) / max(obuf[0], 1e-9)

        if (
            tick.sentiment >= self.config.signal.sentiment_threshold
            and volatility >= self.config.signal.volatility_floor
            and oi_change >= self.config.signal.oi_accumulation_threshold
        ):
            conf = min(0.99, 0.4 + tick.sentiment * 0.3 + volatility * 0.2 + oi_change * 0.1)
            return Signal(tick.ts, tick.symbol, Side.BUY, conf, "sentiment+volatility+oi")

        if tick.sentiment < 0.35 and volatility > self.config.signal.volatility_floor * 1.2:
            return Signal(tick.ts, tick.symbol, Side.SELL, 0.65, "risk-off momentum")

        return Signal(tick.ts, tick.symbol, Side.HOLD, 0.2, "no edge")


@dataclass(slots=True)
class Position:
    qty: float = 0.0
    avg_price: float = 0.0


class Portfolio:
    def __init__(self, initial_cash: float):
        self.cash = initial_cash
        self.equity_peak = initial_cash
        self.positions: dict[str, Position] = defaultdict(Position)

    def market_value(self, marks: dict[str, float]) -> float:
        val = self.cash
        for symbol, pos in self.positions.items():
            val += pos.qty * marks.get(symbol, pos.avg_price)
        return val


class RiskEngine:
    def __init__(self, config: BotConfig):
        self.config = config

    def propose_order(self, signal: Signal, portfolio: Portfolio, marks: dict[str, float]) -> OrderRequest | None:
        if signal.side == Side.HOLD:
            return None

        equity = portfolio.market_value(marks)
        if equity <= 0:
            return None
        dd = 1 - (equity / max(portfolio.equity_peak, 1e-9))
        if dd >= self.config.risk.max_drawdown_pct:
            return None

        symbol_price = marks.get(signal.symbol)
        if not symbol_price:
            return None

        gross_exposure = sum(abs(p.qty) * marks.get(s, p.avg_price) for s, p in portfolio.positions.items())
        if gross_exposure >= self.config.risk.max_gross_exposure_usd:
            return None

        risk_budget = equity * self.config.risk.risk_per_trade_pct * max(0.2, signal.confidence)
        notional = min(risk_budget / max(self.config.risk.stop_loss_pct, 1e-9), self.config.risk.max_position_usd)
        notional = min(notional, portfolio.cash if signal.side == Side.BUY else notional)
        if notional <= 0:
            return None
        return OrderRequest(signal.ts, signal.symbol, signal.side, notional)


class ExecutionEngine:
    def __init__(self, config: BotConfig):
        self.config = config

    def execute(self, order: OrderRequest, mark: float) -> Fill | None:
        if order.notional_usd < self.config.execution.min_order_usd or mark <= 0:
            return None

        slip = self.config.execution.slippage_bps / 10_000
        px = mark * (1 + slip if order.side == Side.BUY else 1 - slip)
        qty = order.notional_usd / px
        fee = order.notional_usd * self.config.execution.fee_bps / 10_000
        return Fill(order.ts, order.symbol, order.side, qty, px, fee)
