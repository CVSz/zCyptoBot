from __future__ import annotations

import hashlib
import hmac
import time

import httpx

from .base import BaseExchange


class BinanceExchange(BaseExchange):
    def __init__(self, key: str, secret: str, base_url: str = "https://fapi.binance.com") -> None:
        self.key = key
        self.secret = secret.encode()
        self.base_url = base_url

    def _sign(self, qs: str) -> str:
        return hmac.new(self.secret, qs.encode(), hashlib.sha256).hexdigest()

    async def place_order(self, symbol: str, side: str, qty: float) -> dict:
        ts = int(time.time() * 1000)
        qs = f"symbol={symbol}&side={side}&type=MARKET&quantity={qty}&timestamp={ts}"
        sig = self._sign(qs)

        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                f"{self.base_url}/fapi/v1/order",
                headers={"X-MBX-APIKEY": self.key},
                params=qs + "&signature=" + sig,
            )
            r.raise_for_status()
            return r.json()
