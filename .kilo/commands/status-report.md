---
description: Progress / status report (ACTIVE or triage/to-tickets → progress/risk → plan-md)
agent: project-manager
replay: safe
---

# Status Report

1. **SSOT**: for **L1**, read `docs/plans/ACTIVE.md`. For **L2**, use the issue tracker (`triage` / `to-tickets`). Never create a second progress table.
2. **`triage` / `to-tickets`** (for L2 or when unblocking): organize item status and blockers.
3. **Progress**: show done / in progress / delayed with **evidence** (PR, commit, test result, ACTIVE evidence column). Mark unconfirmed as unconfirmed.
4. **Risks and next actions**: list delay causes and decisions needing approval.
5. **`plan-md`**: save the status report as Markdown (period, metrics, next actions).
6. Report: **progress / risks / blockers / next approvals**.

## Gates

- Do not assert numbers or dates as fact (**distinguish measured from unverified**).
- Business decisions, contracts, and legal are made by humans.
- Destructive changes, production, and deletions require approval.
