---
description: 市場調査 → 戦略 → 計画（research → research-decision-room → product-discovery → marketing-psychology → plan-md）。提案デッキは任意（`slides` は Markdown/HTML で利用可、pptx は任意）。
agent: market-researcher
---

# Market Plan（市場調査・事業計画）

> **標準フローは Ready のスキルのみ**。外部依存が必要なものは「任意」節に分離（`scripts/readiness.json`）。

2. **調査**：`research`（一次情報。**証拠と推測を分離**）。
3. **整理**：`research-decision-room`（証拠台帳・テーマ・確信度・機会・意思決定メモ）。
4. **製品化**：`product-discovery`（ユーザー成果・受入基準・スコープ・未決事項）。
5. **提示**：`marketing-psychology`（フレーミング/価格の見せ方）。
6. **文書化**：`plan-md` で計画を Markdown に保存。必要なら画像を `fal-gen`（`FAL_KEY`）で生成（未設定ならプレースホルダ＋出典）。
7. 報告：**証拠 / 推測 / 未検証**・意思決定の選択肢・次アクション。

## 任意（セットアップ後のみ）
- `competitive-ads-extractor`／`lead-research-assistant`：**Composio** 導入後。
- `slides`：**Markdown/HTML で利用可**（`/deck`）。`.pptx` は PptxGenJS 導入時のみ。

## ゲート
- **事業判断（価格・契約・法務・提携）は人が決める**。エージェントは選択肢と根拠のみ。
- 個人情報・秘密・**ライセンス未確認の第三者コンテンツ**を含めない（`compliance-legal` を参照）。
- 外部送信・公開・契約は**承認必須**。
