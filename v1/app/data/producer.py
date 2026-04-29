from app.core.event_bus import KafkaBus
from app.data.stream import BinanceStream


class MarketProducer:
    def __init__(self):
        self.bus = KafkaBus()
        self.stream = BinanceStream()

    async def run(self):
        await self.bus.start()

        async for tick in self.stream.stream():
            payload = {
                "price": float(tick["c"]),
                "symbol": tick["s"],
            }
            await self.bus.publish("market", payload)


if __name__ == "__main__":
    import asyncio

    asyncio.run(MarketProducer().run())
