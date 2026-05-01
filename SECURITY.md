# Security Policy

## Supported Versions

We actively support the following branches:

| Branch | Status |
|--------|--------|
| main | ✅ Supported |
| release/* | ✅ Supported |
| others | ❌ Not supported |

---

## Reporting a Vulnerability

**Do not open public issues for security vulnerabilities.**

Please report via:
- Email: security@zypto.io
- Or GitHub Security Advisory (preferred)

Include:
- Affected component/service (api/worker/core/infra)
- Steps to reproduce / PoC
- Impact assessment
- Suggested fix (if available)

**Response SLA**
- Acknowledgement: ≤ 24 hours
- Triage: ≤ 72 hours
- Patch/mitigation: based on severity

---

## Severity & Triage

| Severity | Example | Target Response |
|----------|---------|-----------------|
| Critical | Auth bypass, RCE, key leakage | Immediate |
| High | Privilege escalation, tenant breakout | ≤ 24–72h |
| Medium | Data exposure (non-PII), SSRF (limited) | ≤ 7 days |
| Low | Misconfig, info leak | ≤ 30 days |

We use CVSS v3.1 as guidance.

---

## Secure Development Practices

### 1) Authentication & Authorization
- JWT (short-lived) + refresh tokens
- RBAC enforced at API + worker boundaries
- Tenant isolation on every request (`tenant_id` mandatory)

### 2) Secrets Management
- **No plaintext secrets in repo**
- Use Vault / cloud secret manager / SealedSecrets
- Rotate keys regularly (JWKS with key IDs)

### 3) Input Validation
- Strict schema validation (Pydantic / Zod)
- Reject unknown fields
- Size limits on payloads

### 4) Data Protection
- TLS 1.2+ in transit
- Encrypt sensitive data at rest (KMS)
- Mask PII in logs

### 5) Messaging Safety
- Idempotency keys for all commands/events
- At-least-once delivery with deduplication
- DLQ for poison messages

### 6) Execution Safety (Critical)
- **Risk Engine required before execution**
- Position / cost / rate limits
- Circuit breakers for downstream failures

### 7) Dependency Security
- Automated scanning (Dependabot/CodeQL)
- Pin versions; avoid unmaintained libs

---

## Infrastructure Security

### Kubernetes
- mTLS (Istio/Linkerd) enforced
- NetworkPolicies: default deny
- ReadOnly root filesystem where possible
- Resource limits/requests set for all pods
- Liveness/Readiness probes

### Kafka / Messaging
- TLS + SASL (SCRAM/IAM)
- Topic-level ACLs per service/tenant (when applicable)
- Quotas to prevent abuse

### Cloud (AWS/GCP/Azure)
- Least-privilege IAM
- Separate accounts/projects per env
- Audit logs enabled (CloudTrail/Cloud Audit Logs)

---

## CI/CD Security

- Protected branches (require PR + reviews)
- Required status checks (tests, lint, CodeQL)
- Artifact signing (optional: cosign)
- Secrets only via CI secret store

---

## Logging & Monitoring

- Centralized logs (no secrets)
- Security alerts:
  - auth failures spike
  - privilege escalation attempts
  - anomalous spend (per-tenant budgets)
- SLO/SLI with alerts (latency, error rate)

---

## Incident Response

1. Detect (alerts/monitoring)
2. Contain (revoke keys, isolate pods)
3. Eradicate (patch, redeploy)
4. Recover (restore service, validate)
5. Postmortem (RCA, action items)

Runbooks are in `docs/runbooks/`.

---

## Disclosure Policy

We follow coordinated disclosure:
- Fix developed and validated
- Users notified with mitigation steps
- CVE issued if applicable

---

## Acknowledgements

We appreciate responsible disclosure and will credit researchers upon request.

---

## Contact

- security@zypto.io
- Maintainers: see `CODEOWNERS`
