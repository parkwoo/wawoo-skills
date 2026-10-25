---
name: test-engineering
description: Design, implement, diagnose, and review software tests with evidence-focused coverage across unit, integration, and end-to-end layers. Use for test failures, regressions, new behavior, and test strategy; not as a substitute for implementing a requested product change.
license: MIT
---

# Test Engineering

Create tests that distinguish correct behavior from the specific regression or risk under examination.

## Workflow

1. State the behavior contract: inputs, outputs, side effects, failures, and invariants.
2. Select the lowest test layer that proves the contract. Add integration or end-to-end coverage when boundaries, rendering, persistence, authentication, or deployment wiring are the risk.
3. Make tests deterministic: control time, random values, network, credentials, and external state. Do not silently skip essential assertions.
4. When debugging, reproduce first, reduce to the smallest failing case, then identify whether the defect is in product code, test setup, or an external dependency.
5. Run the focused test first, then the relevant broader suite. Report exact commands and outcomes.
6. Classify each unrun, skipped, flaky, or environment-dependent check with its cause and the next action required to make it reliable.

## Quality rules

- Assert observable behavior, not private implementation details, unless the implementation itself is the contract.
- Cover success, expected failure, and the highest-risk boundary case.
- Do not weaken assertions or mark tests skipped merely to obtain green output.
- Separate environment-dependent smoke tests from deterministic CI tests and document their prerequisites.
- For a defect fix, make the test fail on the pre-fix behavior when practical; otherwise explain why direct regression proof is unavailable.

## Completion criteria

Each changed behavior has a clear test rationale, regression coverage where justified, and a truthful record of any tests that could not run.
