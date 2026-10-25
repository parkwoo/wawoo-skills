---
name: compliance-legal
description: Review OSS license obligations (MIT/Apache-2.0 attribution, NOTICE), SBOM, and product/service legal checklists (terms, privacy, DPA, AI usage policy). Use before release or when introducing third-party assets. Not a substitute for legal advice.
---

# Compliance / Legal（法務・コンプライアンス）

> **法的判断は人が行う。** 本スキルは**証拠収集とチェックリスト**に限定し、最終判断・契約・規約の確定は**人間の承認**を必須とする。

## 1. OSS ライセンス／帰属
- 取り込んだ資産を棚卸し（`.kilo/skills/ATTRIBUTION.md`・`vendor/`）。
- **MIT / Apache-2.0** の義務を確認：
  - MIT：著作権表示・ライセンス文の同梱。
  - Apache-2.0：`LICENSE` 同梱・`NOTICE` 帰属・変更点の明示。
- **第三者由来（marketplace の business 系など）は個別ライセンス未確認**。再配布前に確認。
- **SBOM**（依存の一覧）を作成/更新（例：`pip freeze`・`docker sbom`）。

## 2. 製品/サービス法務チェックリスト
- **利用規約（ToS）**：対象・禁止事項・免責・変更手続き。
- **プライバシーポリシー**：収集項目・目的・保持期間・第三者提供・問い合わせ窓口。
- **DPA**（委託がある場合）：目的・安全管理・再委託・削除。
- **AI 利用ポリシー**：生成物の扱い・学習利用の有無・禁止用途・ログ。
- **記録**：版・承認者・日付・根拠。

## 3. 出力
- チェック結果（該当/非該当/要確認）と**証拠**（ファイル・版・出典）。
- **未確認・法的判断が必要**な点を明示（勝手に断定しない）。

## 4. 関連
- プライバシー：`privacy-review`
- セキュリティ：`security-review`
- リリース：`release-readiness`（版・法務ファイル）
- 本プロジェクトの帰属：`.kilo/skills/ATTRIBUTION.md`
