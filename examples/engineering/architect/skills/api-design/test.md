# Test: api-design skill structure

Scenario: Checking that the api-design skill contains the required elements for designing a REST API — resource hierarchy, HTTP semantics, pagination, error format, and versioning guidance.

## Prompt

Review the api-design skill definition and verify it provides sufficient guidance to produce a well-formed REST API specification.

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
