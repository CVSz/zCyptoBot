from fastapi import APIRouter, Depends

from app.api.deps import current_user
from app.auth.rbac import require
from app.enterprise.saas import enterprise_saas
from app.growth.automation import growth_automation

router = APIRouter()


@router.post("/strategy/toggle")
def toggle_strategy(enable: bool, user=Depends(current_user)):
    require("admin")(user)
    enterprise_saas.add_audit_event(actor=user["username"], action="strategy.toggle", resource=f"enabled={enable}")
    return {"status": "ok", "enabled": enable}


@router.post("/enterprise/rbac/assign")
def assign_role(username: str, role: str, user=Depends(current_user)):
    require("admin")(user)
    return enterprise_saas.assign_role(username=username, role=role)


@router.get("/enterprise/rbac")
def list_roles(user=Depends(current_user)):
    require("admin")(user)
    return {"roles": enterprise_saas.list_roles()}


@router.get("/enterprise/audit")
def audit_log(limit: int = 100, user=Depends(current_user)):
    require("admin")(user)
    return {"events": [e.__dict__ for e in enterprise_saas.get_audit_events(limit=limit)]}


@router.post("/enterprise/slo")
def update_slo(service: str, availability: float, p95_latency_ms: float, error_rate: float, user=Depends(current_user)):
    require("admin")(user)
    return enterprise_saas.upsert_slo(service=service, availability=availability, p95_latency_ms=p95_latency_ms, error_rate=error_rate)


@router.get("/enterprise/slo")
def slo_dashboard(user=Depends(current_user)):
    require("admin")(user)
    return {"dashboard": enterprise_saas.slo_dashboard()}


@router.post("/growth/campaign")
def upsert_growth_campaign(campaign_id: str, model: str, prompt: str, user=Depends(current_user)):
    require("admin")(user)
    return growth_automation.upsert_campaign(campaign_id=campaign_id, model=model, prompt=prompt)


@router.get("/growth/automation/actions")
def growth_actions(user=Depends(current_user)):
    require("admin")(user)
    return {"actions": growth_automation.generate_actions()}


@router.get("/growth/analytics")
def growth_analytics(user=Depends(current_user)):
    require("admin")(user)
    return growth_automation.analytics()
