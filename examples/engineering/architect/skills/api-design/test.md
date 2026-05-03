# Test: api-design skill structure

Scenario: Checking that the api-design skill contains the required elements for designing a REST API — resource hierarchy, HTTP semantics, pagination, error format, and versioning guidance.

## Prompt

Review the api-design skill definition and verify it provides sufficient guidance to produce a well-formed REST API specification.

In your verification report, confirm or flag each of the following items by name. Quote skill text where present:

- **URL hierarchy rule** with the specific clause forbidding flat top-level listings of child resources.
- **HTTP method semantics table** covering ALL FIVE methods (GET, POST, PUT, PATCH, DELETE) with idempotency confirmed per method.
- **Paginated response shape** with all FIVE fields named: `items`, `page`, `size`, `totalItems`, `totalPages`.
- **Error format** complies with **RFC 9457 Problem Details** with all five fields (`type`, `title`, `status`, `detail`, `instance`) AND a status-code table covering at minimum: 400, 401, 403, 404, 409, 422, 429, 500.
- **Versioning strategy** with at least TWO options (e.g. URL prefix `/v2/` vs header `Accept-Version`) and explicit rules for when a new version is required (breaking change vs additive).
- **Authentication**: Bearer tokens with **short-lived access tokens** AND **resource-level authorisation** (not just role-level RBAC).
- **Anti-patterns list (4)**: (1) flat URL namespace, (2) verbs in URLs, (3) silent failures, (4) leaking internal IDs.
- **Output template includes**: an **error catalogue** section AND a **resource hierarchy visual** (tree diagram or similar).
- **Identified gaps**: any of: missing rate-limit response semantics (`Retry-After` header, 429 body shape), ambiguous HATEOAS guidance, no field-level deprecation pattern.

Confirm or flag each by name — do not paraphrase.

## Criteria

- [ ] PASS: Skill defines a URL hierarchy rule — resources must be accessed through parent chains, no flat top-level listings of child resources
- [ ] PASS: Skill specifies HTTP method semantics table covering GET, POST, PUT, PATCH, DELETE with idempotency and success codes
- [ ] PASS: Skill mandates PATCH semantics using RFC 7396 merge patch with optimistic concurrency (lastUpdatedAt conflict detection)
- [ ] PASS: Skill requires every list endpoint to support pagination with a defined response shape (items, page, size, totalItems, totalPages)
- [ ] PASS: Skill specifies error format using RFC 9457 Problem Details with standard status codes and rules against leaking stack traces
- [ ] PASS: Skill provides a versioning strategy section with at least two options and rules for when a new version is required
- [ ] PASS: Skill defines authentication requirements — Bearer token with short-lived access tokens and resource-level authorisation
- [ ] PASS: Skill lists anti-patterns — flat URL namespace, verbs in URLs, silent failures, leaking internal IDs
- [ ] PARTIAL: Skill's output format template includes an error catalogue section and a resource hierarchy visual

## Output expectations

- [ ] PASS: Output is structured as a review of the skill (PASS/FAIL or present/missing per requirement) rather than producing a sample API design
- [ ] PASS: Output verifies the URL hierarchy rule and quotes or references the specific clause forbidding flat top-level listings
- [ ] PASS: Output verifies the HTTP method semantics table covers all five methods (GET, POST, PUT, PATCH, DELETE) and confirms idempotency is documented per method
- [ ] PASS: Output checks for RFC 7396 merge patch + optimistic concurrency via `lastUpdatedAt` and 409 Conflict, naming both elements explicitly
- [ ] PASS: Output verifies the paginated response shape includes all five fields (`items`, `page`, `size`, `totalItems`, `totalPages`)
- [ ] PASS: Output verifies the error format complies with RFC 9457 Problem Details, with the standard fields (`type`, `title`, `status`, `detail`, `instance`) and a status-code table covering at least 400/401/403/404/409/422/429/500
- [ ] PASS: Output verifies the versioning section presents at least two strategies (e.g. URL prefix vs header) with rules for when a new version is required
- [ ] PASS: Output verifies the authentication section specifies Bearer tokens with short-lived access tokens and resource-level (not just role-level) authorisation
- [ ] PASS: Output verifies the anti-patterns list covers flat URLs, verbs in URLs, leaking internal IDs, and silent failures — and flags any missing
- [ ] PARTIAL: Output identifies any gaps or weaknesses in the skill (not just confirming presence) — e.g. missing rate-limit response semantics, ambiguous HATEOAS guidance, or no field-level deprecation pattern
