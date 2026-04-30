"""Per-tenant budget-aware spend allocation helpers."""

from __future__ import annotations

from threading import Lock

BUDGET: dict[str, float] = {
    "tenant_a": 1000,
}

SPENT: dict[str, float] = {}
_LOCK = Lock()


def can_spend(tenant: str, cost: float) -> bool:
    """Check if tenant can spend the requested cost without exceeding budget."""
    if cost < 0:
        return False
    return SPENT.get(tenant, 0) + cost <= BUDGET.get(tenant, 0)


def allocate(tenant: str, cost: float) -> bool:
    """Allocate spend to tenant if budget allows."""
    with _LOCK:
        if not can_spend(tenant, cost):
            return False
        SPENT[tenant] = SPENT.get(tenant, 0) + cost
        return True


def remaining(tenant: str) -> float:
    """Return remaining budget for a tenant."""
    return max(BUDGET.get(tenant, 0) - SPENT.get(tenant, 0), 0)
