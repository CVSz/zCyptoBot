#!/usr/bin/env bash
set -euo pipefail

terraform init
terraform apply -auto-approve

kubectl apply -f ../k8s/istio.yaml
kubectl apply -f ../k8s/spire.yaml
kubectl apply -f ../k8s/dex.yaml
kubectl apply -f ../k8s/app.yaml
