#!/usr/bin/env bash
# Kilo CLI: バージョン + プロジェクト MCP 設定の存在確認（TUI/認証は別）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"

KILO="${KILO_BIN:-kilo}"
if ! command -v "$KILO" >/dev/null 2>&1; then
  if command -v npx >/dev/null 2>&1; then
    KILO="npx --yes @kilocode/cli"
  else
    echo "kilo も npx もありません。npm install -g @kilocode/cli" >&2
    exit 1
  fi
fi

echo "== kilo version =="
# shellcheck disable=SC2086
$KILO --version

echo "== kilo.json MCP =="
python3 -c "import json; d=json.load(open('kilo.json')); print(json.dumps(d.get('mcp',{}), indent=2))"

echo "== kilo mcp list (要: プロジェクトで kilo auth 済みの場合のみ成功) =="
set +e
# shellcheck disable=SC2086
$KILO mcp list
code=$?
set -e
if [[ $code -ne 0 ]]; then
  echo "WARN: kilo mcp list は認証/設定未完了の可能性（スモークは kilo.json の記述確認まで）"
fi

echo "手動 E2E: 本ディレクトリで \`kilo\` を起動し /feature-delivery を実行（internal/docs/audit/KILO-E2E.md）"
