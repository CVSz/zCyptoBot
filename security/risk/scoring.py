def risk_score(tx):
    score = 0.0

    # abnormal amount
    if tx["amount"] > tx["avg"] * 3:
        score += 0.4

    # device anomaly
    if tx["device"] != tx["known_device"]:
        score += 0.3

    # geo mismatch
    if tx["geo"] != tx["last_geo"]:
        score += 0.3

    return min(score, 1.0)


def allow(tx):
    return risk_score(tx) < 0.7
