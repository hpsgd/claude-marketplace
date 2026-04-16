# Test: Write SDK guide

Scenario: Testing whether the write-sdk-guide skill requires a quickstart under 15 lines, a method reference, and code examples that are complete and runnable.

## Prompt


/developer-docs-writer:write-sdk-guide for our Python SDK — it wraps our REST API and currently has no documentation beyond the README installation instructions.

## Criteria


- [ ] PASS: Skill requires a quickstart section that gets developers to a working example in 15 lines or fewer
- [ ] PASS: Skill requires a method reference section documenting each public method with parameters, return types, and exceptions
- [ ] PASS: Skill requires a research step — reading the actual SDK source before writing docs
- [ ] PASS: Skill requires installation instructions as a prerequisite before the quickstart
- [ ] PASS: All code examples must be syntactically correct and complete — no "..." placeholders in runnable code
- [ ] PASS: Skill includes a quality checklist that verifies examples actually work
- [ ] PARTIAL: Skill covers common patterns section with real-world usage examples beyond the quickstart — partial credit if examples are required but common patterns as a distinct section is not
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
