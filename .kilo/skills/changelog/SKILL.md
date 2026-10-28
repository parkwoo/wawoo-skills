---
name: changelog
description: Generate and maintain user-facing changelog/release notes from git history (Conventional Commits) and keep version/tags consistent. Use before a release or when preparing a PR. Complements release-readiness; does not publish anything.
---

# Changelog / Version

## Prerequisites

- `release-readiness` verifies the version, legal files, and tags. This skill owns **generating the change history**.
- **Publishing, tagging, and pushing happen after approval** (`/release-review`).

## Steps

1. Choose the range: `git log <base>..HEAD --oneline` (previous tag → HEAD).
2. **Classify** (Conventional Commits recommended):
   - `feat` (new), `fix`, `perf`, `refactor`, `docs`, `chore`, `BREAKING CHANGE`.
   - Rewrite into user-facing wording (do not paste raw technical commits).
3. Update `CHANGELOG.md` (version, date, sections, PR links).
4. **Version**: SemVer (`MAJOR.MINOR.PATCH`). Breaking changes are MAJOR.
5. Draft the **tag / release notes** (publish after approval).
6. Evidence: show the range, commits, classification, and version rationale.

## Cautions

- Never put secrets, personal data, or internal URLs in the changelog.
