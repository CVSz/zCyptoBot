bootstrap:
	python scripts/bootstrap.py

terraform-init:
	terraform -chdir=infra/terraform init

terraform-apply:
	terraform -chdir=infra/terraform apply -auto-approve

k3s-kubeconfig:
	@echo "Export your kubeconfig from primary server:"
	@echo "ssh ubuntu@$(PRIMARY_IP) 'sudo cat /etc/rancher/k3s/k3s.yaml' > kubeconfig"

helm-install:
	helm upgrade --install zypto-hyperscale infra/helm -n zypto --create-namespace

deploy-live-ai: terraform-apply helm-install
	@echo "Live AI control plane deployed."

validate:
	terraform -chdir=infra/terraform validate
	helm lint infra/helm
