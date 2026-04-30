def optimize_bid(cost, competitor_price):
    """
    Target slightly under competitor while preserving floor margin.
    """
    if cost <= 0:
        raise ValueError("invalid cost")

    bid = min(competitor_price * 0.95, cost * 1.3)
    floor = cost * 1.1
    return max(bid, floor)
