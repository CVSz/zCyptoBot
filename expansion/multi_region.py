def expand_regions(customer):
    if customer["latency"] > 200:
        return ["us", "ap", "eu"]
    return ["us"]
