import json

import redis.asyncio as redis


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(host="redis", port=6379, decode_responses=True)

    async def set_price(self, symbol, price):
        await self.client.set(symbol, price)

    async def get_price(self, symbol):
        return await self.client.get(symbol)

    async def set_book(self, ex: str, symbol: str, bid: float, ask: float, ttl: int = 2):
        key = f"book:{symbol}:{ex}"
        await self.client.set(key, json.dumps({"bid": bid, "ask": ask}), ex=ttl)

    async def get_books(self, symbol: str):
        keys = await self.client.keys(f"book:{symbol}:*")
        out = {}
        for key in keys:
            ex = key.split(":")[-1]
            value = await self.client.get(key)
            if value:
                out[ex] = json.loads(value)
        return out
