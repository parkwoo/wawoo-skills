# 使い方（Kilo / Cursor / MCP）

## 1. 収録
- Skills：`.kilo/skills/<name>/SKILL.md`（55）
- Agents：`.kilo/agents/<name>.md`（21）
- Workflows：`.kilo/commands/<name>.md`（15）
- MCP：`mcp/server.py`
- カタログ（自動生成）：`.kilo/CAPABILITIES.md`

## 2. Kilo CLI / Kilo Code（https://kilo.ai ・ https://kilocode.ai）
1. このディレクトリを開く（`.kilo/` を自動探索、`kilo.json` で MCP 有効）。
2. ワークフロー：`/feature-delivery` など。
3. スキル：モデルが `SKILL.md` を選択、または明示的に参照。

### グローバル配置（全プロジェクトで使う・冪等）
`.kilo/{skills,agents,commands}` を `~/.config/kilo/` へ同期し、MCP と適用範囲メモを冪等登録する（再実行可）。
```bash
python3 scripts/install_global.py --dry-run    # 変更内容の確認
python3 scripts/install_global.py              # 適用（既定ミラー＝余剰を削除）
python3 scripts/install_global.py --no-delete  # 余剰を残す
KILO_GLOBAL_DIR=/path/to/config python3 scripts/install_global.py  # 別の配置先
```
- MCP は絶対パス登録（`/usr/bin/python3` ＋ `WAWOO_SKILLS_ROOT`／`WAWOO_MEMORY_READONLY`）。詳細は `mcp/README.md`。
- 併せて **`ROUTER.md` を生成**し、`instructions` に **絶対パス**で冪等登録、`default_agent` を `wawoo-router` に設定する（既定）。
  - Kilo の `instructions` は**絶対パス必須**（相対 `ROUTER.md` は実行時コンテキストに注入されない）。
  - 既定 agent `wawoo-router` が「最初のツール＝`workflow_get`／`interpret_intent`」を強制し、`code` 既定時のルーティング漏れを防ぐ。
  - 変更は `--default-agent <name>`／`--no-default-agent`／`--force-default-agent` で制御。
- **反映には Kilo の再起動が必要**（agent／command／instruction はサーバ起動時にキャッシュ。VS Code は Reload Window）。
- キットの repo 相対 SSOT を前提とする手順は**キット内でのみ有効**。グローバル `AGENTS.md` にその旨を追記する。
- `validate_assets`：同名 skill／command は **command 側で入口を明文化していれば警告しない**（`design-review`・`research` は対応済み）。未記載の衝突は `WARN` として出る（`scripts/validate_assets.py` の `documents_entry`）。

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
**カタログ系**: `capabilities`・`skill_search`・`skill_get`・`workflow_get`・`agent_get`・`memory_recall`・`memory_save`・`evidence_check`。

**意図ルーティング**（任意だが推奨）: `interpret_intent` → `workflow_get` → … → `workflow_clear`。サブタスクは `delegate_subtask`。

- 対外ガイド：**[docs/INTENT-ROUTING.md](INTENT-ROUTING.md)**（L0–L3・スコア JSON・ツールゲート）
- 実装・常駐：`mcp/README.md`・`docs/design/INTENT-RECEIVER.md`

## 5. 呼び出しの順序
1. **Workflow**（入口）を選ぶ。曖昧な依頼は MCP **`interpret_intent`** で 15 workflow から選ぶ（[INTENT-ROUTING.md](INTENT-ROUTING.md)）。明示できるときは **`/delivery-lite`**（`docs/plans/ACTIVE.md` が進捗 SSOT）。儀式レベルは `docs/METHODOLOGY.md` §5。
2. **カタログ／MCP** で候補を選ぶ（全部読まない）。
3. 必要な **Skill** だけ開く。
4. Workflow の**出力スキーマ**と**ゲート**（承認・証拠）に従う。
5. 作業前に `memory` を想起、決定後に保存（MCP `memory_save` は INDEX＋topic ファイル。`docs/memory/TEMPLATE.md`）。

### 記憶（memory）

- 正本: `docs/memory/`（`MEMORY-TOOLS.md` で Kilo／MCP の優先順）
- 納品経路 `/feature-delivery` の入口・出口でも想起／保存
- CI: `validate_assets.py` が memory 内の秘密らしき文字列を検出
- E2E: `python3 scripts/e2e_flows.py`（**L0–L3**・MCP・workflow）。`python3 scripts/cli_adapters_mock.py`（**Kilo/Cursor 入口モック**）
- 検証 CLI: `plan_active` / `plan_l2_backlog` / `plan_l3_record` / `plan_content`

## 6. コンテキスト予算
- 契約 ≤500tok／カタログ ≤1k／Workflow ≤1.5k／**Skill 1 個 ≤2〜4KB**／Memory top-5。
- 段階的開示：全部を一度に渡さない。
- 予算例外：入口 `SKILL.md` のみ先読み。詳細は各 skill の `references/`（例：`imagegen-frontend-mobile`・`ask-matt`・`wayfinder`・`design-brief`・`writing-for-agents`）。

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
