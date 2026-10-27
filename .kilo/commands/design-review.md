---
description: UI の設計レビュー（design-review → web-design-guidelines → accessibility-audit）
agent: web-designer
---

# Design Review（UI）

> **入口**: `/design-review`（本 command）が入口。手順本体は同名 skill **`design-review`**（`.kilo/skills/design-review/SKILL.md`）。skill はモデルが選択するもので、`/` の入口は本 command に固定する。

2. **`design-review`**：ビジュアル監査 → 修正（before/after の証拠を残す）。
3. **`web-design-guidelines`**：レイアウト・タイポ・色・モーション・アクセシビリティの基準適合を確認。
4. **`accessibility-audit`**：キーボード・フォーカス・コントラスト・セマンティクス。
5. 報告：証拠（スクショ/diff）・未検証・リスク・次アクション。**承認ゲートを飛ばさない**。

## 対象
- 管理后台（`docs/design/30-ADMIN-DESIGN.md`）と API 仕様（`docs/design/12-API-SPEC.md`）の整合。
