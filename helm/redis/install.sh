#!/usr/bin/env bash
set -euo pipefail

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade --install redis bitnami/redis \
  --namespace data \
  --create-namespace \
  -f values-ha.yaml
