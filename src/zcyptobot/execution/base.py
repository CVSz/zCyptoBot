from __future__ import annotations


class BaseExchange:
    async def place_order(self, symbol: str, side: str, qty: float) -> dict:
        raise NotImplementedError
