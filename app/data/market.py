import httpx
import random


class MarketService:
    async def get_data(self, symbol: str):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                "https://fapi.binance.com/fapi/v1/ticker/price",
                params={"symbol": symbol}
            )
            price = float(r.json()["price"])

        return {
            "prices": [price - random.uniform(0, 2) for _ in range(5)],
            "oi": random.uniform(1000, 2000),
            "oi_prev": random.uniform(800, 1000)
        }
