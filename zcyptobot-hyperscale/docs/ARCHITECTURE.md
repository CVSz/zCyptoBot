# Architecture

## Autonomous Self-Evolving AI Infrastructure

This stack deploys a **live autonomy control plane** on k3s:

1. **Autonomy Controller Agent** (Helm deployment):
   - Watches repo state, CI signals, and policy docs.
   - Proposes code/policy rewrites.
   - Applies safe changes only when checks pass.
2. **Policy Engine** (ConfigMap-defined policy):
   - Constrains mutation concurrency.
   - Blocks sensitive directories.
   - Requires static and runtime checks before mutation merge.
3. **Execution Substrate**:
   - Multi-region AWS infrastructure via Terraform.
   - k3s servers per region for low-overhead control-plane runtime.
   - Helm-managed release for autonomous services.

## Deployment Topology

- **Terraform** provisions:
  - Primary and secondary VPCs/subnets.
  - k3s security groups.
  - k3s server instances.
- **k3s** provides lightweight Kubernetes runtime.
- **Helm** installs autonomy controller with policy overlay.

## Safety Model

- Mutation budget via `maxConcurrentMutations`.
- Mandatory checks (`unit-tests`, `policy-scan`).
- Immutable paths for foundational security and CI controls.
