"""Double auction market clearing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Trade:
    buyer: str
    seller: str
    resource: str
    qty: int
    price: float


def clear_market(bids: list[dict[str, Any]], asks: list[dict[str, Any]]) -> list[Trade]:
    bids = sorted(bids, key=lambda x: -x["price"])
    asks = sorted(asks, key=lambda x: x["price"])

    trades: list[Trade] = []
    i = 0
    j = 0

    while i < len(bids) and j < len(asks):
        if bids[i]["res"] != asks[j]["res"]:
            j += 1
            continue

        if bids[i]["price"] >= asks[j]["price"]:
            qty = min(bids[i]["qty"], asks[j]["qty"])
            price = round((bids[i]["price"] + asks[j]["price"]) / 2.0, 4)
            trades.append(
                Trade(
                    buyer=bids[i]["agent"],
                    seller=asks[j]["agent"],
                    resource=bids[i]["res"],
                    qty=qty,
                    price=price,
                )
            )
            bids[i]["qty"] -= qty
            asks[j]["qty"] -= qty
            if bids[i]["qty"] == 0:
                i += 1
            if asks[j]["qty"] == 0:
                j += 1
        else:
            break
    return trades
