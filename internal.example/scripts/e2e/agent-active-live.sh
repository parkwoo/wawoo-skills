#!/usr/bin/env bash
# 実機 E2E: エージェント（または dry）が SSOT 1 行更新 → plan_* 必須通過
# 用法:
#   MODE=dry  ./agent-active-live.sh delivery-lite
#   MODE=cursor WF=delivery-lite ./agent-active-live.sh   # 要 agent login
#   MODE=kilo  ./agent-active-live.sh delivery-lite       # 手順表示（TUI は人が操作）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"

WF="${1:-delivery-lite}"
MODE="${MODE:-dry}"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
EVID="$ROOT/docs/plans/evidence"
SANDBOX="$EVID/sandbox"
mkdir -p "$SANDBOX" "$EVID"

if [[ -d "$ROOT/internal/scripts/e2e/fixtures" ]]; then
  FIX="$ROOT/internal/scripts/e2e/fixtures"
  APPLY="$ROOT/internal/scripts/e2e/active_apply_dryrun.py"
else
  FIX="$ROOT/internal.example/scripts/e2e/fixtures"
  APPLY="$ROOT/internal.example/scripts/e2e/active_apply_dryrun.py"
fi

LOG="$EVID/agent-active-${WF}-${MODE}-${TS}.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== agent-active-live WF=$WF MODE=$MODE TS=$TS ==="

reset_sandbox() {
  case "$WF" in
    delivery-lite)
      cp "$FIX/ACTIVE.sandbox.md" "$SANDBOX/ACTIVE.md"
      TARGET="$SANDBOX/ACTIVE.md"
      PLAN=(python3 "$ROOT/scripts/plan_active.py" "$TARGET")
      ;;
    content-delivery-lite)
      cp "$FIX/CONTENT.sandbox.md" "$SANDBOX/CONTENT.md"
      TARGET="$SANDBOX/CONTENT.md"
      PLAN=(python3 "$ROOT/scripts/plan_content.py" "$TARGET")
      ;;
    *)
      echo "unknown workflow: $WF" >&2
      exit 1
      ;;
  esac
}

reset_sandbox
echo "sandbox: $TARGET"

case "$MODE" in
  dry)
    python3 "$APPLY" --workflow "$WF" --path "$TARGET"
    ;;
  cursor)
    AGENT="${AGENT_BIN:-agent}"
    if ! command -v "$AGENT" >/dev/null 2>&1; then
      echo "Cursor Agent CLI がありません。MODE=dry を使うか agent をインストール。" >&2
      exit 1
    fi
    if [[ -z "${CURSOR_API_KEY:-}" ]] && ! "$AGENT" status >/dev/null 2>&1; then
      echo "未ログイン: agent login または CURSOR_API_KEY" >&2
      exit 1
    fi
    PROMPT_FILE="$SANDBOX/agent-prompt-${WF}.txt"
    cat >"$PROMPT_FILE" <<EOF
ワークフロー \`$WF\` の L1 出口のみ実施してください。

1. 次のファイルを読む: ${TARGET}
2. プレースホルダ行（—）を削除し、1 行だけ追加する:
   - delivery-lite: id=E2E-LIVE-1, status=done, 証拠に python3 scripts/plan_active.py の実行を記載
   - content-delivery-lite: id=CH-LIVE-1, status=done, 証拠に sandbox 内の稿ファイルパス
3. **変更してよいのは上記ファイルのみ**。他ファイル・git commit・push は禁止。
4. 終わったら変更した表の 1 行をチャットに引用して報告。
EOF
    echo "prompt: $PROMPT_FILE"
    "$AGENT" -p --trust --approve-mcps --workspace "$ROOT" "$(cat "$PROMPT_FILE")"
    ;;
  kilo)
    echo "Kilo TUI 実機（人が操作）:"
    echo "  1. 本リポジトリを Kilo で開く"
    echo "  2. /$WF を実行"
    echo "  3. サンドボックスのみ更新: $TARGET"
    echo "  4. ターミナルで: ${PLAN[*]}"
    echo "会話ログは Kilo 側に残る。本スクリプトは sandbox をリセット済み。"
    exit 2
    ;;
  *)
    echo "MODE must be dry|cursor|kilo" >&2
    exit 1
    ;;
esac

echo "=== plan validator ==="
"${PLAN[@]}"
echo "PASS agent-active-live ($WF / $MODE)"
echo "LOG=$LOG"
