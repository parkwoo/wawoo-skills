---
name: performance-audit
description: Measure and improve application or web performance using representative workloads, bottleneck evidence, and regression safeguards. Use for slow pages, APIs, builds, queries, or capacity concerns; not for claiming performance gains without measurement.
license: MIT
---

# Performance Audit

Measure before and after; optimize the limiting path, not a guess.

1. Define the user-visible or operational metric, workload, device/environment, baseline, budget, and percentile or variance where applicable.
2. Inspect critical path work: network, images, fonts, JavaScript, rendering, cache, server latency, database queries, serialization, and external calls as relevant.
3. Identify bottlenecks with profiling, traces, query plans, browser tooling, or reproducible measurement. Prefer a small change with measurable impact.
4. Check correctness, accessibility, cost, cache invalidation, observability, and cold/warm behavior after optimization.
5. Record before/after evidence and a regression guard such as a test, budget, alert, or dashboard.

Do not use production load tests or traffic-generating actions without explicit approval.
