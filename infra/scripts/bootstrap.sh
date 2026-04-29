#!/usr/bin/env bash
set -euo pipefail

terraform -chdir=infra/terraform init
terraform -chdir=infra/terraform apply -auto-approve

ansible-playbook infra/ansible/install-k8s.yml

kubectl apply -f infra/k8s/vault/
kubectl apply -f infra/k8s/kafka/
kubectl apply -f infra/k8s/monitoring/
kubectl apply -f infra/k8s/ingress/
