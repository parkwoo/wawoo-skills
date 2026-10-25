#!/usr/bin/env bash
# Cursor Agent CLI で MCP + ワークスペースを実測（要 CURSOR_API_KEY）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

if [[ -z "${CURSOR_API_KEY:-}" ]]; then
  echo "CURSOR_API_KEY が未設定です。agent login または .env を用意してください。" >&2
  exit 1
fi

AGENT="${AGENT_BIN:-agent}"
if ! command -v "$AGENT" >/dev/null 2>&1; then
  echo "Cursor Agent CLI が見つかりません。インストール:" >&2
  echo "  curl https://cursor.com/install -fsS | bash" >&2
  exit 1
fi

# 読み取り中心（cli.json.example を .cursor/cli.json にコピーするとより安全）
"$AGENT" -p --mode ask --trust --approve-mcps --workspace "$ROOT" \
  "このワークスペースの MCP サーバ wawoo-skills を使えるか確認してください。
1) tools/list 相当で capabilities / skill_search が使えること
2) skill_search で query=code review を実行
3) workflow_get で name=feature-delivery の手順が取れること
4) ファイルは変更しない。結果を箇条書きで返す。"
