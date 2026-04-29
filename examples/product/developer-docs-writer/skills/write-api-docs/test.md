# Test: Write API docs

Scenario: Testing whether the write-api-docs skill requires complete request/response examples, error documentation, and a quality checklist that includes running every code example.

## Prompt


/developer-docs-writer:write-api-docs for our Projects API — endpoints for creating, reading, updating, and archiving projects, with filtering and pagination on the list endpoint.

## Criteria


- [ ] PASS: Skill requires every endpoint to document both success responses AND error responses — not just the happy path
- [ ] PASS: Skill requires every code example to be syntactically correct and runnable — not pseudocode
- [ ] PASS: Skill requires a discovery or research step — reading existing code or specs before writing docs
- [ ] PASS: Skill organises endpoints by resource (Projects) with a consistent structure per endpoint — not a flat alphabetical list
- [ ] PASS: Skill requires an overview section before the endpoint reference — authentication, base URL, common patterns
- [ ] PASS: Skill includes a quality checklist that verifies every code example runs and every error response is documented
- [ ] PARTIAL: Skill covers pagination documentation requirements specifically — partial credit if special cases like pagination are mentioned but not required to be documented
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output covers all four prompt-named operations on Projects — create, read, update, archive — each as a documented endpoint with method, path, request, response
- [ ] PASS: Output's list endpoint documents pagination, at least 2 filter parameters (e.g. status, owner), and at least 1 sort option — not just GET / response
- [ ] PASS: Output documents both success AND error responses per endpoint — at minimum 401, 403, 404, and 422
- [ ] PASS: Output's code examples are runnable — full HTTP request with method, headers, body, and a parseable response example — no pseudocode, no placeholder gaps
- [ ] PASS: Output organises endpoints under a Projects resource heading with consistent structure per endpoint (Description, Request, Response, Errors, Example) — not flat alphabetical
- [ ] PASS: Output includes an overview / authentication section before the endpoint reference — base URL, auth scheme, common request/response headers, and a common error envelope
- [ ] PASS: Output's quality checklist verifies each code example was run and that every documented error response has a worked example
- [ ] PARTIAL: Output addresses pagination behaviour edge cases — what happens for an empty result set, an out-of-range page number, and the maximum page size cap
