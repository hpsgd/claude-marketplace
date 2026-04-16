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
