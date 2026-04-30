"""Deterministic A/B assignment and result comparison helpers."""

from __future__ import annotations

import hashlib
from statistics import mean

RESULTS: dict[str, list[float]] = {"A": [], "B": []}


def assign(user_id: str) -> str:
    """Assign users deterministically into A or B using stable hashing."""
    bucket = int(hashlib.sha1(user_id.encode("utf-8")).hexdigest(), 16)
    return "A" if bucket % 2 == 0 else "B"


def record(group: str, outcome: float) -> None:
    """Record outcome for a given experiment group."""
    if group not in RESULTS:
        raise ValueError(f"Unknown group: {group}")
    RESULTS[group].append(outcome)


def compare() -> tuple[float, float]:
    """Compare mean outcomes between groups A and B.

    Returns 0.0 for groups with no observations.
    """
    a = mean(RESULTS["A"]) if RESULTS["A"] else 0.0
    b = mean(RESULTS["B"]) if RESULTS["B"] else 0.0
    return float(a), float(b)
