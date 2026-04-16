# Algorithm multi file refactor

A developer invokes the algorithm skill to refactor a payment processing module across three files, where getting the execution order wrong would break the system.

## Prompt

> /algorithm Refactor the payment processing module. Move `PaymentGateway` from `src/billing/gateway.ts` into its own service at `src/services/payment-gateway.ts`, update all 7 import references across `src/billing/invoice.ts`, `src/orders/checkout.ts`, and `src/api/payments.ts`, and make sure the existing tests still pass after the move.

```markdown

## Output

### Execution: Move PaymentGateway to src/services/payment-gateway.ts

#### Phase 1: OBSERVE

| Field | Value |
|---|---|
| Effort level | Advanced (<16min, 24-48 ISC) |
| ISC Count | 26 criteria |


##### Ideal State Criteria
- [ ] ISC-1: `src/services/payment-gateway.ts` exists with full `PaymentGateway` class content
- [ ] ISC-2: `PaymentGateway` is no longer defined in `src/billing/gateway.ts`
- [ ] ISC-3: `src/billing/gateway.ts` still exists (not deleted — other things may export from it)
- [ ] ISC-4: Import in `src/billing/invoice.ts` references `@/services/payment-gateway` not `@/billing/gateway`
- [ ] ISC-5: Import in `src/orders/checkout.ts` references `@/services/payment-gateway` not `@/billing/gateway`
- [ ] ISC-6: Import in `src/api/payments.ts` references `@/services/payment-gateway` not `@/billing/gateway`
- [ ] ISC-7: All 7 import references updated (grep confirms 0 remaining references to old path)
- [ ] ISC-8: TypeScript compilation passes with no errors
- [ ] ISC-9: All existing payment-related tests pass
- [ ] ISC-10: No new test failures introduced
... (26 total)

**Approach:** Read → Create service file → Remove from gateway → Update imports → Compile → Test

#### Phase 2: THINK
**Riskiest assumptions:**
1. All 7 import references use the same import path — impact if wrong: grep misses aliased imports or re-exports
2. `src/billing/gateway.ts` only exports `PaymentGateway` — impact if wrong: removing it breaks other exports
3. Tests use the same import path — impact if wrong: tests pass despite broken imports if they mock at a different level

**Premortem failures:**
1. Partial move: new file created but old definition not removed → duplicate class
2. Import path mismatch: updated references use wrong alias → runtime module-not-found error at startup
3. Circular dependency introduced: new services/payment-gateway.ts imports from billing, billing imports from services

#### Phase 3: PLAN
1. Read `src/billing/gateway.ts` to understand full export surface
2. Read all 7 import sites to confirm exact import paths
3. Create `src/services/payment-gateway.ts` with full class content
4. Remove `PaymentGateway` from `src/billing/gateway.ts`
5. Update imports in all 7 locations
6. Run `tsc --noEmit`
7. Run test suite

Risk sequence: create before remove, compile before test.

#### Phase 4: BUILD
Creating `src/services/` directory... already exists ✓
Writing `src/services/payment-gateway.ts`... ✓

#### Phase 5: EXECUTE
Progress: 26/26 criteria met

- [x] ISC-1: `src/services/payment-gateway.ts` created — PaymentGateway class present (Read confirmed)
- [x] ISC-2: PaymentGateway removed from `src/billing/gateway.ts` (Read confirmed)
- [x] ISC-3: `src/billing/gateway.ts` still exists, exports `BillingConfig` and `InvoiceFormatter` (Read confirmed)
- [x] ISC-4: invoice.ts import updated (Edit confirmed)
- [x] ISC-5: checkout.ts import updated (Edit confirmed)
- [x] ISC-6: payments.ts import updated (Edit confirmed)
- [x] ISC-7: 0 remaining references to old path (grep confirms)
...

#### Phase 6: VERIFY
| Criterion | Status | Evidence |
|---|---|---|
| ISC-1: New file exists with class | ✅ | Read(src/services/payment-gateway.ts) — 87 lines, PaymentGateway class present |
| ISC-2: Old definition removed | ✅ | Read(src/billing/gateway.ts) — PaymentGateway not found |
| ISC-7: 0 old import references | ✅ | grep -r "@/billing/gateway" src/ → 0 matches |
| ISC-8: TypeScript clean | ✅ | tsc --noEmit → 0 errors |
| ISC-9: Tests pass | ✅ | npm test → 47 passed, 0 failed |

#### Phase 7: LEARN
- Moving before updating imports prevented any window where TypeScript saw two definitions
- Checking what else `gateway.ts` exports before removing the class prevented accidentally breaking other consumers
- This pattern (read full export surface before modifying) should be default for any class extraction refactor
- The 7 import sites were all straightforward — no aliased re-exports found
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 (94%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Skill begins with Phase 1 and assigns effort level before execution — the "Before Starting" section mandates determining effort level first from the tier table. The Output Format template begins with Phase 1 OBSERVE including "Effort level" as a required field. No execution steps appear before Phase 1 in the definition.
- [x] PASS: ISC criteria generated with atomic items meeting tier floor — Phase 1 step 3 mandates ISC generation and step 4 is the "ISC Count Gate — cannot exit OBSERVE with fewer criteria than the effort tier floor." For Advanced tier (24-48 ISC range), the floor is 24. The definition's "Before Starting" table shows Advanced = "<16min, 24-48 ISC." 26 criteria meets the floor.
- [x] PASS: Phase 2 identifies riskiest assumptions and premortem failure modes — Phase 2 step 1 is "Riskiest assumptions (2-12)" and step 2 is "Premortem (2-12)." Both are mandatory and must occur before Phase 3. The Output Format template includes both fields in Phase 2.
- [x] PASS: Phase 3 sequences work to minimise risk — Phase 3 step 2 states "Sequence the work — what order minimises risk and rework?" The definition doesn't prescribe the specific create-before-remove order (that is left to judgment) but mandates risk-minimising sequencing as a deliberate step. The premortem in Phase 2 surfaces ordering risks.
- [x] PASS: Phase 5 marks each ISC complete as it passes — Phase 5 step 2 states "Mark each ISC complete immediately as it passes — don't batch at the end." Critical Rules also states "Mark progress immediately." These are explicit, non-negotiable instructions.
- [x] PASS: Phase 6 confirms with tool-based evidence — Phase 6 steps 2–3 state "Verify with evidence — tool output, test results, file contents, grep results" and "'I believe it's correct' is not verification. Use a tool." The Output Format Phase 6 template shows a table with Evidence column requiring tool output or file references.
- [x] PASS: Output uses defined template with all seven phases — the Output Format section defines all seven phases including Phase 4 (BUILD), with the exact structure for each. The template is present and structurally complete.
- [~] PARTIAL: Phase 7 reflects on execution — Phase 7 has four reflection questions in the definition. The skill notes "If the user has the learning skill available, capture insights there" — suggesting Phase 7 may delegate to `/learning` rather than being deep in the algorithm output itself. The phase is present in the template but depth requirements are soft (four questions rather than mandatory reflection criteria). PARTIAL ceiling applies per criterion prefix.

### Notes

The algorithm skill is well-structured. The ISC Count Gate (cannot exit OBSERVE below the floor) is a strong enforcement mechanism. One gap: Phase 1 step 3 references `/isc` for the Splitting Test but does not reproduce the Splitting Test criteria within the skill itself. An agent without the isc skill loaded would need to apply the test from memory, potentially weakening criterion atomicity. Phase 4 (BUILD) appears in the Output Format template but is minimal in the Process section — "Create any necessary structure, set up test infrastructure if needed" is lighter than the other phases.
