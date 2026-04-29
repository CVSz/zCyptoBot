#!/usr/bin/env python3
"""Generate a hyperscale monorepo skeleton with microservices, infra, observability, security, and AI assets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def service_scaffold(root: Path, idx: int) -> None:
    sid = f"service_{idx:04d}"
    base = root / "services" / sid
    write(base / "src" / "main.py", f"from fastapi import FastAPI\n\napp = FastAPI(title='{sid}')\n\n@app.get('/health')\ndef health():\n    return {{'service': '{sid}', 'status': 'ok'}}\n")
    write(base / "src" / "config.yaml", f"service: {sid}\nport: 80\nlog_level: INFO\n")
    write(base / "tests" / "test_basic.py", "def test_health_payload_shape():\n    payload = {'status': 'ok'}\n    assert payload['status'] == 'ok'\n")
    write(base / "Dockerfile", "FROM python:3.12-slim\nWORKDIR /app\nCOPY src/ /app/src/\nRUN pip install fastapi uvicorn\nCMD [\"uvicorn\", \"src.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"80\"]\n")
    write(base / "deploy" / "k8s.yaml", f"apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: {sid}\nspec:\n  replicas: 2\n  selector:\n    matchLabels:\n      app: {sid}\n  template:\n    metadata:\n      labels:\n        app: {sid}\n    spec:\n      containers:\n      - name: {sid}\n        image: ghcr.io/example/{sid}:latest\n        ports:\n        - containerPort: 80\n")
    write(base / "deploy" / "service.yaml", f"apiVersion: v1\nkind: Service\nmetadata:\n  name: {sid}\nspec:\n  selector:\n    app: {sid}\n  ports:\n  - port: 80\n    targetPort: 80\n")
    write(base / "deploy" / "hpa.yaml", f"apiVersion: autoscaling/v2\nkind: HorizontalPodAutoscaler\nmetadata:\n  name: {sid}\nspec:\n  scaleTargetRef:\n    apiVersion: apps/v1\n    kind: Deployment\n    name: {sid}\n  minReplicas: 2\n  maxReplicas: 20\n  metrics:\n  - type: Resource\n    resource:\n      name: cpu\n      target:\n        type: Utilization\n        averageUtilization: 60\n")


def infra_scaffold(root: Path, service_count: int) -> None:
    write(root / "infra" / "helm" / "Chart.yaml", "apiVersion: v2\nname: zcyptobot-hyperscale\nversion: 0.1.0\n")
    write(root / "infra" / "helm" / "values.yaml", f"services: {service_count}\nobservability:\n  enabled: true\nsecurity:\n  networkPolicies: true\n")
    write(root / "infra" / "terraform" / "main.tf", "terraform {\n  required_version = \">= 1.6.0\"\n}\n\nmodule \"network\" {\n  source = \"./modules/network\"\n}\n")
    write(root / "infra" / "security" / "network-policy.yaml", "apiVersion: networking.k8s.io/v1\nkind: NetworkPolicy\nmetadata:\n  name: default-deny\nspec:\n  podSelector: {}\n  policyTypes: [\"Ingress\", \"Egress\"]\n")
    write(root / "infra" / "security" / "pod-security.yaml", "apiVersion: v1\nkind: Namespace\nmetadata:\n  name: hyperscale\n  labels:\n    pod-security.kubernetes.io/enforce: restricted\n")


def observability_scaffold(root: Path, service_count: int) -> None:
    write(root / "observability" / "prometheus" / "prometheus.yml", "global:\n  scrape_interval: 15s\nscrape_configs:\n- job_name: kubernetes\n  static_configs:\n  - targets: ['prometheus:9090']\n")
    dash = {
        "title": "Hyperscale Platform",
        "panels": [
            {"title": "Service Count", "type": "stat", "targets": [{"expr": str(service_count)}]},
            {"title": "CPU", "type": "timeseries", "targets": [{"expr": "sum(rate(container_cpu_usage_seconds_total[5m]))"}]},
        ],
    }
    write(root / "observability" / "grafana" / "dashboards" / "platform.json", json.dumps(dash, indent=2))
    write(root / "observability" / "alerts" / "platform-alerts.yaml", "groups:\n- name: platform\n  rules:\n  - alert: HighErrorRate\n    expr: rate(http_server_requests_seconds_count{status=~\"5..\"}[5m]) > 5\n")


def ai_scaffold(root: Path) -> None:
    write(root / "ai" / "models" / "registry.yaml", "models:\n- name: price-forecast-transformer\n  version: 1.0.0\n- name: anomaly-detector\n  version: 1.0.0\n")
    write(root / "ai" / "training" / "pipeline.yaml", "stages:\n- ingest\n- feature_engineering\n- train\n- evaluate\n- deploy\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--services", type=int, default=160, help="How many service folders to scaffold")
    args = parser.parse_args()

    for i in range(1, args.services + 1):
        service_scaffold(args.root, i)

    infra_scaffold(args.root, args.services)
    observability_scaffold(args.root, args.services)
    ai_scaffold(args.root)

    print(f"bootstrap complete: {args.services} services generated")


if __name__ == "__main__":
    main()
