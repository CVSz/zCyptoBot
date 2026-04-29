from typing import Dict, Optional, Tuple


def best_pair(books: Dict[str, Dict[str, float]]) -> Optional[Tuple[str, str, float, float]]:
    best_ask_ex, best_ask = None, float("inf")
    best_bid_ex, best_bid = None, 0.0

    for ex, b in books.items():
        if b["ask"] < best_ask:
            best_ask, best_ask_ex = b["ask"], ex
        if b["bid"] > best_bid:
            best_bid, best_bid_ex = b["bid"], ex

    if best_ask_ex and best_bid_ex and best_bid_ex != best_ask_ex:
        return best_ask_ex, best_bid_ex, best_ask, best_bid
    return None


def net_edge(buy_ask: float, sell_bid: float, fee_buy: float, fee_sell: float) -> float:
    gross = (sell_bid - buy_ask) / buy_ask
    return gross - (fee_buy + fee_sell)


def is_actionable(edge: float, min_edge: float, max_staleness_ms: int, age_ms: int) -> bool:
    return edge > min_edge and age_ms <= max_staleness_ms
