# スキル品質レビュー（機械スキャン + 法務・セキュリティ深掘り）

> 生成: `python3 scripts/audit_skill_quality.py`（2026-10-25）

## スコープ
- 55 skill の `SKILL.md` をサイズ・ゲート語・手順構造・壊れやすい内部参照でスキャン。
- 法務・セキュリティ系 6 件は**実効性**を人が追記評価。

## サマリ
| 指標 | 値 |
|---|---|
| skill 数 | 55 |
| 予算超過（>4KB、入口 SKILL のみ） | 15 |
| 法務/セキュリティでゲート語なし | 0 |

## 予算超過（入口 SKILL.md）

| skill | bytes | 備考 |
|---|---:|---|
| `design-brief` | 13805 | ルーター/長文 — 段階的開示を推奨 |
| `ask-matt` | 12594 | ルーター/長文 — 段階的開示を推奨 |
| `wayfinder` | 12380 | ルーター/長文 — 段階的開示を推奨 |
| `writing-for-agents` | 10886 | ルーター/長文 — 段階的開示を推奨 |
| `diagnosing-bugs` | 8664 | ルーター/長文 — 段階的開示を推奨 |
| `setup-matt-pocock-skills` | 6978 | ルーター/長文 — 段階的開示を推奨 |
| `code-review` | 6670 | ルーター/長文 — 段階的開示を推奨 |
| `triage` | 6558 | ルーター/長文 — 段階的開示を推奨 |
| `codebase-design` | 6446 | ルーター/長文 — 段階的開示を推奨 |
| `research-decision-room` | 6286 | ルーター/長文 — 段階的開示を推奨 |
| `to-tickets` | 5812 | ルーター/長文 — 段階的開示を推奨 |
| `reference-design-contract` | 5366 | ルーター/長文 — 段階的開示を推奨 |
| `frontend-design` | 5240 | ルーター/長文 — 段階的開示を推奨 |
| `retro` | 4369 | ルーター/長文 — 段階的開示を推奨 |
| `pr` | 4169 | ルーター/長文 — 段階的開示を推奨 |

## 全 skill 一覧

| skill | bytes | ゲート語 | 手順構造 | 要確認 |
|---|---:|:---:|:---:|---|
| `accessibility-audit` | 1277 | — | — | — |
| `api-contract-design` | 1160 | — | — | — |
| `architecture-decision` | 1142 | ✅ | — | — |
| `ask-matt` | 12594 | — | ✅ | — |
| `brand-guidelines` | 1384 | — | — | — |
| `change-readiness` | 2501 | ✅ | — | — |
| `changelog` | 1251 | ✅ | ✅ | — |
| `code-review` | 6670 | — | — | — |
| `codebase-design` | 6446 | — | ✅ | — |
| `compliance-legal` | 1982 | ✅ | ✅ | — |
| `database-change-safety` | 1214 | ✅ | — | — |
| `dependency-upgrade` | 1222 | — | — | — |
| `deployment` | 1339 | ✅ | ✅ | — |
| `design-brief` | 13805 | — | ✅ | — |
| `design-md` | 1174 | — | — | — |
| `design-review` | 1204 | — | — | — |
| `diagnosing-bugs` | 8664 | — | ✅ | — |
| `documentation-localization` | 1730 | — | — | — |
| `domain-modeling` | 3346 | — | ✅ | — |
| `engineering-quality` | 1959 | — | — | — |
| `frontend-design` | 5240 | — | — | — |
| `grill-with-docs` | 247 | — | — | — |
| `grilling` | 2049 | — | — | — |
| `handoff` | 940 | — | — | — |
| `imagegen-frontend-mobile` | 2591 | ✅ | ✅ | — |
| `implement` | 622 | — | — | — |
| `implement-spec` | 2780 | — | — | — |
| `incident-debugging` | 1154 | ✅ | — | — |
| `marketing-psychology` | 1266 | — | — | — |
| `memory` | 1399 | — | — | — |
| `pdca-cycle` | 1608 | ✅ | — | — |
| `performance-audit` | 1174 | ✅ | — | — |
| `plan-md` | 1901 | ✅ | — | — |
| `pr` | 4169 | — | — | — |
| `privacy-review` | 1526 | ✅ | ✅ | — |
| `product-discovery` | 1076 | — | — | — |
| `prototype` | 2931 | — | ✅ | — |
| `reference-design-contract` | 5366 | — | ✅ | — |
| `release-readiness` | 1826 | ✅ | — | — |
| `research` | 794 | — | — | — |
| `research-decision-room` | 6286 | — | — | — |
| `retro` | 4369 | — | — | — |
| `screenshots-marketing` | 1373 | — | ✅ | — |
| `security-review` | 1229 | ✅ | ✅ | — |
| `setup-matt-pocock-skills` | 6978 | — | — | — |
| `slides` | 1629 | — | ✅ | — |
| `tdd` | 3629 | — | — | — |
| `test-engineering` | 1987 | — | — | — |
| `to-spec` | 3043 | — | — | — |
| `to-tickets` | 5812 | — | — | — |
| `triage` | 6558 | — | ✅ | — |
| `wayfinder` | 12380 | — | ✅ | — |
| `web-design-guidelines` | 2418 | — | — | — |
| `web-experience-design` | 3533 | ✅ | — | — |
| `writing-for-agents` | 10886 | — | ✅ | — |

