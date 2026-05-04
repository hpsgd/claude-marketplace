# Rollback Assessment

Scenario: Developer invokes the rollback-assessment skill after deploying v3.0.1 — 20 minutes post-deploy, error rate on `/api/invoices` climbed from 0.1% to 8%, and two customers have raised support tickets about invoice generation failures.

## Prompt

> Assess rollback for v3.0.1. Deployed 20 minutes ago. Seeing: error rate on `/api/invoices` jumped from 0.1% (baseline) to 8%. p95 latency on that endpoint went from 220ms to 1.8s. Two support tickets in the last 15 minutes — customers can't generate invoices. The release included: a refactor of the invoice calculation logic, a DB migration adding a `tax_rate` column (non-nullable with default 0), and a dependency upgrade for our PDF library. No feature flags were used — it was a big-bang deploy.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Rollback Assessment: v3.0.1

### Signal
| Signal | Baseline | Current | Threshold | Exceeded? |
|---|---|---|---|---|
| Error rate (`/api/invoices`) | 0.1% | 8% | >2x for 5 min | **YES** (80x) |
| p95 latency (`/api/invoices`) | 220ms | 1,800ms | >3x for 5 min | **YES** (8.2x) |
| Support tickets (invoices) | ~0 in 15 min | 2 in 15 min | >3x normal/hour | **YES** (elevated) |

### Verification
- **False positive ruled out:** No — these are real, measured signals across three independent systems (metrics + support queue). The error rate and latency spikes are dramatic and specific to a single endpoint.
- **Correlated with release:** Yes — deployment completed ~20 minutes ago, signals appeared immediately after. Timing is too tight to be coincidental.
- **External factors ruled out:** No indication of external outage, traffic spike, or infrastructure failure. The spike is isolated to `/api/invoices`, not system-wide.

### Blast Radius
- **Users affected:** Unknown exact count, but enough for 2 support tickets in 15 minutes on a Friday. Invoice generation is likely to see a spike in requests at certain times of day — this could be escalating as more customers attempt to invoice.
- **Features affected:** Invoice generation (core financial feature). This is not a nice-to-have.
- **Trajectory:** Stable at 15-minute mark (2 tickets), but likely to grow if the deployment stays live. Financial operations often batch at end-of-day.
- **Severity:** High — customers cannot generate invoices, affecting immediate business operations and revenue tracking.

### Root Cause Hypothesis
Three changes bundled in this release; suspect invoice calculation refactor:

1. **Invoice calculation refactor** (HIGH suspicion) — The error is specific to `/api/invoices`. A refactor of core business logic often contains subtle bugs in edge cases (rounding, null handling, tax calculation logic). The spike in both error rate and latency suggests the code is either crashing or taking a wrong path.
2. **DB migration** (MEDIUM suspicion) — Non-nullable `tax_rate` column with default 0. Could cause: constraint violations if old code doesn't populate it, query performance degradation from index scans, or locking during the migration. But this would manifest differently (usually lock timeouts or constraint errors on insert).
3. **PDF library upgrade** (MEDIUM suspicion) — If invoices are rendered to PDF, the upgrade could break rendering. Would manifest as errors during generation.

**Confidence:** Medium. The error is clearly in this release, and the invoice calculation refactor is the most likely culprit given the symptom, but without seeing the diff or logs, we can't pinpoint the exact line.

### Decision: **ROLLBACK**

**Reasoning:**
This hits multiple rollback criteria simultaneously:
1. **Error rate threshold exceeded** — 80x baseline (far exceeds the 2x threshold)
2. **Latency threshold exceeded** — 8.2x baseline (far exceeds the 3x threshold)
3. **Financial feature affected** — invoicing is core to the business; customers actively lose money if they can't generate invoices
4. **Multiple changes bundled** — three separate changes (refactor + migration + dependency) with no feature flags to isolate
5. **Root cause unclear** — medium confidence hypothesis is not high enough to forward-fix on a financial endpoint
6. **Time to forward-fix** — would require: identify which change caused it (10 min), fix it (10 min), test (10 min), deploy (5 min) = 35+ minutes. Rollback is 5-10 minutes.

