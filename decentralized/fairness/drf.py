def dominant_share(usage: dict, capacity: dict):
    shares = []
    for r, u in usage.items():
        c = max(1e-6, capacity.get(r, 1.0))
        shares.append(u / c)
    return max(shares) if shares else 0.0


def pick_min_dominant(candidates: list):
    scored = [(c["node_id"], dominant_share(c["usage"], c["capacity"])) for c in candidates]
    scored.sort(key=lambda x: x[1])
    return scored[0][0] if scored else None
