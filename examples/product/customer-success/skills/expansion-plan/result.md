# Output: Expansion plan

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill performs a health prerequisite check as the FIRST step — met. Step 1 is explicitly "Health Prerequisite Check (MANDATORY)" and is the first sequential step in the process.
- [x] PASS: Skill flags that 12/45 active users (27% adoption) indicates an unhealthy account and recommends against expansion — met. Step 1 explicitly checks "active users ÷ licensed seats" and flags below 60% as unhealthy.
- [x] PASS: Skill refuses to produce an expansion plan for an unhealthy account — met. Step 1 states "STOP. Do not produce a normal expansion plan. Switch to the unhealthy-path response below." The output format also includes the unhealthy-path section with explicit conditional gating.
- [x] PASS: Skill recommends a health recovery path before expansion can be attempted — met. Unhealthy-path response item 1 specifies quantified recovery targets with a 60-day window example.
- [x] PASS: Skill frames expansion as customer enablement rather than a sales motion — met. Step 4 explicitly contrasts BAD (sales) vs GOOD (enablement) framing across four expansion types.
- [x] PARTIAL: Skill identifies what specific signals would indicate the account is ready for expansion — fully met. Step 2 includes a quantified readiness thresholds section specifying seat utilisation >=60%, health score >=70, multi-feature engagement, positive relationship scores, and confirmed executive sponsor. Full credit awarded.
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — met. Frontmatter contains `name: expansion-plan`, `description: Plan expansion revenue...`, and `argument-hint: "[customer name or segment...]"`.

### Output expectations

- [x] PASS: Output's FIRST action is a health prerequisite check — met. Step 1 is the mandatory first sequential step; the output format's Health Check section appears first.
- [x] PASS: Output computes the adoption rate explicitly and flags below threshold — met. Step 1 formula "active users ÷ licensed seats" with explicit <60% flag; the output format template shows `[active / licensed = %]`.
- [x] PASS: Output explicitly REFUSES to produce a normal expansion plan — met. "STOP. Do not produce a normal expansion plan." Output format shows "Clear to expand: [Yes / No — if No, complete the Unhealthy-Path Response below and stop]".
- [x] PASS: Output's recovery path lists quantified targets — met. Unhealthy-path response item 1 gives an exact example: "active users need to reach 27 (60% of 45 seats) sustained over a 60-day window."
- [x] PASS: Output frames expansion as customer enablement — met. Step 4 and the Anti-Patterns section both enforce enablement framing explicitly.
- [x] PASS: Output addresses the wasted-spend risk — met. Unhealthy-path response item 3 explicitly covers right-sizing: "if the customer is paying for substantially more capacity than they use (e.g. 33 of 45 seats unused), consider whether reducing seat count is the correct next step."
- [x] PASS: Output names expansion-readiness signals quantitatively — met. Step 2 quantified readiness thresholds section covers adoption rate >=60%, health score >=70, multi-feature engagement, relationship and value scores, executive sponsor confirmed.
- [x] PASS: Output proposes a sequence — met. Unhealthy-path response item 2 explicitly states "Sequence: recover → reassess → plan" with "Do not collapse these into one recommendation."
- [x] PASS: Output's recommended communication to AE/sales explains why expansion is on hold — met. Unhealthy-path response item 4 specifies drafting an internal note explaining the hold, framing as relationship protection, and including recovery targets and reassessment date.
- [~] PARTIAL: Output flags the oversell/handoff issue as a symptom worth feeding back upstream — partially met. Unhealthy-path response item 5 covers this ("if the gap looks like a sales/CS handoff or scoping problem... flag it for the AE and CS lead") but it is a brief item without deeper diagnostic guidance.

## Notes

The skill is well-structured with a clear mandatory gate. The unhealthy-path response maps closely to all the output expectation criteria. The upstream feedback item (criterion 17) is present but brief — it identifies the issue type and instructs flagging but doesn't guide the agent on how to diagnose whether the gap is a handoff problem vs a product-fit problem. This is a minor weakness, not a failure.
