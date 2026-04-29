from dataclasses import dataclass
from enum import Enum


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass(slots=True)
class MarketTick:
    ts: int
    symbol: str
    price: float
    volume: float
    sentiment: float
    open_interest: float


@dataclass(slots=True)
class Signal:
    ts: int
    symbol: str
    side: Side
    confidence: float
    reason: str


@dataclass(slots=True)
class OrderRequest:
    ts: int
    symbol: str
    side: Side
    notional_usd: float


@dataclass(slots=True)
class Fill:
    ts: int
    symbol: str
    side: Side
    qty: float
    price: float
    fee: float
