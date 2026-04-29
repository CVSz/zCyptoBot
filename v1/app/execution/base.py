from typing import Dict


class BaseExchange:
    name: str

    async def get_best_bid_ask(self, symbol: str) -> Dict[str, float]:
        """Return {'bid': float, 'ask': float}."""
        raise NotImplementedError

    async def place_market(self, symbol: str, side: str, qty: float) -> dict:
        """side: BUY or SELL."""
        raise NotImplementedError

    async def fee_rate(self) -> float:
        """Taker fee rate."""
        raise NotImplementedError
