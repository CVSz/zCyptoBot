#!/usr/bin/env bash
set -euo pipefail

helm repo add clickhouse https://charts.clickhouse.com
helm repo update
helm upgrade --install clickhouse clickhouse/clickhouse \
  --namespace data \
  --create-namespace \
  -f values-ha.yaml
