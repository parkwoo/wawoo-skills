---
description: Market research → strategy → plan (research → research-decision-room → product-discovery → marketing-psychology → plan-md). Proposal decks optional (`slides` via Markdown/HTML; pptx optional).
agent: market-researcher
replay: safe
---

# Market Plan (market research / business plan)

> **The standard flow uses only Ready skills.** Items needing external dependencies are separated into the "Optional" section (`scripts/readiness.json`).

**L1 SSOT**: `docs/plans/ACTIVE.md` (milestone rows) + `plan-md` artifacts. For long-form only, `/content-delivery-lite` + `CONTENT.md` also works.

1. Add the planning task to `docs/plans/ACTIVE.md` (an L0 one-off Q&A may skip this).
2. **Research**: `research` (primary sources; **separate evidence from inference**).
3. **Synthesize**: `research-decision-room` (evidence ledger, themes, confidence, opportunities, decision memo).
4. **Productize**: `product-discovery` (user outcome, acceptance criteria, scope, open questions).
5. **Present**: `marketing-psychology` (framing / how pricing is shown).
6. **Document**: save the plan as Markdown with `plan-md`. Generate images with `fal-gen` (`FAL_KEY`) if needed (otherwise a placeholder + source).
7. Update ACTIVE and run `python3 scripts/plan_active.py`.
8. Report: **evidence / inference / unverified**, decision options, and next actions.

## Optional (after setup only)

- `competitive-ads-extractor` / `lead-research-assistant`: after **Composio** is set up.
- `slides`: usable via **Markdown/HTML** (`/deck`). `.pptx` only when PptxGenJS is installed.

## Gates

- **Business decisions (pricing, contracts, legal, partnerships) are made by humans.** Agents provide options and rationale only.
- Do not include personal data, secrets, or **unverified-license third-party content** (see `compliance-legal`).
- External transmission, publishing, and contracts **require approval**.