**When in doubt, roll back.** In this case, we're not even in doubt — three separate thresholds are exceeded.

### Execution Plan

1. **Rollback to v3.0.0** — redeploy the previous stable version via your CI/CD pipeline (likely: git revert + push, or manual deployment from previous tag)
2. **Verify signal resolution** — confirm within 2 minutes that:
   - Error rate on `/api/invoices` drops below 1%
   - p95 latency returns to ~220ms range
   - New support tickets stop coming in
3. **Notify stakeholders** — send to #engineering and #support immediately:
   - What: v3.0.1 rolled back to v3.0.0
   - Why: Error rate spike on invoice generation (8% vs 0.1% baseline)
   - Status: Service restored, customers can generate invoices again
   - Next: Investigating root cause, will re-deploy with feature flags
4. **Update incident tracking** — if you use incident management, log this as SEV-2 (feature broken, customers affected, resolved)

### Post-Action

- **Verify resolution:** Confirm all three signals (error rate, latency, support tickets) have returned to baseline within 5 minutes of rollback completion. Do not declare "done" until you've checked.
- **Notify support:** Let them know invoicing is working again and provide a short message for customers who contacted them.
- **Retrospective scheduled:** Within 48 hours. Investigate:
  - Why were three major changes bundled in one release?
  - Why were there no feature flags?
  - Which change caused the issue? (revert one at a time if needed)
  - What testing gap let this through?
- **Plan the re-deploy:** For the next attempt:
  - Split this release: dependency upgrade separately, DB migration separately, calculation refactor separately — or use feature flags to roll out each change independently
  - Add acceptance tests for invoice calculation (edge cases like zero tax, high values, negative adjustments)
  - Canary deploy: roll out to 10% of traffic first, monitor for 10 minutes before 100%

---

