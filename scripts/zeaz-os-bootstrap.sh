#!/usr/bin/env bash
set -Eeuo pipefail

# Deterministic Ubuntu 24.04 bootstrap and cleanup utility.
# Defaults to plan mode. Use --apply to mutate the host and --clean to remove residual state.

MODE="plan"
CLEAN="false"
INSTALL_K8S_TOOLS="true"
LOG_DIR="/var/log/zeaz-bootstrap"
STATE_DIR="/var/lib/zeaz-bootstrap"
DRY_PREFIX="[plan]"

usage() {
  cat <<USAGE
Usage: $0 [--plan|--apply] [--clean] [--no-k8s-tools]

Options:
  --plan          Print actions without changing the system (default).
  --apply         Execute actions. Must run as root or through sudo.
  --clean         Stop known services/processes and remove residual container/cron state.
  --no-k8s-tools  Skip kubectl/helm/argocd CLI installation.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --plan) MODE="plan" ;;
    --apply) MODE="apply" ;;
    --clean) CLEAN="true" ;;
    --no-k8s-tools) INSTALL_K8S_TOOLS="false" ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 2 ;;
  esac
  shift
done

if [[ "$MODE" == "apply" ]]; then
  DRY_PREFIX=""
  if [[ "${EUID}" -ne 0 ]]; then
    echo "--apply requires root. Re-run with sudo." >&2
    exit 1
  fi
fi

run() {
  if [[ "$MODE" == "plan" ]]; then
    printf '%s %q ' "$DRY_PREFIX" "$1"; shift || true; printf '%q ' "$@"; printf '\n'
  else
    "$@"
  fi
}

run_bash() {
  if [[ "$MODE" == "plan" ]]; then
    echo "$DRY_PREFIX bash -c $1"
  else
    bash -c "$1"
  fi
}

require_ubuntu_2404() {
  if [[ -r /etc/os-release ]]; then
    # shellcheck disable=SC1091
    source /etc/os-release
    if [[ "${ID:-}" != "ubuntu" || "${VERSION_ID:-}" != "24.04" ]]; then
      echo "Warning: expected Ubuntu 24.04, detected ${PRETTY_NAME:-unknown}." >&2
    fi
  fi
}

clean_environment() {
  echo "==> Cleaning known residual state"
  run mkdir -p "$LOG_DIR" "$STATE_DIR"

  # Stop repository-specific compose projects without deleting unrelated containers by default.
  if command -v docker >/dev/null 2>&1; then
    run_bash "docker ps --format '{{.Names}}' | awk '/(zeaz|zypto|zwallet|zlinebot|abt|tiktok|zvath)/ {print}' | xargs -r docker stop"
    run_bash "docker ps -a --format '{{.Names}}' | awk '/(zeaz|zypto|zwallet|zlinebot|abt|tiktok|zvath)/ {print}' | xargs -r docker rm"
    run_bash "docker volume ls --format '{{.Name}}' | awk '/(zeaz|zypto|zwallet|zlinebot|abt|tiktok|zvath)/ {print}' | xargs -r docker volume rm"
    run_bash "docker network ls --format '{{.Name}}' | awk '/(zeaz|zypto|zwallet|zlinebot|abt|tiktok|zvath)/ {print}' | xargs -r docker network rm"
  fi

  # Remove managed cron block only; never wipe user crontab.
  run_bash "(crontab -l 2>/dev/null || true) | sed '/# ZEAZ-MANAGED-BEGIN/,/# ZEAZ-MANAGED-END/d' | crontab -"

  # Disable managed systemd units if present.
  run_bash "systemctl list-unit-files 'zeaz-*' 'zypto-*' --no-legend 2>/dev/null | awk '{print \$1}' | xargs -r systemctl disable --now"

  # Remove known local runtime directories created by legacy installers.
  run rm -rf /tmp/zeaz /tmp/zypto /tmp/zwallet /tmp/zlinebot
}

install_base_packages() {
  echo "==> Installing deterministic base packages"
  run mkdir -p "$LOG_DIR" "$STATE_DIR" /etc/apt/keyrings
  run apt-get update
  run apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg lsb-release jq git unzip tar xz-utils \
    build-essential pkg-config make gcc g++ python3 python3-venv python3-pip \
    golang-go nodejs npm openssl age sops auditd apparmor apparmor-utils \
    chrony ufw
}

install_container_runtime() {
  echo "==> Installing Docker/containerd"
  run install -m 0755 -d /etc/apt/keyrings
  run_bash "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
  run chmod a+r /etc/apt/keyrings/docker.gpg
  run_bash "echo \"deb [arch=\$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu noble stable\" > /etc/apt/sources.list.d/docker.list"
  run apt-get update
  run apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  run systemctl enable --now containerd docker
  run_bash "containerd config default > /etc/containerd/config.toml.tmp && mv /etc/containerd/config.toml.tmp /etc/containerd/config.toml"
  run systemctl restart containerd
}

install_k8s_tools() {
  [[ "$INSTALL_K8S_TOOLS" == "true" ]] || return 0
  echo "==> Installing Kubernetes/GitOps CLIs"
  run_bash "curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.30/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg"
  run_bash "echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /' > /etc/apt/sources.list.d/kubernetes.list"
  run apt-get update
  run apt-get install -y kubectl
  run_bash "curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash"
  run_bash "curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64 && chmod +x /usr/local/bin/argocd"
}

harden_defaults() {
  echo "==> Applying secure defaults"
  run systemctl enable --now auditd chrony
  run ufw default deny incoming
  run ufw default allow outgoing
  run ufw allow OpenSSH
  run_bash "ufw --force enable"
  run sysctl -w net.ipv4.ip_forward=1
  run_bash "cat >/etc/sysctl.d/99-zeaz.conf <<'SYSCTL'\nnet.ipv4.ip_forward=1\nnet.ipv4.conf.all.rp_filter=1\nnet.ipv4.tcp_syncookies=1\nnet.ipv6.conf.all.disable_ipv6=0\nSYSCTL"
}

write_state() {
  run_bash "cat >${STATE_DIR}/bootstrap.env <<STATE\nmode=${MODE}\nclean=${CLEAN}\ncompleted_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)\nSTATE"
}

main() {
  require_ubuntu_2404
  [[ "$CLEAN" == "true" ]] && clean_environment
  install_base_packages
  install_container_runtime
  install_k8s_tools
  harden_defaults
  write_state
  echo "==> Bootstrap ${MODE} complete"
}

main "$@"
