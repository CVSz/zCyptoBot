# ZCYPTOBOT

AI Quant Trading System (Production Ready)

## Run

```bash
docker-compose up --build
```

## Endpoint

GET /health

## Strategy

- Volatility + Momentum + OI

## Risk

- Max risk per trade
- Drawdown kill-switch

## Tier-1 On-Prem Infrastructure (Ubuntu 24.04 + VMware)

This repository now includes an on-premises, cloud-grade infrastructure scaffold under `infra/` for:

- Terraform + vSphere VM provisioning
- Ansible Kubernetes bootstrap (kubeadm)
- Self-hosted Vault (HA-ready StatefulSet)
- Strimzi Kafka baseline
- Prometheus + Grafana manifests
- Ingress + bootstrap automation script

### Layout

```text
infra/
├── terraform/
├── ansible/
├── k8s/
│   ├── vault/
│   ├── kafka/
│   ├── monitoring/
│   └── ingress/
└── scripts/
```

### Bootstrap (example)

```bash
./infra/scripts/bootstrap.sh
```

> Note: manifests are starter templates and should be hardened for production (TLS, RBAC, NetworkPolicies, storage classes, and secret management).

## Warning

No guaranteed profit. Use carefully.
