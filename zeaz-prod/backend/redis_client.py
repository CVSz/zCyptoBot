import json
import os

import redis

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)


def publish(channel: str, data: dict) -> None:
    r.publish(channel, json.dumps(data))


def cache_set(key: str, data: dict, ttl: int = 30) -> None:
    r.setex(key, ttl, json.dumps(data))
