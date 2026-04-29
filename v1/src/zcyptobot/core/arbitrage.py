from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VenueQuote:
    venue: str
    bid: float
    ask: float
    taker_fee_bps: float


@dataclass(slots=True)
class ArbOpportunity:
    buy_venue: str
    sell_venue: str
    gross_edge_bps: float
    net_edge_bps: float


class MultiExchangeArbitrage:
    def find(self, quotes: list[VenueQuote], min_net_bps: float = 3.0) -> ArbOpportunity | None:
        best_buy = min(quotes, key=lambda q: q.ask)
        best_sell = max(quotes, key=lambda q: q.bid)
        gross = ((best_sell.bid - best_buy.ask) / best_buy.ask) * 10_000
        fee = best_buy.taker_fee_bps + best_sell.taker_fee_bps
        net = gross - fee
        if best_buy.venue == best_sell.venue or net < min_net_bps:
            return None
        return ArbOpportunity(best_buy.venue, best_sell.venue, gross, net)
