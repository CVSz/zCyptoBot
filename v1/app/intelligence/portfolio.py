def size(vol: float, capital: float = 10000, target_risk: float = 0.02) -> float:
    if vol <= 0:
        return 0
    return capital * target_risk / vol
