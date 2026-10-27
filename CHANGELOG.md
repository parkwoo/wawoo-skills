# 変更履歴

本プロジェクトの notable な変更を記録する。形式は [Semantic Versioning](https://semver.org/) に準拠。

## [Unreleased]

### 追加
- 意図ルーティング: L0 slash／L1 学習 SQLite／L2 上流 JSON スコア、workflow `description` 付きカタログ。
- MCP: `interpret_intent`・`route_task`・`workflow_clear`・`delegate_subtask`、確定後 `mcp_tools_allow` ゲート。
- 対外ドキュメント: `docs/INTENT-ROUTING.md`、`mcp/README.md` 全面更新。

### 変更
- MCP server バージョン表記 `0.4.0`（意図ツール・ゲート）。
- L3 `delegation_hint` 既定を `upstream-subagent` に（特定 API 製品名を含めない）。
- 設計文書: co-taro 等とは**別プロジェクト**として境界を明記。
- Kilo: `config.instructions` は**絶対パス**で指定する（相対 `ROUTER.md` は実行時コンテキストに注入されない）。§4 に「非自明な依頼は最初のツール呼び出しを `workflow_get`／`interpret_intent` にする」を強制として追加。
- `gen_router.py`: ルーター手順を必須化（`workflow_get` を必ず呼ぶ・ネイティブ `skill` での代替禁止）。
- `/delivery-lite`: 手順 0 で `wawoo-skills_workflow_get` を呼び、MCP の手順を正本にする。
- 既存 agent 定義（21）に `## Routing (MCP first)` を追加: 最初のツールを `workflow_get`／`interpret_intent` にし、親 workflow が確定済みならそれに従う。ネイティブ `skill` は MCP 不能時のみ。
- 新規 agent `wawoo-router`（`mode: primary`）: 既定の入口として非自明な依頼で必ず MCP を先に呼び、その workflow を自ら実行する。`instructions` は絶対パス、`default_agent` 既定を `wawoo-router` に。
- `install_global.py`: `ROUTER.md` 生成・`instructions` 絶対パス登録・`default_agent` 設定を追加（`--default-agent`／`--no-default-agent`／`--force-default-agent`）。

## [0.5.0] - 2026-10-25

### 追加
- 実機 E2E（internal.example）: `agent-active-live.sh`（delivery-lite / content-delivery-lite、MODE=dry|cursor|kilo）。
- 公開 CI: `e2e_flows` に `agent_active_sandbox_dry`。

## [0.4.9] - 2026-10-25

### 追加
- `/content-delivery-lite`、`CONTENT.example.md`、`scripts/plan_content.py`。
- `scripts/cli_adapters_mock.py` — Kilo `/slash` と Cursor `@commands` の MCP parity モック（実 CLI 不要）。
- METHODOLOGY §5.1 交付物タイプ表。

### 変更
- `/ui-delivery`・`/research`・`/market-plan` を `ACTIVE.md` + `plan_active` に接続。
- E2E: content 契約・交付物 hook・CLI モック。

## [0.4.8] - 2026-10-25

### 追加
- E2E: `l0_simulated_flow`・`l2_simulated_flow`・`l3_simulated_flow`・`ceremony_levels_matrix`。
- `scripts/plan_l2_backlog.py`・`plan_l3_record.py`。
- `docs/plans/BACKLOG.example.md`・`RETRO.example.md`。

### 変更
- `/sprint-plan` を L2 SSOT・`plan_l2_backlog` 検証付きに整理。
- `AGENTS.md` SSOT 表に L2 バックログ・L3 retro を追記。

## [0.4.7] - 2026-10-25

### 追加
- `scripts/e2e_flows.py` — 契約・ACTIVE 状態機械・MCP・workflow の E2E（API 不要）。
- `scripts/plan_active.py` — ACTIVE タスク表の Gₑ 検証 CLI。

### 変更
- `/delivery-lite` 検証手順に `plan_active`・`e2e_flows` を追加。
- `/status-report` を ACTIVE（L1）と issue（L2）で整理。
- CI・`internal.example` smoke に memory E2E を追加。

## [0.4.6] - 2026-10-25

### 追加
- `/delivery-lite` — L1 軽量納品（`docs/plans/ACTIVE.md` 状態機械）。
- `docs/plans/`（`README.md`・`ACTIVE.md` テンプレ）。
- `docs/METHODOLOGY.md` §5 儀式レベル L0–L3。

### 変更
- `AGENTS.md` §3 タスク SSOT、既定入口を `/delivery-lite` に。
- `commands/README.md`・USAGE・PROCESS・PUBLICATION・README を追随。

## [0.4.5] - 2026-10-25

### 追加
- `mcp/memory_ops.py` — memory 想起・保存・秘密スキャン（INDEX＋topic ファイル）。
- `docs/memory/TEMPLATE.md`・`MEMORY-TOOLS.md`・`kit.md`。
- `mcp/test_memory_ops.py`。

### 変更
- MCP `memory_recall`／`memory_save` を skill と一致（セクション・MEM id・tags／source）。
- `memory` スキル、`/feature-delivery`、AGENTS、PROCESS P4、PUBLICATION、USAGE を配線。
- `validate_assets.py` が `docs/memory/` を秘密パターン検査。

## [0.4.4] - 2026-10-25

### 変更
- METHODOLOGY / PROCESS-PHILOSOPHY 監査反映（WARO と D 段の分離、正本の明示、ゲート符号統一、効き方の限界）。

## [0.4.3] - 2026-10-25

### 追加
- `docs/PROCESS-PHILOSOPHY.md` — 工程思想論（納品ライフサイクル・ゲート理論・環境反復）。

## [0.4.2] - 2026-10-25

### 追加
- `docs/METHODOLOGY.md` — Skill・Agent・ワークフロー方法論（問題定義・三層・WARO・ゲート）。

## [0.4.1] - 2026-10-25

### 変更
- README に「skill／workflow が呼ばれない」問題への設計思想（なぜこのキットか）を追記。

## [0.4.0] - 2026-10-25

### 変更
- メンテナ・監査・実測資産を **git 管理外**（`internal/`）に移行。テンプレは `internal.example/` + `scripts/bootstrap-internal.sh`。
- 公開範囲の説明: `docs/PUBLICATION.md`。

### 削除（公開 clone から除外）
- `docs/audit/`、`docs/MAINTAINER.md`、`scripts/e2e/`、`docker/e2e/`、監査用 `scripts/audit_*.py` 等（`internal.example` に同梱）。

## [0.3.4] - 2026-10-25

### 変更
- 公開 README からメンテナ向け E2E/Docker 記述を除去し `docs/MAINTAINER.md` に移動。

## [0.3.3] - 2026-10-25

### 追加
- `scripts/e2e/install-compose-v2.sh`（`docker compose` プラグイン導入）
- `scripts/e2e/compose.sh`（V2 優先ラッパー）

### 変更
- CLI-E2E 手順に Compose V2 トラブルシュートを追記

## [0.3.2] - 2026-10-25

### 変更
- Cursor Agent CLI 実測を **`agent login` 優先**に修正（`CURSOR_API_KEY` は CI 用オプション）。

## [0.3.1] - 2026-10-25

### 追加
- CLI 実測環境: `docker/e2e/`、`scripts/e2e/`、`docs/audit/CLI-E2E-ENV.md`
- `.env.example`、`.cursor/cli.json.example`（Cursor Agent 読み取り専用用）

## [0.3.0] - 2026-10-25

### 追加
- OpenDesign 7 skill に `LICENSE.txt` / `NOTICE.txt` を同梱。
- `docs/audit/KILO-E2E.md`（Kilo 実機 `/feature-delivery` + MCP 手順）。
- `scripts/split_skill_reference.py`（skill 分割用）。

### 変更
- 大型 skill を `references/` に分割：`ask-matt`・`wayfinder`・`design-brief`・`writing-for-agents`。
- 監査記録を再生成（ライセンス要確認 0 件）。

## [0.2.0] - 2026-10-25

### 追加
- GitHub Actions `validate`（`validate_assets.py`・`mcp/test_server.py`）。
- 監査スクリプトと記録：`scripts/audit_license_headers.py`、`scripts/audit_skill_quality.py`、`docs/audit/`。
- `imagegen-frontend-mobile` の詳細を `references/mobile-image-direction.md` に分割。

### 変更
- ワークフロー文言の中国語を日本語化（`/research`、`/self-improve` 系）。
- `CHANGELOG.md` を日本語化。
- `privacy-review` の汎用キット向け参照パスを修正。
- `AGENTS.md`・`docs/USAGE.md` に Skill 予算例外を明記。

## [0.1.0] - 2026-10-25

### 追加
- 汎用キット：55 skills、21 agents、13 workflows。
- MCP 能力サーバ（stdio・stdlib のみ）：`capabilities`、`skill_search`、`skill_get`、`workflow_get`、`agent_get`、`memory_recall`、`memory_save`、`evidence_check`。
- Cursor ルールと `AGENTS.md` 契約。
- `scripts/gen_capabilities.py`（カタログ）と `scripts/validate_assets.py`（検証）。

### 注記
- ライセンス不明の第三者資産は同梱しない（Marketplace business 3 件、`fal-gen`）。
