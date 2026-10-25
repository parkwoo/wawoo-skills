# スキル 実行可能性（Readiness）

対象：`.kilo/skills` **55**・`.kilo/agents` **21**・`.kilo/commands` **13**。

## 1. 機械検証
- `python3 scripts/validate_assets.py` … `name=dir`・参照・重複・JSON・readiness を検証。
- `python3 mcp/test_server.py` … MCP（initialize/tools/call）を検証。

## 2. 前提が必要なもの（3）
| スキル | 前提 | 対応 |
|---|---|---|
| `to-spec` / `to-tickets` / `triage` | **issue tracker 設定** | 初回 `setup-matt-pocock-skills` |

- `scripts/readiness.json` に記載。MCP `capabilities {ready_only:true}` で除外可能。
- **これ以外は外部依存なし**。

## 3. 画像生成
- `imagegen-frontend-mobile` は**プロンプト／ビジュアル指針**（画像生成ツールは同梱しない）。
- 生成は利用可能な画像ツール（OpenAI Images／fal／社内ツール等）で行う。ツールが無ければ**プロンプトのみ**納品。
- `screenshots-marketing` は **Playwright 任意**（未導入なら撮影計画＋既存証拠）。

## 4. 公開のためのライセンス整理（重要）
- **除外**：Marketplace business 3 件（`license: NOASSERTION`）／`fal-gen`（ライセンス不明）。
- 同梱の由来：skills-main（MIT）／OpenDesign（Apache-2.0）／Kilo 組み込み（frontmatter の MIT）／本リポジトリ（MIT）。
- 詳細：`.kilo/skills/ATTRIBUTION.md`・`LICENSES/`。

## 5. Cursor
- `AGENTS.md`＋`.cursor/rules`＋**MCP**＋`@file`。**slash command／agent／SKILL のネイティブ実行は無い**。
- 詳細：`docs/plans/CURSOR-SETUP.md`。
