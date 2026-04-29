import random

import httpx


class DataCollector:
    async def get_market(self, symbol: str = "BTCUSDT") -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://fapi.binance.com/fapi/v1/ticker/price",
                params={"symbol": symbol},
                timeout=10,
            )
            price = float(response.json()["price"])

        return {
            "price": price,
            "oi": random.uniform(1000, 2000),
            "sentiment": random.uniform(-1, 1),
        }
