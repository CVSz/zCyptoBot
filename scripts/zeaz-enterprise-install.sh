#!/usr/bin/env bash
set -Eeuo pipefail

# One-command environment-aware ZeaZ/Zypto platform installer.
# Safe default is --plan; --apply requires explicit environment and kube context.

ENVIRONMENT="dev"
MODE="plan"
DOMAIN="zeaz.dev"
NAMESPACE_PREFIX="zeaz"
REPO_URL="https://github.com/cvsz/zypto.git"
ARGO_NAMESPACE="argocd"
VALUES_DIR="generated/platform"
BOOTSTRAP_OS="false"

usage() {
  cat <<USAGE
Usage: $0 [--env dev|staging|prod] [--plan|--apply] [--domain zeaz.dev] [--repo URL] [--bootstrap-os]

Examples:
  $0 --env dev --plan
  $0 --env prod --apply --domain zeaz.dev --repo https://github.com/cvsz/zypto.git
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env) ENVIRONMENT="$2"; shift ;;
    --plan) MODE="plan" ;;
    --apply) MODE="apply" ;;
    --domain) DOMAIN="$2"; shift ;;
    --repo) REPO_URL="$2"; shift ;;
    --bootstrap-os) BOOTSTRAP_OS="true" ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

case "$ENVIRONMENT" in dev|staging|prod) ;; *) echo "Invalid --env: $ENVIRONMENT" >&2; exit 2 ;; esac

run() {
  if [[ "$MODE" == "plan" ]]; then
    printf '[plan] %q ' "$@"; printf '\n'
  else
    "$@"
  fi
}

run_bash() {
  if [[ "$MODE" == "plan" ]]; then
    echo "[plan] bash -c $1"
  else
    bash -c "$1"
  fi
}

need() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 1; }
}

preflight() {
  need git
  if [[ "$MODE" == "apply" ]]; then
    need kubectl
    need helm
    need jq
    kubectl config current-context >/dev/null
  fi
}

generate_values() {
  local out="${VALUES_DIR}/${ENVIRONMENT}"
  run mkdir -p "$out"
  if [[ "$MODE" == "apply" ]]; then
    cat >"$out/platform-values.yaml" <<YAML
platform:
  environment: ${ENVIRONMENT}
  domain: ${DOMAIN}
  wildcardDomain: "*.${DOMAIN}"
  namespacePrefix: ${NAMESPACE_PREFIX}
  repoURL: ${REPO_URL}
security:
  mtls: STRICT
  spiffeTrustDomain: ${ENVIRONMENT}.${DOMAIN}
  vaultNamespace: ${ENVIRONMENT}
observability:
  prometheus: true
  grafana: true
  opentelemetry: true
  elk: true
gitops:
  autoSync: true
  prune: true
  selfHeal: true
YAML
  else
    echo "[plan] write ${out}/platform-values.yaml"
  fi
}

install_argocd() {
  run_bash "kubectl create namespace '$ARGO_NAMESPACE' --dry-run=client -o yaml | kubectl apply -f -"
  run helm repo add argo https://argoproj.github.io/argo-helm
  run helm repo update
  run helm upgrade --install argocd argo/argo-cd \
    --namespace "$ARGO_NAMESPACE" \
    --set configs.params."server\.insecure"=false \
    --set controller.metrics.enabled=true \
    --set server.metrics.enabled=true \
    --wait
}

apply_platform_manifests() {
  run_bash "kubectl create namespace '${NAMESPACE_PREFIX}-${ENVIRONMENT}' --dry-run=client -o yaml | kubectl apply -f -"
  run kubectl label namespace "${NAMESPACE_PREFIX}-${ENVIRONMENT}" "zeaz.dev/environment=${ENVIRONMENT}" --overwrite
  run kubectl apply -f infra/platform/security/spire-istio-vault.yaml
  run kubectl apply -f infra/platform/argocd/zeaz-root-app.yaml
}

post_install_report() {
  cat <<REPORT
ZeaZ enterprise install ${MODE} complete.
Environment: ${ENVIRONMENT}
Domain:      *.${DOMAIN}
GitOps repo: ${REPO_URL}
Next steps:
  1. Store CLOUDFLARE_API_TOKEN and VAULT_TOKEN in your secret manager.
  2. Run Terraform in infra/platform/cloudflare and infra/platform/terraform.
  3. Verify ArgoCD sync and mTLS policy status.
REPORT
}

main() {
  preflight
  if [[ "$BOOTSTRAP_OS" == "true" ]]; then
    run sudo scripts/zeaz-os-bootstrap.sh --apply
  fi
  generate_values
  install_argocd
  apply_platform_manifests
  post_install_report
}

main "$@"
