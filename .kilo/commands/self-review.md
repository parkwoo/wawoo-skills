---
description: Self-correction (code-review → code-skeptic → diagnosing-bugs/tdd → fix → verify)
agent: code-reviewer
replay: safe
---

# Self Review

1. Read `AGENTS.md` and recall `memory` (existing decisions, constraints, gotchas).
2. **`code-review`**: review the change from a fixed point along two axes (standards / spec).
3. **Critical review**: apply the viewpoint in `.kilo/agents/code-skeptic.md` to critically test assumptions, design, and tests (in Kilo you may delegate to `code-skeptic` via Task; **do not assume switching agents mid-command**).
4. **`diagnosing-bugs`**: if there is a defect or performance regression, find the cause (do not fix by guessing).
5. **`tdd` / `test-engineering`**: fix test-first. Add regressions.
6. Fix → **re-verify** (tests, lint, types). Keep evidence.
7. **`memory`**: save recurring gotchas and their avoidance.

## Gates

- Do not treat "it ran" as done (**state what is unverified**).
- Destructive changes, production, and deletions require approval.
- For security boundaries, also use `security-review`.
