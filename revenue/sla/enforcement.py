SLA = {
    "latency": 200,
    "uptime": 0.999,
}


def check(metrics):
    if metrics["latency"] > SLA["latency"]:
        return "violation"
    return "ok"
