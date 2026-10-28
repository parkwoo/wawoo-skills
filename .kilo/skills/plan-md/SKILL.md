---
name: plan-md
description: Always save planning deliverables (fix plans, implementation plans, design direction, review responses) as a Markdown file. Use for tasks that create a plan or a fix/implementation/design plan.
---

# plan-md — a plan is always a Markdown file

Planning deliverables (fix plans, implementation plans, refactor plans, design direction, review-response plans, task breakdowns) must not end as a chat answer only: **always save them as a Markdown file**.

## Where to save

1. If the target repository has `docs/`, use `docs/`.
2. If you are inside a subdirectory, use the nearest `docs/` or the target folder.
3. If ambiguous, use the work root (e.g. `FIX-PLAN.md`, `IMPLEMENTATION-PLAN.md`).
4. If an equivalent plan already exists, prefer **updating the existing file** over creating a new one.

## Naming

- A descriptive ASCII name + `.md` (e.g. `FIX-PLAN.md`, `<feature>-design.md`).
- Include the saved path in the final report.

## Standard sections (adjust as needed)

- Title (`#`) and meta (scope, assumptions, status)
- Background / goal
- Current problem list (#, severity, location `file:line`, description)
- Approach (what stays / what changes)
- Steps (number, target file, change) grouped into phases
- Verification and done criteria
- Risks and rollback
- Execution order (review → approval → implement → verify)
- Change history

## Constraints

- Producing a plan does not change code (implement in a separate task after approval).
- Never write secrets (API keys, tokens, passwords, `.env` contents).
- Follow the project language policy (`AGENTS.md` §1): engineering records and responses use the working language; code, paths, commands, and identifiers stay verbatim.
