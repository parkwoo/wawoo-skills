---
description: Design, implement, and audit a web UI change across responsive and accessibility states.
agent: web-designer
---

# UI Delivery

1. Inspect the current UI, design tokens, primary user task, target viewports, and existing states.
2. Use `web-experience-design` to define hierarchy, content, interaction, desktop/mobile behavior, and non-goals.
3. **画像が必要な場合のみ** `fal-gen`（`FAL_KEY` 必要）で**必要分だけ**生成（hero／挿絵／背景／テクスチャ／モバイル画面）。未設定なら**プレースホルダ＋出典**で進める。生成物は `docs/.../assets/` に保存し、コミット可否を確認。
4. Implement the smallest consistent UI change; retain semantic HTML and keyboard behavior.
5. Use `test-engineering`, `accessibility-audit`, and `performance-audit` as applicable.
6. Inspect rendered desktop/mobile states. Report evidence and explicitly list unavailable browsers, devices, states, or data.
7. Run `change-readiness` before handoff. Do not replace brand assets, alter tracking, or publish without approval.
