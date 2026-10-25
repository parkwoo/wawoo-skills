#!/usr/bin/env bash
# `docker compose`（V2）を優先。無ければ standalone `docker-compose` にフォールバック。
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
FILE="${ROOT}/internal/docker/e2e/docker-compose.yml"

if docker compose version >/dev/null 2>&1; then
  exec docker compose -f "$FILE" "$@"
fi

if command -v docker-compose >/dev/null 2>&1; then
  echo "WARN: docker compose プラグインなし。docker-compose にフォールバック（./internal/scripts/e2e/install-compose-v2.sh 推奨）" >&2
  exec docker-compose -f "$FILE" "$@"
fi

echo "Compose がありません。先に: ./internal/scripts/e2e/install-compose-v2.sh" >&2
exit 1
