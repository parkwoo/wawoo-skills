# 変更履歴

本プロジェクトの notable な変更を記録する。形式は [Semantic Versioning](https://semver.org/) に準拠。

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
