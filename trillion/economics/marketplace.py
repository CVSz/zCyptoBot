def match_supply(demand, suppliers):
    """
    Choose supplier meeting SLO at lowest effective price.
    """
    viable = [s for s in suppliers if s["latency"] <= demand["max_latency"]]
    if not viable:
        raise RuntimeError("no viable suppliers")
    return min(viable, key=lambda s: s["price"])
