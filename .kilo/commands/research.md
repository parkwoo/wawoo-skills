---
description: Research → decision (research → product-discovery → to-spec/to-tickets)
agent: product-owner
replay: safe
---

# Research

> **Entry**: `/research` (this command) is the entry. The procedure body is the skill of the same name, **`research`** (`.kilo/skills/research/SKILL.md`). Skills are model-selected; the `/` entry is fixed to this command.

**L1**: put research task rows in `docs/plans/ACTIVE.md` (done = evidence, i.e. a link into `docs/`). **L2**: use an issue / BACKLOG.

1. Read `docs/plans/ACTIVE.md` and add the research task as `todo` (a small check may skip this at L0).
2. **`research`**: use primary sources and **separate fact from inference**, recording findings in Markdown (do not fabricate certainty).
3. **`research-decision-room`** (if needed): structure options, rationale, and risks into decision material.
4. **`product-discovery`**: settle user outcome, acceptance criteria, scope, and open questions.
5. As needed, use **`to-spec`** / **`to-tickets`** to specify and ticket (and **`plan-md`** to write the plan).
6. Set ACTIVE to `done` + evidence. Verify with `python3 scripts/plan_active.py`.
7. Report: distinguish **evidence / inference / unverified**, and state the decision and next actions.

## Cautions

- Business decisions (pricing, contracts, legal) are **made by humans**. Agents present options and rationale only.
- If you keep findings in `docs/`, do not include secrets (personal data, keys).
