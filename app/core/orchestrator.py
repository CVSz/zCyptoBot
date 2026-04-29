import asyncio
from app.signal.engine import SignalEngine
from app.risk.engine import RiskEngine
from app.execution.binance import BinanceExchange
from app.data.market import MarketService
from app.config import settings


class Orchestrator:
    def __init__(self):
        self.signal = SignalEngine()
        self.risk = RiskEngine(settings.MAX_RISK, settings.MAX_DRAWDOWN)
        self.exec = BinanceExchange(settings.BINANCE_API_KEY, settings.BINANCE_SECRET)
        self.market = MarketService()

    async def run(self):
        while True:
            data = await self.market.get_data("BTCUSDT")

            sig = self.signal.compute(
                data["prices"],
                data["oi"],
                data["oi_prev"]
            )

            if sig == "HOLD":
                await asyncio.sleep(1)
                continue

            if not self.risk.check_drawdown():
                print("KILL SWITCH TRIGGERED")
                continue

            qty = self.risk.size(data["prices"][-1])

            await self.exec.place_order("BTCUSDT", sig, qty)

            await asyncio.sleep(2)
