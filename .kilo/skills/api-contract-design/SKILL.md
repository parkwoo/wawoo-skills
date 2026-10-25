---
name: api-contract-design
description: Design or review HTTP, RPC, event, or internal API contracts for clear inputs, outputs, errors, authentication, compatibility, and verification. Use for new or changed interfaces; not for general application implementation without an interface change.
license: MIT
---

# API Contract Design

Define a contract consumers can implement and test without guessing.

1. Identify consumers, user outcome, resource ownership, authentication/authorization, idempotency, and compatibility constraints.
2. Specify request fields, validation, response shape, error taxonomy, pagination/filtering, rate limits, and asynchronous behavior where relevant.
3. Define versioning and backward-compatible evolution. Do not silently change existing meaning or remove fields without a migration plan.
4. Provide representative success, validation-error, authorization-error, and boundary examples. Keep secrets out of examples.
5. Verify the contract against implementation, generated schema/OpenAPI where used, integration tests, and consumer needs.

Report unresolved ownership, security, or versioning decisions rather than guessing.
