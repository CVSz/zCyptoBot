from app.core.event_bus import KafkaConsumerWrapper
from app.execution.binance import BinanceExchange
from app.risk.engine import RiskEngine
from app.ai.inference import RLInference
from app.features.builder import FeatureBuilder


class SignalWorker:
    def __init__(self):
        self.consumer = KafkaConsumerWrapper("market")
        self.rl = RLInference()
        self.features = FeatureBuilder()
        self.risk = RiskEngine(0.02, 0.2)
        self.exec = BinanceExchange("KEY", "SECRET")
        self.buffer = []

    async def run(self):
        await self.consumer.start()

        async for msg in self.consumer.listen():
            price = msg["price"]
            self.buffer.append(price)

            if len(self.buffer) < 5:
                continue

            state = self.features.build(self.buffer, 1000, 900)
            sig = self.rl.predict(state)

            if sig == "HOLD":
                continue

            if not self.risk.check_drawdown():
                continue

            qty = self.risk.size(price)
            await self.exec.place_order("BTCUSDT", sig, qty)
            self.buffer.pop(0)


if __name__ == "__main__":
    import asyncio

    asyncio.run(SignalWorker().run())
