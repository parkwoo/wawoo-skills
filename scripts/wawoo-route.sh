#!/usr/bin/env bash
# Optional: call the task-router CLI from the shell (a fallback when MCP is not connected)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ROUTER="$ROOT/scripts/task-router.py"

if [[ ! -f "$ROUTER" ]]; then
  echo "task-router not found: $ROUTER" >&2
  exit 1
fi

if [[ $# -lt 1 ]]; then
  echo "Usage: $(basename "$0") '<task description>'"
  echo "Example: $(basename "$0") 'research the API'"
  echo ""
  echo "With MCP, prefer interpret_intent / route_task (the resident receiver is optional)."
  exit 0
fi

python3 "$ROUTER" "$*"
