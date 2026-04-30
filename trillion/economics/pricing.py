def value_based_price(cost: float, savings_ratio: float) -> float:
    """
    Price anchored to delivered savings; guard rails for margin.
    """
    if savings_ratio < 0:
        raise ValueError("invalid savings_ratio")
    base = cost * (1 + 0.2)  # floor margin
    value = cost * (1 + savings_ratio * 0.5)
    return max(base, value)
