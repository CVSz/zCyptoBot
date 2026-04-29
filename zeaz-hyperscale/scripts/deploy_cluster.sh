#!/usr/bin/env bash
set -e
cd infra/terraform
terraform init
terraform apply -auto-approve -var="key_name=${KEY_NAME}"

IP=$(terraform output -raw public_ip)
echo "Instance IP: $IP"

scp -o StrictHostKeyChecking=no -i ~/.ssh/${KEY_NAME}.pem ec2-user@$IP:/home/ec2-user/.kube/config ./kubeconfig
export KUBECONFIG=$(pwd)/kubeconfig
kubectl get nodes
