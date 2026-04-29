import time

from app.arb.detector import best_pair, is_actionable, net_edge
from app.core.event_bus import KafkaBus, KafkaConsumerWrapper
from app.core.topics import ARBITRAGE_OPP, MARKET_RAW
from app.infra.redis_client import RedisClient

MIN_EDGE = 0.0012
MAX_STALENESS = 300


class ArbitrageEngine:
    def __init__(self):
        self.consumer = KafkaConsumerWrapper(MARKET_RAW)
        self.bus = KafkaBus()
        self.redis = RedisClient()

    async def run(self):
        await self.consumer.start()
        await self.bus.start()

        async for m in self.consumer.listen():
            await self.redis.set_book(m["ex"], m["symbol"], m["bid"], m["ask"])

            books = await self.redis.get_books(m["symbol"])
            pair = best_pair(books)
            if not pair:
                continue

            buy_ex, sell_ex, ask, bid = pair
            age = int(time.time() * 1000) - int(m["ts"])
            edge = net_edge(ask, bid, fee_buy=0.0005, fee_sell=0.0005)

            if is_actionable(edge, MIN_EDGE, MAX_STALENESS, age):
                await self.bus.publish(
                    ARBITRAGE_OPP,
                    {
                        "symbol": m["symbol"],
                        "buy_ex": buy_ex,
                        "sell_ex": sell_ex,
                        "buy_ask": ask,
                        "sell_bid": bid,
                        "edge": edge,
                        "ts": int(time.time() * 1000),
                    },
                )


if __name__ == "__main__":
    import asyncio

    asyncio.run(ArbitrageEngine().run())
