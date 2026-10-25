---
name: change-readiness
description: Perform an evidence-based pre-handoff review of a non-trivial software change before requesting human or external audit. Use after implementation and verification, or when preparing a pull request, release, or review report; not for approving production changes.
license: MIT
---

# Change Readiness（引渡し前レビュー）

Prepare a review package that lets another engineer audit the change without rediscovering basic facts.

## Review sequence

1. Restate the requested outcome and map each acceptance criterion to changed code, configuration, tests, or documentation.
2. Inspect the working-tree diff and status. Identify unrelated changes, generated files, untracked artifacts, credentials, migrations, and compatibility-sensitive edits. Do not remove user-owned changes.
3. Verify behavior proportionately: focused regression checks first, then relevant broader tests, builds, lint, type checks, or UI/API smoke checks.
4. Review risk boundaries: authentication and authorization, input validation, data loss, concurrency, external APIs, performance-sensitive paths, accessibility, localization, and operational rollback where relevant.
5. Reconcile documentation, configuration examples, versions, manifests, and release notes with the implementation.

For a non-trivial UI change, use `web-experience-design` and include rendered desktop/mobile evidence plus unverified interaction states in the handoff.

## Handoff report

Use these exact sections:

- **Requested outcome** — concise acceptance criteria.
- **Implementation** — changed files and why each change is necessary.
- **Verification evidence** — commands, observable results, and scope of each check.
- **Not verified / blocked** — exact reason, impact, and required next action.
- **Risk and rollback** — remaining risks, compatibility notes, and how to revert safely.
- **Approval required** — any external, production, financial, destructive, or publication action still awaiting user approval.

## Rules

- Do not present skipped tests, unavailable environments, or inferred behavior as verified.
- Do not claim a remote push, release, deployment, or public page is complete without checking the remote result.
- Findings are review evidence, not authorization to change production or external systems.

## Completion criteria

The reviewer can trace every requirement to evidence, identify all unverified areas, and understand the safe next action without guessing.
