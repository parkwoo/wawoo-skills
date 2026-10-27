#!/usr/bin/env bash
# 任意: シェルから task-router CLI を呼ぶ（MCP 未接続時の補助）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ROUTER="$ROOT/scripts/task-router.py"

if [[ ! -f "$ROUTER" ]]; then
  echo "task-router が見つかりません: $ROUTER" >&2
  exit 1
fi

if [[ $# -lt 1 ]]; then
  echo "使い方: $(basename "$0") '<タスク説明>'"
  echo "例: $(basename "$0") 'API の調査'"
  echo ""
  echo "MCP 利用時は interpret_intent / route_task を優先（常駐受信器は任意）。"
  exit 0
fi

python3 "$ROUTER" "$*"
