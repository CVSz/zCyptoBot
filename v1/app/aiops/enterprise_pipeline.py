from typing import Any, Dict

from app.aiops.audit.logger import AuditLogger
from app.aiops.compliance.engine import ComplianceEngine
from app.aiops.fairness.monitor import FairnessMonitor
from app.aiops.risk.circuit import CircuitBreaker
from app.aiops.risk.limits import Limits


audit = AuditLogger()
comp = ComplianceEngine()
fair = FairnessMonitor()
risk = CircuitBreaker()


def process(decision: Dict[str, Any], tenant: Dict[str, Any]) -> Dict[str, Any]:
    audit.log({"stage": "input", "decision": decision, "tenant": tenant.get("id")})

    ok, reason = comp.check(decision)
    if not ok:
        risk.record(False)
        audit.log({"stage": "blocked", "by": "compliance", "reason": reason})
        return {"blocked": "compliance", "reason": reason}

    if not fair.check_bias([decision]):
        risk.record(False)
        audit.log({"stage": "blocked", "by": "fairness"})
        return {"blocked": "fairness"}

    if not Limits().allow(tenant, decision):
        risk.record(False)
        audit.log({"stage": "blocked", "by": "limit"})
        return {"blocked": "limit"}

    if risk.open():
        audit.log({"stage": "blocked", "by": "circuit"})
        return {"blocked": "circuit"}

    risk.record(True)
    audit.log({"stage": "approved", "decision": decision})
    return {"status": "execute"}
