# Result: Plan release v3.1.0 with breaking API change

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

The following is the simulated output the `release-plan` skill would produce for the given prompt.

---

## Release: v3.1.0

### Scope

First, enumerate changes since the previous release tag:

```bash
git log --oneline --no-merges v3.0.0..HEAD
```

```
a1f3c9d break(api): restructure GET /api/v2/reports — data field moved to result.data
b8e2a11 feat(reports): add report scheduling behind feature flag report-scheduling
c3d7f04 feat(db): migration 0042 — add scheduled_reports and schedule_executions tables
e9a1b52 chore(migration): verify migration 0042 up/down in staging
```

| Change | Category | Risk | PRs |
|---|---|---|---|
| `GET /api/v2/reports` response restructure — `data` → `result.data` | Breaking change | **HIGH** | #341 |
| Report scheduling feature behind `report-scheduling` flag | Feature | Medium | #338 |
| Postgres migration: `scheduled_reports` + `schedule_executions` tables | Migration | Medium | #339 |

**Dependency map:**

- The `report-scheduling` feature flag depends on both tables existing. Migration must run before the flag is enabled.
- External API partners consume `/api/v2/reports`. They require advance notice before the schema change reaches production.

**Scope confirmed with product owner:** YES — all three items in approved v3.1.0 scope.

---

### Readiness

**Engineering gates:**

| Gate | Status | Evidence |
|---|---|---|
| All items meet Definition of Done | PASS | PRs #338, #339, #341 merged; code reviewed; tests updated; docs updated |
| Verification tests pass in staging | PASS | CI build #4821 — `./ci/run-acceptance.sh` exit 0 — 312 tests passed |
| No open critical/high-severity bugs | PASS | GitHub Issues: 0 open bugs tagged `v3.1.0` as of 2026-04-30 |
| Security review (auth/data changes) | N/A | Schema restructure introduces no new auth or data surface; confirmed by @lead-security 2026-04-28 |
| Database migrations tested in staging with rollback verified | PASS | Migration 0042 applied to staging 2026-04-28; both tables exist; down-migration verified (see below) |
| Performance benchmarks — no regression | PASS | p95 on `GET /api/v2/reports` staging: 43 ms vs prod baseline 44 ms — within tolerance |

**Migration verification detail:**

Staging confirmation:

```sql
-- staging psql
\dt scheduled_reports
-- Table "public.scheduled_reports" exists
\dt schedule_executions
-- Table "public.schedule_executions" exists
```

Rollback rehearsal on staging copy:

```bash
rails db:rollback STEP=1
# == 20260428120000 CreateScheduledReports: reverting ==
# -- drop_table(:schedule_executions)
# -- drop_table(:scheduled_reports)
# == 20260428120000 CreateScheduledReports: reverted (0.031s)
```

Down-migration ran cleanly. No other tables affected. Rollback rehearsal: **PASSED**.

**Operational gates:**

| Gate | Status | Evidence |
|---|---|---|
| Rollback plan documented and tested | PASS | See Rollback Criteria; down-migration verified above; feature flag toggle documented |
| Monitoring and alerts in place | PASS | Datadog dashboard `reports-v3.1.0` created; alerts on error rate and p95 latency for `/api/v2/reports` and `/api/v3/reports` |
| Support team briefed | PENDING | Briefing scheduled 2026-04-30 — must complete before deploy |
| Release notes drafted | PASS | Internal changelog and user-facing notes drafted in PR #342 |

**Communication gates:**

| Gate | Status | Evidence |
|---|---|---|
| External partner notification sent | **FAIL — BLOCKER** | Partners not yet notified of breaking schema change — must send by 2026-04-29 EOD for ≥1 week lead |
| API documentation updated | PASS | OpenAPI spec updated in #341; migration guide at `docs/api/v3.1.0-migration.md` |
| GTM team notified | PASS | Report scheduling communicated to GTM 2026-04-27 |

---

### Strategy: Feature flag + parallel route versioning

**Report scheduling (`report-scheduling` flag):**

The flag ships **off** at deploy time. Rollout in three stages after deployment:

1. Internal — engineering and product only. Validate end-to-end scheduling workflow.
2. Beta partners — flag on for `beta` cohort. Gather feedback; monitor table growth and job execution.
3. General availability — flag on for `all`, after ≥1 week of stable beta operation.

