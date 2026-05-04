# Release Coordination

Scenario: User needs to coordinate a release that includes database migrations, a new feature behind a feature flag, a dependency security patch, and a rollback plan — with support team briefing before go-live.

## Prompt

> We need to release v2.4.0 this Thursday. It includes:
> 1. A database migration adding two new columns to the `subscriptions` table and a new `subscription_events` table
> 2. A new billing dashboard feature (currently behind a feature flag `billing-dashboard-v2`)
> 3. A security patch for CVE-2024-38372 in one of our dependencies
> 4. Some internal refactoring of the subscription service
> 
> The migration has been tested on staging. The security patch bumps a minor version. Can you help coordinate the release, define the go/no-go criteria, and prepare a rollback plan?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Based on the repo state, let me build your comprehensive v2.4.0 release plan. I'll structure it per the 6-step process and flag what evidence I need from you.

## Release Plan: v2.4.0 (Deploy Thursday 2026-05-08)

### Step 1: Define Release Scope

| Change | Category | Risk | Status | Dependencies |
|---|---|---|---|---|
| New columns on `subscriptions` table + `subscription_events` table | Migration | **High** | Tested on staging | Must deploy before feature code |
| Billing dashboard v2 (behind `billing-dashboard-v2` flag) | Feature | Medium | Ready | Depends on migration |
| CVE-2024-38372 dependency patch (minor version bump) | Security | Medium | Ready | No dependencies |
| Subscription service refactoring | Enhancement | Low | Ready | Non-blocking |

**Blast radius:** Migration impacts all subscription flows. Billing dashboard is flag-gated (low blast). Security patch is standard dependency bump. Refactoring is internal.

**Critical dependency:** Database migration must be deployed and validated before the billing dashboard code runs in production.

---

### Step 2: Readiness Assessment

I need **evidence** for each gate. Here's what I need from you before we can mark gates as PASS:

| Gate | Evidence needed | Current status |
|---|---|---|
| **Code review** | PRs merged, reviewer sign-off for each of the 4 changes | ? |
| **Unit & integration tests** | Test command exit 0, coverage report for new code | ? |
| **Staging verification** | Acceptance test results from staging (includes migration rollback test) | Partial: migration tested ✓, feature flag tested? |
| **Security review** | CVE details reviewed, patch verified, any other auth/data changes audited | ? |
| **Performance baseline** | Current metrics (error rate, p95 latency, DB query time) recorded for comparison | ? |
| **Database migration** | Rollback script tested on staging data (not just forward migration) | Need verification |
| **Documentation** | Release notes drafted, API docs updated (if any endpoints changed) | ? |
| **Feature flag setup** | `billing-dashboard-v2` flag configured in production, can be toggled by ops | ? |

**Questions for you:**

1. Do you have test results showing all acceptance tests pass?
2. Has the migration rollback been tested (not just the forward migration)?
3. Is the feature flag wired up in production and tested?
4. What are your current baseline metrics (error rate %, p95 latency in ms, etc.)?
5. Has the security patch been reviewed against the CVE details?

---

### Step 3: Deployment Strategy

**Recommended: Hybrid approach**

| Component | Strategy | Why |
|---|---|---|
| Database migration | **Separate deploy (pre-feature code)** | Migrations are one-way; must succeed before feature code expects the schema |
| Billing dashboard | **Feature flag with percentage rollout** | New feature, flag-gated, allows safe validation in production before ramping to 100% |
| Security patch | **Big bang (standard deploy)** | Standard dependency update, non-breaking, low risk |
| Refactoring | **Big bang (standard deploy)** | Internal only, no user impact |

**Deployment sequence:**

```
1. Deploy migration in isolation → monitor 5 min → verify schema
2. Deploy code (features gated, patch included) → monitor 10 min
3. Enable billing-dashboard-v2 flag at 10% traffic
4. Monitor error rate, latency, support tickets for 30 min
5. If stable, ramp to 50%, then 100% (each step 30 min)
```

---

### Step 4: Define Rollback Criteria

**Before Thursday, I need you to provide:**

1. **Current baseline metrics** — what is "normal" for your system?
   - Error rate (errors per minute, or % of requests)
   - p95 latency (milliseconds)
   - Database query latency (milliseconds)
   - Support ticket volume (issues per hour)

Once I have these, I'll fill in the thresholds. For now, **draft criteria:**

| Signal | Trigger | Action | Owner |
|---|---|---|---|
| Error rate | >2x baseline for 5 min consecutive | Automatic: toggle `billing-dashboard-v2` to 0% |  |
| p95 latency | >3x baseline for 5 min | Investigate; if persists 10 min → toggle flag off |  |
| Database lock contention | Any subscription queries timing out (>2s) | Immediate: rollback migration → re-apply in maintenance window |  |
| Support spike | >3x normal ticket rate within 30 min with "subscription" or "billing" in subject | Investigate; if product-related → toggle flag off |  |
| Data corruption signal | Any alert from data validation checks | Immediate: rollback migration, contact incident commander |  |

