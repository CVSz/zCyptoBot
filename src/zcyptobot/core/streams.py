from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

import redis.asyncio as redis


class RedisStreamsBus:
    """Redis Streams transport for low-latency fanout and replay."""

    def __init__(self, url: str = "redis://redis:6379/0") -> None:
        self.url = url
        self._client = redis.from_url(url, decode_responses=True)

    async def publish(self, stream: str, payload: dict[str, Any], maxlen: int = 200_000) -> str:
        data = {"payload": json.dumps(payload)}
        return await self._client.xadd(stream, data, maxlen=maxlen, approximate=True)

    async def consume_group(
        self,
        stream: str,
        group: str,
        consumer: str,
        block_ms: int = 5000,
        count: int = 100,
    ) -> AsyncIterator[tuple[str, dict[str, Any]]]:
        try:
            await self._client.xgroup_create(stream, group, id="$", mkstream=True)
        except redis.ResponseError as exc:
            if "BUSYGROUP" not in str(exc):
                raise

        while True:
            messages = await self._client.xreadgroup(
                group,
                consumer,
                streams={stream: ">"},
                count=count,
                block=block_ms,
            )
            for _, entries in messages:
                for message_id, fields in entries:
                    payload = json.loads(fields["payload"])
                    yield message_id, payload

    async def ack(self, stream: str, group: str, message_id: str) -> int:
        return await self._client.xack(stream, group, message_id)

    async def close(self) -> None:
        await self._client.close()
