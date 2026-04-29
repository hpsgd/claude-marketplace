# Test: algorithm multi-file refactor

Scenario: A developer invokes the algorithm skill to refactor a payment processing module across three files, where getting the execution order wrong would break the system.

## Prompt

/algorithm Refactor the payment processing module. Move `PaymentGateway` from `src/billing/gateway.ts` into its own service at `src/services/payment-gateway.ts`, update all 7 import references across `src/billing/invoice.ts`, `src/orders/checkout.ts`, and `src/api/payments.ts`, and make sure the existing tests still pass after the move.

## Criteria

- [ ] PASS: Skill begins with Phase 1 (OBSERVE) and assigns an effort level before any execution begins
- [ ] PASS: ISC criteria are generated in Phase 1 with atomic, individually-verifiable items — count meets the floor for the assigned effort tier
- [ ] PASS: Phase 2 (THINK) identifies riskiest assumptions and premortem failure modes before planning
- [ ] PASS: Phase 3 (PLAN) sequences work to minimise risk — moving the file before updating imports, not the reverse
- [ ] PASS: Phase 5 (EXECUTE) marks each ISC criterion complete as it passes, not in a batch at the end
- [ ] PASS: Phase 6 (VERIFY) confirms each criterion with tool-based evidence (file read, grep, test output) — not assertions without proof
- [ ] PASS: Output uses the defined execution template with all seven phases present
- [ ] PARTIAL: Phase 7 (LEARN) reflects on the execution and notes anything worth remembering for similar refactors

## Output expectations

- [ ] PASS: Output's Phase 1 (OBSERVE) lists ISC criteria as atomic items — at minimum: file moved to new location, all 7 imports updated to new path, no broken imports remain, tests still pass — each individually verifiable
- [ ] PASS: Output's Phase 2 (THINK) identifies riskiest assumptions — e.g. "no other file outside the named three imports `PaymentGateway`", "moving the file doesn't break circular import resolution", "tests don't rely on the old path being importable" — with a premortem listing how each could fail
- [ ] PASS: Output's Phase 3 (PLAN) sequences work to minimise risk — moves the file FIRST then updates imports, NOT the other way around — with reasoning that broken imports fail loudly and can be caught immediately
- [ ] PASS: Output uses `grep` (or equivalent) to verify there are exactly 7 import references across the named three files — and surfaces any references in files outside the named set as a discovered ISC criterion
- [ ] PASS: Output's Phase 5 (EXECUTE) marks each ISC criterion complete as it passes — not all at the end — so progress is visible and a failure stops at the right step
- [ ] PASS: Output's Phase 6 (VERIFY) confirms each criterion with tool-based evidence — `cat src/services/payment-gateway.ts`, `grep -r "from.*billing/gateway" src/` returning no matches, `npm test` exit code 0 — not assertions without proof
- [ ] PASS: Output's import-update phase uses a deterministic approach (find/replace with the exact path string, not a fuzzy regex) and lists which files were updated, with a per-file diff or change summary
- [ ] PASS: Output runs the test suite explicitly after the move and reports the command and exit code — not "tests should still pass" without verification
- [ ] PASS: Output's effort tier is appropriate to the work — multi-file refactor with import changes is medium effort, requiring the corresponding ISC count from the algorithm rules (not minimum)
- [ ] PARTIAL: Output's Phase 7 (LEARN) notes anything reusable for similar refactors — e.g. "always run `grep -r oldpath` after the move to catch missed imports", "run typecheck before tests for faster feedback"
