#!/usr/bin/env bash
set -euo pipefail
GITEA_SERVER_URL="https://git.zeaz.dev"
REPO_FULL="CVSz/zCyptoBot"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
GITEA_TOKEN="${GITEA_TOKEN:-}"
[ -n "$GITEA_TOKEN" ] || { echo "GITEA_TOKEN not set"; exit 1; }
curl -s -X POST -H "Content-Type: application/json" -H "Authorization: token ${GITEA_TOKEN}" \
  -d "{\"head\":\"${BRANCH}\",\"base\":\"main\",\"title\":\"DeepScan Autofix: automated fixes\",\"body\":\"Automated fixes applied by DeepScan. Please review changes.\"}" \
  "${GITEA_SERVER_URL}/api/v1/repos/${REPO_FULL}/pulls"
