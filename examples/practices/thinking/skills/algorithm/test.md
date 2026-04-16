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
