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

## Output expectations

- [ ] PASS: Output's backbone covers the guest checkout flow as 3-7 verb-phrase activities — e.g. "Review cart", "Enter delivery details", "Choose payment method", "Confirm order", "Receive confirmation" — not nouns like "Cart" or "Payment page"
- [ ] PASS: Output's walking skeleton is a thinnest end-to-end slice — touching every backbone activity with the minimum task per — e.g. cart with 1 item, hardcoded delivery address, single payment method, basic confirmation — explicitly distinct from the MVP
- [ ] PASS: Output's tasks under each backbone activity are ordered top-to-bottom by priority — must-have at the top (within the walking skeleton), nice-to-have below — and the priority is visible in the grid layout
- [ ] PASS: Output's release slices each touch ALL backbone activities — never a slice that only adds payment methods without touching cart / delivery / confirmation; if a single-activity enhancement is needed it's an iteration, not a release slice
- [ ] PASS: Output explicitly excludes orphan stories — every task is under one backbone activity; no "miscellaneous" or "support" categories
- [ ] PASS: Output's validation checklist confirms backbone completeness (no gaps in the activity sequence), walking skeleton coverage, story independence (one task per release doesn't depend on a parallel task), and edge case coverage (failed payment, abandoned cart, address validation failure)
- [ ] PASS: Output's grid layout has activities as column headers and tasks as rows ordered by priority — visible as a Markdown table or ASCII grid, not a flat list of tasks under each activity
- [ ] PASS: Output identifies edge-case scenarios as explicit tasks lower in the grid — e.g. "card declined retry path", "out-of-stock during checkout", "delivery address outside service area" — not omitted because they're "complex"
- [ ] PASS: Output addresses the GUEST aspect specifically — what's different from authenticated checkout (no saved addresses, no order history, possible account-creation prompt at the end) — relevant tasks per activity
- [ ] PARTIAL: Output addresses task independence — each task is described to be deliverable on its own, with the rule that one task should not require a parallel task in another activity to complete