**Rollback mechanisms:**

1. **Feature flag rollback** (instant): toggle `billing-dashboard-v2` to 0% in production control panel
2. **Migration rollback** (5-10 min): run rollback script (pre-tested on staging), verify with SELECT queries
3. **Code rollback** (15-20 min): deploy previous release tag

**Who rolls back?** Assign:
- Feature flag owner: [name + on-call contact]
- Database owner: [name + on-call contact]
- Release manager: [name + on-call contact]

---

### Step 5: Communication Plan

| Audience | Message | Timing | Owner | Channel |
|---|---|---|---|---|
| **Support team** | New billing dashboard behind flag, may see "Dashboard v2" in requests. Subscription schema changes (transparent to users). Rollback scenarios. | **Tuesday 5/6 AM** | Product Manager | Slack + written brief |
| **Engineering (on-call)** | Deploy sequence, monitoring dashboards, rollback contacts, escalation process. | **Wednesday 5/7 PM** | Release Manager | Team standup + doc |
| **Database team** | Migration sequence, rollback procedure, expected query load. | **Wednesday 5/7 PM** | DBA / DevOps | Ops channel |
| **Leadership** | Release summary, risk assessment, go/no-go decision. | **Thursday 5/8 AM (pre-deploy)** | Release Manager | Status update |
| **Customers** | What changed, what's new (once stable). Billing dashboard availability. | **Thursday 5/8 PM (post-validation)** | Product Manager | Release notes + email |

**Support brief template (fill in actual details):**

```markdown
### v2.4.0 Release Brief — Thursday 5/8

**What's shipping:**
- New billing dashboard (behind feature flag, starts at 10% traffic)
- Database schema update (two new columns, new events table)
- Security patch for [CVE details]

**What you need to know:**
- Users will see "Billing Dashboard v2" in UI if they're in the rollout cohort
- All subscription operations continue to work normally
- No action required from customers
- If issues arise, escalate to [on-call contact]

**Known edge cases:**
- [List any known issues or limitations]

**Rollback procedure:**
- If billing dashboard breaks: toggle feature flag off (instant)
- If database issues: revert migration (5-10 min, incident response)
- Support should NOT attempt rollback; escalate to on-call engineer
```

---

### Step 6: Go/No-Go Decision Framework

**GO criteria (all must be true):**
- ✓ All 4 readiness gates above show PASS with evidence
- ✓ Migration rollback tested and confirmed on staging
- ✓ Feature flag wired and tested in production
- ✓ Baseline metrics recorded
- ✓ Support briefed and FAQs prepared
- ✓ On-call contacts assigned and available Thursday
- ✓ Rollback owner confirmed for each component
- ✓ Security patch reviewed and approved

**NO-GO triggers:**
- Any readiness gate fails (tests, security review, migration rollback test)
- Feature flag not working in production
- On-call team unavailable Thursday
- Active incident in progress at deploy time
- Migration rollback not tested on staging data

**CONDITIONAL GO (requires CTO sign-off):**
- One non-critical gate pending (e.g., performance baseline not yet recorded, but not a blocker)
- Enhanced monitoring plan in place
- CTO approval documented in ticket/email

---

## What I Need From You This Week

**By Tuesday 5/6 (48 hours):**
1. Test results showing all tests pass
2. Baseline metrics (error rate, latency, DB query time — exact numbers)
3. Confirmation migration rollback has been tested on staging
4. Feature flag verified wired in production

**By Wednesday 5/7 (24 hours):**
1. Support team briefed
2. Rollback owners assigned (names + on-call contacts)
3. Release notes drafted
4. On-call availability confirmed for Thursday

**By Thursday 5/8 morning:**
1. Final go/no-go decision
2. Deployment sequence confirmed
3. Monitoring dashboards open
4. Incident commander on standby

---

## Next Steps

1. **Gather the evidence above** — reply with test results, metrics, and confirmations
2. **Run `/release-manager:rollback-assessment`** — I'll create a detailed rollback runbook once you confirm the metrics
3. **Pre-deploy validation** — test the migration rollback script one more time on staging Thursday morning
4. **Deploy** — follow the sequence (migration → code → flag ramp)

