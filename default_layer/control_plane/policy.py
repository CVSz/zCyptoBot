def allow(claims, action):
    if action.get("data_class") == "PII" and claims.get("region") != action.get("target_region"):
        return False
    if action.get("latency_ms", 0) > action.get("slo_ms", 9999):
        return False
    if action.get("cost", 0) > action.get("budget", float("inf")):
        return False
    return True
