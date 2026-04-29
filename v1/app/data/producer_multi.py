import asyncio
import json

import websockets

from app.core.event_bus import KafkaBus
from app.core.topics import MARKET_RAW

WS = {
    "BINANCE": "wss://fstream.binance.com/ws/btcusdt@bookTicker",
    "OKX": "wss://ws.okx.com:8443/ws/v5/public",
    "BYBIT": "wss://stream.bybit.com/v5/public/linear",
}


class MultiProducer:
    def __init__(self):
        self.bus = KafkaBus()

    async def _binance(self):
        async with websockets.connect(WS["BINANCE"]) as ws:
            while True:
                m = json.loads(await ws.recv())
                payload = {"ex": "BINANCE", "symbol": "BTCUSDT", "bid": float(m["b"]), "ask": float(m["a"]), "ts": int(m["E"])}
                await self.bus.publish(MARKET_RAW, payload)

    async def _okx(self):
        async with websockets.connect(WS["OKX"]) as ws:
            await ws.send(json.dumps({"op": "subscribe", "args": [{"channel": "tickers", "instId": "BTC-USDT-SWAP"}]}))
            while True:
                m = json.loads(await ws.recv())
                if "data" in m and m["data"]:
                    d = m["data"][0]
                    payload = {"ex": "OKX", "symbol": "BTCUSDT", "bid": float(d["bidPx"]), "ask": float(d["askPx"]), "ts": int(d["ts"])}
                    await self.bus.publish(MARKET_RAW, payload)

    async def _bybit(self):
        async with websockets.connect(WS["BYBIT"]) as ws:
            await ws.send(json.dumps({"op": "subscribe", "args": ["tickers.BTCUSDT"]}))
            while True:
                m = json.loads(await ws.recv())
                d = m.get("data")
                if isinstance(d, dict):
                    payload = {"ex": "BYBIT", "symbol": "BTCUSDT", "bid": float(d["bid1Price"]), "ask": float(d["ask1Price"]), "ts": int(d["ts"])}
                    await self.bus.publish(MARKET_RAW, payload)

    async def run(self):
        await self.bus.start()
        await asyncio.gather(self._binance(), self._okx(), self._bybit())


if __name__ == "__main__":
    asyncio.run(MultiProducer().run())
