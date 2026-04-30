def score(proposal, weights):
    """
    proposal: dict with keys (price, tech, compliance, sla)
    weights: dict with weights summing to 1
    """
    required = {"price", "tech", "compliance", "sla"}
    if not required.issubset(proposal):
        raise ValueError("missing fields")

    return (
        proposal["price"] * weights["price"]
        + proposal["tech"] * weights["tech"]
        + proposal["compliance"] * weights["compliance"]
        + proposal["sla"] * weights["sla"]
    )
