from dataclasses import dataclass, field
from typing import List


@dataclass
class Order:
    order_id: str
    side: str  # "buy" (consumer) or "sell" (provider)
    price: float  # unit price
    qty: float  # normalized compute units
    node_id: str = ""  # provider id for sell orders


@dataclass
class OrderBook:
    bids: List[Order] = field(default_factory=list)  # buy
    asks: List[Order] = field(default_factory=list)  # sell

    def add(self, o: Order):
        if o.side == "buy":
            self.bids.append(o)
            self.bids.sort(key=lambda x: -x.price)
        else:
            self.asks.append(o)
            self.asks.sort(key=lambda x: x.price)
