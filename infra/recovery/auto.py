def recover(system_state):
    if system_state["latency"] > 500:
        return "failover_region"
    if system_state["error"] > 0.1:
        return "restart_service"
    return "stable"
