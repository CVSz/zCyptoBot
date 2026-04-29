from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ChangeRequest:
    component: str
    risk_tier: str
    description: str


class ApprovalPolicy:
    """Minimal 4-eye governance policy for production changes."""

    def __init__(self, max_auto_risk_tier: str = "low") -> None:
        self.max_auto_risk_tier = max_auto_risk_tier
        self._rank = {"low": 1, "medium": 2, "high": 3, "critical": 4}

    def requires_human_approval(self, request: ChangeRequest) -> bool:
        return self._rank[request.risk_tier] > self._rank[self.max_auto_risk_tier]
