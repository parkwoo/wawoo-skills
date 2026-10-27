---
description: Deliver a feature through discovery, design, implementation, testing, review, and approval gates.
agent: delivery-lead
---

# Feature Delivery

L1 の通常依頼は `/delivery-lite` と `docs/plans/ACTIVE.md` を先に検討。本 workflow はゲート・探索・UI/セキュリティ境界が厚いとき。

1. Read project instructions and inspect repository status; preserve unrelated changes.
2. **Memory (entry)**: `memory_recall` or read `docs/memory/INDEX.md` for prior decisions, constraints, and gotchas (`memory` skill).
3. Use `product-discovery` to establish user outcome, acceptance criteria, scope, and open decisions.
4. Use `architecture-decision` when interfaces, data, dependencies, or significant tradeoffs change.
5. Delegate implementation and apply `engineering-quality`.
6. Use `test-engineering`; add `web-experience-design` and `accessibility-audit` for UI work, and `security-review` for sensitive boundaries.
7. Run `change-readiness` and report requested outcome, implementation, evidence, unverified items, risks, rollback, and approval required.
8. **Memory (exit)**: persist new decisions, constraints, or gotchas via `memory_save` or `docs/memory/` append (PROCESS P4 / D7).
9. Do not publish, deploy, push, tag, or perform external mutations unless explicitly approved.
