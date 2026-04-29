import json

import websockets


class BinanceStream:
    def __init__(self, symbol: str = "btcusdt"):
        self.url = f"wss://fstream.binance.com/ws/{symbol}@ticker"

    async def stream(self):
        async with websockets.connect(self.url) as ws:
            while True:
                data = await ws.recv()
                yield json.loads(data)
