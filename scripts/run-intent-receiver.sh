#!/usr/bin/env bash
# Start the intent receiver as a resident process (Unix socket)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOCKET="${WAWOO_INTENT_SOCKET:-/tmp/wawoo-intent.sock}"
export WAWOO_INTENT_SOCKET="$SOCKET"
exec python3 "$ROOT/mcp/intent_receiver.py" --socket "$SOCKET"
