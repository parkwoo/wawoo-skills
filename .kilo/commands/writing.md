---
description: Creative/article writing (explore → beats → shape), optionally with magazine/blog layout; runs parallel to content-delivery-lite.
agent: docs-specialist
replay: safe
---

# Writing (article / blog / fiction draft)

**Goal**: turn raw ideas into a finished piece through **explore → structure → draft**, without losing the writer's material.

> Entry: `/writing`. The procedure SSOT is this command. The three writing skills are MIT (see `.kilo/skills/ATTRIBUTION.md`).

## When to use

- Blog posts, essays, columns, newsletters, fiction drafts, scripts (drafting), talk / stand-up material.
- For knowledge-heavy long-form with sources and chapter tracking, combine with `/content-delivery-lite` (CONTENT.md); `/writing` handles prose craft.

## Modes

- **general** (default): `writing-fragments` → `writing-beats` → `writing-shape`.
- **science / 科普**: add `science-writing` (audience, plain language, sources) before drafting; fact-check with `research`; use `teach` for a multi-session lesson.
- **viral / 人气**: add `viral-hooks` (title/hook/payoff) and `marketing-psychology` (framing); keep the ethics rules (no clickbait).

## Steps

1. (Optional) Track the piece in `docs/plans/CONTENT.md` (via `/content-delivery-lite`) when it is long or multi-chapter.
2. **Explore** — `writing-fragments`: mine raw fragments from the conversation into one Markdown file (no structure yet). Capture from the first message.
3. **Structure** — `writing-beats`: turn the fragment pile into a journey of beats; ground each term before a beat relies on it.
4. **Draft** — `writing-shape`: shape the material into the final article, paragraph by paragraph (do not edit the raw file).
5. (Optional) **Layout** — for an HTML presentation, use OpenDesign `article-magazine` / `blog-post` (Apache-2.0; if not present, produce Markdown).
6. **Review** — factual checks (`research`), tone, and web checks (`web-design-guidelines`). Mark unverified claims.
7. Save under `docs/` (or the project's content dir) and record evidence (file path, word count, review date).

## Gates

- Approval required before publishing / external transmission.
- Separate fact from inference; do not fabricate sources or quotes.
- Preserve third-party attribution for the writing skills (MIT).

## Related

- `/content-delivery-lite` — knowledge long-form, CONTENT.md, `plan_content.py`
- `/research` — factual grounding
