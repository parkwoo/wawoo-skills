# 実機 E2E — ACTIVE / CONTENT 更新と plan_* 検証

> **§0 一文**: サンドボックス SSOT をエージェント（または dry）が 1 行更新し、`plan_active` / `plan_content` が通ることをログに残す。

## 対象ワークフロー（2）

| workflow | サンドボックス | 検証 |
|----------|----------------|------|
| `delivery-lite` | `docs/plans/evidence/sandbox/ACTIVE.md` | `plan_active.py` |
| `content-delivery-lite` | `docs/plans/evidence/sandbox/CONTENT.md` | `plan_content.py` |

本番の `docs/plans/ACTIVE.md` は**触らない**。

## モード

| MODE | 要否 | 説明 |
|------|------|------|
| **dry** | API・login 不要 | `active_apply_dryrun.py` がエージェント相当の更新を適用（CI・手元スモーク向け） |
| **cursor** | `agent login` または `CURSOR_API_KEY` | `agent -p` でサンドボックスのみ編集させる |
| **kilo** | Kilo TUI | 手順を表示し exit 2（会話は Kilo 側に取证） |

## 手順

```bash
./scripts/bootstrap-internal.sh   # 初回のみ
chmod +x internal/scripts/e2e/agent-active-live.sh

# 1) 決定的（推奨・毎回）
MODE=dry internal/scripts/e2e/agent-active-live.sh delivery-lite
MODE=dry internal/scripts/e2e/agent-active-live.sh content-delivery-lite

# 2) Cursor 実機
MODE=cursor internal/scripts/e2e/agent-active-live.sh delivery-lite

# 3) Kilo（人が TUI で /delivery-lite 後、ターミナルで plan を実行）
MODE=kilo internal/scripts/e2e/agent-active-live.sh delivery-lite
```

## 取证

| 成果物 | パス |
|--------|------|
| 実行ログ | `docs/plans/evidence/agent-active-<wf>-<mode>-<UTC>.log` |
| サンドボックス SSOT | `docs/plans/evidence/sandbox/` |
| Cursor プロンプト写し | `docs/plans/evidence/sandbox/agent-prompt-*.txt` |

`docs/plans/evidence/` は `.gitignore`（ローカル証跡）。要約は PR にログを貼るか `e2e_with_evidence.sh` と併用。

## 公開 CI との関係

`scripts/e2e_flows.py` の `test_agent_active_sandbox_dry` が **dry 両 workflow** を回す（`internal.example` から fixtures 参照）。実 `agent -p` は CI では走らない。

## 受入

| id | Pass |
|----|------|
| A1 | dry で両 workflow が exit 0 |
| A2 | cursor 後 `plan_*` が exit 0（手動） |
| A3 | 本番 ACTIVE / CONTENT が diff されない |
