RATINGS = {}


def rate(partner, score):
    if not (1 <= score <= 5):
        raise ValueError("score 1..5")
    RATINGS.setdefault(partner, []).append(score)


def avg(partner):
    s = RATINGS.get(partner, [])
    return sum(s) / len(s) if s else 0