This framework ensures Thursday's deploy is reversible, communicated, and gated. What evidence can you provide first?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/18.0 (94%) |
| Evaluated | 2026-05-04 |
| Target duration | 44192 ms |
| Target cost | $0.0687 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent checks all engineering gates (tests, staging verification, security review, migration rollback verified) before issuing a go/no-go | PASS | Step 2 'Readiness Assessment' lists eight named gates with 'Evidence needed' per gate: code review, unit/integration tests, staging verification, security review, performance baseline, database migration rollback script, documentation, feature flag setup. Go/No-Go section requires 'All 4 readiness gates above show PASS with evidence'. |
| c2 | Agent recommends feature flag strategy for the billing dashboard feature — not big-bang deployment | PASS | Step 3 table: 'Feature flag with percentage rollout — New feature, flag-gated, allows safe validation in production before ramping to 100%'. Deployment sequence explicitly enables flag at 10%, waits 30 min, ramps to 50%, then 100%. |
| c3 | Agent defines rollback criteria with specific thresholds (error rate >2x baseline, p95 latency >3x baseline) and assigns a rollback owner | PASS | Rollback Criteria table: 'Error rate: >2x baseline for 5 min consecutive → toggle billing-dashboard-v2 to 0%'; 'p95 latency: >3x baseline for 5 min'. Rollback owner section requests '[name + on-call contact]' for Feature flag owner, Database owner, and Release manager. |
| c4 | Agent confirms support team must be briefed BEFORE deployment, not after | PASS | Communication plan: Support team brief is scheduled 'Tuesday 5/6 AM' (two days before Thursday deploy). 'What I Need From You This Week — By Wednesday 5/7: Support team briefed'. The brief template is included in the output. |
| c5 | Agent categorises each change by risk: migration (medium-high), security patch (low-medium), feature flag (low), refactoring (low) | PARTIAL | Scope table does categorise all four items by risk. Migration is 'High' (criterion expects medium-high — defensibly more conservative). Billing dashboard is 'Medium' rather than the expected 'low' for a flag-gated feature; the blast-radius note contradicts this ('low blast') but the table entry is wrong. Security patch is 'Medium' (criterion says low-medium). Refactoring is 'Low' (matches). The billing dashboard risk level is a clear mismatch from the expected classification. |
| c6 | Agent records current baseline metric values before deployment so rollback thresholds can be evaluated post-deploy | PASS | 'What I Need From You This Week — By Tuesday 5/6: Baseline metrics (error rate, latency, DB query time — exact numbers)'. Go/No-Go requires 'Baseline metrics recorded'. Readiness gate explicitly asks for 'Current metrics (error rate %, p95 latency in ms, etc.) recorded for comparison'. |
| c7 | Agent identifies the migration as requiring special attention — rollback of a migration that has already altered production data is different from code rollback | PASS | Rollback mechanisms list three separate mechanisms, with migration rollback explicitly distinct: 'Migration rollback (5-10 min): run rollback script (pre-tested on staging), verify with SELECT queries' vs 'Code rollback (15-20 min): deploy previous release tag'. Strategy table notes 'Migrations are one-way; must succeed before feature code expects the schema'. |
| c8 | Agent produces a structured output with Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and Decision | PARTIAL | All six components are present: Step 1 (Scope table), Step 2 (Readiness Assessment / gates), Step 3 (Deployment Strategy), Step 4 (Rollback Criteria), Step 5 (Communication Plan), Step 6 (Go/No-Go Decision Framework). Full coverage of the required structure. |
| c9 | Agent refuses to override a failed engineering gate under time pressure | PASS | Go/No-Go section: 'NO-GO triggers: Any readiness gate fails (tests, security review, migration rollback test)'. CONDITIONAL GO requires CTO sign-off only for 'one non-critical gate pending' with 'enhanced monitoring plan in place and CTO approval documented'. No pathway allows overriding a failed critical gate. |
| c10 | Output's scope table lists all four release items individually — migration (subscriptions columns + subscription_events table), billing dashboard feature, CVE-2024-38372 patch, subscription service refactor — with risk per item | PASS | Step 1 scope table rows: 'New columns on subscriptions table + subscription_events table — High'; 'Billing dashboard v2 (behind billing-dashboard-v2 flag) — Medium'; 'CVE-2024-38372 dependency patch (minor version bump) — Medium'; 'Subscription service refactoring — Low'. All four items listed with CVE identifier and risk. |
| c11 | Output's risk classification matches the asks: migration medium-high (data shape change + new table), security patch low-medium (named CVE, minor bump), feature flag low (off by default), refactor low (unless tests are weak), with reasoning per | PARTIAL | Refactoring is correctly 'Low'. Security patch 'Medium' is close to 'low-medium'. Migration 'High' vs expected 'medium-high' is a minor over-classification. Billing dashboard 'Medium' vs expected 'low' is a substantive mismatch — the criterion explicitly expects 'low' because the flag is off by default. The blast-radius note says 'low blast' for the billing dashboard, creating internal inconsistency. Reasoning is provided inline but the billing dashboard classification is wrong. |
| c12 | Output's go/no-go gates require evidence per gate — staging test pass with screenshot/log, migration applied + reverted on staging, security scan re-run, baseline metrics captured — not just 'team confirms' | PASS | Step 2 table has 'Evidence needed' column per gate: 'Test command exit 0, coverage report', 'Acceptance test results from staging', 'CVE details reviewed, patch verified', 'Rollback script tested on staging data (not just forward migration)'. Questions section explicitly asks for evidence artefacts, not team confirmation. |
| c13 | Output's rollback plan distinguishes code rollback (redeploy previous artefact) from data/migration rollback (the new columns/table either need a separate down-migration or a forward-fix-only policy if data was already written), naming which it is for THIS migration | PASS | Three distinct rollback mechanisms listed: '(1) Feature flag rollback (instant)', '(2) Migration rollback (5-10 min): run rollback script (pre-tested on staging), verify with SELECT queries', '(3) Code rollback (15-20 min): deploy previous release tag'. The migration rollback is named as a pre-tested rollback script (down-migration approach), distinct from code rollback. Does not address data-already-written edge case but names the approach. |
| c14 | Output's rollback thresholds are concrete and pre-defined — error rate >2x baseline, p95 latency >3x baseline (or similar), with the baseline values recorded BEFORE deploy so the comparison is well-defined | PASS | Rollback criteria table: 'Error rate: >2x baseline for 5 min consecutive', 'p95 latency: >3x baseline for 5 min', 'DB lock contention: subscription queries timing out >2s', 'Support spike: >3x normal ticket rate within 30 min'. Baseline must be captured before deploy per the 'By Tuesday 5/6' requirements. |
| c15 | Output assigns a named rollback owner (single accountable person, not 'the team') with on-call coverage for at least the post-deploy window | PASS | Rollback mechanisms section: 'Feature flag owner: [name + on-call contact]', 'Database owner: [name + on-call contact]', 'Release manager: [name + on-call contact]'. Three distinct single-person owners with explicit on-call contact field. Placeholders are correct given the agent doesn't know team membership. |
| c16 | Output's communication plan briefs the support team BEFORE deploy with the new feature flag state, the migration impact (none expected user-facing), and the support script for any billing dashboard questions | PASS | Support brief template includes: flag state ('behind feature flag, starts at 10% traffic'), migration impact ('Database schema update (two new columns, new events table)'), user-facing impact ('Users will see Dashboard v2 in UI if in rollout cohort'), escalation path, rollback procedure. Scheduled Tuesday 5/6, before Thursday deploy. |
| c17 | Output's feature flag strategy keeps `billing-dashboard-v2` off in production at deploy time, with a stated rollout plan (% rollout or whitelist of customers) AFTER the deploy is verified stable | PASS | Deployment sequence Step 2: 'Deploy code (features gated, patch included) → monitor 10 min' then Step 3: 'Enable billing-dashboard-v2 flag at 10% traffic'. Flag is explicitly off at code deploy. Staged rollout: 10% → 50% → 100%, each with 30-minute monitoring window before ramping. |
| c18 | Output explicitly states the agent will NOT override a failed engineering gate under Thursday-deadline pressure — if any gate fails, NO-GO and reschedule | PASS | Step 6 NO-GO triggers: 'Any readiness gate fails (tests, security review, migration rollback test)' is listed first. CONDITIONAL GO requires CTO sign-off only for 'one non-critical gate pending' with enhanced monitoring. No carve-out for deadline pressure. The 'What I Need From You This Week' section frames all gates as prerequisites, not optional. |
| c19 | Output's structured format covers Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and a final GO/NO-GO Decision with reasoning | PARTIAL | All six sections present and clearly headed: Step 1 (Scope table with 5-column table), Step 2 (Readiness Assessment with gates table), Step 3 (Deployment Strategy with component table and numbered sequence), Step 4 (Rollback Criteria with thresholds table and three mechanisms), Step 5 (Communication Plan with audience table and brief template), Step 6 (Go/No-Go Decision Framework with GO criteria, NO-GO triggers, and CONDITIONAL GO). Full structural coverage. |

### Notes

The output is comprehensive and well-structured, covering all major release coordination concerns with appropriate depth. The most notable gap is the risk classification for the billing dashboard feature: the output tables it as 'Medium' risk when the expected classification is 'low' (because it deploys behind a feature flag that is off by default), creating an internal inconsistency with the blast-radius note that correctly says 'low blast'. This affects both c5 and c11. The migration rollback treatment is solid in distinguishing it from code rollback but stops short of addressing the data-written-to-new-columns scenario (forward-fix-only vs down-migration choice if rows were inserted). The feature flag percentage rollout strategy, pre-deploy support briefing, concrete rollback thresholds, and evidence-based gates are all handled correctly and in the right sequence.
