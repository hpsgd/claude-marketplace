# Test: define-okrs

Scenario: A user invokes the skill to define OKRs for a product team for a quarter. Does the skill enforce the OKR rules — qualitative objectives, quantified key results with baselines, 70% ambition target, mix of leading/lagging indicators, and a guardrail metric?

## Prompt

/coordinator:define-okrs "Onboarding team at Stackform, Q3 2026. Context: last quarter we shipped a new onboarding wizard but activation (users who complete setup and send their first API request) is still only 38%. We want to fix this. Parent objective: grow the number of paying customers by 30% this year."

## Criteria

- [ ] PASS: Objectives are qualitative — contain no numbers, describe a desired future state in human language
- [ ] PASS: Each key result includes a specific metric, a stated baseline (with data source), and a numeric target
- [ ] PASS: Targets reflect 70% ambition — not trivially achievable at 100%, not wildly unrealistic
- [ ] PASS: Key results include at least one leading indicator (e.g. wizard step completion rate) and one lagging indicator (e.g. 30-day retention)
- [ ] PASS: At least one KR is a guardrail metric — something that must not worsen while pursuing the others
- [ ] PASS: No binary KRs — all KRs have a spectrum of achievement, not done/not done
- [ ] PASS: Each KR documents a measurement method (tool, frequency, owner)
- [ ] PASS: Output is written to a file at `docs/okrs-[name]-[period].md`
- [ ] PARTIAL: Objectives are limited to 2-4 and each has 3-5 KRs — not over-specified or under-specified

## Output expectations

- [ ] PASS: Output's objectives are qualitative descriptions of the desired future state — e.g. "New users find their footing fast and reach their first 'aha' moment" — and contain NO numeric targets in the objective text itself
- [ ] PASS: Output's key results focus on activation outcomes — at least one KR targets the activation rate (current 38% baseline) with a specific target around 70% ambition (e.g. moving to 55% in Q3)
- [ ] PASS: Output's KRs each include a stated baseline — current value, the data source (analytics tool, internal dashboard), and measurement frequency — not just a target floating without a starting point
- [ ] PASS: Output's KR target reflects 70% ambition — moving from 38% to 55% (+17pp) is a stretch but achievable; moving to 80% would be unrealistic in one quarter, and moving to 42% would be trivial
- [ ] PASS: Output includes both leading indicators (e.g. wizard step completion rate, time to first API request) and lagging indicators (e.g. 30-day retention of activated users, paid conversion rate) — not just lagging metrics
- [ ] PASS: Output includes at least one guardrail KR — something that must NOT regress while pursuing activation, e.g. "support ticket volume per user does not increase by more than 5%" or "payment success rate stays above 98%"
- [ ] PASS: Output's KRs are spectrum-based (achievable at 30%, 60%, 100%) — none are binary "ship feature X" or "complete project Y"
- [ ] PASS: Output ties to the parent objective (grow paying customers by 30% this year) — at least one KR connects activation to downstream paid conversion or trial-to-paid rate
- [ ] PASS: Output is written to `docs/okrs-onboarding-2026-q3.md` (or equivalent path matching the team and quarter) — not only returned as conversation text
- [ ] PASS: Output documents per-KR measurement method — the tool (e.g. Mixpanel, Amplitude, internal dashboard), the cadence (weekly check-in, end-of-quarter scoring), and the named owner
