def route(models):
    valid = [m for m in models if m.get("region", "").startswith("eu")]
    if not valid:
        raise RuntimeError("no EU models available")

    # minimize cost + latency
    return min(valid, key=lambda m: m["cost"] + m["latency"])
