---
name: slides
description: Create slide decks as Markdown/HTML by default (no external dependencies); optionally export .pptx with PptxGenJS if installed. Use for plans, proposals, and kickoff decks. Optional — not part of standard development workflows.
---

# Slides（提案・計画デッキ）

> **標準の開発フローには含めない**。`/deck` などで明示的に呼ぶときだけ使う。

## 既定（依存なし・推奨）
- **Markdown**：`docs/decks/<name>.md` に「1 スライド＝1 メッセージ」で構成。
  - 各スライド：`## タイトル`＋本文＋「話すポイント」。
- 必要なら**自己完結 HTML**（`<section>` スライド）に変換。
- 図表はプレースホルダ＋**出典**を明記。

## 任意（PptxGenJS）
- `pptxgenjs` が**導入済みの場合のみ** `.pptx` を生成（`npx pptxgenjs` 等）。
- 未導入なら**Markdown/HTML で納品**（pptx を無理に作らない）。

## 手順
1. 目的・聴衆・持ち時間・**意思決定してほしいこと**を確認。
2. アウトライン（10〜15 枚）→ 1 枚 1 メッセージ。
3. 事実と**出典**（`research`／`research-decision-room` の証拠）を明記。推測は推測と書く。
4. 生成 → 必要なら `design-review`／`web-design-guidelines` で見直し。
5. 保存：`docs/decks/`（Markdown/HTML）／任意で `.pptx`。

## 注意
- 秘密・個人情報・**ライセンス未確認の素材**を使わない（`compliance-legal`）。
- 事業判断・価格・契約は**人が決める**。デッキは選択肢と根拠を示すに留める。
