# 使い方（Kilo / Cursor / MCP）

## 1. 収録
- Skills：`.kilo/skills/<name>/SKILL.md`（55）
- Agents：`.kilo/agents/<name>.md`（21）
- Workflows：`.kilo/commands/<name>.md`（13）
- MCP：`mcp/server.py`
- カタログ（自動生成）：`.kilo/CAPABILITIES.md`

## 2. Kilo CLI / Kilo Code（https://kilo.ai ・ https://kilocode.ai）
1. このディレクトリを開く（`.kilo/` を自動探索、`kilo.json` で MCP 有効）。
2. ワークフロー：`/feature-delivery` など。
3. スキル：モデルが `SKILL.md` を選択、または明示的に参照。

## 3. Cursor（https://cursor.com）
1. このディレクトリを開く（`AGENTS.md` と `.cursor/rules` を読む）。
2. **Settings → MCP** で `wawoo-skills` を有効化（`.cursor/mcp.json`）。
3. ツール `capabilities`／`skill_search`／`skill_get` を利用。

**Cursor の制約**：
- slash command（`/feature-delivery` 等）は**動かない**。
- agent の切替は**無い**（役割は `@.kilo/agents/<role>.md` を読んで適用）。
- `SKILL.md` の**自動発見・自動起動**は**無い**。

**フォールバック（MCP 無し）**：
```
@.kilo/CAPABILITIES.md を見て候補を選び、必要な @.kilo/skills/<name>/SKILL.md を読んで従って。
@.kilo/commands/<name>.md の手順を適用して。
```

## 4. MCP（Model Context Protocol: https://modelcontextprotocol.io）
```bash
python3 mcp/server.py        # stdio（通常はクライアントが起動）
python3 mcp/test_server.py   # スモークテスト
```
Tools：`capabilities`・`skill_search`・`skill_get`・`workflow_get`・`agent_get`・`memory_recall`・`memory_save`・`evidence_check`。
詳細：`mcp/README.md`。

## 5. 呼び出しの順序
1. **Workflow**（入口）を選ぶ。
2. **カタログ／MCP** で候補を選ぶ（全部読まない）。
3. 必要な **Skill** だけ開く。
4. Workflow の**出力スキーマ**と**ゲート**（承認・証拠）に従う。
5. 作業前に `memory` を想起、決定後に保存。

## 6. コンテキスト予算
- 契約 ≤500tok／カタログ ≤1k／Workflow ≤1.5k／**Skill 1 個 ≤2〜4KB**／Memory top-5。
- 段階的開示：全部を一度に渡さない。
- 予算例外：`imagegen-frontend-mobile` は入口 `SKILL.md` のみ先に読み、詳細は `references/mobile-image-direction.md` を必要時だけ開く。

## 7. 前提が必要なスキル（3）
`to-spec`・`to-tickets`・`triage` は issue tracker が必要。初回に `setup-matt-pocock-skills` を実行。
`scripts/readiness.json` に記載。

## 8. 保守
```bash
python3 scripts/validate_assets.py
python3 scripts/gen_capabilities.py
python3 mcp/test_server.py
```
版管理：`docs/VERSIONING.md`。
