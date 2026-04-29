import hashlib
import hmac
import time

import httpx

from app.execution.base import BaseExchange


class BinanceExchange(BaseExchange):
    def __init__(self, key, secret):
        self.name = "BINANCE"
        self.key = key
        self.secret = secret.encode()
        self.base = "https://fapi.binance.com"

    def sign(self, qs):
        return hmac.new(self.secret, qs.encode(), hashlib.sha256).hexdigest()

    async def get_best_bid_ask(self, symbol):
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{self.base}/fapi/v1/ticker/bookTicker", params={"symbol": symbol})
            r.raise_for_status()
            j = r.json()
            return {"bid": float(j["bidPrice"]), "ask": float(j["askPrice"])}

    async def place_market(self, symbol, side, qty):
        ts = int(time.time() * 1000)
        qs = f"symbol={symbol}&side={side}&type=MARKET&quantity={qty}&timestamp={ts}"
        sig = self.sign(qs)

        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.post(
                f"{self.base}/fapi/v1/order",
                headers={"X-MBX-APIKEY": self.key},
                params=qs + "&signature=" + sig,
            )
            r.raise_for_status()
            return r.json()

    async def fee_rate(self) -> float:
        return 0.0004

    async def place_order(self, symbol, side, qty):
        return await self.place_market(symbol, side, qty)
