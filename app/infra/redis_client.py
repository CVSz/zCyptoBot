import redis.asyncio as redis


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(host="redis", port=6379, decode_responses=True)

    async def set_price(self, symbol, price):
        await self.client.set(symbol, price)

    async def get_price(self, symbol):
        return await self.client.get(symbol)
