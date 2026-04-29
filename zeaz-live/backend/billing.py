USAGE = {}


def track(tenant: str, cost: float):
    USAGE[tenant] = USAGE.get(tenant, 0.0) + cost


def get_usage(tenant: str) -> float:
    return USAGE.get(tenant, 0.0)
