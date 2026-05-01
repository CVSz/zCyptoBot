#!/usr/bin/env bash
set -euo pipefail

spire-server entry create \
  -spiffeID spiffe://zypto/api \
  -selector k8s:pod-label:app:zypto-api
