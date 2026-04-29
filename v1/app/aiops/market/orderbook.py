"""Redis-backed market orderbook primitives."""

from __future__ import annotations

import json
from typing import Any

import redis

r = redis.Redis(host="redis", decode_responses=True)


class OrderBook:
    """Simple FIFO order queues for bids and asks."""

    def __init__(self, namespace: str = "aiops:market") -> None:
        self._bids_key = f"{namespace}:bids"
        self._asks_key = f"{namespace}:asks"

    def add_bid(self, agent: str, resource: str, price: float, qty: int) -> None:
        r.rpush(
            self._bids_key,
            json.dumps({"agent": agent, "res": resource, "price": price, "qty": qty}),
        )

    def add_ask(self, agent: str, resource: str, price: float, qty: int) -> None:
        r.rpush(
            self._asks_key,
            json.dumps({"agent": agent, "res": resource, "price": price, "qty": qty}),
        )

    def get(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        bids = [json.loads(x) for x in r.lrange(self._bids_key, 0, -1)]
        asks = [json.loads(x) for x in r.lrange(self._asks_key, 0, -1)]
        return bids, asks

    def clear(self) -> None:
        r.delete(self._bids_key)
        r.delete(self._asks_key)
