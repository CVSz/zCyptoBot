# Cross-Repository Deep Analysis

This document consolidates the repositories requested on 2026-05-05 into one platform map. The analysis was performed from shallow GitHub clones under `/tmp/zypto_repos` plus this checked-out `zypto` repository.

## Source inventory and availability

| Repository | Status | Primary stack | Core role in consolidated platform |
|---|---:|---|---|
| `cvsz/zgitcp` | cloned | Bash | Git control panel automation and operator CLI patterns. |
| `cvsz/zwallet` | cloned | TypeScript, Python, Kotlin, Go, SQL | Wallet, ledger, transaction orchestration, swap, portfolio, policy, fraud, mobile, and security middleware. |
| `cvsz/ABTPi18n` | cloned | FastAPI, Next.js, Celery, Prisma, Python strategies | Automated trading platform with i18n, pluggable strategies, exchange connectivity, payments, rental contracts, Telegram, and monitoring. |
| `cvsz/zypto` | cloned/current | Python, Kubernetes, Helm, Terraform, docs | Broad monorepo containing AI/Ops, trading, compliance, tenant, audit, infra, hyperscale simulation, GitHub security workflows, and governance assets. |
| `cvsz/ZeaZDev-Omega` | cloned | NestJS, React Native/Expo, Solidity, Unity | Consumer/miniapp, rewards, DeFi, fintech, WorldID auth, smart contracts, and game bridge. |
| `cvsz/ztsaff` | cloned | Bash, Terraform, Python, YAML | Exported installer/automation corpus, Gitea/dev-stack orchestration, TikTok review SaaS fragments, and environment scripts. |
| `cvsz/zLinebot` | cloned | TypeScript, Python, SQL, Kubernetes | LINE bot platform with LLM, billing, CRM/automation, DB migrations, ML, Kubernetes, and domain scripts. |
| `cvsz/zlttbots` | cloned | Python, JS, Docker, YAML | Multi-service bot and platform estate with many service Dockerfiles, enterprise maturity docs, scripts, tests, and infra. |
| `cvsz/zttlbots` | cloned | TypeScript, Bash, YAML | Lean LINE bot service with LLM, billing meter/ledger, Cloudflare Zero Trust scripts, domain bind scripts, and bootstrap scripts. |
| `cvsz/zTTato-Platform` | unavailable | unknown | Clone failed; treat as an external capability to re-ingest when access is restored. |
| `cvsz/zvath` | cloned | Python, FastAPI, TSX, Kubernetes | Viral/AI platform with OAuth, Stripe webhook, inference/generation, vector search, tenant enforcement, MLOps, Istio, Vault, Jaeger, Kafka, and progressive delivery. |
| `cvsz/tiktok-shop-bot` | cloned | Python | Outreach bot with templating, dedupe, rate limiting, CSV-driven CLI, and email templates. |
| `cvsz/tiktokshop-api-client` | cloned | PHP | Minimal TikTok Shop API client with tests and `.env.example`. |
| `cvsz/tiktok-shop-sdk` | cloned | TypeScript monorepo | TikTok Shop SDK, docs app, examples, webhook/auth/client abstractions, and package build/test tooling. |
| `cvsz/tiktok-shop-sdk` | cloned | TypeScript monorepo | Same repository name as requested; use as canonical TS SDK implementation. |
| `cvsz/tiktokshop-php` | cloned | PHP | Fuller TikTok Shop PHP SDK with source and PHPUnit tests. |
| `cvsz/zLinebot-automos` | cloned | JS, TS, Python, K8s, frontend/backend | Autonomous LINE/bot + web platform, Kubernetes manifests, infra scripts, landing/frontend/backend surfaces. |
| `cvsz/zeaz-platform` | cloned | Bash | Single Ubuntu dev-stack installer script; useful as legacy bootstrap input only. |
| `cvsz/zeapay` | unavailable | unknown | Clone failed; treat as external payment provider placeholder until access is restored. |

## Consolidated capability catalog

### Wallet, payments, fintech, and blockchain

- Wallet engines, transaction orchestrators, swap services, indexers, policy and portfolio services from `zwallet`.
- Ledger constraints, settlement, clearing, reconciliation, idempotency, system accounts, final consistency, and bank-grade hardening patterns from `zwallet`.
- PromptPay/rental payments from `ABTPi18n`; Stripe webhooks from `zvath`; DeFi/rewards/tokenomics/contracts from `ZeaZDev-Omega`; payment marketplace patterns from `zypto`.
- Required refactor: collapse these into `payment-service`, `wallet-service`, `ledger-service`, `policy-service`, `settlement-worker`, and `chain-indexer` with shared event contracts.

### Trading, exchange, strategy, and automation

