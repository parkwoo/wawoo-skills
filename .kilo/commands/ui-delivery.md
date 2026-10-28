---
description: Design, implement, and audit a web UI change across responsive and accessibility states.
agent: web-designer
replay: safe
---

# UI Delivery

**L1 SSOT**: `docs/plans/ACTIVE.md` (tasks) + `DESIGN.md` (`design-md`) if needed. Update ACTIVE at the exit and pass `python3 scripts/plan_active.py`.

1. Read `docs/plans/ACTIVE.md` and inspect the current UI, design tokens, primary user task, target viewports, and existing states.
2. Use `web-experience-design` to define hierarchy, content, interaction, desktop/mobile behavior, and non-goals.
3. **Only if images are needed**, generate **just what you need** with `fal-gen` (requires `FAL_KEY`; hero / illustration / background / texture / mobile screens). If unset, proceed with a **placeholder + source**. Save outputs under `docs/.../assets/` and confirm whether they should be committed.
4. Implement the smallest consistent UI change; retain semantic HTML and keyboard behavior.
5. Use `test-engineering`, `accessibility-audit`, and `performance-audit` as applicable.
6. Inspect rendered desktop/mobile states. Report evidence and explicitly list unavailable browsers, devices, states, or data.
7. Run `change-readiness` before handoff. Update ACTIVE (evidence = screenshots, audit results, PR). Do not replace brand assets, alter tracking, or publish without approval.
