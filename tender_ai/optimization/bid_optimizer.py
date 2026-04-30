def optimize(cost, competitor, min_margin=0.1):
    if cost <= 0:
        raise ValueError("invalid cost")

    bid = competitor * 0.97
    floor = cost * (1 + min_margin)
    return max(bid, floor)
