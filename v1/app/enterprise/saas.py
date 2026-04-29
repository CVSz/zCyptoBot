from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List

from app.tenancy.context import get_tenant


@dataclass
class AuditEvent:
    actor: str
    action: str
    resource: str
    tenant_id: str
    ts: str


class EnterpriseSaaS:
    """In-memory enterprise control-plane primitives for RBAC/audit/SLO/tenancy."""

    def __init__(self) -> None:
        self._role_bindings: Dict[str, Dict[str, str]] = {}
        self._audit_logs: List[AuditEvent] = []
        self._slo: Dict[str, Dict[str, float]] = {}

    def assign_role(self, username: str, role: str, tenant_id: str | None = None) -> Dict[str, str]:
        tid = tenant_id or get_tenant()
        self._role_bindings.setdefault(tid, {})[username] = role
        self._append_audit(actor="system", action="role.assign", resource=f"{username}:{role}", tenant_id=tid)
        return {"tenant_id": tid, "username": username, "role": role}

    def list_roles(self, tenant_id: str | None = None) -> Dict[str, str]:
        tid = tenant_id or get_tenant()
        return self._role_bindings.get(tid, {})

    def add_audit_event(self, actor: str, action: str, resource: str, tenant_id: str | None = None) -> AuditEvent:
        tid = tenant_id or get_tenant()
        event = self._append_audit(actor=actor, action=action, resource=resource, tenant_id=tid)
        return event

    def get_audit_events(self, tenant_id: str | None = None, limit: int = 100) -> List[AuditEvent]:
        tid = tenant_id or get_tenant()
        return [e for e in self._audit_logs if e.tenant_id == tid][-limit:]

    def upsert_slo(self, service: str, availability: float, p95_latency_ms: float, error_rate: float, tenant_id: str | None = None) -> Dict[str, float | str]:
        tid = tenant_id or get_tenant()
        self._slo.setdefault(tid, {})[service] = {
            "availability": availability,
            "p95_latency_ms": p95_latency_ms,
            "error_rate": error_rate,
        }
        self._append_audit(actor="system", action="slo.upsert", resource=service, tenant_id=tid)
        return {"tenant_id": tid, "service": service, **self._slo[tid][service]}

    def slo_dashboard(self, tenant_id: str | None = None) -> Dict[str, Dict[str, float]]:
        tid = tenant_id or get_tenant()
        return self._slo.get(tid, {})

    def _append_audit(self, actor: str, action: str, resource: str, tenant_id: str) -> AuditEvent:
        event = AuditEvent(
            actor=actor,
            action=action,
            resource=resource,
            tenant_id=tenant_id,
            ts=datetime.now(timezone.utc).isoformat(),
        )
        self._audit_logs.append(event)
        return event


enterprise_saas = EnterpriseSaaS()
