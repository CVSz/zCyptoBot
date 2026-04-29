from __future__ import annotations

from dataclasses import dataclass

from zcyptobot.core.arbitrage import MultiExchangeArbitrage, VenueQuote


@dataclass(slots=True)
class ExchangeBalance:
    venue: str
    quote_balance: float
    base_balance: float


@dataclass(slots=True)
class ArbitrageExecutionPlan:
    buy_venue: str
    sell_venue: str
    quantity: float
    expected_net_bps: float


class ArbitrageRouterV6:
    """v6: multi-exchange arbitrage routing with balance-aware sizing."""

    def __init__(self, min_notional: float = 50.0, max_notional: float = 5_000.0) -> None:
        self.min_notional = min_notional
        self.max_notional = max_notional
        self.engine = MultiExchangeArbitrage()

    def plan(self, quotes: list[VenueQuote], balances: list[ExchangeBalance], min_net_bps: float = 3.0) -> ArbitrageExecutionPlan | None:
        opp = self.engine.find(quotes, min_net_bps=min_net_bps)
        if opp is None:
            return None

        by_venue = {b.venue: b for b in balances}
        if opp.buy_venue not in by_venue or opp.sell_venue not in by_venue:
            return None

        buy_quote = next(q for q in quotes if q.venue == opp.buy_venue)
        buy_power = by_venue[opp.buy_venue].quote_balance
        sell_inventory = by_venue[opp.sell_venue].base_balance

        max_qty_from_cash = buy_power / buy_quote.ask
        qty = min(max_qty_from_cash, sell_inventory, self.max_notional / buy_quote.ask)
        if qty * buy_quote.ask < self.min_notional or qty <= 0:
            return None

        return ArbitrageExecutionPlan(opp.buy_venue, opp.sell_venue, qty, opp.net_edge_bps)
