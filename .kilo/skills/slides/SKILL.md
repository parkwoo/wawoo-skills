---
name: slides
description: Create slide decks as Markdown/HTML by default (no external dependencies); optionally export .pptx with PptxGenJS if installed. Use for plans, proposals, and kickoff decks. Optional — not part of standard development workflows.
---

# Slides (plan / proposal decks)

> **Not part of the standard development flow.** Use only when explicitly invoked (e.g. via `/deck`).

## Default (no dependencies · recommended)

- **Markdown**: `docs/decks/<name>.md`, structured as "one slide = one message".
  - Each slide: `## Title` + body + "talking points".
- Convert to **self-contained HTML** (`<section>` slides) if needed.
- Mark figures with placeholders + **sources**.

## Optional (PptxGenJS)

- Generate `.pptx` **only if `pptxgenjs` is installed** (`npx pptxgenjs`, etc.).
- If not installed, **deliver Markdown/HTML** (do not force pptx).

## Steps

1. Confirm purpose, audience, time, and **the decision you want**.
2. Outline (10–15 slides) → one message per slide.
3. State facts and **sources** (evidence from `research` / `research-decision-room`). Label inference as inference.
4. Generate → review with `design-review` / `web-design-guidelines` if needed.
5. Save to `docs/decks/` (Markdown/HTML), optionally `.pptx`.

## Cautions

- Do not use secrets, personal data, or **unverified-license assets** (`compliance-legal`).
- Business decisions, pricing, and contracts are **made by humans**. A deck only presents options and rationale.
