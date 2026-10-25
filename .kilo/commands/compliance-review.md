---
description: 法務・プライバシー・セキュリティのゲート（compliance-legal → privacy-review → security-review → release-readiness）
agent: compliance-reviewer
---

# Compliance Review（法務・プライバシー・セキュリティ）

> **法的判断は人が行う。** 本ワークフローは**証拠とチェックリスト**を揃え、**人間の承認**を必須にする。

2. **`compliance-legal`**：
   - OSS ライセンス（MIT/Apache-2.0 の LICENSE・NOTICE 帰属）と **SBOM**。
   - 利用規約・プライバシーポリシー・DPA・AI 利用ポリシーのチェックリスト。
3. **`privacy-review`**：PII の流れ・最小化・保持・マスキング・越境。
4. **`security-review`**：境界（認証・SSRF・秘密・テナント分離）。
5. **`release-readiness`**：版・法務ファイル・CHANGELOG・ロールバック。
6. 出力：**該当/非該当/要確認**・証拠（パス/版/出典）・残存リスク・**必要な人間承認**。
7. **承認なしに**公開・契約・規約変更・本番反映をしない。

## 既知の注意
- 本プロジェクトは MIT/Apache-2.0 の資産を利用（`.kilo/skills/ATTRIBUTION.md`）。**Marketplace の business 系は第三者ソースで個別ライセンス未確認**。
- 設計上の PII 方針：`docs/design/60-SECURITY-OPS.md` §7.4（既定で本文を保存しない）。
