# ドキュメント

| 文書 | 内容 |
|---|---|
| [USAGE.md](./USAGE.md) | **対外メイン** — Kilo／Cursor／MCP、呼び出し順、コンテキスト予算 |
| [INTENT-ROUTING.md](./INTENT-ROUTING.md) | **対外** — workflow 意図ルーティング（L0–L3・`interpret_intent`・ツールゲート） |
| [METHODOLOGY.md](./METHODOLOGY.md) | Skill・Agent・ワークフローの方法論（なぜ三層か・WARO） |
| [PROCESS-PHILOSOPHY.md](./PROCESS-PHILOSOPHY.md) | 工程思想論（ライフサイクル D0–D7・ゲート・トレーサビリティ） |
| [VERSIONING.md](./VERSIONING.md) | バージョン管理（SemVer・CHANGELOG・タグ） |
| [PUBLICATION.md](./PUBLICATION.md) | 公開（git 管理）と内部資産の区分 |
| [memory/INDEX.md](./memory/INDEX.md) | 記憶の索引（`MEMORY-TOOLS.md`・`TEMPLATE.md` 同梱） |

**設計（利用者が深掘りする場合）**: [design/INTENT-RECEIVER.md](./design/INTENT-RECEIVER.md)（常駐受信器・監査は [design/INTENT-RECEIVER-AUDIT.md](./design/INTENT-RECEIVER-AUDIT.md)）

## リポジトリ全体
- `README.md` … 概要・収録・クイックスタート
- `AGENTS.md` … エージェント契約（呼び出し規約・ガードレール）
- `mcp/README.md` … MCP サーバのツール・設定・セキュリティ
- `.kilo/skills/ATTRIBUTION.md` … スキルの出典とライセンス
- `LICENSES/` … ライセンス全文
- `CHANGELOG.md` / `VERSION` … 変更履歴・現在の版

メンテナ向け（git 外）: `./scripts/bootstrap-internal.sh` → `internal/`（詳細は [PUBLICATION.md](./PUBLICATION.md)）
