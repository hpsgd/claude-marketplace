# Result: Rollback assessment after deployment causes elevated errors

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16/19 criteria met (84%) |
| **Evaluated** | 2026-04-29 |
| **Skill source** | `plugins/engineering/release-manager/skills/rollback-assessment/SKILL.md` |

---

## Results

### Criteria

- [x] PASS: Skill classifies the signal correctly — error rate spike (High urgency) + health impact — and does not downplay severity. Step 1 table classifies "Error rate spike" as "High — users are failing" and "Latency degradation" as "High — users are waiting." The rule "Multiple signals compound urgency — if you see error rate AND latency, treat as the higher urgency" is explicit.
- [x] PASS: Skill applies the verification step — checks the signal is real, correlated with the release timing, and not a false positive or external factor. Step 2 defines all three checks: false positive (monitoring health, multiple vantage points), pre-existing baseline comparison, timing correlation, and external factors. The 5-minute cap on verification for critical signals is stated.
- [x] PASS: Skill assesses blast radius — quantifies affected users/requests, identifies trajectory (growing/stable/shrinking). Step 3 requires quantification ("approximately 15% of requests failing is actionable; 'Some users are affected' is not") and lists trajectory as a required dimension with escalation rules for each state.
- [x] PASS: Skill applies the rollback threshold criteria — error rate >2x baseline for 5 minutes is the threshold, and 8% vs 0.1% baseline clearly exceeds it. Step 5 decision table states: "Error rate | >2x baseline for 5 minutes | Rollback." The scenario is 80x baseline.
- [x] PASS: Skill recommends ROLLBACK (not forward-fix) given: unknown root cause confidence, wide blast radius, no feature flag available, and threshold exceeded. Step 5 "Rollback when" list covers all four conditions. Forward-fix requires ALL conditions including high-confidence root cause — not met here.
- [x] PASS: Skill identifies the big-bang deploy as the reason rollback is slower (full redeploy) vs feature flag (toggle off). Step 6 execution table contrasts "Feature flag → Toggle flag off → Seconds" with "Standard deploy → Redeploy previous version → 5–10 minutes."
- [x] PASS: Skill specifies post-rollback verification — confirm error rate returns to baseline before declaring resolution. Step 6 requires "Verify resolution — confirm the signal that triggered the assessment has returned to baseline." Step 7 strengthens this: "confirm ALL signals have returned to baseline, not just the primary one." Anti-patterns section names "No post-rollback verification" explicitly.
- [~] PARTIAL: Skill narrows the root cause hypothesis to the three changes (invoice refactor, migration, PDF library upgrade) and rates confidence level for each. Step 4 instructs reviewing release scope, correlating each change with the signal, and rating confidence. However, the output template provides a single `Suspected cause` and single `Confidence` field — it does not enforce per-change confidence ratings. An agent would surface all three candidates in analysis but the template pulls them into a composite rating rather than a per-change table.
- [x] PASS: Output includes Signal table, Verification, Blast Radius, Root Cause Hypothesis, Decision with reasoning, Execution Plan, and Post-Action steps. The Output section defines all seven sections with required sub-fields and a prescriptive template.

### Output expectations

- [x] PASS: Output's signal table lists the exact prompt facts — error rate jumped from 0.1% baseline to 8% (80x), p95 went from 220ms to 1.8s (8x), 2 support tickets in 15 min, 20 minutes since deploy — with the timestamp anchors. Step 1 mandates recording "metric name, current value, normal baseline, when it started" and the Signal table template captures Baseline/Current/Threshold/Exceeded.
- [x] PASS: Output's verification step correlates the spike with the deploy timestamp (20 min ago) and rules out external factors. Step 2 explicitly covers all three checks: timing correlation with deploy, false positive ruling (monitoring health), and external factors (third-party outage, traffic spike, infrastructure event).
- [x] PASS: Output's blast radius quantifies affected requests/customers and notes trajectory. Step 3 mandates quantification and trajectory as a required dimension ("Growing blast radius = escalate urgency"). An agent following Step 3 would estimate requests/min at 8% failure and note the growing ticket pattern.
- [x] PASS: Output applies the rollback threshold rule explicitly. Step 5 decision table provides the exact rule ("Error rate | >2x baseline for 5 minutes | Rollback"), and an agent citing this table would produce the "80x for ≥15 min" calculation the criterion requires.
- [x] PASS: Output recommends ROLLBACK and names the four reasons: unknown root cause confidence, wide blast radius, no feature flag toggle, threshold exceeded for >5 minutes. Step 5 "Rollback when" covers all four; "When in doubt, roll back" is the cardinal rule.
- [x] PASS: Output flags the big-bang deploy as the reason rollback is slower and quantifies expected duration. Step 6 table gives "Standard deploy → Redeploy previous version → 5–10 minutes" — an agent would cite this directly.
- [~] PARTIAL: Output's root cause hypothesis lists all three changes with a confidence rating and reasoning per change. Step 4 instructs correlating each change with the signal and rating confidence, but the output template collapses this into a single `Suspected cause` / `Confidence` pair. An agent producing a per-change table would be following Step 4's process but overriding the template. The template gap means this is not reliably enforced.
- [~] PARTIAL: Output's execution plan includes specific steps including a decision on whether to roll back the migration. Step 6 covers redeploy, verify, and notify. The migration rollback decision is addressed in Step 5's forward-fix criteria ("rolling back a migration that has already been applied to production data") but the execution plan template and Step 6 instructions do not specifically prompt the agent to surface the migration decision as a distinct step. An agent would likely include it as a note but the skill does not enforce it.
- [x] PASS: Output's post-rollback verification requires confirming error rate returns to 0.1% baseline AND p95 returns to ~220ms before declaring resolution. Step 7 explicitly says "confirm ALL signals have returned to baseline, not just the primary one."
- [~] PARTIAL: Output's post-action steps include a blameless retro addressing why no feature flag was used, why staging tests didn't catch this, and whether this category of change needs a stricter gate. Step 7 schedules a retrospective and mentions "understand what gates missed the issue" — but does not enumerate the three specific sub-questions. An agent would run a retro but would not reliably surface all three angles without prompting.

---

## Notes

The skill is well-constructed. The 7-step sequential structure, the decision table with explicit thresholds, and the cardinal rule ("when in doubt, roll back") set the right disposition for a time-pressured incident response skill. The anti-patterns section is particularly strong — naming "No post-rollback verification" and "Forward-fixing when root cause is unknown" as explicit failure modes steers agents away from the most common mistakes.

Two structural gaps recur across both the Criteria and Output expectations sections. First, the root cause hypothesis template (single `Suspected cause` / `Confidence` pair) doesn't match the Step 4 process that asks for per-change correlation and confidence. In a multi-change release, this means the structured output will compress what should be a table into a sentence. Widening the template to a per-change table would close this without changing the process logic.

Second, the execution plan in Step 6 doesn't explicitly address DB migration handling as a rollback consideration. The skill surfaces this in Step 5's forward-fix criteria ("rolling back a migration that has already been applied to production data"), but by Step 6 the decision is already made and the migration question may not resurface. Adding a migration checkpoint to Step 6 ("If the release included schema migrations, assess whether rolling back the application code is sufficient or whether the migration also needs to be reversed") would make this reliable.

The retrospective in Step 7 mentions "what gates missed the issue" but doesn't enumerate the sub-questions an agent should bring to that retro. For a skill that ends at the point of resolution, this is a minor gap — the retro is out of scope for the assessment itself.
