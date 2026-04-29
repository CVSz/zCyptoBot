import asyncio
import json

import httpx
from aiokafka import AIOKafkaProducer

from app.config import settings


async def run() -> None:
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKER)
    await producer.start()

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            while True:
                response = await client.get(
                    "https://fapi.binance.com/fapi/v1/ticker/price",
                    params={"symbol": "BTCUSDT"},
                )
                response.raise_for_status()
                price = float(response.json()["price"])

                payload = {"price": price}
                await producer.send_and_wait("market", json.dumps(payload).encode())
                await asyncio.sleep(1)
    finally:
        await producer.stop()
