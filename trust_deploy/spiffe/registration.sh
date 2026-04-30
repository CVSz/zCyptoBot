#!/usr/bin/env bash
set -euo pipefail

spire-server entry create \
  -spiffeID spiffe://trust/app \
  -selector k8s:ns:default
