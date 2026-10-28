---
name: compliance-legal
description: Review OSS license obligations (MIT/Apache-2.0 attribution, NOTICE), SBOM, and product/service legal checklists (terms, privacy, DPA, AI usage policy). Use before release or when introducing third-party assets. Not a substitute for legal advice.
---

# Compliance / Legal

> **A human makes the legal call.** This skill is limited to **evidence gathering and checklists**; final decisions, contracts, and terms require **human approval**.

## 1. OSS licenses / attribution

- Inventory the assets you ship (`vendor/`, `.kilo/skills/ATTRIBUTION.md`).
- Check **MIT / Apache-2.0** obligations:
  - MIT: include the copyright notice and license text.
  - Apache-2.0: ship `LICENSE`, keep `NOTICE` attribution, state modifications.
- **Third-party assets (e.g. marketplace "business" ones) have unverified licenses.** Verify before redistribution.
- Create/update an **SBOM** (dependency list) (e.g. `pip freeze`, `docker sbom`).

## 2. Product/service legal checklist

- **Terms of Service (ToS)**: scope, prohibited use, disclaimers, change process.
- **Privacy policy**: data collected, purpose, retention, third-party sharing, contact.
- **DPA** (if processing on behalf): purpose, safeguards, sub-processing, deletion.
- **AI usage policy**: handling of generated output, training use, prohibited uses, logs.
- **Records**: version, approver, date, basis.

## 3. Output

- Checklist results (applicable / not applicable / needs confirmation) with **evidence** (file, version, source).
- Explicitly flag **unverified points and points needing a legal decision** (do not assert conclusions).

## 4. Related

- Privacy: `privacy-review`
- Security: `security-review`
- Release: `release-readiness` (version, legal files)
- Project attribution: `.kilo/skills/ATTRIBUTION.md`
