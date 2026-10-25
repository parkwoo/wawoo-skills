#!/usr/bin/env bash
# API キー不要: 資産 + MCP プロトコルスモーク
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"
echo "== validate_assets =="
python3 scripts/validate_assets.py
echo "== mcp test_server =="
python3 mcp/test_server.py
echo "OK: smoke (no API keys)"
