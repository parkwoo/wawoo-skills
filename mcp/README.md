# this project Capability MCP Server

`wawoo-skills` の **skill／agent／workflow／memory／evidence** を **MCP ツール**として提供する。
目的：**agent が散文の指示ではなく「ツール呼び出し」で確実に能力を呼べる**ようにする（Kilo / Cursor 共通）。

- 実装：`mcp/server.py`（**stdlib のみ**・依存なし）
- トランスポート：**stdio / JSON-RPC 2.0（改行区切り）**
- protocolVersion：`2024-11-05`

## Tools

| Tool | 入力 | 出力 |
|---|---|---|
| `capabilities` | — | 全 skill/agent/workflow の 1 行一覧 |
| `skill_search` | `query`, `limit?` | 候補（name/desc/path） |
| `skill_get` | `name` | `SKILL.md` 全文 |
| `workflow_get` | `name` | command 全文 |
| `agent_get` | `name` | agent 定義 |
| `memory_recall` | `query`, `top_k?` | `docs/memory/` の関連抜粋 |
| `memory_save` | `text`, `tags?` | `docs/memory/INDEX.md` に追記（**秘密は拒否**） |
| `evidence_check` | `scope: assets` | `scripts/validate_assets.py` の結果 |

## 使い方（推奨フロー）
1. `capabilities` または `skill_search` で候補を選ぶ（**全部読まない**）。
2. `workflow_get` で入口の手順を取得。
3. 必要な `skill_get` だけ取得（段階的開示）。
4. `memory_recall` で関連知識を取得。
5. `evidence_check` で資産整合を確認。

## 設定
- **Kilo**：`kilo.json`
  ```json
  {"mcp":{"wawoo-skills":{"type":"local","command":["python3","mcp/server.py"],"enabled":true}}}
  ```
- **Cursor**：`.cursor/mcp.json`
  ```json
  {"mcpServers":{"wawoo-skills":{"command":"python3","args":["mcp/server.py"]}}}
  ```

## 実行・テスト
```bash
python3 mcp/server.py        # stdio（通常はクライアントが起動）
python3 mcp/test_server.py   # スモークテスト（initialize/tools/list/tools/call）
```

## セキュリティ
- `skill_get`/`workflow_get`/`agent_get` は **`.kilo` 配下のみ**（パストラバーサル拒否）。
- `memory_save` は**追記のみ**、**秘密らしき文字列を拒否**。
- `evidence_check` は `scope=assets` のみ（**任意コマンド実行はしない**）。
- 読み取り中心。破壊的操作なし。

## 制約
- サーバは**プロジェクトルートからの相対パス**で `.kilo` を解決（Cursor 設定は絶対パス推奨）。
- MCP クライアントの起動方法はツール依存。起動しない場合は `python3 mcp/server.py` の権限/パスを確認。
