"""Self-evolution helpers for autonomous model tuning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass
class TunableModel:
    lr: float


def evolve(model: TunableModel, metrics: Mapping[str, float]) -> float:
    """Apply simple learning-rate adaptation and return updated value."""
    latency = metrics.get("latency", 0)
    revenue = metrics.get("revenue", 0)

    if latency > 200:
        model.lr *= 0.9
    if revenue < 1000:
        model.lr *= 1.1
    return model.lr
