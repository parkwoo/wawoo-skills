---
name: language-policy
description: Decide and enforce the writing language for code, engineering records, and explanatory docs via a three-tier policy (code = English; engineering records and responses = project working language; public explanatory docs = English primary + Japanese secondary). Use when adding files, writing docs, or reviewing i18n changes.
---

# Language Policy

Use this skill when choosing the language for code, documents, or responses in a project that adopts this kit. wawoo-skills uses a **three-tier** policy.

## Policy (three tiers)

| Target | Language |
|--------|----------|
| Code: comments, identifiers, strings, commit messages, config keys | **English** |
| Engineering records: `plans/`, `ACTIVE.md`, `RETRO-*`, `evidence/`, `memory/` — **and agent responses** | **Project working language** (wawoo-skills: Japanese) |
| Explanatory / user-facing docs: `README.md`, `docs/USAGE.md`, etc. | **English (primary) + Japanese (secondary)** — two files |

## Rules

- Keep **code and comments in English** even in non-English projects, so tools and contributors share one language for code. Never translate identifiers.
- Keep **engineering records and responses** in the project working language (wawoo-skills: Japanese).
- For **public explanatory docs**, ship both an **English primary** and a **Japanese secondary** version; keep headings, links, and structure equivalent (see `documentation-localization`).
- Never mix: do not write code comments in Japanese; do not write engineering records in English.
- Attribution: when translating a third-party asset, keep its original license/attribution (see `.kilo/skills/ATTRIBUTION.md`).

## Authority

The contract is authoritative: **`AGENTS.md` §1**. `ROUTER.md` restates it for routing.

## When to apply

- Deciding the language of a new file, comment, or document.
- Reviewing i18n changes for consistency.
