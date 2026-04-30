"""Shadow mode decision comparison for safe rollout checks."""

from __future__ import annotations

from typing import Any, Callable


def shadow_decision(
    new_policy: Callable[[Any], float],
    old_policy: Callable[[Any], float],
    input: Any,
) -> dict[str, float | bool]:
    """Run old policy as source-of-truth and compare with new policy output."""
    real = old_policy(input)
    shadow = new_policy(input)
    diff = shadow - real
    return {
        "real": real,
        "shadow": shadow,
        "diff": diff,
        "regression": diff < 0,
    }
