import httpx
import time
import hmac
import hashlib


class BinanceExchange:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret.encode()

    def sign(self, qs):
        return hmac.new(self.secret, qs.encode(), hashlib.sha256).hexdigest()

    async def place_order(self, symbol, side, qty):
        ts = int(time.time() * 1000)
        qs = f"symbol={symbol}&side={side}&type=MARKET&quantity={qty}&timestamp={ts}"
        sig = self.sign(qs)

        async with httpx.AsyncClient() as client:
            r = await client.post(
                "https://fapi.binance.com/fapi/v1/order",
                headers={"X-MBX-APIKEY": self.key},
                params=qs + "&signature=" + sig
            )
            r.raise_for_status()
            return r.json()
