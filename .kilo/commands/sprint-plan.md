---
description: Sprint planning L2 (wayfinder → to-tickets → priority/estimate/capacity → plan-md)
agent: project-manager
replay: safe
---

# Sprint Plan

**L2**: the progress SSOT is the **issue tracker** (when unset, a local copy in the `docs/plans/BACKLOG.example.md` format validated by `plan_l2_backlog.py`). **Do not make `ACTIVE.md` a second progress table.**

1. **Readiness**: check `scripts/readiness.json` for `to-tickets` / `triage` availability. If unset, stop creating issues and switch to the local backlog flow.
2. **`wayfinder`**: turn the large work into a map of **decision tickets** (scope, dependencies, open items).
3. **`to-tickets`** (when possible): break into tracer-bullet tickets (state the blocking edges).
4. **Priority / estimate / capacity**: priority, estimates (**separate inference from basis**), team capacity, scope adjustment.
5. **`plan-md`**: save the sprint plan as Markdown (in scope, out of scope, risks, acceptance).
6. Update the backlog table and ensure `python3 scripts/plan_l2_backlog.py <path>` passes (**Gₑ**).
7. Report: plan, assumptions, risks, and **decisions needing approval**.

## Gates

- **Scope and schedule are business decisions made by humans.**
- Destructive changes, production, and external transmission require approval.
