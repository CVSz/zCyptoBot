def explain(state: dict[str, float], action: str) -> dict:
    reasons: list[str] = []
    if state["latency"] > 200:
        reasons.append("High latency triggered scaling")
    if state["error"] > 0.05:
        reasons.append("Error rate triggered restart")

    return {"action": action, "reasons": reasons or ["Default policy"]}
