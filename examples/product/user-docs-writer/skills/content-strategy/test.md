# Test: Content strategy

Scenario: Testing whether the content-strategy skill uses the Diataxis framework, requires a content inventory, and produces a prioritised content roadmap.

## Prompt


/user-docs-writer:content-strategy for our help centre — we have 140 articles written over 3 years, significant product changes since most were written, and support tickets suggesting users can't find answers to common questions.

## Criteria


- [ ] PASS: Skill uses the Diataxis framework — classifying content as Tutorial, How-to, Reference, or Explanation — not an ad-hoc taxonomy
- [ ] PASS: Skill requires a content inventory step before any recommendations — auditing what exists before deciding what to create
- [ ] PASS: Skill produces a gap analysis — identifying what content types are missing or underrepresented for each product area
- [ ] PASS: Skill produces a prioritised content roadmap — what to create first, with rationale based on user impact
- [ ] PASS: Skill defines content standards — what good looks like for each content type in this context
- [ ] PASS: Skill requires a coverage matrix — mapping content to user tasks to identify blind spots
- [ ] PARTIAL: Skill addresses content maintenance — how to keep existing content current as the product evolves — partial credit if this is mentioned but not required as a strategy component
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
