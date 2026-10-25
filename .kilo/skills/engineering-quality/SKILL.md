---
name: engineering-quality
description: Plan and implement software changes with explicit scope, evidence-based verification, safe migrations, and rollback readiness. Use for feature work, bug fixes, refactors, or implementation reviews; not for cloud-resource operations.
license: MIT
---

# Engineering Quality

Deliver a small, verifiable change that addresses the requested outcome without expanding scope.

## Workflow

1. Read applicable project instructions and inspect repository status before editing. Treat pre-existing changes as user-owned unless their purpose is known.
2. Establish the observable current behavior and the requested outcome. Locate the relevant code, tests, configuration, and data paths before proposing a fix. Identify assumptions, affected interfaces, data migrations, and compatibility risk.
3. Write a compact implementation plan with acceptance criteria before editing. Do not invent product requirements.
4. Prefer the smallest coherent change. Preserve existing user changes and avoid unrelated cleanup.
5. Add or update tests at the layer that proves the changed behavior. Run relevant lint, unit, integration, and build checks when available.
6. For non-trivial changes, use `change-readiness` before handoff. Report evidence: changed files, commands run, results, known limitations, and rollback path.

## Decision boundaries

- Stop for confirmation before destructive migrations, production changes, external messages, credential changes, or irreversible data actions.
- Treat a failing or unavailable test environment as a result to report, not as a passing verification.
- Keep secrets out of source, logs, commits, and generated artifacts.
- Do not use a broad revert, reset, or overwrite to remove changes that were not created for the current task.

## Completion criteria

The change meets stated acceptance criteria, has proportionate verification, and documents any unverified risk or required follow-up.
