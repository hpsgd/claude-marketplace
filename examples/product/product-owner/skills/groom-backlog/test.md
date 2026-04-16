# Test: Groom backlog

Scenario: Testing whether the groom-backlog skill definition contains the required process steps, classification system, and RICE scoring requirements.

## Prompt


/product-owner:groom-backlog for our Q2 feature backlog, which has 24 items ranging from customer-reported bugs to internal tech debt to new feature requests.

## Criteria


- [ ] PASS: Skill defines a structured multi-step process (not a single-step instruction)
- [ ] PASS: Skill requires RICE scoring (Reach, Impact, Confidence, Effort) for items being evaluated for prioritisation
- [ ] PASS: Skill defines a classification system with at least these states: Ready, Needs Refinement, and Blocked
- [ ] PASS: Skill requires dependency mapping — identifying which items block or are blocked by others
- [ ] PASS: Skill specifies what "Ready" means — criteria a story must meet before it can be pulled into a sprint
- [ ] PASS: Skill requires output as a structured table or list with status, score, and reasoning — not prose
- [ ] PARTIAL: Skill addresses how to handle items that lack sufficient data to score — partial credit if data gaps are mentioned but no specific guidance on how to proceed
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
