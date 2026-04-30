USAGE = []


def record(tenant, metric, value):
    USAGE.append({
        "tenant": tenant,
        "metric": metric,
        "value": value,
    })