- `ABTPi18n` supplies FastAPI/Celery trading loops, strategy registry/autoload, CCXT exchange adapter concepts, TradingView webhook ingestion, risk management, backtesting, paper trading, ML signal scoring, and Telegram alerts.
- `zypto` adds orchestration, signal/risk engines, AI/Ops control modules, simulations, policy-as-code, and hyperscale service fixtures.
- Required refactor: isolate trading into `strategy-service`, `execution-service`, `risk-service`, `market-data-service`, and `backtest-worker`.

### Bot, messaging, LLM, and outreach

- LINE bot platforms from `zLinebot`, `zLinebot-automos`, `zttlbots`, and `zlttbots` contain webhook ingestion, CRM/automation, LLM tools/safety/streaming, billing meter/ledger, and domain bootstrap scripts.
- `tiktok-shop-bot` contributes outreach templating, dedupe, and rate-limit mechanics.
- Required refactor: route all webhook/bot events through `bot-gateway`, then tenant-aware `conversation-service`, `automation-worker`, `llm-service`, and `billing-meter`.

### TikTok Shop commerce integrations

- TypeScript SDK from `tiktok-shop-sdk` is the canonical typed client.
- PHP clients (`tiktokshop-api-client`, `tiktokshop-php`) indicate cross-language SDK needs and test fixtures.
- Required refactor: create `commerce-connector-service` with signed TikTok API requests, webhook verification, product/order/seller sync jobs, and SDK wrappers generated from one OpenAPI schema.

### AI, ML, MLOps, and recommendations

- `zvath` contains generation/inference routes, vector search, model registry load/log utilities, KServe/Kubeflow/Feast assets, GPU node manifests, RL/recommendation tests, and autonomous SRE assets.
- `zypto` contains AI control, pricing, fraud, world model, cost optimizer, autonomous organization modules, and governance simulations.
- Required refactor: standardize around `ai-gateway`, `feature-service`, `vector-service`, `model-registry`, `inference-worker`, and `mlops-pipeline`.

### Identity, auth, access control, compliance, and audit

- Google OAuth in `ABTPi18n`, WorldID in `ZeaZDev-Omega`, OAuth in `zvath`, RBAC/tenant/audit modules in `zypto`, and risk/security middleware in `zwallet` should be unified.
- Compliance and evidence engines exist in `zypto` (`cert_saas`, `regulatory_moat`, `audit_simulation`, `trust_fabric`).
- Required refactor: implement a shared `identity-service`, `tenant-service`, `authorization-service`, `audit-service`, `evidence-service`, and `policy-engine`.

### Platform, DevOps, and infrastructure

- Existing patterns include Docker Compose, Helm, Kubernetes, Istio mTLS, Vault, Prometheus/Grafana, Jaeger, Kafka, Redis, Postgres, NATS, ArgoCD, Terraform, Packer-like install scripts, Cloudflare scripts, GitHub Actions, CodeQL, SAST/DAST/SBOM/provenance workflows, and k6/Locust tests.
- Hidden state sources include named Docker volumes, Redis append-only files, Postgres data directories, generated `.env` files, cron entries, systemd units, NATS JetStream state, and bootstrap scripts that mutate host packages.
- Required refactor: make all state explicit in Terraform, Helm values, Vault paths, and GitOps manifests; scripts must default to dry-run where destructive.

## Dominant execution flows

### Trading signal to execution

1. External signal enters via TradingView webhook, exchange websocket, bot command, or strategy scheduler.
2. API gateway authenticates tenant/user/service identity.
3. Strategy service validates payload and resolves tenant-scoped strategy plugin/version.
4. Risk service evaluates exposure, drawdown, rate limits, policy constraints, and circuit breakers.
5. Execution service submits exchange order through connector adapter.
6. Wallet/ledger service records intent, hold, settlement, fees, and final state.
7. Outbox emits `trade.executed`, `ledger.posted`, and audit events.
8. Notification service publishes Telegram/LINE/email/webhook updates.
9. Observability pipeline correlates request ID, trace ID, tenant ID, strategy ID, and order ID.

### Wallet transfer / swap / settlement

1. API gateway receives transfer, withdraw, deposit, or swap request with idempotency key.
2. Authorization service enforces RBAC, tenant boundary, device posture, HMAC/replay checks, and risk score.
3. Transaction orchestrator creates saga state and ledger reservation.
4. Policy service checks sanctions, velocity, risk, route constraints, and tenant plan limits.
5. Wallet engine builds unsigned transaction or internal ledger movement.
6. TSS signing coordinator requests threshold signing from isolated signers over mTLS/SPIFFE.
7. Chain adapter or banking connector broadcasts transaction/payment instruction.
8. Indexer/clearing/settlement workers reconcile confirmations and post final ledger entries.
9. Audit service stores immutable request/action/trace evidence.

### Bot conversation to action

