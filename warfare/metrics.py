def kpis(uptime, latency_ms, cost, violations):
    return {
        "Uptime": uptime,
        "LatencyP95_ms": latency_ms,
        "Cost": cost,
        "ComplianceViolations": violations,
    }
