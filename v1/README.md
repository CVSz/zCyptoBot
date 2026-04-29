# ZCYPTOBOT — FULL STACK (AI + HFT + INFRA)

A progressive, end-to-end trading system scaffold that combines AI/RL strategy workflows, event-driven data pipelines, arbitrage execution, infrastructure automation, and low-latency HFT hooks.

## Layers

- AI Quant Engine (RL + signals)
- Event-driven processing (Kafka)
- Arbitrage engine (multi-exchange)
- Infra automation (Terraform + Ansible + K8s + Vault + monitoring)
- HFT hooks (eBPF + DPDK + AF_XDP)

## Repository Structure (high level)

```text
app/            # Trading app modules (data, signal, risk, execution, AI, arb)
infra/          # Terraform, Ansible, K8s, scripts, and HFT support files
src/zcyptobot/  # Packaged core modules and simulation stack
tests/          # Unit/integration regression suite
```


## Merged Blueprint

See `docs/MERGED_BLUEPRINT.md` for the merged end-to-end architecture snapshot and path mapping used in this repository.

## Quick Start

```bash
docker-compose up --build
```

Service health endpoint:

```text
GET /health
```

## Infrastructure Deploy

```bash
bash infra/scripts/deploy.sh
```

## Deployment UI

```bash
uvicorn infra.scripts.ui:app --port 9000
```

## Phase 2 Validation

```bash
k6 run infra/phase2/k6/load.js
kubectl apply -f infra/phase2/chaos/
```

## Reality Check

This repository provides **institutional-style architecture patterns** for research/lab usage. Running true production HFT in live venues still requires specialized hardware and exchange colocation.

## Warning

No guaranteed profit. Trade responsibly.
