# E2E とワークフローの対応（証跡の見方）

## ログ・証跡を残す

```bash
./scripts/e2e_with_evidence.sh
# → docs/plans/evidence/e2e-run-<UTC>.log
# → docs/plans/evidence/e2e-run-<UTC>.summary.md
```

CI（GitHub Actions `validate.yml`）でも同系のコマンドを実行。PR のチェックログが**クラウド側の証跡**。

手元の **ACTIVE / CONTENT** を更新したタスクの証跡は、表の「証拠」列（コマンド・ファイルパス）。

## 今回の自動テストが証明すること

| 層 | スクリプト | 証跡出力 |
|----|------------|----------|
| 資産整合 | `validate_assets.py` | stdout（WARN/OK） |
| MCP プロトコル | `mcp/test_server.py` | stdout |
| Memory 実装 | `mcp/test_memory_ops.py` | stdout |
| Kilo/Cursor 入口 | `cli_adapters_mock.py` | parity 5 workflow + Cursor slash 拒否 |
| 儀式 L0–L3 | `e2e_flows.py` | 27+ 項目 PASS/FAIL |
| SSOT 表検証 | `plan_*.py` | ACTIVE / BACKLOG / RETRO / CONTENT OK 行 |
| **実機 SSOT（dry）** | `internal.example/.../agent-active-live.sh` | `docs/plans/evidence/agent-active-*.log` |

## 15 ワークフロー — 役割と E2E の深さ

| workflow | いつ使う | SSOT | E2E で何を見ているか |
|----------|----------|------|----------------------|
| `/delivery-lite` | コード L1 既定 | ACTIVE | parity・L1 シミュレーション・**sandbox dry 実機** |
| `/content-delivery-lite` | 長文・書籍 L1 | CONTENT | 同上・**sandbox dry 実機** |
| `/feature-delivery` | 厚い機能納品 | ACTIVE + ゲート | delivery-lite へのエスカレーション文言 |
| `/ui-delivery` | Web/UI | ACTIVE + DESIGN | ACTIVE 接続・agent 存在 |
| `/research` | 調査 | ACTIVE + docs | ACTIVE 接続 |
| `/market-plan` | 事業・市場計画 | ACTIVE + plan-md | ACTIVE 接続 |
| `/design-review` | UI レビューのみ | — | agent/description のみ |
| `/deck` | スライド | plan-md | 同上 |
| `/compliance-review` | 法務ゲート | — | 同上 |
| `/release-review` | リリース前 | — | 同上 |
| `/incident-response` | 障害 | — | 同上 |
| `/sprint-plan` | L2 スプリント | BACKLOG/issue | L2 シミュレーション |
| `/status-report` | 進捗報告 | ACTIVE or issue | ACTIVE/L1 文言 |
| `/self-review` | コード自己修正 | — | 同上 |
| `/self-improve` | L3 改善 | RETRO + memory | L3 シミュレーション |

## 実 CLI（Kilo TUI / `agent -p`）

| 種別 | 場所 | 要否 |
|------|------|------|
| モック parity | `scripts/cli_adapters_mock.py` | 不要 |
| **ACTIVE/CONTENT 1 行更新（dry）** | `internal.example/scripts/e2e/agent-active-live.sh` | 不要 |
| **Cursor 実機** | 同上 `MODE=cursor` | `agent login` |
| **Kilo TUI** | 同上 `MODE=kilo` + [AGENT-ACTIVE-E2E.md](../../internal.example/docs/audit/AGENT-ACTIVE-E2E.md) | 人が操作 |

手順全文: `internal.example/docs/audit/AGENT-ACTIVE-E2E.md`（`bootstrap-internal.sh` 後は `internal/docs/audit/`）。
