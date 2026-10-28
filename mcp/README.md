# wawoo-skills Capability MCP Server

skill／agent／workflow／memory／evidence と **意図ルーティング**を MCP ツールで提供します。エージェントが散文だけで進めず、**ツール呼び出しで入口と権限を固定**するためのサーバです（Kilo / Cursor 共通）。

- 実装：`mcp/server.py`（**stdlib のみ**）
- トランスポート：**stdio / JSON-RPC 2.0**（改行区切り）
- 対外ガイド（意図ルーティング）：**[docs/INTENT-ROUTING.md](../docs/INTENT-ROUTING.md)**

## Tools

### カタログ・手順

| Tool | 入力 | 出力 |
|------|------|------|
| `capabilities` | `ready_only?` | skill / agent / workflow の 1 行一覧 |
| `skill_search` | `query`, `limit?` | 候補（name / desc / path） |
| `skill_get` | `name` | `SKILL.md` 全文 |
| `workflow_get` | `name` | `.kilo/commands/<name>.md` 全文 |
| `agent_get` | `name` | agent 定義 |
| `memory_recall` | `query`, `top_k?` | `docs/memory/` チャンク想起 |
| `memory_save` | `text`, `tags?`, `source?` | INDEX + topic 追記（**秘密拒否**） |
| `evidence_check` | `scope: assets` | `validate_assets.py` 結果 |

### 意図ルーティング（L0–L2）

| Tool | 入力 | 出力 |
|------|------|------|
| `interpret_intent` | `text`, `scoring?`, `learn?`, `via_receiver?` | JSON（`schedule` または `needs_scoring`） |
| `route_task` | `task` | 人間向けテキスト（スコア待ち時は `NEEDS SCORING`） |

`schedule` が確定すると **MCP ツールゲート**が有効になり、`mcp_tools_allow` 以外のツールは拒否されます（`interpret_intent` / `route_task` / `workflow_clear` / `delegate_subtask` は常に可）。

### セッション・委譲（L3）

| Tool | 入力 | 出力 |
|------|------|------|
| `workflow_clear` | — | ゲート解除 |
| `delegate_subtask` | `subtask`, `label?`, `background?`, `agent?` | L3 委譲 JSON（**子セッションは作らない**。IDE の Task / subagent が実行） |

## 推奨フロー

1. `interpret_intent` で workflow を決める（必要なら L2 で JSON スコアを返して再呼び出し）。
2. `workflow_get` → 必要な `skill_get` のみ。
3. サブタスク分割 → `delegate_subtask` → 上流で並列実行。
4. 終了 → `workflow_clear`。

詳細は [docs/INTENT-ROUTING.md](../docs/INTENT-ROUTING.md)。

## 設定

**Kilo（プロジェクト）**

```json
{"mcp":{"wawoo-skills":{"type":"local","command":["python3","mcp/server.py"],"enabled":true}}}
```

**Kilo（グローバル）** — 絶対パス推奨

```json
{"mcp":{"wawoo-skills":{
  "type":"local",
  "command":["/usr/bin/python3","/abs/path/wawoo-skills/mcp/server.py"],
  "environment":{"WAWOO_SKILLS_ROOT":"/abs/path/wawoo-skills","WAWOO_MEMORY_READONLY":"1"},
  "enabled":true}}}
```

**Cursor** — `.cursor/mcp.json`

```json
{"mcpServers":{"wawoo-skills":{"command":"python3","args":["/abs/path/wawoo-skills/mcp/server.py"],"env":{"WAWOO_SKILLS_ROOT":"/abs/path/wawoo-skills"}}}}
```

## 環境変数

| 変数 | 既定 | 用途 |
|------|------|------|
| `WAWOO_SKILLS_ROOT` | `server.py` の親の親 | `.kilo` / `scripts` / `docs` の基点 |
| `WAWOO_MEMORY_ROOT` | `<root>/docs/memory` | memory ツールの対象 |
| `WAWOO_MEMORY_READONLY` | 無効 | `1` で `memory_save` 拒否（recall-only）。`install_global.py --memory-writable` は `0` を登録して書込を許可 |
| `WAWOO_INTENT_LEARN_DB` | `data/intent_learned.db` | 学習 trigger |
| `WAWOO_INTENT_SOCKET` | 空 | 常駐 `intent_receiver.py`（任意） |

## 実行・テスト

```bash
python3 mcp/server.py
python3 mcp/test_server.py
python3 mcp/test_memory_ops.py
python3 mcp/test_intent.py
python3 mcp/test_intent_session.py
```

常駐受信器: [docs/design/INTENT-RECEIVER.md](../docs/design/INTENT-RECEIVER.md)

## セキュリティ

- `skill_get` / `workflow_get` / `agent_get` は **`.kilo` 配下のみ**。
- `memory_save` は追記のみ・秘密パターン拒否・`WAWOO_MEMORY_READONLY` で無効化可（`install_global.py` の既定は `1`＝recall-only。`--memory-writable` で `0`）。
- `evidence_check` は `scope=assets` のみ（任意シェル不可）。
- workflow ゲートで誤ルート時のツール被害を抑止（例: 監査 workflow で `memory_save` 不可）。

## モジュール構成（意図）

| ファイル | 役割 |
|----------|------|
| `intent_catalog.py` | workflow 台帳・description・`mcp_tools_allow` |
| `intent_commands.py` | L0 slash と command パス |
| `intent_interpreter.py` | L0–L2 オーケストレーション |
| `intent_upstream.py` | 上流 JSON プロンプト |
| `intent_learned_store.py` / `intent_learn_queue.py` | L1 学習（非同期書込） |
| `intent_session.py` | B3 MCP ゲート |
| `intent_delegation.py` | L3 ペイロード |
| `intent_receiver.py` / `intent_client.py` | 常駐 NDJSON（任意） |
