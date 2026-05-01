# Zypto Hyperscale Platform

Production-grade monorepo scaffold with CI/CD and multi-region Terraform.

## Generator

Use the bootstrap generator to create a full repo scaffold including:
- 220+ microservice folders (config, code, tests, Docker, k8s, HPA, Service)
- Helm chart skeleton
- Terraform root modules
- Observability stack (Prometheus + Grafana dashboard + alerts)
- Security hardening baselines (network policy + pod security)
- AI model registry and training pipeline templates

```bash
python3 scripts/bootstrap.py --services 220
```

Set `--services` higher/lower as needed.
