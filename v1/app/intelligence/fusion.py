def fuse(momentum: float, sentiment: float, whale: float, funding: float) -> str:
    score = 0.4 * momentum + 0.2 * sentiment + 0.3 * whale + 0.1 * funding
    if score > 0.2:
        return "LONG"
    if score < -0.2:
        return "SHORT"
    return "HOLD"
