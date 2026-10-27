# 意図スコアリング — 監査と反映

§0 **監査指摘の反映記録と、ルート層・カタログ拡張（2026-10-26）の自己点検。**

---

## 反映済み（P1）

| id | 指摘 | 反映 |
|---|---|---|
| A1 | `route_task` が `needs_scoring` を delivery-lite 扱い | `format_needs_scoring_text` |
| A2 | 学習 DB 汚染 | MCP `learn` **既定 false**、明示 true のみ昇格 |
| A3 | `promote` が workflow 未検証 | `WORKFLOW_AGENTS` で拒否 |
| A4 | キュー worker が古い store に bind | 各ジョブに `db_path` を載せて都度 open |
| A5 | テスト不安定 | `reset_learn_queue`・DB をワークスペース配下 |

---

## 反映済み（カタログ・ルート層）

| id | 内容 | 反映先 |
|---|---|---|
| C1 | workflow に description | `mcp/intent_catalog.py` `WORKFLOWS` |
| C2 | 上流プロンプトに description 付き候補 | `mcp/intent_upstream.py` |
| C3 | L0/L1/L2 名前統一 | `mcp/intent_interpreter.py` `route_layer` |
| C4 | L0 slash = commands 台帳 | `mcp/intent_commands.py` + `.kilo/commands/*.md` |
| C5 | workflow ごと MCP ツール許可 | `IntentSchedule.mcp_tools_allow` |
| C6 | L3 委譲は interpret 外 | `delegate_subtask` MCP（ホストが実行）。他製品は同スキーマを HTTP 等で流用可 |
| C7 | B3 MCP ゲート | `interpret_intent`/`route_task` 後に `mcp_tools_allow` を強制 |

---

## 残課題（P2）

| id | 内容 |
|---|---|
| B1 | `find_match` 全表スキャン — 件数増で要インデックス |
| B2 | 上流プロンプト長 — description 付きで改善済み。さらに削るなら動的 top-k |
| B3 | ~~MCP 側での `mcp_tools_allow` 強制~~ → **実装済**（`intent_session` + `server.py` ゲート） |

---

## 受入（Pass）

| 期待 | Pass |
|---|---|
| `python3 mcp/test_intent.py` が成功 | 全テスト OK |
| L0 で `command_path` が付く | `/research` で `.kilo/commands/research.md` |
| L2 needs_scoring に `workflow_catalog` | payload に配列 |
| compliance で `memory_save` 不在 | `mcp_tools_allow` |

---

## 更新履歴

| 日付 | 内容 |
|---|---|
| 2026-10-26 | 初版（監査反映表） |
| 2026-10-26 | C1–C6 カタログ・ルート層・監査追記 |
