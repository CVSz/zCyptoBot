def recover(metrics):
    if metrics["error_rate"] > 0.05:
        return "rollback"
    if metrics["latency"] > 300:
        return "failover_region"
    return "stable"
