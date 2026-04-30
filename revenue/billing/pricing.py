RATES = {
    "cpu": 0.02,
    "gpu": 0.5,
    "request": 0.0001,
}


def price(usage):
    return sum(u["value"] * RATES[u["metric"]] for u in usage)
