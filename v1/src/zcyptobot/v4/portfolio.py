from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class StrategySlice:
    name: str
    target_weight: float
    expected_vol: float


class PortfolioAllocator:
    """Risk-budget allocator for multi-strategy portfolio."""

    def allocate(self, slices: list[StrategySlice], gross_limit: float = 1.0) -> dict[str, float]:
        if not slices:
            return {}
        inv_vol = {s.name: 1.0 / max(s.expected_vol, 1e-6) for s in slices}
        raw = {s.name: inv_vol[s.name] * s.target_weight for s in slices}
        scale = gross_limit / sum(raw.values())
        return {k: v * scale for k, v in raw.items()}
