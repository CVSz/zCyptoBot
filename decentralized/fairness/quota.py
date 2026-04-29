LIMITS = {}


def set_limit(t: str, units: float):
    LIMITS[t] = units


def allow(t: str, used: float) -> bool:
    return used <= LIMITS.get(t, float("inf"))
