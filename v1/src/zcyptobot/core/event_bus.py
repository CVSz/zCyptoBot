from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


class EventBus:
    """Minimal async Kafka wrapper for typed JSON events."""

    def __init__(self, brokers: str, client_id: str = "zypto") -> None:
        self.brokers = brokers
        self.client_id = client_id
        self._producer = AIOKafkaProducer(bootstrap_servers=brokers, client_id=client_id)

    async def start(self) -> None:
        await self._producer.start()

    async def publish(self, topic: str, payload: dict[str, Any]) -> None:
        await self._producer.send_and_wait(topic, json.dumps(payload).encode("utf-8"))

    async def consume(self, topic: str, group_id: str) -> AsyncIterator[dict[str, Any]]:
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.brokers,
            group_id=group_id,
            client_id=self.client_id,
            enable_auto_commit=True,
        )
        await consumer.start()
        try:
            async for msg in consumer:
                yield json.loads(msg.value)
        finally:
            await consumer.stop()

    async def stop(self) -> None:
        await self._producer.stop()
