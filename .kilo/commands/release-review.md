---
description: Prepare a release-review package with legal/compliance, privacy, version, security, test, artifact, remote, and rollback evidence before publication approval.
agent: release-manager
---

# Release Review

1. Use `release-readiness` to inspect working tree, version, compatibility, LICENSE, README, changelog/release notes, manifests, tests, and rollback.
2. **Legal/compliance gate**：use `compliance-legal`（OSS ライセンス/NOTICE/SBOM・規約/プライバシー/DPA のチェック）and `privacy-review`（PII・保持・マスキング）。**法的判断は人間の承認**。
3. Use `security-review` for security boundaries and `documentation-localization` for public/multilingual release documentation.
   - **委譲の効率**: 監査を `security-reviewer` 等へ `Task` 委譲するときは、必要な skill の要点を**タスク文に内联**し、子に同じ skill を `skill_get` で再取得させない。子は read-only（shell は read-only サブセット）で、`read` は行範囲に絞る。
4. Run `change-readiness` and provide verified versus unverified remote state.
5. Present the release package for explicit approval. Do not push, tag, publish, deploy, or create a GitHub Release before that approval.
