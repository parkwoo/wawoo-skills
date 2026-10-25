---
name: database-change-safety
description: Plan, implement, and review schema changes, data migrations, backfills, and cleanup with integrity, availability, observability, and rollback safeguards. Use whenever persistent data shape or meaning changes; not for read-only queries.
license: MIT
---

# Database Change Safety

Treat data changes as staged, observable operations.

1. Identify affected tables, records, constraints, indexes, data volume, readers/writers, retention needs, and current production behavior.
2. Prefer expand-migrate-contract: add compatible structure, backfill in bounded batches, switch readers/writers, verify, then remove legacy paths only after approval.
3. Define validation counts, sample checks, error handling, resume behavior, rate limits, monitoring, and a tested rollback or forward-fix path.
4. Make migrations idempotent where practical. Avoid long locks, unbounded transactions, and destructive rewrites in a single step.
5. Separate dry-run, staging, and production execution. Require explicit approval before production migrations, backfills, deletion, or irreversible cleanup.

Handoff must state data impact, verification evidence, residual risk, and recovery steps.