1. LINE/TikTok/Telegram webhook arrives at bot gateway.
2. Tenant, channel, user, and conversation context are resolved.
3. Safety/rate-limit/billing guards evaluate request.
4. LLM/tool router calls retrieval, commerce, wallet, order, or CRM tools.
5. Domain service emits typed command event.
6. Worker performs side effect and emits notification/audit event.
7. Billing meter and anomaly detector update usage, risk, and alert streams.

### Commerce sync and outreach

1. Commerce connector signs TikTok Shop API request or verifies webhook.
2. Product/order/customer data is normalized into canonical events.
3. Dedupe and rate-limit modules prevent duplicate outreach/actions.
4. Template engine renders tenant-approved communication.
5. Worker sends email/bot response and records consent/audit state.

## Configuration and extensibility points

| Area | Existing pattern | Unified target |
|---|---|---|
| Runtime config | `.env`, compose env blocks, package scripts, installer defaults | Versioned `config/{env}.yaml`, ExternalSecrets/Vault paths, Helm values, Terraform variables. |
| Strategies/plugins | Python registry/autoload and module loaders | Signed plugin manifest with WASM/container/Python runner options and policy gates. |
| Connectors | CCXT, TikTok SDKs, Stripe, PromptPay, LINE, Telegram, Cloudflare scripts | Connector SDK interface with retries, idempotency, webhook verifier, and tenant credentials in Vault. |
| Workers | Celery loops, Python scripts, JS workers, cron-like shell | NATS/Kafka event workers with outbox/inbox, DLQ, retries, backoff, and replay. |
| Security middleware | HMAC, replay, rate signatures, adaptive rate limiters, risk engines | Central Envoy/Istio authz plus library-side request verification and risk scoring. |
| Observability | Prometheus/Grafana, Jaeger, structured loggers | OpenTelemetry-first traces/metrics/logs with SIEM schema and tenant-safe labels. |
| Infra | Compose, Helm, K8s YAML, Terraform, install scripts | GitOps-only cluster state with Terraform/Packer for substrate and ArgoCD for workloads. |

## Hidden and implicit behaviors to eliminate

- Bootstrap scripts installing packages and starting services without a plan/apply boundary.
- Docker Compose named volumes and local DB directories persisting across reruns.
- Cron/systemd entries created outside IaC.
- Environment files generated with secrets on disk.
- Broad container privileges and host path mounts in legacy scripts.
- SDK/API clients reading credentials from ambient environment variables rather than explicit secret references.
- Workers performing side effects without idempotency keys or outbox records.
- Plugin autoload behavior that executes unreviewed Python/JS modules.
- Multi-tenant actions with implicit default tenant or missing tenant ID propagation.

## Repository-to-service consolidation map

| Unified service | Inputs from repositories | Notes |
|---|---|---|
| `api-gateway` | `zwallet`, `zvath`, `ABTPi18n`, `zLinebot` | Go gateway with OIDC, mTLS, tenant routing, rate limits, and OpenAPI aggregation. |
| `identity-service` | Google OAuth, WorldID, OAuth routes, RBAC modules | OIDC broker plus SPIFFE workload identity. |
| `tenant-service` | `zypto/backend/tenant.py`, `zvath` tenant enforcer | Enforces data partitioning, namespaces, quotas, plans. |
| `wallet-service` | `zwallet` wallet engine | Balance projection, address/account management, chain abstraction. |
| `ledger-service` | `zwallet` ledger SQL/services | Double-entry ledger with immutable journal and reconciliation. |
| `payment-service` | PromptPay, Stripe, zeapay placeholder, marketplace payment | External payment adapters and settlement lifecycle. |
| `tss-signing-service` | `zwallet` signing/security concepts | Isolated threshold signing boundary; HSM-ready; no key material in API services. |
| `commerce-connector-service` | TikTok SDKs and clients | Canonical TikTok Shop connector and webhook ingestion. |
| `bot-gateway` | LINE/TikTok/Telegram platforms | Channel normalization and webhook verification. |
| `automation-worker` | outreach bots, bot scripts, strategy schedulers | Idempotent side-effect workers. |
| `strategy-service` | `ABTPi18n` strategy registry | Versioned, signed, tenant-scoped strategies. |
| `risk-service` | trading risk, wallet fraud/risk, AI fraud | Shared risk score and policy checks. |
| `ai-gateway` | `zvath`, `zypto` AI modules, zLinebot LLM | Model/tool routing with safety, billing, and trace propagation. |
| `audit-service` | `zypto`, `ABTPi18n`, `zwallet` audit/logging | Append-only event log, SIEM export, evidence retention. |
| `observability-stack` | existing monitoring assets | Prometheus, Grafana, OTEL Collector, Tempo/Jaeger, ELK. |
| `platform-operator` | install scripts, Cloudflare scripts, Terraform/Helm | Declarative provisioning and drift remediation. |
