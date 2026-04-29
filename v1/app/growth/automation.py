from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List

from app.tenancy.context import get_tenant


@dataclass
class FunnelEvent:
    user_id: str
    stage: str
    tenant_id: str


class GrowthAutomation:
    def __init__(self) -> None:
        self._events: List[FunnelEvent] = []
        self._campaigns: Dict[str, Dict[str, str]] = {}

    def track_stage(self, user_id: str, stage: str, tenant_id: str | None = None) -> FunnelEvent:
        tid = tenant_id or get_tenant()
        event = FunnelEvent(user_id=user_id, stage=stage, tenant_id=tid)
        self._events.append(event)
        return event

    def upsert_campaign(self, campaign_id: str, model: str, prompt: str, tenant_id: str | None = None) -> Dict[str, str]:
        tid = tenant_id or get_tenant()
        key = f"{tid}:{campaign_id}"
        self._campaigns[key] = {"tenant_id": tid, "campaign_id": campaign_id, "model": model, "prompt": prompt}
        return self._campaigns[key]

    def generate_actions(self, tenant_id: str | None = None) -> List[Dict[str, str]]:
        tid = tenant_id or get_tenant()
        stage_counts = Counter([e.stage for e in self._events if e.tenant_id == tid])
        actions: List[Dict[str, str]] = []
        if stage_counts.get("signup", 0) > stage_counts.get("activated", 0):
            actions.append({"play": "activation_nudge", "channel": "email", "goal": "activate_new_users"})
        if stage_counts.get("trial", 0) > stage_counts.get("paid", 0):
            actions.append({"play": "trial_to_paid", "channel": "in_app", "goal": "expand_revenue"})
        if not actions:
            actions.append({"play": "retention_loop", "channel": "push", "goal": "protect_nrr"})
        return actions

    def analytics(self, tenant_id: str | None = None) -> Dict[str, Dict[str, int]]:
        tid = tenant_id or get_tenant()
        per_stage: Dict[str, int] = Counter([e.stage for e in self._events if e.tenant_id == tid])
        per_user = defaultdict(int)
        for e in self._events:
            if e.tenant_id == tid:
                per_user[e.user_id] += 1
        return {"stages": dict(per_stage), "active_users": len(per_user), "events": sum(per_stage.values())}


growth_automation = GrowthAutomation()
