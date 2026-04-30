from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

CHECKS = {
    "access_control": False,
    "encryption": False,
    "logging": False,
    "monitoring": False,
    "backup_dr": False,
    "incident_response": False,
    "vendor_risk": False,
}


@dataclass
class SOC2Config:
    rbac: bool = False
    sso: bool = False
    tls: bool = False
    aes: bool = False
    audit: bool = False
    immutable_logs: bool = False
    metrics: bool = False
    slo_alerts: bool = False
    backup: bool = False
    dr: bool = False
    incident_runbook: bool = False
    vendor_assessment: bool = False


def run_checks(config: Dict[str, bool]) -> Dict[str, bool]:
    CHECKS["access_control"] = bool(config.get("rbac") and config.get("sso"))
    CHECKS["encryption"] = bool(config.get("tls") and config.get("aes"))
    CHECKS["logging"] = bool(config.get("audit") and config.get("immutable_logs"))
    CHECKS["monitoring"] = bool(config.get("metrics") and config.get("slo_alerts"))
    CHECKS["backup_dr"] = bool(config.get("backup") and config.get("dr"))
    CHECKS["incident_response"] = bool(config.get("incident_runbook"))
    CHECKS["vendor_risk"] = bool(config.get("vendor_assessment"))
    return CHECKS.copy()


def compliance_score() -> float:
    return sum(CHECKS.values()) / len(CHECKS)


if __name__ == "__main__":
    report = run_checks(SOC2Config().__dict__)
    print(report)
    print(f"score={compliance_score():.2%}")
