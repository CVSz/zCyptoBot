#!/bin/bash
set -euo pipefail

echo "[1/3] Terraform apply"
terraform -chdir=infra/terraform init
terraform -chdir=infra/terraform apply -auto-approve

echo "[2/3] Ansible bootstrap + k8s + networking"
ansible-playbook infra/ansible/bootstrap.yml
ansible-playbook infra/ansible/k8s.yml
ansible-playbook infra/ansible/cilium.yml
ansible-playbook infra/ansible/istio.yml

echo "[3/3] Core services"
kubectl apply -f infra/k8s/namespaces.yaml
kubectl apply -f infra/k8s/vault.yaml
kubectl apply -f infra/k8s/kafka.yaml
kubectl apply -f infra/k8s/redis.yaml
kubectl apply -f infra/k8s/monitoring.yaml
kubectl apply -f infra/k8s/argocd.yaml
kubectl apply -f infra/k8s/zypto/

echo "DONE"
