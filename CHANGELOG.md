# 変更履歴

本プロジェクトの notable な変更を記録する。形式は [Semantic Versioning](https://semver.org/) に準拠。

> **リリースタグについて**: 付与済みは `v0.1.0`・`v0.2.0`・`v0.3.0`・`v0.4.0`。
> `0.4.1`〜`0.5.0` は本 CHANGELOG に記載があるが、**各版に対応するリリース commit が存在しない**
> （見出しは後続 commit、主に `c6d07f4` で追記された）ため **タグを付与しない**（誤った出所を作らない）。
> 以降は `v0.6.0` から連番でタグ付けする。

## [0.6.0] - 2026-10-28

### 追加
- **L1 トリガ分類器（決定論・無料）**: `intent_catalog.TRIGGER_KEYWORDS` を正本に、`interpret_intent` が `L0 slash → L1 学習 → L1 トリガ → L2 上流` の順で解決。閾値未満・競合時は `needs_scoring` にフォールバックし、採用時は学習 DB へ非同期昇格。
- **workflow phases**: `WorkflowSpec.phases` と `workflow_get {name, phase}`。`audit`/`research`/`verify` は `readonly-parallel`、実装系だけが `implement` を持つ。`delegate_subtask {phase}` が `exit_criteria` を添えて委譲。
- 意図ルーティング: L0 slash／L1 学習 SQLite／L2 上流 JSON スコア、workflow `description` 付きカタログ。
- MCP: `interpret_intent`・`route_task`・`workflow_clear`・`delegate_subtask`、確定後 `mcp_tools_allow` ゲート。
- 対外ドキュメント: `docs/INTENT-ROUTING.md`、`mcp/README.md` 全面更新。
- **kilo ログ分析（run `c956c7f2`）に基づく実行効率改善**（詳細: `docs/plans/RETRO-20261028-log-optimization.md`）:
  - `scripts/kilo_snapshot_gc.sh`（既定 dry-run、`--apply` で stale `index.lock` 除去＋`git gc --auto`）。
  - `mcp/conftest.py`（pytest 収集時の学習ストア隔離）。
- `install_global.py --memory-writable`: MCP 登録時に `WAWOO_MEMORY_READONLY=0` を指定して `memory_save` を有効化（既定は recall-only を維持）。`mcp/README.md`・`docs/USAGE.md` に反映。
- 配布物: 顶层 `NOTICE`（Apache-2.0 帰属の集約）と `SECURITY.md`（脆弱性報告窓口）を追加。

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
- AGENTS §4.1「実行衛生・収束ゲート」を追加: 1 セッション 1 対象／workflow 逸脱の明示／失敗の収束／後始末／記憶 1 件／トークン衛生／ローカル検証。`wawoo-router`・`ROUTER.md`・`test-engineering`・`release-readiness` にも反映（プロジェクト非依存）。
- **kilo ログ分析（run `c956c7f2`）に基づく実行効率改善**（変更点は上記 `追加`・下記 `修正` と本項の各 agent／契約更新。詳細: `docs/plans/RETRO-20261028-log-optimization.md`）。
- §4.1 に「サブエージェント委譲の効率」（skill 重複排除・read-only read 規律）を追加。
- read-only subagent（security-reviewer / accessibility-reviewer / architect / performance-reviewer / product-owner / docs-localization-reviewer）に「実行効率（トークン衛生）」節を追加。
- `security-reviewer`: `bash` を read-only サブセット許可へ（`git status/log/diff/show/rev-parse/ls-files`・`ls`・`rg`・`grep`・`find`。`*` は deny、`edit: deny` は維持）。
- `mcp/server.py`: `capabilities` が read-only（`WAWOO_MEMORY_READONLY`）時に `memory_save` 無効を明示。
- `mcp/intent_catalog.py`: `self-improve` トリガ語に log／呼び出し状況の語を追加（`日志分析`・`调用状况`・`调用排查`・`invocation status` 等）。`ROUTER.md` を再生成。
- `/release-review`: 監査委譲時の skill 要点の内联と read-only 規律を明記。
- `.kilo/skills/ATTRIBUTION.md` を実体に一致（agents 22・新規 `wawoo-router` を登記）。

### 修正
- pytest 収集時に既定の学習ストア（`data/intent_learned.db`）を参照し、`test_trigger_classifier_ja` が `source=trigger` を期待しても `learned` になる非決定性を修正（`mcp/conftest.py`）。
- `mcp/server.py`: `safe_read` のパス判定を文字列接頭辞から `Path.is_relative_to` に変更（兄弟ディレクトリの接頭辞一致を遮断）。
- `mcp/intent_receiver.py`: Unix socket を生成後に `chmod 0o600` し、`XDG_RUNTIME_DIR` を優先（`/tmp` 既定の緩い権限を回避）。
- `scripts/e2e_flows.py`: `l0_simulated_flow` が実 `ACTIVE.md` の空を要求していた不具合を修正（合成ファイルで検証）。

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
