import time

import httpx

from app.execution.base import BaseExchange


class OKXExchange(BaseExchange):
    def __init__(self, key: str, secret: str, passphrase: str, base="https://www.okx.com"):
        self.name = "OKX"
        self.key = key
        self.secret = secret.encode()
        self.passphrase = passphrase
        self.base = base

    async def get_best_bid_ask(self, symbol: str):
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(f"{self.base}/api/v5/market/ticker", params={"instId": symbol})
            r.raise_for_status()
            j = r.json()["data"][0]
            return {"bid": float(j["bidPx"]), "ask": float(j["askPx"])}

    async def place_market(self, symbol: str, side: str, qty: float):
        body = {
            "instId": symbol,
            "tdMode": "cross",
            "side": "buy" if side == "BUY" else "sell",
            "ordType": "market",
            "sz": str(qty),
        }
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.post(
                f"{self.base}/api/v5/trade/order",
                json=body,
                headers={
                    "OK-ACCESS-KEY": self.key,
                    "OK-ACCESS-TIMESTAMP": str(time.time()),
                    "OK-ACCESS-PASSPHRASE": self.passphrase,
                },
            )
            r.raise_for_status()
            return r.json()

    async def fee_rate(self) -> float:
        return 0.0005
