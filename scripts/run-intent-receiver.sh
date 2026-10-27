#!/usr/bin/env bash
# 意図受信器を常駐起動（Unix ソケット）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOCKET="${WAWOO_INTENT_SOCKET:-/tmp/wawoo-intent.sock}"
export WAWOO_INTENT_SOCKET="$SOCKET"
exec python3 "$ROOT/mcp/intent_receiver.py" --socket "$SOCKET"
