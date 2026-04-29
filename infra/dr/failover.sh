#!/usr/bin/env bash
set -euo pipefail

echo "Simulating region failure..."
kubectl cordon node-a
kubectl drain node-a --ignore-daemonsets

echo "Routing traffic to region B..."
kubectl apply -f istio-failover.yaml
