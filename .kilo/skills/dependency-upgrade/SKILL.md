---
name: dependency-upgrade
description: Safely evaluate, apply, and verify software dependency, runtime, container-image, or toolchain upgrades with compatibility, security, lockfile, rollout, and rollback controls. Use for version upgrades or vulnerability remediation; not for unrelated refactoring.
license: MIT
---

# Dependency Upgrade

Upgrade deliberately, one compatibility boundary at a time.

1. Identify current and target versions, transitive changes, support status, vulnerability context, runtime requirements, licenses, and affected environments.
2. Read primary release notes and migration guidance. Separate security urgency from optional feature upgrades.
3. Change manifests and lockfiles together using the project's supported tooling. Do not hand-edit generated lock data unless the tool requires it.
4. Run focused compatibility checks, relevant test/build suites, and smoke tests. Inspect changed dependency graph and generated artifacts.
5. Define staged rollout, monitoring, known incompatibilities, and rollback to the prior locked version or image digest.

Do not update every dependency opportunistically. Escalate before accepting a new license, major runtime change, or production rollout.
