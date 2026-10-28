---
description: Investigate and safely resolve an incident or urgent regression with evidence and follow-up.
agent: delivery-lead
replay: unsafe
---

# Incident Response

1. Use `incident-debugging` to capture impact, scope, timeline, current mitigation, owner, and evidence.
2. Reproduce or isolate the fault with the least invasive diagnostic path; state confidence and unknowns.
3. Separate immediate mitigation from permanent repair. Require explicit approval for production actions, rollback, data repair, feature flags, or external communication.
4. Implement and verify the approved repair with `test-engineering`; use security or performance review when relevant.
5. Complete `retro` with cause, evidence, prevention, owner, and next review point.
