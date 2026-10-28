---
name: screenshots-marketing
description: Produce marketing screenshots (landing hero, App Store, changelog visuals). Use Playwright when available; otherwise produce a capture checklist and reuse design-review evidence. Optional — not part of standard development workflows.
---

# Marketing Screenshots

> **Not part of the standard development flow.** Use only when needed.

## Default (no dependencies)

- Build a **capture plan**: target screens, states, resolution (desktop/mobile), annotations, and where each is used.
- **Reuse existing evidence**: before/after screenshots from `design-review` / `web-experience-design`.
- If you cannot capture, mark it **NOT CAPTURED** and leave manual capture steps.

## Playwright (optional)

- Only if Playwright is installed: `npx playwright screenshot <url> <out.png>`, etc.
- Do not force an install if it is missing (substitute a plan + existing evidence).

## Steps

1. Confirm the use (LP hero / store / CHANGELOG) and size.
2. Enumerate the target URLs/screens and states.
3. Capture (Playwright or manual) → save to `docs/screenshots/`.
4. Record annotations, sources, and capture date.

## Cautions

- Do not capture secrets, personal data, or unverified-license assets.
- Keep marketing exaggeration **separate from facts** (also when using `marketing-psychology`).
