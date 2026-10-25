# Agent 呼び出し ＆ コンテキスト設計

## 1. 呼び出しアーキテクチャ
```
L0 契約      AGENTS.md / .cursor/rules（短い）
L1 カタログ  .kilo/CAPABILITIES.md（生成物・1行説明）
L2 Workflow  .kilo/commands/*.md（入口・手順・ゲート・出力形）
L3 Skill     .kilo/skills/<name>/SKILL.md（選択時のみ全文）
L4 Reference 必要時のみ
L5 MCP       capability server（skill_search/get, workflow_get, memory_*, evidence_check）
L6 CI        validate_assets + lint/test（決定的）
```
- **ユーザーは Workflow を起動**（Kilo: `/name`、Cursor: `@.kilo/commands/<name>.md`）。
- Workflow 本文に**読むべき skill のパス**を明記。**agent 任せにしない**。
- Skill は**選ばれたものだけ全文**。ゲートは CI/スクリプトで決定的に。

## 2. MCP（能力サーバ）
`mcp/server.py`（標準ライブラリのみ・stdio JSON-RPC）。
Tools：`capabilities`・`skill_search`・`skill_get`・`workflow_get`・`agent_get`・`memory_recall`・`memory_save`・`evidence_check`。
- 設定：`kilo.json`／`.cursor/mcp.json`。
- テスト：`python3 mcp/test_server.py`。

## 3. モデルへの渡し方（コンテキスト）
**組立順**：契約 → タスク → Workflow → 選択 Skill → Reference → 関連 Memory → Tool 結果。

| 要素 | 予算 |
|---|---|
| 契約 | ≤500 tokens |
| カタログ | ≤1,000 |
| Workflow 1 本 | ≤1,500 |
| Skill 1 個 | ≤2〜4KB |
| Memory | top-5 |

- **段階的開示**：全部を一度に渡さない。
- **構造化出力**：Workflow の出力スキーマに従う。
- **停止条件**：承認・証拠・失敗観察。
- 大きいツール結果は**要約＋ID**。矛盾を置かない（SSOT 1 つ）。

## 4. 計測（推奨）
- workflow 成功率・平均トークン・再試行回数・ゲート通過率。
- 失敗は `memory` に observed failure として保存し、skill を改善。
