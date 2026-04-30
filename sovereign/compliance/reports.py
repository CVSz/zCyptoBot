def compliance_summary(metrics: dict) -> str:
    return (
        f"Incidents={metrics.get('incidents', 0)}, "
        f"SLO={metrics.get('slo', 'n/a')}, "
        f"DSR_SLA={metrics.get('dsr_sla', 'n/a')}"
    )
