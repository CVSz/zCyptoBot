# Incident Response (DORA-aligned)

Detection:
- Alert via SLO breach (latency/error)

Triage:
- Severity (SEV1–SEV3)
- Impacted tenants/regions

Containment:
- Traffic shift (failover_region)
- Rate limit / circuit breaker

Eradication:
- Patch / rollback

Recovery:
- Restore service (SLO back within target)

Postmortem:
- RCA within 72h
- Actions tracked
