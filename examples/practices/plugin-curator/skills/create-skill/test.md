# Test: create-skill new skill for existing agent

Scenario: A contributor asks the create-skill skill to add a `review-go` skill to the coding-standards agent, covering Go-specific conventions for type safety, error handling, and testing patterns.

## Prompt

/create-skill review-go for coding-standards — Go code review skill covering error handling patterns, interface usage, goroutine safety, and table-driven tests.

## Criteria

- [ ] PASS: Step 1 reads the skill template and CLAUDE.md before creating anything
- [ ] PASS: Step 2 reads the parent agent (coding-standards) and checks for existing sibling skills to understand boundaries and avoid duplication
- [ ] PASS: SKILL.md frontmatter includes all required fields: name, description, argument-hint, user-invocable, and allowed-tools
- [ ] PASS: Description is specific enough for auto-invocation — includes what it produces and when to use it, not just "helps review Go code"
- [ ] PASS: Skill body includes sequential mandatory steps, rules with anti-patterns, and a structured output format template
- [ ] PASS: Step 6 self-containment check is performed — skill is verified to work without reading the parent agent
- [ ] PASS: README is updated to add review-go to the coding-standards agent's skill list
- [ ] PARTIAL: Examples in the skill use generic identifiers (e.g., `myservice`, `@org/shared`) — no private company names or internal package references
