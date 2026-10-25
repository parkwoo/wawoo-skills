#!/usr/bin/env bash
# Cursor Agent CLI で MCP + ワークスペースを実測（要: agent login 済み、または CURSOR_API_KEY）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

AGENT="${AGENT_BIN:-agent}"
if ! command -v "$AGENT" >/dev/null 2>&1; then
  echo "Cursor Agent CLI が見つかりません。インストール:" >&2
  echo "  curl https://cursor.com/install -fsS | bash" >&2
  echo "  （PATH に ~/.cursor/bin を通す）" >&2
  exit 1
fi

# 認証: 通常は `agent login`（ブラウザ）。CI/無人のみ CURSOR_API_KEY。
if [[ -z "${CURSOR_API_KEY:-}" ]]; then
  if ! "$AGENT" status >/dev/null 2>&1; then
    echo "未ログインです。先に次を実行してください:" >&2
    echo "  agent login" >&2
    echo "" >&2
    echo "（GitHub Actions 等の無人実行だけ CURSOR_API_KEY を使います）" >&2
    exit 1
  fi
  echo "== agent status (login セッション) =="
  "$AGENT" status || true
else
  echo "== CURSOR_API_KEY による認証（無人向け） =="
fi

# 読み取り中心（cli.json.example を .cursor/cli.json にコピーするとより安全）
"$AGENT" -p --mode ask --trust --approve-mcps --workspace "$ROOT" \
  "このワークスペースの MCP サーバ wawoo-skills を使えるか確認してください。
1) tools/list 相当で capabilities / skill_search が使えること
2) skill_search で query=code review を実行
3) workflow_get で name=feature-delivery の手順が取れること
4) ファイルは変更しない。結果を箇条書きで返す。"
