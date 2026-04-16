# Test: Write story map

Scenario: Testing whether the write-story-map skill definition requires a backbone of activities, a walking skeleton slice, release slices, and a validation checklist.

## Prompt


/product-owner:write-story-map for the guest checkout flow — from cart review through to order confirmation.

## Criteria


- [ ] PASS: Skill requires a backbone of activities as verb phrases (3-7 activities), not features or nouns
- [ ] PASS: Skill defines a walking skeleton as the thinnest end-to-end slice touching every backbone activity — and explicitly distinguishes it from the MVP
- [ ] PASS: Skill requires tasks to be ordered top-to-bottom by priority — rows below the happy path are less critical than rows above
- [ ] PASS: Skill prohibits orphan stories — every task must sit under a backbone activity
- [ ] PASS: Skill requires each release slice to touch every backbone activity — a slice covering only one activity is not valid
- [ ] PASS: Skill includes a validation checklist (backbone completeness, walking skeleton coverage, story independence, edge case coverage)
- [ ] PARTIAL: Skill specifies that each task must be independently deliverable — partial credit if this is mentioned as a goal but not enforced as a rule
- [ ] PASS: Skill produces a 2D grid output (activities as columns, tasks as rows by priority) not a flat list
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
