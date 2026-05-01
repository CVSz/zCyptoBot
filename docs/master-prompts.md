# Master Prompts: End-to-End System Evolution

## Prompt 1 — Full System Generator

```text
You are a principal distributed systems architect.

Generate a production-grade AI decision platform with:

- Clean architecture (apps/core/infra)
- Event-driven system (Kafka)
- Multi-tenant SaaS (auth, billing, RBAC)
- OPA policy enforcement
- SPIFFE identity + Istio mesh
- CodeQL + Semgrep security
- Feature store + RL engine

Constraints:
- No TODO / no placeholders
- Full working code
- Docker + K8s + Terraform included
- Observability (Prometheus + Grafana)

Output:
- full repo structure
- then files in batches
```

## Prompt 2 — Security Hardening

```text
Upgrade the system to zero-trust:

- Add OPA policies (tenant, cost, RBAC)
- Add SPIFFE + workload identity
- Add Istio mTLS mesh
- Add Kyverno enforce signed images
- Add Falco runtime security

Ensure:
- No cross-tenant leakage
- All execution paths validated
- All services authenticated via mTLS
```

## Prompt 3 — AI + Optimization

```text
Add AI optimization layer:

- Feature store (online/offline)
- RL engine (policy gradient)
- Cost optimization per tenant
- Dynamic pricing model

Add:
- online learning loop
- experiment tracking
- A/B testing + uplift modeling
```

## Prompt 4 — Hyperscaler Expansion

```text
Upgrade system to multi-cloud federation:

- AWS + GCP + Azure
- global load balancing
- cross-region identity federation
- data locality compliance

Add:
- cost routing optimizer
- global control plane
```
