from __future__ import annotations

import asyncio
from dataclasses import dataclass

from zypto.execution.binance import BinanceExchange
from zypto.risk.engine import RiskEngine
from zypto.signal.engine import SignalEngine


@dataclass(slots=True)
class OrchestratorConfig:
    symbol: str = "BTCUSDT"
    interval_seconds: float = 1.0


class OrchestratorV2:
    def __init__(self, exchange: BinanceExchange, config: OrchestratorConfig | None = None) -> None:
        self.signal = SignalEngine()
        self.risk = RiskEngine(0.02, 0.2)
        self.exchange = exchange
        self.config = config or OrchestratorConfig()

    async def process(self, market_data: dict) -> dict | None:
        prices = market_data["prices"]
        oi_now = market_data["oi"]
        oi_prev = market_data["oi_prev"]

        sig = self.signal.compute(prices, oi_now, oi_prev)
        if sig == "HOLD":
            return None
        if not self.risk.check_drawdown():
            return {"status": "blocked", "reason": "kill_switch"}

        qty = self.risk.size(prices[-1])
        result = await self.exchange.place_order(self.config.symbol, sig, qty)
        return {"status": "executed", "signal": sig, "qty": qty, "result": result}

    async def run(self) -> None:
        while True:
            mock = {"prices": [100, 101, 102, 103], "oi": 1200, "oi_prev": 1000}
            await self.process(mock)
            await asyncio.sleep(self.config.interval_seconds)
