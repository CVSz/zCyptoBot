# Zypto Monorepo

Zypto is a large multi-domain monorepo for autonomous trading infrastructure, AI/Ops orchestration, compliance automation, sovereign cloud patterns, growth systems, and hyperscale service simulation.

This repository combines:
- **Core product code** (API/services, execution, signal/risk engines).
- **Platform and infra assets** (Kubernetes, Helm, Terraform, observability).
- **Governance/compliance frameworks** (policy-as-code, auditing, public-sector controls).
- **Commercial and GTM materials** (pitch decks, dataroom docs, sales playbooks).
- **Hyperscale simulation suites** for multi-service operational patterns.

---

## Quick Start

### 1) Explore the documentation first
Start with the curated docs map:
- [`docs/DOCUMENTATION_INDEX.md`](docs/DOCUMENTATION_INDEX.md)
- [`docs/DEEP_REPO_OVERVIEW.md`](docs/DEEP_REPO_OVERVIEW.md)

### 2) Focus on primary implementation tracks
- **`v1/`**: main Python implementation track with app code, tests, infra manifests, and deployment modules.
- **`zeaz/`, `zeaz-v12/`, `zeaz-live/`**: adjacent platform variants/evolutions.
- **`frontend/`**: UI pages and dashboard surface.
- **`tests/` + `v1/tests/`**: contract/security/system-level tests.

### 3) Baseline local checks
```bash
git status
rg --files | wc -l
pytest -q v1/tests/test_v2_core.py
```

> Tip: Given repository size, prefer targeted test runs over full-suite execution unless in CI.

---

## Monorepo Topology (High Level)

| Area | Purpose |
|---|---|
| `v1/` | Primary codebase for orchestrator, AI/Ops modules, execution, API, and infra artifacts |
| `zeaz*` families | Variant stacks, enterprise/hyperscale packaging, and deployment assets |
| `zcyptobot-hyperscale/` | Large generated multi-service simulation and deployment corpus |
| `policy/`, `sovereign*`, `public_sector_eu/` | Governance, compliance, sovereignty, and regulated workloads |
| `pitchdeck/`, `dataroom/`, `sales*`, `fundraising/` | Narrative, commercialization, and investor materials |
| `helm/`, `k8s/`, `infra/`, `monitoring/` | Cluster, deployment, and observability scaffolding |

---

## Development Guidelines

1. Make small, scoped changes with clear commit history.
2. Run local checks relevant to touched areas.
3. Prefer explicit documentation updates whenever behavior or architecture changes.
4. Keep policy, security, and compliance implications visible in PR descriptions.

---

## Recommended Reading Path

1. [`docs/DOCUMENTATION_INDEX.md`](docs/DOCUMENTATION_INDEX.md)
2. [`docs/DEEP_REPO_OVERVIEW.md`](docs/DEEP_REPO_OVERVIEW.md)
3. [`docs/architecture.md`](docs/architecture.md)
4. [`docs/FINAL_RELEASE_DOCUMENTATION.md`](docs/FINAL_RELEASE_DOCUMENTATION.md)
5. `v1/README.md`

---

## License and Governance

Refer to licensing and governance documentation in submodules (for example `v1/LICENSE`) and policy folders for domain-specific obligations.
