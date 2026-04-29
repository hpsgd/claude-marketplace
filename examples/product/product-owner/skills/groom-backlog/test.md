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

## Output expectations

- [ ] PASS: Output works through all 24 backlog items — not a top-N subset — assigning each a state (Ready / Needs Refinement / Blocked) and either a RICE score or a "data needed" flag
- [ ] PASS: Output classifies items by type — customer-reported bugs, internal tech debt, new features — and applies prioritisation logic appropriately (bugs with revenue impact compete with features; pure tech debt sits in its own track)
- [ ] PASS: Output's RICE scoring shows the four columns numerically — Reach, Impact (0.25 / 0.5 / 1 / 2 / 3), Confidence (% based on evidence quality), Effort (person-weeks or story points) — with the formula `(R × I × C) / E` applied per scorable item
- [ ] PASS: Output flags items with insufficient data to score — naming the missing data per item ("need usage analytics for X feature", "need sales-team interview for Y customer-reported bug") rather than assigning made-up confidence
- [ ] PASS: Output's "Ready" definition is concrete — has user story + acceptance criteria + estimate + dependencies identified — not just "looks fine"
- [ ] PASS: Output's dependency map identifies blocking relationships — e.g. "Item 12 (mobile feature) blocked by Item 7 (auth refactor)" — so the team can plan in the right order
- [ ] PASS: Output's recommended sprint candidates are based on RICE ranking + team capacity + dependencies — not "the top 5 by RICE" (which may be all blocked)
- [ ] PASS: Output's data-gap recommendations are actionable — e.g. "instrument feature X before scoring", "interview 3 enterprise customers about Y" — with effort estimates so the data work itself can be prioritised
- [ ] PASS: Output produces the result as a structured table — Item | Type | State | RICE | Dependencies | Reasoning — not prose paragraphs
- [ ] PARTIAL: Output addresses how stale backlog items are handled — items >6 months old without movement should be archived or reconfirmed, not silently kept on the list
