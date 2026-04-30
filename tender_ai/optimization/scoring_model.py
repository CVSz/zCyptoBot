def score(p):
    # normalized scoring (0–1)
    return (
        0.3 * p["price"]
        + 0.3 * p["tech"]
        + 0.25 * p["compliance"]
        + 0.15 * p["sla"]
    )
