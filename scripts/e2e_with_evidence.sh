#!/usr/bin/env bash
# 全 E2E を実行し、docs/plans/evidence/ にタイムスタンプ付きログを残す（API キー不要）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
EVID="$ROOT/docs/plans/evidence"
mkdir -p "$EVID"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="$EVID/e2e-run-${TS}.log"
SUMMARY="$EVID/e2e-run-${TS}.summary.md"

{
  echo "# E2E 実行サマリ"
  echo ""
  echo "- **UTC**: ${TS}"
  echo "- **ログ全文**: \`$(basename "$LOG")\`"
  echo ""
} > "$SUMMARY"

run() {
  local label="$1"
  shift
  echo "=== ${label} ===" | tee -a "$LOG"
  if "$@" >>"$LOG" 2>&1; then
    echo "- [x] ${label}" >> "$SUMMARY"
    echo "OK: ${label}" | tee -a "$LOG"
  else
    echo "- [ ] **FAIL** ${label}" >> "$SUMMARY"
    echo "FAIL: ${label}" | tee -a "$LOG"
    exit 1
  fi
}

echo "=== wawoo-skills E2E evidence ${TS} ===" | tee "$LOG"
run validate_assets python3 scripts/validate_assets.py
run mcp_test_server python3 mcp/test_server.py
run mcp_test_memory_ops python3 mcp/test_memory_ops.py
run cli_adapters_mock python3 scripts/cli_adapters_mock.py
run e2e_flows python3 scripts/e2e_flows.py
run plan_active python3 scripts/plan_active.py
run plan_l2_backlog python3 scripts/plan_l2_backlog.py
run plan_l3_record python3 scripts/plan_l3_record.py
run plan_content python3 scripts/plan_content.py

echo "" >> "$SUMMARY"
echo "すべて成功。" >> "$SUMMARY"
echo "SUMMARY=$SUMMARY"
echo "LOG=$LOG"
