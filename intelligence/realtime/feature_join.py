"""Real-time feature join between online (Redis) and offline stores."""

from __future__ import annotations

import hashlib
import json
from typing import Any

import redis


def _redis_client() -> redis.Redis:
    """Build a Redis client with text responses enabled."""
    return redis.Redis(decode_responses=True)


def get_online(user_id: str) -> dict[str, Any]:
    """Fetch online features for a user from Redis.

    Returns an empty dictionary if key is missing, payload is invalid, or Redis is unreachable.
    """
    try:
        payload = _redis_client().get(f"user:{user_id}")
    except redis.RedisError:
        return {}

    if not payload:
        return {}

    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return {}

    return parsed if isinstance(parsed, dict) else {}


def join_features(user_id: str, offline: dict[str, Any]) -> dict[str, Any]:
    """Merge online and offline features and compute a combined score."""
    online = get_online(user_id)

    offline_score = float(offline.get("score", 0) or 0)
    online_score = float(online.get("score", 0) or 0)

    return {
        **offline,
        **online,
        "feature_join_version": "v1",
        "combined_score": online_score + offline_score,
        "join_key": hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:12],
    }
