#!/usr/bin/env bash
set -euo pipefail

helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm upgrade --install vault hashicorp/vault \
  --namespace vault \
  --create-namespace
