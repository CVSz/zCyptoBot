# Runbook

## Prerequisites

- AWS credentials configured for Terraform.
- Terraform >= 1.6.
- Helm 3.x.
- SSH key pair created in AWS.

## Deploy Cluster + Live AI

1. Set required Terraform vars (example):
   - `TF_VAR_ami_id`
   - `TF_VAR_ssh_key_name`
   - `TF_VAR_k3s_cluster_token`
2. Initialize and apply infrastructure:

```bash
make terraform-init
make terraform-apply
```

3. Pull kubeconfig from primary k3s server and export `KUBECONFIG`.
4. Install helm release:

```bash
make helm-install
```

5. Verify autonomy controller:

```bash
kubectl -n zcyptobot get pods
kubectl -n zcyptobot logs deploy/zcyptobot-hyperscale-autonomy-controller
```

## Mutation Guardrails

Tune `infra/helm/values.yaml`:
- `autonomy.codeRewriteEnabled`
- `autonomy.policy.maxConcurrentMutations`
- `autonomy.policy.requiredChecks`
- `autonomy.policy.blockedPaths`

## Rollback

```bash
helm -n zcyptobot rollback zcyptobot-hyperscale
terraform -chdir=infra/terraform destroy
```