## 法務・セキュリティスキルの実効性（人レビュー）

### `compliance-legal`
- **強み**: OSS 帰属・SBOM・ToS/プライバシー/DPA/AI ポリシーのチェックリスト。人の承認を明記。
- **弱み**: プロダクト固有の規制（業種・地域）はスコープ外。証拠の保存先テンプレは無い。
- **実効性**: **中〜高**（リリース前の棚卸しゲートとして機能。最終判断は人）。

### `privacy-review`
- **強み**: PII フロー・最小化・保持・マスキング・越境の観点。
- **弱み**: `docs/design/60-SECURITY-OPS.md` 等**本キットに無いパス**を参照（汎用リポジトリではリンク切れ）。
- **実効性**: **中**（チェックは使えるが、消費側でセキュリティ文書パスを差し替える必要）。

### `security-review`
- **強み**: 信頼境界・認証認可・注入・秘密・依存のレビュー手順。本番変更・PoC 禁止。
- **弱み**: 出力フォーマット（重大度テンプレ）が短い。自動スキャンツール連携は無い。
- **実効性**: **中〜高**（コードレビュー補助として妥当）。

### `release-readiness`
- **強み**: 版・タグ・ロールバック・承認境界が明確。`change-readiness` 連携。
- **弱み**: CI/パッケージ種別ごとの具体コマンドは消費側依存。
- **実効性**: **高**（本リポジトリの `VERSIONING.md` と整合）。

### `change-readiness` / `database-change-safety`
- **強み**: 変更種別ごとの検証・ロールバック意識。
- **弱み**: 本番 DB の組織ポリシーは記載不能（汎用キットの限界）。
- **実効性**: **中**（チェックリスト起動用）。

## Kilo 実機 E2E

| 項目 | 結果 |
|---|---|
| Kilo CLI / Kilo Code の実行 | **未実施**（この環境に `kilo` コマンドなし） |
| MCP stdio スモーク | **合格**（`python3 mcp/test_server.py`） |
| 推奨手動 E2E | 1) 本 repo を Kilo で開く 2) `/feature-delivery` 3) MCP `skill_search`→`skill_get` 4) `memory_save` 拒否テスト |

## 改善 backlog（優先）
1. `privacy-review` の設計パスをプレースホルダ（`docs/security/` 等）に一般化。
2. 予算超過 skill の `references/` 分割（`ask-matt`・`wayfinder` 等）。
3. `security-review` に findings テンプレ（重大度・再現・修正・検証）を追加。
