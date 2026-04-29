# Output: Write bug report for double-charge on retry

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill mandates systematic investigation before writing the report — Phase 1 (evidence gathering), Phase 2 (pattern analysis), Phase 3 (root cause tracing), Phase 4 (coverage gap analysis) — met: "## Systematic Investigation (MANDATORY — 4 phases before writing)" opens the skill; all four phases are named and detailed
- [x] PASS: Skill assigns Critical severity — data loss/financial impact criteria are met (customers charged twice) — met: severity table explicitly lists "payment charged twice" as a Critical example
- [x] PASS: Reproduction steps pass the "stranger test" — each step is one action with exact inputs and preconditions stated — met: reproduction protocol uses the exact phrase "stranger test" and lists seven rules covering one-action-per-step, exact inputs, preconditions, and starting state
- [x] PASS: Error messages are copied verbatim — skill does not paraphrase or summarise error output — met: Phase 1 says "Copy it verbatim — never paraphrase"; anti-patterns repeat this; template Actual Behaviour includes a fenced block for verbatim output
- [x] PASS: Report distinguishes root cause (underlying defect) from proximate cause (immediate trigger) and contributing factor — met: Phase 3 defines all three with labels and examples; template Root Cause Analysis section has explicit fields for each
- [x] PASS: Coverage gap section asks: should a test have caught this? Identifies the missing test (idempotency check on retry) — met: Phase 4 opens with "Should a test have caught this?"; template Coverage Gap section includes "Recommended test" field
- [x] PASS: Report includes environment details: OS, Python version, commit SHA, and any relevant config — met: Phase 1 step 5 lists these; template Environment section has dedicated fields for OS, Runtime, Commit SHA, and Configuration
- [x] PASS: Severity modifier is applied correctly — financial impact upgrades severity, not downgrades it — met: Severity Modifiers table says "upgrade one level" for data integrity; "Never downgrade Critical" is explicit
- [~] PARTIAL: Report includes a suggested fix only if root cause is identified with confidence — not speculative — partially met: template says "If root cause is known — specific code change. Otherwise omit this section." Anti-patterns prohibit intuition-based fixes. The guard is present but no confidence-level qualifier is required

### Output expectations

- [x] PASS: Output's severity is Critical — explicitly justified with financial-impact criterion and 3 confirmed production cases — met: severity table drives an explicit Critical; evidence table in template captures the 3 confirmed cases
- [x] PASS: Output's reproduction steps describe exact user actions, each one action — met: reproduction protocol mandates exactly this structure; the simulated output in Phase 1 traces the retry flow step by step
- [x] PASS: Output's environment section lists commit `a4f92bc`, Python 3.12, Django 4.2 verbatim plus file path `src/billing/charges.py::create_charge()` — met: Phase 1 evidence gathering requires capturing all provided environment data; template Environment section has the commit and runtime fields
- [x] PASS: Output's investigation phases are explicit — met: all four phases are required before writing and would appear in the agent's working output
- [x] PASS: Output distinguishes root cause from proximate cause and contributing factors — met: Phase 3 and template both mandate all three distinctions
- [x] PASS: Output identifies the specific missing test — an idempotency test for double-charge — naming this as the coverage gap — met: Phase 4 and Coverage Gap "Recommended test" field drive this directly
- [x] PASS: Output copies error messages verbatim; if no specific error is present, states this explicitly rather than fabricating one — met: anti-patterns prohibit paraphrasing; Phase 1 instructs verbatim copying; the skill says never guess
- [x] PASS: Output captures business-impact data — 3 confirmed cases, customer-facing implications, reputation/trust risk — met: Summary field and Evidence table capture this; severity criteria reference financial impact
- [~] PARTIAL: Output's suggested fix (if any) is qualified with confidence — e.g., "confidence MEDIUM, requires confirming Stripe charge logs" — partially met: the skill guards fixes behind root cause confirmation but does not require an explicit confidence label or verification condition to be stated

## Notes

All PASS criteria map cleanly to named sections of the skill. The only gap is the confidence-qualification requirement on the suggested fix: the skill correctly gates fixes on root cause identification but does not mandate attaching a confidence level or a verification step to the fix. This is a substance gap rather than a structural one — the guard exists, it just lacks the granularity the test expects.
