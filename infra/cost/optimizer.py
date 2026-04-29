def score(region):
    return (
        region["price"] * 0.5
        + region["latency"] * 0.3
        + region["carbon"] * 0.2
    )


def choose(regions):
    return min(regions, key=score)
