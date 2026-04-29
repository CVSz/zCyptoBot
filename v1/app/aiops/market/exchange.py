"""Exchange loop: order ingest + clearing + governance gate + execution."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from app.aiops.governance.policy_guard import PolicyGuard
from app.aiops.governance.voting import Voting
from app.aiops.market.clearing import Trade, clear_market
from app.aiops.market.orderbook import OrderBook


class MarketExchange:
    def __init__(self, orderbook: OrderBook | None = None) -> None:
        self.orderbook = orderbook or OrderBook()
        self.guard = PolicyGuard()

    def run_once(self, voters: Voting) -> list[dict[str, Any]]:
        bids, asks = self.orderbook.get()
        trades = clear_market(bids, asks)
        if not trades:
            return []

        action = {
            "type": "scale_cluster",
            "cost": sum(t.price * t.qty for t in trades),
            "trades": len(trades),
        }
        if not (voters.result() and self.guard.allow(action)):
            return []

        return [asdict(t) for t in trades]


def execute_trades(trades: list[Trade]) -> list[str]:
    events = []
    for trade in trades:
        events.append(
            f"{trade.buyer} buys {trade.qty} {trade.resource} from {trade.seller} @ {trade.price}"
        )
    return events
