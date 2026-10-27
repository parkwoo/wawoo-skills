---
description: Design, implement, and audit a web UI change across responsive and accessibility states.
agent: web-designer
---

# UI Delivery

**L1 SSOT**: `docs/plans/ACTIVE.md`（タスク）＋必要なら `DESIGN.md`（`design-md`）。出口で ACTIVE を更新し `python3 scripts/plan_active.py` を通す。

1. Read `docs/plans/ACTIVE.md` and inspect the current UI, design tokens, primary user task, target viewports, and existing states.
2. Use `web-experience-design` to define hierarchy, content, interaction, desktop/mobile behavior, and non-goals.
3. **画像が必要な場合のみ** `fal-gen`（`FAL_KEY` 必要）で**必要分だけ**生成（hero／挿絵／背景／テクスチャ／モバイル画面）。未設定なら**プレースホルダ＋出典**で進める。生成物は `docs/.../assets/` に保存し、コミット可否を確認。
4. Implement the smallest consistent UI change; retain semantic HTML and keyboard behavior.
5. Use `test-engineering`, `accessibility-audit`, and `performance-audit` as applicable.
6. Inspect rendered desktop/mobile states. Report evidence and explicitly list unavailable browsers, devices, states, or data.
7. Run `change-readiness` before handoff. Update ACTIVE（証拠＝スクショ・audit 結果・PR）。Do not replace brand assets, alter tracking, or publish without approval.
