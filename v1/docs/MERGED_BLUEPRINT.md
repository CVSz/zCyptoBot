# Merged End-to-End Blueprint

This document captures the merged architecture requested for the repository and maps it to the current implementation layout in this codebase.

## Included capabilities

- v1–v7 trading system (AI + Kafka + RL + arbitrage)
- Infrastructure automation (Kubernetes + Terraform + Vault + monitoring)
- HFT support layer (eBPF + DPDK + AF_XDP hooks)
- One-click deploy + deployment UI + phase2 load/chaos assets

## Repository mapping

Requested merged structure references top-level `phase2/` and `infra/ebpf|dpdk|afxdp` folders. In this repository, those are organized as:

- `infra/phase2/` for load and chaos assets
- `infra/hft/ebpf`, `infra/hft/dpdk`, and `infra/hft/afxdp` for low-latency hooks

The core app tree (`app/`) and infra automation tree (`infra/terraform`, `infra/ansible`, `infra/k8s`, `infra/scripts`) are already present and aligned with progressive enablement.

## Critical path files

- App entrypoint: `app/main.py`
- Runtime orchestrator: `app/core/orchestrator.py`
- Event bus: `app/core/event_bus.py`
- Arbitrage detector: `app/arb/detector.py`
- RL inference: `app/ai/inference.py`
- Infra deployment script: `infra/scripts/deploy.sh`
- Deployment UI endpoint: `infra/scripts/ui.py`

## Baseline run commands

```bash
docker-compose up --build
bash infra/scripts/deploy.sh
uvicorn infra.scripts.ui:app --port 9000
k6 run infra/phase2/k6/load.js
kubectl apply -f infra/phase2/chaos/
```

## Notes

This implementation is a research/lab baseline for progressive enablement. Production-grade HFT in live venues still requires highly specialized hardware, network topology, and exchange colocation.
