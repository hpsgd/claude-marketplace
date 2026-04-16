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
