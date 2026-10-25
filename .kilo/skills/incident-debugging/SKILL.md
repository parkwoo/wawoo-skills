---
name: incident-debugging
description: Diagnose a software incident or high-impact defect through reproduction, evidence collection, fault isolation, mitigation, verification, and follow-up. Use for outages, regressions, production errors, or urgent failures; not for routine feature planning.
license: MIT
---

# Incident Debugging

Stabilize first, then learn without guessing.

1. Record impact, affected users, timeline, current mitigation, owner, and safe communication channel.
2. Gather evidence from reproducible requests, logs, metrics, traces, versions, configuration, and recent changes. Preserve timestamps and avoid collecting secrets or unnecessary personal data.
3. Form competing hypotheses, test the least invasive one first, and isolate the fault from symptoms and unrelated noise.
4. Propose mitigation and permanent fix separately. Require approval for production changes, rollback, data repair, feature flags, or customer communication.
5. Verify recovery with observable signals, add regression coverage, and complete a brief post-incident PDCA record.

Report facts, confidence, unknowns, and next safe action at every handoff.
