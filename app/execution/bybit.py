import httpx

from app.execution.base import BaseExchange


class BybitExchange(BaseExchange):
    def __init__(self, key: str, secret: str, base="https://api.bybit.com"):
        self.name = "BYBIT"
        self.key = key
        self.secret = secret.encode()
        self.base = base

    async def get_best_bid_ask(self, symbol: str):
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(f"{self.base}/v5/market/tickers", params={"category": "linear", "symbol": symbol})
            r.raise_for_status()
            j = r.json()["result"]["list"][0]
            return {"bid": float(j["bid1Price"]), "ask": float(j["ask1Price"])}

    async def place_market(self, symbol: str, side: str, qty: float):
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.post(
                f"{self.base}/v5/order/create",
                json={"category": "linear", "symbol": symbol, "side": side, "orderType": "Market", "qty": str(qty)},
            )
            r.raise_for_status()
            return r.json()

    async def fee_rate(self) -> float:
        return 0.0006
