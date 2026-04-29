from __future__ import annotations

import json
from collections.abc import AsyncIterator

import websockets


class BinanceStream:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol.upper()
        self.url = f"wss://fstream.binance.com/ws/{symbol.lower()}@ticker"

    async def listen(self) -> AsyncIterator[dict]:
        async with websockets.connect(self.url, ping_interval=20) as ws:
            while True:
                msg = await ws.recv()
                yield json.loads(msg)
