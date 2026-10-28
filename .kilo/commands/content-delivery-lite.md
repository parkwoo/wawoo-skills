---
description: L1 knowledge delivery — books, long docs, reports via CONTENT.md state machine (not code implement).
agent: docs-specialist
replay: safe
---

# Content Delivery Lite (knowledge / long-form delivery)

**Goal**: manage **non-code** deliverables (research reports, business plans, book chapters) in `docs/plans/CONTENT.md`. The knowledge variant of `/delivery-lite`.


> **Creative prose in parallel**: for fiction, essays, or scripts, pair this with `/writing` (explore → beats → shape). `CONTENT.md` tracks chapters/progress; `/writing` handles prose craft. The two can run together on the same piece.

## Applicability

- **L1 (default)**: this workflow + `CONTENT.md`
- **L0**: single section or memo → SSOT update may be skipped (user says "L0")
- **Strategy / market**: for larger work, enter via `/market-plan` or `/research` and link results with `plan-md` + a CONTENT row
- **L2/L3**: `/sprint-plan`, `/self-improve` (process only)

## Steps

1. Read `AGENTS.md` §3 and `docs/plans/CONTENT.md` (if absent, copy `CONTENT.example.md`).
2. **Memory (entry)**: only when touching constraints, use `memory_recall` or `docs/memory/INDEX.md`.
3. **Outline**: add chapters/sections to the CONTENT table as `todo`. Structure can also live in `docs/plans/<id>-outline.md` via `plan-md`.
4. **Write**: keep exactly one `doing`; use `writing-for-agents` / `documentation-localization` as needed.
5. **Verify**: `python3 scripts/plan_content.py docs/plans/CONTENT.md`. For kit changes, `python3 scripts/e2e_flows.py`.
6. **Complete**: `done` + evidence (draft path, word count, review date). Memory holds **decisions and style rules** only.
7. **Commit**: only when the user explicitly asks.

## Output

- Updated `CONTENT.md` and draft files
- Chat carries the summary only

## Gates

- **Gₐ**: get approval for publishing, contracts, or third-party asset rights.
- **Gₑ**: no `done` without evidence (`plan_content.py`).
- **Gₒ**: separate fact from inference (same as `/research` for research work).
