# Regenerated Specification (from provided screenshots)

This file is a clean, text-native regeneration of the screenshot content so it can be edited, diffed, and reused in the repository.

## 1) System Goal

Build an institutional-style crypto trading platform that combines:
- real-time market data ingestion,
- hybrid signal generation (rules + AI),
- strict risk controls,
- multi-exchange execution,
- event-driven orchestration,
- infra automation and observability,
- optional low-latency/HFT extension points.

## 2) Architecture Layers

1. **Data Layer**
   - Exchange collectors (REST + WS)
   - Kafka topics for normalized ticks/candles/orderbook
   - Redis cache for hot-path reads
2. **Feature & Signal Layer**
   - Feature builder (returns, volatility, momentum, OI proxies)
   - Rule engine + optional RL/ML inference
3. **Risk Layer**
   - Position sizing and exposure caps
   - Drawdown throttles and kill switch
   - Pre-trade and post-trade checks
4. **Execution Layer**
   - Exchange adapter abstraction
   - Idempotent order submission and reconciliation
   - Slippage and retry controls
5. **Orchestration Layer**
   - Event bus with explicit topics
   - Pipeline coordinator
   - Health-aware service supervision
6. **Infrastructure Layer**
   - Docker/K8s deploy paths
   - Terraform + Ansible automation
   - Monitoring/alerting and secret handling
7. **HFT Hooks (optional)**
   - AF_XDP/eBPF/DPDK placeholders
   - Kernel/network tuning scripts

## 3) Mandatory Safety Constraints

- No martingale, all-in, or doubling strategies.
- Strict per-trade risk and portfolio-level exposure limits.
- Kill switch for abnormal latency, drawdown, or API failure patterns.
- All network calls must be timeout-bounded and retry-aware.

## 4) Event-Driven Topic Contract

Suggested topics:
- `market.ticks.raw`
- `market.book.normalized`
- `features.vector`
- `signals.generated`
- `risk.approved`
- `orders.submitted`
- `orders.filled`
- `portfolio.updated`
- `alerts.risk`

## 5) Core Modules to Implement

- `app/data/` market adapters + producers
- `app/features/` feature builder
- `app/signal/` deterministic + model-assisted scoring
- `app/risk/` limits, sizing, kill-switch
- `app/execution/` unified exchange adapters
- `app/arb/` optional cross-venue spread detector/executor
- `app/core/` orchestration + event bus
- `infra/` terraform/ansible/k8s + scripts
- `tests/` strategy/risk/execution/orchestration regression

## 6) Minimal Regeneration Checklist

- [ ] Deterministic configuration object for all runtime services
- [ ] Health endpoint and startup self-checks
- [ ] Integration test for end-to-end event flow
- [ ] Risk engine unit tests for cap enforcement
- [ ] Execution adapter tests for retry + idempotency
- [ ] Containerized local stack (`docker-compose`)
- [ ] Deployment path (`infra/scripts/deploy.sh`)

## 7) Recommended Runtime Sequence

1. bootstrap config
2. connect data streams
3. compute features
4. generate signal score
5. run risk approval
6. place/track order
7. publish fills and update portfolio
8. emit metrics/alerts

## 8) Regeneration Notes

Because screenshot text is image-based and difficult to diff/maintain, this regenerated markdown is intended to preserve the same structure and intent in a source-controlled format.
