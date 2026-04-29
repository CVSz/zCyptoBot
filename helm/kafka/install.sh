#!/usr/bin/env bash
set -euo pipefail

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade --install kafka bitnami/kafka \
  --namespace data \
  --create-namespace \
  -f values-ha.yaml
