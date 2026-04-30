def classify(use_case: str) -> str:
    high_risk = ["biometrics", "credit_scoring", "healthcare"]
    if use_case in high_risk:
        return "high"
    return "low"
