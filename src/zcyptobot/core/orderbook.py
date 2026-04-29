from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DepthSnapshot:
    best_bid: float
    best_ask: float
    bid_notional_topn: float
    ask_notional_topn: float
    bid_vwap_topn: float
    ask_vwap_topn: float


class OrderbookDepthModel:
    """Microstructure features for spread, imbalance, and pressure."""

    def snapshot(self, bids: list[tuple[float, float]], asks: list[tuple[float, float]], topn: int = 10) -> DepthSnapshot:
        top_bids = bids[:topn]
        top_asks = asks[:topn]
        bid_notional = sum(p * q for p, q in top_bids)
        ask_notional = sum(p * q for p, q in top_asks)
        bid_qty = sum(q for _, q in top_bids) or 1e-9
        ask_qty = sum(q for _, q in top_asks) or 1e-9

        return DepthSnapshot(
            best_bid=top_bids[0][0],
            best_ask=top_asks[0][0],
            bid_notional_topn=bid_notional,
            ask_notional_topn=ask_notional,
            bid_vwap_topn=bid_notional / bid_qty,
            ask_vwap_topn=ask_notional / ask_qty,
        )

    @staticmethod
    def spread_bps(depth: DepthSnapshot) -> float:
        mid = (depth.best_bid + depth.best_ask) / 2
        return ((depth.best_ask - depth.best_bid) / mid) * 10_000

    @staticmethod
    def imbalance(depth: DepthSnapshot) -> float:
        denom = depth.bid_notional_topn + depth.ask_notional_topn
        return (depth.bid_notional_topn - depth.ask_notional_topn) / max(denom, 1e-9)
