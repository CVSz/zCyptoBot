from dataclasses import dataclass
from typing import List


@dataclass
class Target:
    name: str
    revenue: float
    growth: float
    synergy_score: float  # 0-1
    integration_risk: float  # 0-1


def score(t: Target) -> float:
    """Score a target by balancing upside and integration risk."""
    return (0.5 * t.synergy_score + 0.3 * t.growth) - (0.2 * t.integration_risk)


def shortlist(targets: List[Target], k: int = 5) -> List[Target]:
    """Return the top-k ranked targets by strategic fit."""
    ranked = sorted(targets, key=score, reverse=True)
    return ranked[:k]
