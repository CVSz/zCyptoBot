USAGE = {}


def record(tenant, n):
    USAGE[tenant] = USAGE.get(tenant, 0) + n
