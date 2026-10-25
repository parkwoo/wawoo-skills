#!/usr/bin/env bash
# Docker Compose V2 プラグイン（`docker compose`）を入れる。
# Ubuntu の docker.io だけではプラグインが無いことがある。
set -euo pipefail

COMPOSE_VER="${COMPOSE_VERSION:-v2.32.4}"
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64) BIN=docker-compose-linux-x86_64 ;;
  aarch64|arm64) BIN=docker-compose-linux-aarch64 ;;
  *)
    echo "未対応 ARCH: $ARCH" >&2
    exit 1
    ;;
esac

URL="https://github.com/docker/compose/releases/download/${COMPOSE_VER}/${BIN}"

if docker compose version >/dev/null 2>&1; then
  echo "already ok: $(docker compose version)"
  exit 0
fi

# ユーザー領域（sudo 不要）
USER_PLUGIN="${HOME}/.docker/cli-plugins/docker-compose"
mkdir -p "${HOME}/.docker/cli-plugins"
echo "install -> ${USER_PLUGIN}"
curl -fsSL "$URL" -o "$USER_PLUGIN"
chmod +x "$USER_PLUGIN"

if docker compose version >/dev/null 2>&1; then
  echo "OK: $(docker compose version)"
  exit 0
fi

echo "まだ docker compose が使えません。PATH または Docker の再ログインを確認してください。" >&2
echo "全ユーザー向け（要 sudo）:" >&2
echo "  sudo mkdir -p /usr/libexec/docker/cli-plugins" >&2
echo "  sudo curl -fsSL $URL -o /usr/libexec/docker/cli-plugins/docker-compose" >&2
echo "  sudo chmod +x /usr/libexec/docker/cli-plugins/docker-compose" >&2
exit 1
