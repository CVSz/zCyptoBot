def score(claims: dict, att: dict, action: dict) -> int:
    risk = 0
    if action.get("data_class") == "PII" and claims.get("region") != action.get("target_region"):
        risk += 50
    if not att.get("secure", False):
        risk += 30
    if action.get("predicted_latency_ms", 0) > action.get("latency_slo_ms", 9999):
        risk += 10
    if action.get("unit_cost", 0) > action.get("max_unit_cost", float("inf")):
        risk += 10
    return min(risk, 100)