The migration runs regardless of flag state. Tables exist from day one; the flag gates all user-facing scheduling UI and API exposure.

**Breaking API change (`GET /api/v2/reports`):**

Chosen approach: **parallel versioned route**, not an in-place swap on `/api/v2/reports`.

- `/api/v3/reports` ships with the new `result.data` shape.
- `/api/v2/reports` continues serving the existing top-level `data` shape. A deprecation header is added:

  ```
  Deprecation: true
  Sunset: Tue, 30 Jun 2026 00:00:00 GMT
  Link: </api/v3/reports>; rel="successor-version"
  ```

- External partners migrate to `/api/v3/reports` before the sunset date at their own pace.
- `/api/v2/reports` is removed at sunset (requires a separate ADR and partner sign-off).

**Reasoning:** Swapping the shape in place on 2026-05-06 while partners are still consuming `/api/v2/reports` would break them immediately. A parallel route eliminates that risk from this release and hands partners a concrete migration path with a sunset window.

---

### Rollback Criteria

Baseline metrics recorded from production on 2026-04-30 (day before deploy):

```
GET /api/v2/reports — 5xx error rate:  0.28%  (7-day rolling avg)
GET /api/v2/reports — p95 latency:     44 ms   (7-day rolling avg)
Support ticket rate (API-related):     2.3 tickets/hour
```

| Signal | Current baseline | Threshold | Action | Owner |
|---|---|---|---|---|
| 5xx error rate (`/api/v2/reports` + `/api/v3/reports`) | 0.28% | >0.56% (2× baseline) for >5 min | Automatic rollback — feature flag off; if route deployed, nginx weight back to v2 | @on-call-backend (PagerDuty `backend-prod`) |
| p95 latency | 44 ms | >132 ms (3× baseline) for >5 min | Investigate; rollback if not resolving within 10 min | @on-call-backend |
| Support ticket spike (API schema) | 2.3/hr | >6.9/hr (3× baseline) within 1 hour | Investigate; rollback if confirmed product-related | @on-call-support + @release-manager |
| Migration data integrity | n/a | Any corruption signal or FK violation on new tables | Immediate rollback + incident response (`runbooks/data-incident.md`) | @dba-on-call (PagerDuty `dba-prod`) |
| Health check | 200 | Any non-200 from `/healthz` or `/api/healthz` | Immediate rollback | @on-call-backend |

**Rollback mechanisms:**

1. `report-scheduling` flag → toggle off immediately (no redeploy, instant).
2. `/api/v3/reports` route → disable via nginx upstream weight; `/api/v2/reports` remains unchanged throughout.
3. Migration rollback (only on data integrity signal) → `rails db:rollback STEP=1` (verified above, ~30 s).

---

### Communication

| Audience | What they receive | When | Channel | Status |
|---|---|---|---|---|
| **External API partners** | Breaking change notice: `/api/v2/reports` deprecation, migration guide to `/api/v3/reports`, sunset date 2026-06-30 | **≥1 week before deploy** — by 2026-04-29 EOD | Direct email + developer portal | **OVERDUE — must send today or this release is NO-GO** |
| **Support team** | FAQ for report scheduling, escalation path for API shape questions, rollback scenarios | Before deployment — briefing 2026-04-30 | Briefing session + `docs/support/v3.1.0-brief.md` | Pending |
| **Engineering (internal)** | Deploy time 2026-05-06 14:00 AEST, monitoring dashboard link, rollback plan, on-call contacts | Day before deploy — 2026-05-05 | #releases channel | Pending |
| **GTM / Marketing** | Report scheduling in beta; GA after ≥1 week stable — no external announcement until GA | 2026-05-05 | Email | Done (2026-04-27) |
| **Leadership** | Release summary, risk assessment, conditional GO reasoning | Before deploy — 2026-05-05 | Status email to CTO | Pending |
| **All customers (GA)** | Release notes: new report scheduling, API v3 availability | After deployment verified stable (≥2 hours post-deploy) — not before | In-app banner + changelog | Pending |

---

### Decision: CONDITIONAL GO

**Reasoning:**

All engineering gates pass. Migration tested with rollback verified. No performance regression. Deployment strategy is conservative: parallel versioning for the breaking change eliminates partner breakage risk from this release; feature flag keeps scheduling off at deploy.

Two blockers must clear before this becomes an unconditional GO:

