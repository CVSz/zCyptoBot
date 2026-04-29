import asyncio

from app.core.event_bus import KafkaConsumerWrapper
from app.core.topics import ARBITRAGE_OPP
from app.execution.binance import BinanceExchange
from app.execution.bybit import BybitExchange
from app.execution.okx import OKXExchange
from app.risk.engine import RiskEngine

EX_MAP = {
    "BINANCE": lambda: BinanceExchange("KEY", "SECRET"),
    "OKX": lambda: OKXExchange("KEY", "SECRET", "PASSPHRASE"),
    "BYBIT": lambda: BybitExchange("KEY", "SECRET"),
}


class ArbitrageExecutor:
    def __init__(self):
        self.consumer = KafkaConsumerWrapper(ARBITRAGE_OPP)
        self.risk = RiskEngine(0.01, 0.15)

    async def run(self):
        await self.consumer.start()
        async for opp in self.consumer.listen():
            if not self.risk.check_drawdown():
                continue

            symbol = opp["symbol"]
            buy_ex = EX_MAP[opp["buy_ex"]]()
            sell_ex = EX_MAP[opp["sell_ex"]]()

            qty = self.risk.size(opp["buy_ask"])

            buy = buy_ex.place_market(symbol, "BUY", qty)
            sell = sell_ex.place_market(symbol, "SELL", qty)
            results = await asyncio.gather(buy, sell, return_exceptions=True)

            if any(isinstance(r, Exception) for r in results):
                # Compensation hook for partially filled legs.
                pass


if __name__ == "__main__":
    asyncio.run(ArbitrageExecutor().run())
