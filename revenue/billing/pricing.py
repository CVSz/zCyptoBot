"""Simple pricing utilities for metered usage billing.

Security/compliance note:
- Unknown metrics are rejected instead of silently ignored to prevent accidental
  under-billing and improve auditability.
"""

from typing import Iterable, Mapping

RATES = {
    "cpu": 0.02,
    "gpu": 0.5,
    "request": 0.0001,
}


def price(usage: Iterable[Mapping[str, float]]) -> float:
    """Compute total price from usage records.

    Each usage record must contain:
    - ``metric``: one of ``cpu``, ``gpu``, ``request``
    - ``value``: numeric usage quantity
    """
    total = 0.0
    for entry in usage:
        metric = entry["metric"]
        if metric not in RATES:
            raise ValueError(f"Unsupported metric: {metric}")
        total += entry["value"] * RATES[metric]
    return total
