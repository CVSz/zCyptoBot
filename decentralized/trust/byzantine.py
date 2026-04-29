from statistics import median


def filter_outliers(values):
    if not values:
        return []
    m = median(values)
    return [v for v in values if abs(v - m) / max(1e-6, m) < 0.5]


def quorum(votes: list, required: int = 2):
    return sum(1 for v in votes if v) >= required