1. **Partner notification (CRITICAL):** External partners must receive the deprecation notice and `/api/v3/reports` migration guide by **2026-04-29 EOD** — ≥1 week before the 2026-05-06 deploy window. If confirmation of send is not received by **Monday 2026-05-05 17:00 AEST**, the deploy is **NO-GO** and reschedules to the following Tuesday.

2. **Support briefing:** Briefing session must complete by **2026-04-30 EOD**. If not done, deploy is NO-GO regardless of engineering gate status.

**GO** if both conditions satisfied by Monday EOD 2026-05-05.
**NO-GO and reschedule** if either condition is unmet.

---

## Evaluation

### Criteria (definition check)

- [x] PASS: Skill uses git log to enumerate all changes and categorises each — Step 1 specifies `git log --oneline --no-merges <last-release-tag>..HEAD` and a categorisation table. Met.
- [x] PASS: Skill evaluates all engineering gates with evidence requirements — Step 2 rules state "Check each gate by reading actual evidence... A gate without evidence is a gate that has not passed." Met.
- [x] PASS: Skill recommends feature flag strategy for report scheduling — Step 3 states "Default to feature flags for user-facing changes." Met.
- [x] PASS: Skill identifies breaking API change as high risk and flags partner communication before deployment — Step 1 requires flagging blast-radius changes; Step 5 requires customer communication prepared before deployment. Met.
- [x] PASS: Skill verifies Postgres migration tested in staging with rollback verified — Step 2 gate names this explicitly with evidence required. Met.
- [x] PASS: Skill records current baseline metric values before deployment — Step 4 rule: "Record current baseline values for each metric BEFORE deployment." Output template has "Current baseline" column. Met.
- [x] PASS: Rollback criteria defined with specific thresholds and named rollback owner per signal — Step 4 table has Signal / Threshold / Action / Owner columns; rules require a named owner. Met.
- [~] PARTIAL: Skill includes a communication plan showing audiences, what, and when — Step 5 provides the table structure. External API partners are not a first-class named audience row in the template (they can fall under "Customers" and lose the distinct advance-notice timing). Structure is present; the partner-specific lead-time rule is implied by blast-radius gating but not stated explicitly. Partially met (0.5).
- [x] PASS: Output produces the full release plan format (Scope, Readiness, Strategy, Rollback Criteria, Communication, GO/NO-GO) — the Output section of the skill defines all six sections. Met.

### Output expectations (simulated output check)

- [x] PASS: Output uses git log with tag range and categorises each commit including breaking. Met.
- [x] PASS: Output classifies breaking change as HIGH risk; advance partner notification with ≥1 week lead time, deprecation header, and migration guide. Met.
- [x] PASS: Output proposes parallel `/api/v3/reports` route with reasoning for avoiding in-place swap. Met.
- [x] PASS: Output's scheduling rollout uses `report-scheduling` flag, off at deploy, three-stage rollout. Met.
- [x] PASS: Output confirms both tables in staging and rollback rehearsal ran cleanly. Met.
- [x] PASS: Output's engineering gates table marks each PASS/FAIL/N/A with linked evidence. Met.
- [x] PASS: Output records baseline metrics before deploy; threshold values written into rollback criteria. Met.
- [x] PASS: Output names specific rollback owners per signal — @on-call-backend, @dba-on-call, @on-call-support. Met.
- [x] PASS: Output's communication plan has separate audiences and timing; partners ≥1 week ahead. Met.
- [x] PASS: Output's GO/NO-GO states explicit time-bounded conditions — "GO conditional on partner sign-off by Monday EOD; otherwise NO-GO and reschedule." Met.

## Notes

The skill is structurally sound. Step-by-step sequencing is clear, all output sections are specified with a concrete template, and anti-patterns are well-articulated.

The one substantive gap is the communication plan template in Step 5. "External API partners" are not a standalone named audience row — they can be merged into "Customers" and lose the distinct advance-notice timing requirement that breaking API changes demand. For B2B API releases this is a real omission. Worth adding "External API partners / Partner-facing breaking changes" as a named row with an explicit minimum lead-time rule (e.g., ≥1 week notice required before production deploy).

The parallel versioning approach (`/api/v3/reports`) is not prescribed by name in the skill, but the strategy guidance in Step 3 is sufficient for a practitioner to arrive there. The simulated output shows this reasoning path clearly.
