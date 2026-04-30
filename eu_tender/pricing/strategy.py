def tender_price(cost, margin=0.25, strategic=False):
    """
    strategic: allow lower margin to land lighthouse deal
    """
    if cost <= 0:
        raise ValueError("invalid cost")

    if strategic:
        return cost * 1.1  # low margin to win
    return cost * (1 + margin)
