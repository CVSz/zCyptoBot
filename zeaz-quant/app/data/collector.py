import random

import httpx


class DataCollector:
    async def get_market(self, symbol: str = "BTCUSDT") -> dict[str, float]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                "https://fapi.binance.com/fapi/v1/ticker/price",
                params={"symbol": symbol},
            )
            response.raise_for_status()
            payload = response.json()

        return {
            "price": float(payload["price"]),
            "oi": random.uniform(1000, 2000),
            "sentiment": random.uniform(-1, 1),
        }
