---
name: security-review
description: Perform a read-first security review of application code, configuration, dependencies, and delivery changes. Use for requested security audits, sensitive features, authentication, external APIs, file handling, or pre-release review; not for authorizing production changes.
license: MIT
---

# Security Review

Review threats and evidence before recommending remediation.

1. Establish scope, trust boundaries, data classification, actors, entry points, and deployed environment assumptions.
2. Inspect authentication, authorization, session handling, input/output encoding, CSRF, injection risks, file access, SSRF, redirects, secrets, dependency provenance, logging, and error disclosure as relevant.
3. Rate findings by realistic exploitability and impact. Cite file/location, evidence, affected flow, remediation, and validation method.
4. Distinguish confirmed vulnerabilities from hardening opportunities and unverified risks.
5. Re-test remediation proportionately without exposing credentials or exploiting production systems.

This skill is advisory. Do not change production, rotate credentials, contact third parties, or run destructive proof-of-concept actions without approval.
