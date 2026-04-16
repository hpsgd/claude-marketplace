# Test: isc request decomposition with negatives

Scenario: A developer asks for help with a task that has multiple components, explicit exclusions, and implied requirements. The ISC skill must catch all parts including the anti-criteria.

## Prompt

/isc Update the user profile page to show the new avatar upload feature. The upload should accept JPEG and PNG only, max 5MB, and resize to 200x200 on save. Don't touch the password change section — we're in the middle of a security audit. Also make sure the existing profile tests still pass, and don't add any new npm dependencies.

## Criteria

- [ ] PASS: Step 1 extracts all five categories — explicit wants, implied wants, explicit not-wanted, implied not-wanted, and gotchas
- [ ] PASS: Explicit not-wanted items (don't touch password section, no new npm dependencies) appear as separate ISC criteria
- [ ] PASS: The Splitting Test is applied — compound criteria like "accept JPEG and PNG" become separate verifiable items
- [ ] PASS: Each criterion is stated as verifiable — includes what tool would confirm it and what you'd see
- [ ] PASS: Effort level is assigned and the ISC count meets the floor for that tier before execution begins
- [ ] PASS: ISC count gate is enforced — if below floor, skill explicitly states the criterion count is insufficient and decomposes further
- [ ] PASS: Criteria are presented as a numbered checklist with checkboxes, ready to be marked during execution
- [ ] PARTIAL: Domain-specific decomposition is applied — UI criteria split by element/state, validation criteria split by rule
