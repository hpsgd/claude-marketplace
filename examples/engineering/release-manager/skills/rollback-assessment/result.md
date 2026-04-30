# Result: Rollback assessment after deployment causes elevated errors

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 17/19 criteria met (89%) |
| **Evaluated** | 2026-04-30 |
| **Skill source** | `plugins/engineering/release-manager/skills/rollback-assessment/SKILL.md` |

---

## Output

The following is a simulated output from the rollback-assessment skill given the v3.0.1 incident prompt.

---

## Rollback Assessment: v3.0.1

### Signal

| Signal | Baseline | Current | Threshold | Exceeded? |
|---|---|---|---|---|
| Error rate (`/api/invoices`) | 0.1% | 8% (80x) | >2x baseline for 5 min | YES — exceeded for ~15 min |
| p95 latency (`/api/invoices`) | 220ms | 1,800ms (8x) | >3x baseline for 5 min | YES — exceeded for ~15 min |
| Support tickets | ~0/hr | 2 in 15 min (~8/hr) | >3x normal rate/hour | YES |
| Health check failures | N/A | None reported | Any non-200 | NO |

**Assessment:** Deploy at T-20min. All three signal types triggered simultaneously and remain elevated. Multiple compounding signals — treating as High urgency per the "multiple signals compound urgency" rule.

### Verification

- **False positive ruled out:** monitoring system appears healthy — error rate spike is isolated to `/api/invoices`, not a global metrics failure. Other endpoints show normal error rates. Signal confirmed from two vantage points (APM + support tickets independently corroborate).
- **Correlated with release:** spike began within minutes of v3.0.1 deployment completing, 20 minutes ago. Pre-deploy baseline was 0.1% error rate. The timing alignment is direct. `git log --oneline -5` confirms v3.0.1 is the most recent change.
- **External factors ruled out:** no third-party outage in status pages checked (PDF provider, payment gateway). No marketing campaign or traffic event — request volume to `/api/invoices` is normal. No adjacent infrastructure event.

**Verdict:** Signal is real and release-correlated. Proceeding.

### Blast Radius

- **Users affected:** all users attempting to generate invoices — `/api/invoices` is a core billing endpoint, not a segment or feature-flagged path. No way to narrow to a subset.
- **Features affected:** invoice generation. Downstream effects: PDF export, automated billing emails, and finance reconciliation workflows likely affected if invoice generation is failing at source.
- **Quantified impact:** at 8% error rate, if `/api/invoices` receives 200 req/min (estimate), that is ~16 failed invoice generations per minute, ~320 failed generations in the 20 minutes since deploy.
- **Trajectory:** GROWING. Two support tickets in the first 15 minutes suggests the complaint queue is filling. Invoice generation failures are high-friction — customers notice immediately. Expect more tickets if not resolved.

**Escalation trigger:** growing blast radius with unknown root cause = rollback immediately per the cardinal rule.

### Root Cause Hypothesis

| Change | Suspicion | Confidence | Reasoning |
|---|---|---|---|
| DB migration — `tax_rate` column (non-nullable, default 0) | HIGH | High | Non-nullable `tax_rate` with default 0 means existing invoices calculate with 0% tax. If invoice calculation logic reads this column, all pre-migration customers get wrong totals. This would cause downstream validation errors if expected tax > 0, or produce wrong-but-not-erroring output. Latency spike is consistent with a calculation path hitting an unexpected value and retrying or throwing. |
| Invoice calculation refactor | MEDIUM | Medium | Refactor is the second most likely candidate — latency + error spike on the invoice endpoint is a strong match for a calculation logic bug. Without inspecting the diff, confidence is medium. Could be the primary cause or compounding with the migration. |
| PDF library dependency upgrade | LOW | Low | PDF rendering is downstream of calculation. Error spike at calculation level (8% error rate, not PDF generation failures specifically) makes this less likely as the primary cause. Cannot rule out entirely without inspecting the library changelog for breaking changes. |

**Overall confidence in having found the root cause:** LOW. All three candidates are plausible. The migration is the highest-probability single cause but the refactor may be the actual trigger or may compound it. This is a multi-change release with no feature flags — we cannot isolate.

### Decision: ROLLBACK

**Reasoning:**

1. **Threshold exceeded decisively.** Error rate is 80x baseline (threshold: >2x for 5 min). p95 latency is 8x baseline (threshold: >3x for 5 min). Both have been exceeded for approximately 15 minutes. The criteria are not marginal.
2. **Root cause is unknown.** Three plausible candidates exist. We cannot identify the specific cause with confidence in the 10-minute limit — forward-fixing blind is guessing.
3. **Blast radius is wide and growing.** All users hitting `/api/invoices` are affected. Two support tickets in 15 minutes indicates the blast radius is expanding, not stabilising.
4. **No feature flag available.** This was a big-bang deploy. There is no toggle to isolate or partially revert. The only fast mitigation is a full application rollback.

Forward-fix is not available: root cause not identified with high confidence, fix cannot be shipped within 15 minutes, and the issue is not isolated to a specific well-understood area.

**Forward-fix consideration for DB migration:** rolling back the application code will not undo the `tax_rate` column — it has been added to the production schema. If any invoice records have been written using the new schema in the last 20 minutes, running a down-migration would destroy that data. The column is additive with a default — the previous code version can tolerate it being present (the column did not exist before, so previous code does not reference it). **Policy: roll back the application code only. Do NOT run the down-migration. Assess migration handling separately after service is restored.**

### Execution Plan

1. **Initiate application rollback** — redeploy v3.0.0 (the previous release artifact). Mechanism: standard deploy (big-bang, no feature flag or blue/green). Expected rollback duration: **5-10 minutes**.
2. **Do NOT run DB down-migration.** The `tax_rate` column is additive and harmless to the previous code version. Running the down-migration risks destroying any invoice data written in the past 20 minutes. Escalate migration handling to the engineering lead after service is restored.
3. **Monitor during rollback** — watch error rate and p95 latency on `/api/invoices` actively during the redeploy.
4. **Notify support immediately** — inform them invoice generation is affected, a rollback is in progress, ETA ~10 minutes. Provide them a holding message for customers.
5. **Notify engineering** — rollback in progress, reason, expected completion.

### Post-Action

**Verify resolution before declaring done:**

- Confirm error rate on `/api/invoices` returns to 0.1% baseline (not just "stopped climbing" — confirm return to baseline)
- Confirm p95 latency returns to ~220ms
- Confirm both signals are stable at baseline for at least 5 minutes
- Check that customers who received errors have a clear path to retry their invoice generation

**Stakeholders to notify on resolution:**

| Audience | Message |
|---|---|
| Support | Invoice generation restored; customers can retry; brief summary of impact window |
| Engineering | Rollback complete, v3.0.0 running, post-mortem scheduled |
| Leadership | SEV summary — billing endpoint affected for ~30 minutes, service restored, RCA in progress |

**Retrospective scheduled within 48 hours.** Agenda:

1. Why was no feature flag used for the invoice calculation refactor? A change to billing logic is high-risk — should it require a flag by policy?
2. Why did staging not surface this? Was the `tax_rate` migration applied on staging? Were invoice generation flows tested against the migrated schema?
3. Should this category of change (billing logic + DB migration together) require a stricter deployment gate — e.g., mandatory canary deployment or a 1-hour soak on a subset of traffic before full rollout?
4. How should the `tax_rate` migration be re-attempted safely? (This needs a forward plan before v3.0.1 is re-deployed.)

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
