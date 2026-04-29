from fastapi import APIRouter, Depends

from app.api.deps import current_user
from app.auth.rbac import require
from app.guardrails.budgets import Budget
from app.guardrails.circuit import CircuitBreaker
from app.guardrails.kill_switch import KillSwitch

router = APIRouter()
ks = KillSwitch()
budget = Budget(1_000_000)
cb = CircuitBreaker(threshold=0.15)


@router.post("/kill-switch")
def kill(on: bool, user=Depends(current_user)):
    require("god")(user)
    ks.set(on)
    return {"kill": ks.is_on()}


@router.post("/budget")
def set_budget(v: float, user=Depends(current_user)):
    require("god")(user)
    tenant = user.get("tenant_id", "public")
    budget.set(tenant, v)
    return {"tenant": tenant, "budget": budget.get(tenant)}


@router.post("/circuit")
def set_circuit(v: float, user=Depends(current_user)):
    require("god")(user)
    tenant = user.get("tenant_id", "public")
    cb.set(tenant, v)
    return {"tenant": tenant, "threshold": cb.get(tenant)}
