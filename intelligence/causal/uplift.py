"""Minimal uplift modeling utility for rollout gating."""

from __future__ import annotations

import numpy as np


class UpliftModel:
    """Collect treatment/control outcomes and estimate uplift."""

    def __init__(self) -> None:
        self.treatment: list[float] = []
        self.control: list[float] = []

    def add(self, treated: bool, outcome: float) -> None:
        """Add one observed outcome under treatment or control."""
        if treated:
            self.treatment.append(outcome)
        else:
            self.control.append(outcome)

    def uplift(self) -> float:
        """Return estimated average treatment effect (treatment - control)."""
        t = float(np.mean(self.treatment)) if self.treatment else 0.0
        c = float(np.mean(self.control)) if self.control else 0.0
        return t - c

    def is_rollout_safe(self, minimum_uplift: float = 0.0) -> bool:
        """Gate rollout by checking whether uplift exceeds a threshold."""
        return self.uplift() > minimum_uplift
