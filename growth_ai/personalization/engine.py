from __future__ import annotations

from growth_ai.llm.client import generate
from growth_ai.llm.prompts import RETENTION, UPSELL, WELCOME


def segment(user: dict) -> str:
    if user.get("usage", 0) > 1000:
        return "power"
    if user.get("days_inactive", 0) > 7:
        return "churn_risk"
    return "new"


def message(user: dict) -> str:
    seg = segment(user)
    if seg == "new":
        return generate(WELCOME, {"segment": seg})
    if seg == "churn_risk":
        return generate(RETENTION, {"segment": seg})
    return generate(UPSELL, {"segment": seg})
