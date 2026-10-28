---
name: publication-boundary
description: Keep internal development materials out of the public tree of an open-source repo. Use when adding docs or scripts, or auditing what gets published. Defines what is public vs internal and how to check.
---

# Publication Boundary

This repository is an open-source kit. Keep **only consumer-facing assets** in the public tree; keep **development-process materials** internal (not published).

## Public vs internal

**Public** (published): `README.md`, `AGENTS.md`, `docs/USAGE.md`, `docs/INTENT-ROUTING.md`, `docs/VERSIONING.md`, templates (`docs/plans/*.example.md`, `docs/memory/{TEMPLATE,MEMORY-TOOLS,INDEX.example}.md`), `.kilo/`, `.cursor/`, `mcp/`, `scripts/` (kit tooling), `LICENSE(S)`, `NOTICE`, `SECURITY.md`, `CHANGELOG.md`, `VERSION`.

**Internal** (not published — keep under `internal/`, git-ignored): research/analysis notes, audits (`*-AUDIT.md`), `RETRO-*`, `self-improve-*`, E2E evidence, publishing drafts, design/process docs (`METHODOLOGY.md`, `PROCESS-PHILOSOPHY.md`, `PUBLICATION.md`, `docs/README.md`, `design/INTENT-RECEIVER.md`), and this repo's own `docs/plans/ACTIVE.md` and `docs/memory/*` content.

## Check

`python3 scripts/validate_assets.py` fails when internal dev materials are tracked in the public tree (see `INTERNAL_PUBLIC_PATTERNS`). Full policy: `internal/docs/PUBLICATION.md` (non-public).

## Rules

- Planning docs and tests stay internal / non-public.
- Do not track `internal/`, `data/*.db`, the live `ACTIVE.md` / `CONTENT.md`, `docs/memory` content (templates excepted), audits, retros, or blog drafts.
- Never commit secrets. Never redistribute unverified-license assets.
