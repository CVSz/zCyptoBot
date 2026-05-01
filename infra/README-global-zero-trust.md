# Global Zero-Trust Federation + Confidential Compute

This baseline extends the current Istio + OPA + Kyverno + Cosign setup into a
multi-region, multi-cluster, identity-first deployment model.

## Components

- **SPIRE federation** via trust bundle endpoint (`infra/spire/server.conf`)
- **Istio multi-primary** mesh trust domain configuration (`infra/k8s/istio-mesh.yaml`)
- **Cross-cluster access control** based on SPIFFE IDs (`infra/k8s/authz-global.yaml`)
- **Global policy sync** using OPA bundles:

```bash
opa run --server \
  --set=services.global.url=https://policy.zypto.global \
  --set=bundles.main.service=global \
  --set=bundles.main.resource=/bundles/policy.tar.gz
```

- **Confidential compute** runtime scaffold (`infra/tee/Dockerfile`)
- **Remote attestation verification hook** (`infra/tee/verify.py`)
- **Attestation → SPIFFE binding** (`infra/identity/bind.py`)
- **OPA policy gate** to permit only attested workloads (`policy/opa/policies/tee.rego`)

## Federation bootstrap

Run in each cluster with peer bundle material:

```bash
spire-server bundle set \
  -id spiffe://zypto.global \
  -path /tmp/peer-bundle.pem
```
