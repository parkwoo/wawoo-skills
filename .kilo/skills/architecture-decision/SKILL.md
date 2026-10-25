---
name: architecture-decision
description: Evaluate software architecture choices, dependencies, interfaces, constraints, and tradeoffs, then produce a concise decision record. Use before major features, integrations, migrations, or refactors; not for routine local code edits.
license: MIT
---

# Architecture Decision

Make a reversible, evidence-based design decision.

1. Inspect existing architecture, project instructions, ownership boundaries, runtime constraints, and operational data.
2. State the decision, drivers, non-goals, interfaces, data ownership, compatibility needs, and failure modes.
3. Compare realistic alternatives by complexity, security, performance, cost, operability, migration risk, and rollback.
4. Select the smallest option that meets the stated drivers. Record consequences and deferred work in an ADR-style note.
5. Define implementation stages, test strategy, migration/rollback plan, and approval boundaries.

Do not adopt a framework, service, or redesign solely because it is fashionable. Escalate decisions involving vendor contracts, production topology, irreversible data changes, or material cost.
