---
name: release-readiness
description: Prepare and review a software release for versioning, legal files, changelog accuracy, tags, release notes, deployment checks, and rollback. Use when publishing, tagging, shipping, or auditing a release; not for making production changes without approval.
license: MIT
---

# Release Readiness

Make releases reproducible, traceable, legally distributable, and reversible.

## Release checklist

1. Confirm the release scope, target commit, version scheme, supported compatibility range, and working-tree cleanliness.
2. Verify required distribution files: LICENSE, README, CHANGELOG or release notes, security-reporting guidance where appropriate, and package or manifest metadata.
3. Run the release-proportionate test suite and record the exact version of tools and artifacts used.
4. Ensure version identifiers agree across manifests, documentation, tags, and release notes. Never move or rewrite an already published tag.
5. Prepare a rollback procedure using the preceding immutable version, including configuration or data compatibility notes.
6. After an approved publication, verify the remote branch, immutable tag, release page or package, and downloadable artifact rather than relying on local Git state.

## Approval boundaries

- Do not push, tag, publish packages, create GitHub Releases, deploy, or alter production configuration without explicit user approval.
- Do not call a release complete when artifacts are only local or a remote push is unverified.

## Completion criteria

Produce a release checklist with passed checks, blocked items, artifact locations, version/tag, compatibility statement, and rollback instructions.

Before presenting the checklist for publication approval, use `change-readiness` to make verification gaps and external actions explicit.
