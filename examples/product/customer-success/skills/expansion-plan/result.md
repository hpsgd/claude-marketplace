# Output: Expansion plan

**Verdict:** PARTIAL
**Score:** 12.5/17 criteria met (74%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill performs a health prerequisite check as the FIRST step — Step 1 is "Health Prerequisite Check (MANDATORY)" with an explicit "STOP" gate before any plan proceeds.
- [x] PASS: Skill flags low adoption as an unhealthy account signal — the "Expanding without adoption" anti-pattern states "if the customer isn't using current features, adding more features increases complexity without value"; 27% utilisation triggers the health gate.
- [x] PASS: Skill refuses to produce an expansion plan for unhealthy accounts — Step 1 says "STOP. Fix the health first." The output format also includes "Clear to expand: [Yes / No — if No, stop here]."
- [x] PASS: Skill recommends a health recovery path before expansion — "Fix the health first. Run `/health-assessment` to diagnose."
- [x] PASS: Skill frames expansion as customer enablement — Step 4 provides an explicit BAD (sales) vs GOOD (enablement) comparison table for each expansion type.
- [~] PARTIAL: Skill identifies signals indicating expansion readiness — signals in Step 2 are qualitative; no numeric thresholds (e.g., adoption >=60%) are specified for readiness. Partial credit for the named signal categories and the "at least 2 signals" rule.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three present in the opening front matter.

### Output expectations

- [x] PASS: Output's FIRST action is a health prerequisite check — the sequential process mandates Step 1 runs before Steps 2–7; the output template opens with "Health Check."
- [ ] FAIL: Output computes adoption rate explicitly — the skill has no instruction to calculate adoption percentage (12/45 = 27%) or compare against a numeric expansion-readiness threshold (typically 60-70%); health criteria reference composite score and churn signals, not adoption rate directly.
- [x] PASS: Output explicitly refuses to produce a normal expansion plan — the hard STOP gate and "Clear to expand: No — stop here" output section cover this.
- [ ] FAIL: Output's recovery path lists quantified targets — the skill directs to run `/health-assessment` but gives no quantified recovery targets for the unhealthy-account path (e.g., "active users need to reach 27 = 60% of 45 within 60 days").
- [x] PASS: Output frames expansion as customer enablement — Step 4's enablement framing is thorough and explicit.
- [ ] FAIL: Output addresses the wasted-spend risk — no instruction in the skill to flag unused seats (33 in this scenario) or discuss reducing seat count before any expansion conversation.
- [ ] FAIL: Output names expansion-readiness signals quantitatively — no quantified thresholds (adoption >=60%, health score targets for readiness); the "at least 2 signals" rule is the only numeric criterion and it is about signal count, not signal magnitude.
- [ ] FAIL: Output proposes a three-phase sequence — the skill moves from STOP straight to the standard planning steps (2–7) for healthy accounts; there is no recover → assess → plan sequence for the blocked unhealthy-account case.
- [ ] FAIL: Output's communication to AE/sales explains why expansion is on hold — the skill has no stakeholder communication step when expansion is blocked.
- [~] PARTIAL: Output flags the overselling symptom as a CS/sales handoff problem worth feeding back upstream — the anti-pattern "Expanding without adoption" is a forward-looking caution, not an instruction to retrospectively diagnose and escalate the root cause of the Fenwick seat oversell.

## Notes

The skill's health gate (Step 1) is well designed and would correctly block expansion for Fenwick Capital. The enablement framing in Step 4 is thorough. The weakness is almost entirely in the unhealthy-account path: the skill says "STOP, fix health first" but provides almost no guidance on what follows that stop. A CSM following this skill for Fenwick would know not to expand but would get no recovery roadmap, no wasted-seat diagnosis, no quantified readiness targets, and no guidance on communicating the hold to the AE or sales team. The output expectations in the test were written to probe exactly that gap, and the skill doesn't cover it.
