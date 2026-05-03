# Define Okrs

Scenario: A user invokes the skill to define OKRs for a product team for a quarter. Does the skill enforce the OKR rules — qualitative objectives, quantified key results with baselines, 70% ambition target, mix of leading/lagging indicators, and a guardrail metric?

## Prompt

> /coordinator:define-okrs "Onboarding team at Stackform, Q3 2026. Context: last quarter we shipped a new onboarding wizard but activation (users who complete setup and send their first API request) is still only 38%. We want to fix this. Parent objective: grow the number of paying customers by 30% this year."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

OKRs written to `docs/okrs-onboarding-q3-2026.md`. Here's a summary of what was produced and why:

---

**2 objectives, 7 KRs total.**

**Objective 1 — Make developers go from signup to first API call without hitting a wall**
- KR1 is the headline: activation rate from **38% → 60%** (the one known baseline)
- KR2 and KR3 are honest establish-baseline KRs for time-to-first-request and funnel drop-off — improvement targets deferred to July 14 once data lands, rather than setting fake relative targets against unknown numbers
- KR4 is a guardrail: onboarding support tickets must not increase

**Objective 2 — Turn activated users into Stackform's next wave of paying customers**
- All three KRs stay in the Onboarding team's zone of control: sticky activation (10 calls in 7 days), activated-to-paid conversion (14-day window), and 4-week early return rate — not 30-day retention, which depends on product quality, billing, and support that Onboarding doesn't own
- The 4-week return rate is the lagging indicator, and it can be baselined using Q2 cohort data

**Key structural decision:** Six of seven KRs have no baseline today — the doc surfaces this prominently as a credibility problem and makes week-1 instrumentation a named precondition, not a footnote.

### Artifacts written

#### `work/docs/okrs-onboarding-q3-2026.md`

