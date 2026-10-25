---
name: screenshots-marketing
description: Produce marketing screenshots (landing hero, App Store, changelog visuals). Use Playwright when available; otherwise produce a capture checklist and reuse design-review evidence. Optional — not part of standard development workflows.
---

# Marketing Screenshots

> **標準の開発フローには含めない**。必要時のみ使う。

## 既定（依存なし）
- **撮影計画**を作る：対象画面・状態・解像度（desktop/mobile）・注釈・使用先。
- **既存の証拠**を再利用：`design-review`／`web-experience-design` の before/after スクショ。
- 取得できない場合は「**未取得**」と明記し、手動撮影の手順を残す。

## Playwright（任意）
- Playwright が導入済みの場合のみ：`npx playwright screenshot <url> <out.png>` 等。
- 未導入でも**無理に導入しない**（計画＋既存証拠で代替）。

## 手順
1. 用途（LP hero／ストア／CHANGELOG）とサイズを確認。
2. 対象 URL／画面と状態を列挙。
3. 取得（Playwright or 手動）→ `docs/screenshots/` に保存。
4. 注釈・出典・取得日を記録。

## 注意
- 秘密・個人情報・ライセンス未確認の素材を写さない。
- マーケ用の誇張表現は**事実と分離**（`marketing-psychology` 使用時も同様）。
