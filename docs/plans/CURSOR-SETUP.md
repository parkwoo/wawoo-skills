# Cursor での使い方

## 結論
- **開くだけ**：Cursor は **`AGENTS.md`** と **`.cursor/rules/*.mdc`** を読む。
- **自動実行はされない**：`.kilo/commands`（slash）・`.kilo/agents`（切替）・`SKILL.md`（自動起動）は**ネイティブ非対応**。
- **MCP を有効化**すると、`capabilities`／`skill_search`／`skill_get` 等を**ツール呼び出し**で使える（推奨）。

## 設定
- `AGENTS.md`（プロジェクト直下）
- `.cursor/rules/00-contract.mdc`・`10-skills.mdc`・`20-workflows.mdc`（`alwaysApply: true`）
- `.cursor/mcp.json`（MCP サーバ `wawoo-skills`）

> パスは環境に合わせる。相対で起動できない場合は**絶対パス**。

## 有効化
1. このディレクトリを開く。
2. **Settings → MCP** で `wawoo-skills` を有効化。
3. ツールに `capabilities`・`skill_search`・`skill_get` が出るか確認。
4. 出ない場合：`python3 mcp/server.py` が起動するか確認。

## 動作確認
```
MCP の capabilities を実行して、使える skill と workflow を一覧して。
```
```
workflow_get で feature-delivery の手順を取得して、その手順に従って。
```
```
skill_search で「セキュリティ」を検索し、該当する skill_get を取得して。
```

## フォールバック（MCP 無し）
```
@.kilo/CAPABILITIES.md を見て候補を選び、必要な @.kilo/skills/<name>/SKILL.md を読んで従って。
@.kilo/commands/<name>.md の手順を適用して。
```
- **モデル依存**（飛ばすことがある）。MCP が確実。

## できないこと
- `/feature-delivery` 等の **slash command**。
- `.kilo/agents` の **agent 切替**（役割は `@.kilo/agents/<role>.md` を読んで適用）。
- `SKILL.md` の**自動発見・自動起動**。

## トークン予算
- ルールは短く（合計 < 500 行推奨）。
- スキルは必要分だけ取得（全部読まない）。

## 検証
- `python3 mcp/test_server.py`
- `python3 scripts/validate_assets.py`
- `python3 scripts/gen_capabilities.py`
