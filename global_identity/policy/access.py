def allow(claims: dict, att: dict, action: dict) -> bool:
    if action.get("data_class") == "PII" and claims.get("region") != action.get("target_region"):
        return False
    if not att.get("secure"):
        return False
    if action.get("predicted_latency_ms", 0) > action.get("latency_slo_ms", 9999):
        return False
    if action.get("unit_cost", 0) > action.get("max_unit_cost", float("inf")):
        return False
    return True
