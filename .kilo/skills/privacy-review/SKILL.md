---
name: privacy-review
description: Review personal data (PII) flows, minimization, retention, masking, logging, and cross-border handling for a feature or service. Use when a change touches user data, logs, analytics, or third parties. Human sign-off required for legal conclusions.
---

# Privacy Review（プライバシー）

> **法的判断は人が行う。** 本スキルは**データフローの可視化とチェック**に限定する。

## 1. データフロー
- 収集する PII（アカウント・利用ログ・プロンプト/レスポンス本文）を列挙。
- 第三者提供・外部送信（上流プロバイダ・分析）の有無。

## 2. チェック
- **最小化**：目的に必要な項目のみ。
- **保持**：期間・削除手段（既定で本文を保存しない＝`design/60` §7.4）。
- **マスキング**：ログ・監査に秘密/PII を出さない（`audit_log` は秘密非記録）。
- **同意/通知**：必要なら利用規約・ポリシーに反映。
- **越境**：保管リージョンと法的要件。

## 3. 出力
- データフロー図（テキスト可）・チェック結果・**残存リスク**・要人間判断。
- 変更が必要なら `docs/design/60-SECURITY-OPS.md` と規約/ポリシーを更新。

## 4. 関連
- 法務：`compliance-legal`／セキュリティ：`security-review`／リリース：`release-readiness`
