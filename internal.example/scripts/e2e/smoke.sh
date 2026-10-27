#!/usr/bin/env bash
# API キー不要: 資産 + MCP プロトコルスモーク
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
echo "== validate_assets =="
python3 scripts/validate_assets.py
echo "== mcp test_server =="
python3 mcp/test_server.py
echo "== mcp test_memory_ops =="
python3 mcp/test_memory_ops.py
echo "== e2e_flows =="
python3 scripts/e2e_flows.py
echo "== cli_adapters_mock =="
python3 scripts/cli_adapters_mock.py
echo "== agent-active-live (dry) =="
AE="${ROOT}/internal/scripts/e2e/agent-active-live.sh"
[[ -x "$AE" ]] || AE="${ROOT}/internal.example/scripts/e2e/agent-active-live.sh"
MODE=dry bash "$AE" delivery-lite
MODE=dry bash "$AE" content-delivery-lite
echo "OK: smoke (no API keys)"
