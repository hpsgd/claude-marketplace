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

## Output expectations

- [ ] PASS: Output's explicit-wants list includes avatar upload, JPEG and PNG accepted, max 5MB, resize to 200x200 on save — split where the Splitting Test demands ("JPEG accepted" and "PNG accepted" as separate verifiable items, not "both formats accepted")
- [ ] PASS: Output's explicit-not-wanted list includes "do not modify password change section" and "no new npm dependencies" as separate ISC criteria — and these are framed as ANTI-criteria that must be verified false at completion (e.g. `git diff` shows no changes to password section)
- [ ] PASS: Output's implied-wants includes things like "validation errors are user-visible", "upload progress indication exists", "accessibility for the file picker" that the prompt didn't say but the feature requires
- [ ] PASS: Output's implied-not-wanted (gotchas) includes "do not regress existing avatar functionality if any", "do not break tests in unrelated areas", and "do not introduce client-side image processing libraries when the prompt forbids new npm dependencies"
- [ ] PASS: Output's criteria each name a verification method — e.g. "Tool: open profile page in browser → see new upload button" or "Tool: `git diff -- src/profile/password*` → shows no changes" or "Tool: `npm ls --depth=0` → no new package added"
- [ ] PASS: Output assigns an effort level (likely Small or Medium given file upload + validation + resize + tests) and the resulting ISC criterion count meets the floor for that tier — explicitly stated
- [ ] PASS: Output enforces the count gate — if the initial decomposition is below the floor, the skill states the count is insufficient and decomposes further (e.g. splitting "validation" into per-rule items)
- [ ] PASS: Output applies domain-specific decomposition — file upload split by validation rule (format, size, resize), UI split by state (idle, uploading, success, error), test continuity split by named test files
- [ ] PASS: Output presents criteria as a numbered checklist with `[ ]` checkboxes, ready to be marked during execution
- [ ] PARTIAL: Output addresses the resize requirement specifically — what aspect ratio handling (crop, letterbox, distort), what library performs the resize (server-side vs client-side), what happens to non-square inputs
