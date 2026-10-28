---
name: privacy-review
description: Review personal data (PII) flows, minimization, retention, masking, logging, and cross-border handling for a feature or service. Use when a change touches user data, logs, analytics, or third parties. Human sign-off required for legal conclusions.
---

# Privacy Review

> **A human makes the legal call.** This skill is limited to **visualizing data flows and checking them**.

## 1. Data flow

- Enumerate the PII collected (account data, usage logs, prompt/response bodies).
- Note any third-party sharing or external transmission (upstream providers, analytics).

## 2. Checks

- **Minimization**: collect only what the purpose requires.
- **Retention**: period and deletion path (follow the consuming project's retention policy; avoid storing prompt/response bodies by default).
- **Masking**: never emit secrets/PII into logs or audit trails.
- **Consent/notice**: reflect in terms/policy when needed.
- **Cross-border**: storage region and legal requirements.

## 3. Output

- Data-flow diagram (text is fine), checklist results, **residual risk**, and points needing human judgment.
- If changes are needed, update the consuming project's security/privacy documents (e.g. `docs/security/`) and its terms/policy.

## 4. Related

- Legal: `compliance-legal` / Security: `security-review` / Release: `release-readiness`