```
# OKRs: Onboarding Team — Q3 2026

**Context:** Q2 2026, the team shipped the new onboarding wizard. Despite this, activation — users who complete setup and send their first API request — remains at 38%. The wizard improved completion rates but has not yet translated into users experiencing the product's core value. This quarter, the team shifts focus from shipping the wizard to making it actually work.

**Parent objective:** Grow the number of paying customers by 30% in 2026.

> **Precondition — week 1 instrumentation sprint:** Six of the seven KRs below have no baseline today. This is a credibility gap: the team shipped a wizard last quarter without the telemetry to know whether it worked. The first deliverable of Q3 is an instrumentation pass to establish all unknown baselines by July 7. Until that data lands, targets marked "TBD — set by July 14" are intentionally deferred. Targets will be committed and locked by July 14 at the latest.

---

## Objective 1: Make developers go from signup to first API call without hitting a wall

**Why this objective:** 62% of new users never send a single API request — they never experience what makes Stackform worth paying for. Until users hit that first success, they have no reason to upgrade, recommend the product, or stay. Activation is the single highest-leverage intervention between signup and revenue, and it directly unblocks the company's paying customer growth goal.

| KR | Metric | Baseline | Target | Measurement | Type |
|----|--------|----------|--------|-------------|------|
| KR1 | Activation rate (setup complete + first successful API request) | 38% — product analytics, Q2 2026 weekly cohort average | 60% | Product analytics cohort report, measured weekly, owned by Onboarding PM | Leading |
| KR2 | Establish baseline: median time from signup to first API request | Unknown | Baseline documented by July 7; improvement target committed by July 14 | Instrument signup → first-API-call event, product analytics funnel, owned by Eng Lead | Leading |
| KR3 | Establish baseline: drop-off rate at the highest-friction step in the wizard | Unknown | Baseline documented by July 7; reduction target committed by July 14 | Product analytics wizard funnel, step-level breakdown, weekly report, owned by Product Analyst | Leading |
| KR4 | Onboarding-related support tickets per 100 new signups | Unknown — establish baseline by July 7 | Does not increase above baseline across Q3 | Support tool "onboarding" tag count / new signup volume, weekly, owned by Support Lead | Guardrail |

**Key initiatives (inputs, not measured):**
- Instrumentation pass in week 1 to establish all KR2, KR3, and KR4 baselines
- 10 moderated research sessions with users who dropped off before their first API call
- Embedded interactive quickstart ("Hello World" API guide) inside the wizard
- Contextual help added at the highest drop-off step identified from funnel data
- Re-engagement email sequence for users who complete setup but never call the API

---

## Objective 2: Turn activated users into Stackform's next wave of paying customers

**Why this objective:** Activation is the gateway, not the destination. A user who sends one API request and disappears contributes nothing to the 30% paying customer growth goal. This objective ensures the users we unlock in Objective 1 build habits and convert — closing the loop between onboarding work and revenue. All KRs here sit within the Onboarding team's zone of influence: early-habit formation, nurture sequences, and upgrade path friction.

| KR | Metric | Baseline | Target | Measurement | Type |
|----|--------|----------|--------|-------------|------|
| KR1 | % of activated users who make ≥10 API calls in their first 7 days (sticky activation) | Unknown — establish baseline by July 7 | Committed by July 14 after baseline lands | Product analytics, weekly activated cohort, owned by Onboarding PM | Leading |
| KR2 | Activated-to-paid conversion rate within 14 days of first API request | Unknown — establish baseline by July 7 | Committed by July 14 after baseline lands | Billing data joined to activation event (Stripe + product analytics), bi-weekly, owned by Growth PM | Leading |
| KR3 | % of Q3 activated users who return to make API calls in week 4 of their first month (4-week early retention) | Unknown — establish using Q2 activated cohort data by July 14 | Committed by July 14 after baseline lands | Product analytics, cohort retention curve, 4-week mark, owned by Onboarding PM | Lagging |

**Key initiatives (inputs, not measured):**
- Post-activation nurture sequence: day 1, day 3, day 7 check-ins with usage tips and next-step prompts
- In-app milestone moments: acknowledge first 10 calls, first 100 calls
- Success team outreach to activated free-tier users who have not upgraded after 7 days
- Trial-to-paid friction audit: identify and remove blockers in the upgrade and checkout flow

---

## Risks and Dependencies

- **Instrumentation gap (P0):** Six of seven KRs have no baseline today. The week-1 instrumentation sprint is not optional — it is the gating condition for the rest of the quarter. Eng Lead owns delivery of this by July 7.
- **Attribution accuracy:** Activation events and paid conversion events live in different systems (product analytics vs. Stripe). Resolve the data join before publishing KR2/Obj2 baseline — a bad join produces a meaningless number.
- **Root cause is still unknown:** The Q2 wizard shipped but did not move activation. We do not yet know whether the problem is friction, clarity, motivation, or something else. The research sessions in weeks 1–3 are critical before the team commits to solutions at scale.
- **Cross-team dependencies:** KR4 requires Support to consistently tag onboarding tickets. KR2/Obj2 and the outreach initiative require alignment with the Success team on ownership. Both must be confirmed before Q3 begins.
- **Top-of-funnel risk:** Activation rate is a rate metric. If marketing reduces signup volume, improving activation alone may not deliver the 30% paying customer growth in absolute terms. This team owns the rate; it does not own the volume.

---

## Scoring Framework

At the end of Q3, each KR is scored 0–1:

| Score | Meaning |
|-------|---------|
| 0.0 | No progress |
| 0.3 | Some progress, fell well short |
| 0.5 | Meaningful progress, roughly half the target |
| 0.7 | Strong result — expected "good" outcome |
| 1.0 | Fully achieved — target may have been too conservative |

A team score of **0.6–0.7** reflects healthy ambition and strong execution. The team OKR score is the average of all KR scores.

**Scoring note for KRs with deferred targets:** KR2 and KR3 of Objective 1, and all three KRs of Objective 2, have targets committed by July 14. If a baseline is not established by that date, the KR scores 0.0 — instrumentation is a prerequisite, not a nice-to-have. Once targets are locked, scoring follows the standard 0–1 scale.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/18.5 (86%) |
| Evaluated | 2026-05-01 |
| Target duration | 319297 ms |
| Target cost | $0.6474 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Objectives are qualitative — contain no numbers, describe a desired future state in human language | PASS | Obj1: 'Make developers go from signup to first API call without hitting a wall'; Obj2: 'Turn activated users into Stackform's next wave of paying customers' — both are qualitative, no numbers in objective text. |
| c2 | Each key result includes a specific metric, a stated baseline (with data source), and a numeric target | PARTIAL | Only Obj1 KR1 has all three: metric (activation rate), baseline (38% — product analytics, Q2 2026 weekly cohort average), and numeric target (60%). The remaining 6 KRs have 'Unknown' baselines and deferred targets ('committed by July 14'), failing the 'each' requirement. |
| c3 | Targets reflect 70% ambition — not trivially achievable at 100%, not wildly unrealistic | PARTIAL | Only Obj1 KR1 has a committed numeric target (38%→60%), which reflects meaningful ambition. The remaining 6 KRs have no committed targets (deferred to July 14), making ambition level unverifiable for them. |
| c4 | Key results include at least one leading indicator (e.g. wizard step completion rate) and one lagging indicator (e.g. 30-day retention) | PASS | Leading indicators present: Obj1 KR1 (activation rate), KR2 (time-to-first-request), KR3 (drop-off rate), Obj2 KR1 (sticky activation), KR2 (paid conversion). Lagging indicator present: Obj2 KR3 (4-week early retention), explicitly labeled 'Lagging' in the Type column. |
| c5 | At least one KR is a guardrail metric — something that must not worsen while pursuing the others | PASS | Obj1 KR4: 'Onboarding-related support tickets per 100 new signups... Does not increase above baseline across Q3' — explicitly labeled 'Guardrail' in the Type column. |
| c6 | No binary KRs — all KRs have a spectrum of achievement, not done/not done | PARTIAL | Obj1 KR2 and KR3 are 'establish baseline' KRs with targets like 'Baseline documented by July 7' — effectively binary (documented or not). The scoring note confirms: 'If a baseline is not established by that date, the KR scores 0.0.' The remaining KRs (activation rate, sticky activation, paid conversion, retention) are spectrum-based. |
| c7 | Each KR documents a measurement method (tool, frequency, owner) | PASS | All 7 KRs have a Measurement column entry. E.g., Obj1 KR1: 'Product analytics cohort report, measured weekly, owned by Onboarding PM'; Obj2 KR2: 'Billing data joined to activation event (Stripe + product analytics), bi-weekly, owned by Growth PM'. Minor gap: Obj1 KR2 lacks explicit cadence but names tool and owner. |
| c8 | Output is written to a file at `docs/okrs-[name]-[period].md` | PASS | Artifact written to `work/docs/okrs-onboarding-q3-2026.md`, matching the pattern docs/okrs-[name]-[period].md. |
| c9 | Objectives are limited to 2-4 and each has 3-5 KRs — not over-specified or under-specified | PARTIAL | 2 objectives (within 2-4 range); Obj1 has 4 KRs and Obj2 has 3 KRs, both within the 3-5 range. Ceiling is PARTIAL per test specification. |
| c10 | Output's objectives are qualitative descriptions of the desired future state — e.g. 'New users find their footing fast and reach their first 'aha' moment' — and contain NO numeric targets in the objective text itself | PASS | Obj1: 'Make developers go from signup to first API call without hitting a wall'; Obj2: 'Turn activated users into Stackform's next wave of paying customers' — both are purely qualitative, no numbers in objective headers or why-text. |
| c11 | Output's key results focus on activation outcomes — at least one KR targets the activation rate (current 38% baseline) with a specific target around 70% ambition (e.g. moving to 55% in Q3) | PASS | Obj1 KR1: 'Activation rate (setup complete + first successful API request)' with baseline 38% and target 60% — directly uses the given 38% baseline and sets a stretch target (+22pp) comparable to the example 55% (+17pp). |
| c12 | Output's KRs each include a stated baseline — current value, the data source (analytics tool, internal dashboard), and measurement frequency — not just a target floating without a starting point | PARTIAL | Obj1 KR1 has full baseline: '38% — product analytics, Q2 2026 weekly cohort average.' The other 6 KRs list 'Unknown' as baseline value (with plan to establish by July 7). The criterion requires 'each' KR to have a current value — 6 of 7 do not. |
| c13 | Output's KR target reflects 70% ambition — moving from 38% to 55% (+17pp) is a stretch but achievable; moving to 80% would be unrealistic in one quarter, and moving to 42% would be trivial | PASS | Obj1 KR1 target is 60% (+22pp from 38%). This is more ambitious than the example threshold of 55% (+17pp) but below the 'unrealistic' 80% ceiling. The scoring framework explicitly targets 0.6-0.7 as 'healthy ambition,' supporting 60% as a well-calibrated stretch goal. |
| c14 | Output includes both leading indicators (e.g. wizard step completion rate, time to first API request) and lagging indicators (e.g. 30-day retention of activated users, paid conversion rate) — not just lagging metrics | PASS | Leading indicators: Obj1 KR1 (activation rate), KR2 (time to first API request), KR3 (wizard drop-off rate), Obj2 KR1 (sticky activation), KR2 (paid conversion). Lagging: Obj2 KR3 (4-week early retention), explicitly labeled 'Lagging.' |
| c15 | Output includes at least one guardrail KR — something that must NOT regress while pursuing activation, e.g. 'support ticket volume per user does not increase by more than 5%' or 'payment success rate stays above 98%' | PASS | Obj1 KR4 (Type: Guardrail): 'Onboarding-related support tickets per 100 new signups... Does not increase above baseline across Q3' — prevents quality regression while pursuing activation gains. |
| c16 | Output's KRs are spectrum-based (achievable at 30%, 60%, 100%) — none are binary 'ship feature X' or 'complete project Y' | PARTIAL | Obj1 KR2 and KR3 are 'establish baseline' KRs with binary framing ('Baseline documented by July 7'). The scoring note confirms: 'If a baseline is not established by that date, the KR scores 0.0' — making these effectively pass/fail milestones. The remaining 5 KRs are spectrum-based (activation rate, sticky activation, paid conversion, retention). |
| c17 | Output ties to the parent objective (grow paying customers by 30% this year) — at least one KR connects activation to downstream paid conversion or trial-to-paid rate | PASS | Obj2 KR2: 'Activated-to-paid conversion rate within 14 days of first API request' directly links activation to paying customers. The 'Why this objective' text for Obj2 explicitly states: 'closing the loop between onboarding work and revenue' and references the 30% paying customer growth goal. |
| c18 | Output is written to `docs/okrs-onboarding-2026-q3.md` (or equivalent path matching the team and quarter) — not only returned as conversation text | PASS | Artifact section shows file written to `work/docs/okrs-onboarding-q3-2026.md`. The path contains 'docs/', team name 'onboarding', and period 'q3-2026' — equivalent to the expected pattern despite minor date-format difference (q3-2026 vs 2026-q3). |
| c19 | Output documents per-KR measurement method — the tool (e.g. Mixpanel, Amplitude, internal dashboard), the cadence (weekly check-in, end-of-quarter scoring), and the named owner | PASS | All 7 KRs include a Measurement column with tool, cadence, and owner. Examples: Obj1 KR1: 'Product analytics cohort report, measured weekly, owned by Onboarding PM'; Obj2 KR2: 'Billing data joined to activation event (Stripe + product analytics), bi-weekly, owned by Growth PM'. KR2 Obj1 lacks explicit cadence but is a week-1 instrumentation action, a minor gap. |

### Notes

The output is structurally strong and demonstrates clear OKR methodology: qualitative objectives, explicit guardrail, leading/lagging balance, measurement metadata, and appropriate ambition on the one concrete target (38%→60% activation). The primary weakness is that 6 of 7 KRs have no committed baseline or numeric target — they defer to a July 14 instrumentation sprint. The doc acknowledges this honestly as a 'credibility gap' and makes instrumentation a named precondition, but the criteria require each KR to actually contain baseline values and targets, not just a plan to establish them. This causes PARTIAL scores on c2, c3, and c12. Additionally, the 'establish baseline by July 7' KRs (Obj1 KR2, KR3) are effectively binary milestones, not spectrum-based outcomes, causing PARTIAL on c6 and c16. Despite these gaps, the output earns 86.5% by satisfying the structural, qualitative, measurement, file output, and parent-objective linkage criteria cleanly.