**Action:** Roll back to v3.0.0 now. You have clear thresholds exceeded and financial operations at stake. The retrospective will tell you how to prevent this next time.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/18.0 (86%) |
| Evaluated | 2026-05-04 |
| Target duration | 36645 ms |
| Target cost | $0.1033 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill classifies the signal correctly — error rate spike (High urgency) + health impact — and does not downplay severity | PASS | Blast Radius section states 'Severity: High — customers cannot generate invoices, affecting immediate business operations and revenue tracking.' Signal table marks all three thresholds as 'YES' exceeded. Decision section opens with 'ROLLBACK' in bold. |
| c2 | Skill applies the verification step — checks the signal is real, correlated with the release timing, and not a false positive or external factor | PASS | Dedicated '### Verification' section with three explicit checks: 'False positive ruled out: No — real, measured signals across three independent systems'; 'Correlated with release: Yes — deployment completed ~20 minutes ago, signals appeared immediately after'; 'External factors ruled out: No indication of external outage, traffic spike, or infrastructure failure.' |
| c3 | Skill assesses blast radius — quantifies affected users/requests, identifies trajectory (growing/stable/shrinking) | PASS | '### Blast Radius' section identifies affected feature (invoice generation, core financial), notes '2 support tickets in 15 minutes on a Friday', and explicitly addresses trajectory: 'Stable at 15-minute mark (2 tickets), but likely to grow if the deployment stays live. Financial operations often batch at end-of-day.' |
| c4 | Skill applies the rollback threshold criteria — error rate >2x baseline for 5 minutes is the threshold, and 8% vs 0.1% baseline clearly exceeds it | PASS | Signal table column 'Threshold' shows '>2x for 5 min' for error rate and 'Exceeded? YES (80x)'. Decision reasoning states: 'Error rate threshold exceeded — 80x baseline (far exceeds the 2x threshold)'. |
| c5 | Skill recommends ROLLBACK (not forward-fix) given: unknown root cause confidence, wide blast radius, no feature flag available, and threshold exceeded | PASS | Decision is 'ROLLBACK' with five numbered reasons including: 'Root cause unclear — medium confidence hypothesis is not high enough to forward-fix on a financial endpoint', 'Multiple changes bundled — three separate changes (refactor + migration + dependency) with no feature flags to isolate', 'Error rate threshold exceeded', and financial blast radius. |
| c6 | Skill identifies the big-bang deploy as the reason rollback is slower (full redeploy) vs feature flag (toggle off) | PARTIAL | Output notes 'Rollback is 5-10 minutes' and the execution plan specifies 'redeploy the previous stable version via your CI/CD pipeline'. Post-action mentions 'use feature flags to roll out each change independently' as a future lesson. However, the explicit comparison — 'big-bang deploy requires full redeploy (5-10 min) whereas a feature flag would have enabled an instant toggle' — is never stated directly. |
| c7 | Skill specifies post-rollback verification — confirm error rate returns to baseline before declaring resolution | PASS | Post-Action: 'Confirm all three signals (error rate, latency, support tickets) have returned to baseline within 5 minutes of rollback completion. Do not declare done until you've checked.' Execution Plan step 2 adds: 'Error rate on /api/invoices drops below 1%, p95 latency returns to ~220ms range'. |
| c8 | Skill narrows the root cause hypothesis to the three changes (invoice refactor, migration, PDF library upgrade) and rates confidence level for each | PARTIAL | Root Cause Hypothesis section lists all three: 'Invoice calculation refactor (HIGH suspicion)', 'DB migration (MEDIUM suspicion)', 'PDF library upgrade (MEDIUM suspicion)', with per-change reasoning. Ceiling is PARTIAL. |
| c9 | Output includes Signal table, Verification, Blast Radius, Root Cause Hypothesis, Decision with reasoning, Execution Plan, and Post-Action steps | PASS | All seven required sections are present with markdown headers: '### Signal' (table), '### Verification', '### Blast Radius', '### Root Cause Hypothesis', '### Decision: ROLLBACK' with 'Reasoning:', '### Execution Plan', '### Post-Action'. |
| c10 | Output's signal table lists the exact prompt facts — error rate jumped from 0.1% baseline to 8% (80x), p95 went from 220ms to 1.8s (8x), 2 support tickets in 15 min, 20 minutes since deploy — with the timestamp anchors | PASS | Signal table rows show: '0.1%' baseline → '8%' current, 'YES (80x)'; '220ms' → '1,800ms', 'YES (8.2x)'; '~0 in 15 min' → '2 in 15 min'. The '20 minutes since deploy' timestamp anchor appears in Verification: 'deployment completed ~20 minutes ago, signals appeared immediately after'. |
| c11 | Output's verification step correlates the spike with the deploy timestamp (20 min ago) and rules out external factors (no upstream provider outage, no traffic spike, no adjacent unrelated deploy) | PASS | Verification states: 'Correlated with release: Yes — deployment completed ~20 minutes ago, signals appeared immediately after. Timing is too tight to be coincidental.' And: 'External factors ruled out: No indication of external outage, traffic spike, or infrastructure failure. The spike is isolated to /api/invoices, not system-wide.' |
| c12 | Output's blast radius quantifies affected requests/customers — e.g. "8% of `/api/invoices` traffic affected; if endpoint runs at X req/min, that's Y failed invoice generations per minute" — and notes the trajectory is growing (2 tickets in 15 min suggests more pending) | PARTIAL | Trajectory is present: 'Stable at 15-minute mark (2 tickets), but likely to grow if the deployment stays live. Financial operations often batch at end-of-day.' However, the absolute quantification ('if endpoint runs at X req/min, that's Y failed per minute') is absent — output states 'Unknown exact count' and makes no attempt to calculate absolute failure volume from the 8% error rate. |
| c13 | Output applies the rollback threshold rule explicitly — "error rate >2x baseline for ≥5 min triggers rollback; we have 80x for ≥15 min" — and concludes the threshold is decisively breached | PASS | Signal table shows threshold '>2x for 5 min' and 'YES (80x)'. Decision states 'Error rate threshold exceeded — 80x baseline (far exceeds the 2x threshold)'. The 20-minute post-deploy context implies ≥15 minutes above threshold. The conclusion 'far exceeds' conveys decisive breach. |
| c14 | Output recommends ROLLBACK (not forward-fix) and names the four reasons: unknown root cause confidence, wide blast radius, no feature flag toggle, threshold exceeded for >5 minutes | PASS | Decision section lists five numbered reasons covering all four: (1) 'Error rate threshold exceeded — 80x baseline'; (2) 'Financial feature affected'; (3) 'Multiple changes bundled... with no feature flags to isolate'; (4) 'Root cause unclear — medium confidence hypothesis is not high enough to forward-fix'; (5) time-to-forward-fix comparison (35+ min vs 5-10 min rollback). |
| c15 | Output flags the big-bang deploy as the reason rollback is slower (full redeploy of the previous artefact) — and quantifies the expected rollback duration | PARTIAL | Rollback duration is quantified: 'Rollback is 5-10 minutes'. Execution plan specifies 'redeploy the previous stable version via your CI/CD pipeline'. But the output does not explicitly state 'because this was a big-bang deploy without feature flags, rollback requires a full artefact redeploy rather than an instant flag toggle' — the causal connection between deploy strategy and rollback mechanism/speed is implicit at best. |
| c16 | Output's root cause hypothesis lists all three changes (invoice refactor, `tax_rate` migration, PDF library upgrade) with a confidence rating and reasoning per — e.g. migration is high suspicion if non-nullable default-0 doesn't match expected per-customer rates; refactor is medium; PDF library is low unless it touches calculation | PARTIAL | All three changes are listed with ratings (refactor HIGH, migration MEDIUM, PDF library MEDIUM) and per-change reasoning. However, the priority ordering is inverted from the criterion's suggested analysis (refactor HIGH vs migration HIGH). The specific concern about `tax_rate` default-0 not matching expected per-customer tax rates is absent — migration reasoning only addresses constraint violations and query performance. PDF library is rated MEDIUM without strong justification rather than LOW. |
| c17 | Output's execution plan includes specific steps — initiate redeploy of previous version, decide whether to roll back the migration (and how — `tax_rate` column with default may be safe to leave; the `subscription_events` table is additive so it stays), notify support, watch error rate | PARTIAL | Execution plan includes: redeploy step ('Rollback to v3.0.0'), verification of signals ('watch error rate'), and stakeholder notification ('Notify stakeholders — send to #engineering and #support'). However, the DB migration rollback decision is entirely absent — the plan says nothing about whether to roll back the `tax_rate` schema change, whether it is safe to leave in place, or how to handle it. This is a material omission given the migration is one of three release changes. |
| c18 | Output's post-rollback verification requires confirming error rate returns to the 0.1% baseline AND p95 returns to ~220ms BEFORE declaring resolution — not just "errors stopped climbing" | PASS | Execution Plan step 2: 'Error rate on /api/invoices drops below 1%' and 'p95 latency returns to ~220ms range'. Post-Action: 'Confirm all three signals (error rate, latency, support tickets) have returned to baseline within 5 minutes of rollback completion. Do not declare done until you've checked.' Both specific metrics are required before resolution is declared. |
| c19 | Output's post-action steps include a blameless retro to identify why no feature flag was used, why the staging tests didn't catch this, and whether this category of change should have a stricter gate | PARTIAL | Post-Action retrospective covers: 'Why were there no feature flags?' and 'What testing gap let this through?' (covers staging tests). Missing is an explicit question about 'whether this category of change (calculation refactor + non-nullable migration) should have a stricter deployment gate.' The retro questions are present but incomplete against the criterion's three specific items. Ceiling is PARTIAL. |

### Notes

The output is a strong, well-structured rollback assessment that correctly identifies the severity, applies the threshold criteria explicitly (80x baseline), recommends rollback with clear reasoning, and includes all required sections. The main gaps are: (1) the DB migration rollback decision is completely absent from the execution plan — a critical omission since the `tax_rate` column adds schema complexity to rollback sequencing; (2) absolute blast radius quantification is skipped ('unknown exact count') rather than estimated from the 8% error rate; (3) the explicit causal link between big-bang deploy strategy and full-redeploy rollback mechanism (vs feature flag toggle) is implied but never stated; and (4) the root cause priority ordering is inverted from what the criterion suggests — the migration's default-0 tax rate concern (the sharpest diagnostic signal) is under-weighted relative to the refactor. Despite these gaps, the output scores above the PASS threshold at 86.1%.
