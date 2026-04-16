# Plan release v3.1.0 with breaking API change

Developer invokes the release-plan skill for v3.1.0, which includes a breaking change to the `/api/v2/reports` response schema, a new report scheduling feature, and a Postgres migration adding two tables.

## Prompt

> Plan release v3.1.0. It includes: (1) a breaking change to `GET /api/v2/reports` — the `data` field is now nested under `result.data` instead of at the top level, (2) a new report scheduling feature behind feature flag `report-scheduling`, (3) a Postgres migration adding `scheduled_reports` and `schedule_executions` tables. Some API consumers are external partners who need advance notice. Target deploy: next Tuesday.

## Output

**Step 1 — Define release scope:**

```bash
git log --oneline --no-merges <last-release-tag>..HEAD
```

| Change | Category | Risk | PRs |
|---|---|---|---|
| Breaking change `GET /api/v2/reports` — `data` → `result.data` | Enhancement | HIGH — external partners will break without migration | #421 |
| Report scheduling feature (flag `report-scheduling`) | Feature | LOW — flag off at deploy | #418 |
| Postgres migration: `scheduled_reports`, `schedule_executions` tables | Migration | HIGH — production schema change, rollback requires down-migration | #419 |

Breaking change blast radius: external partners consuming `GET /api/v2/reports` will receive malformed responses after deployment if they have not updated their integration. This is the widest blast radius in this release and requires advance communication BEFORE Tuesday.

**Step 2 — Readiness assessment (every gate checked with evidence):**

| Gate | Status | Evidence |
|---|---|---|
| All items meet Definition of Done | PASS/FAIL | [code review approvals, CI pass] |
| Verification tests pass in staging | PASS/FAIL | [vitest run output, exit code] |
| No open critical/high-severity bugs | PASS/FAIL | [issue tracker review] |
| Security review for auth/data changes | N/A | [no auth or PII changes in this scope] |
| DB migration tested in staging (rollback verified) | PASS/FAIL | [staging run log + down-migration tested] |
| Performance benchmarks met | PASS/FAIL | [benchmark comparison vs baseline] |
| Rollback plan documented | PASS/FAIL | [mechanism identified] |
| Support briefed | PASS/FAIL | [date + briefing document link] |
| API docs updated for breaking change | PASS/FAIL | [changelog entry + API docs updated] |
| External partners notified | PASS/FAIL | [notification sent, date] |

A gate without evidence is a gate that has not passed.

**Step 3 — Strategy:**

Report scheduling: feature flag (flag `report-scheduling` stays OFF at deploy). Feature not visible to users until explicitly toggled on after deployment verified stable.

Breaking API change: external partners must receive migration guide and advance notice BEFORE Tuesday's deployment. Partners still expecting `data` at top level will receive parsing errors after deployment. Communication must precede the release, not follow it.

Postgres migration: standard deploy with down-migration staged and verified. The migration creates two new tables — a down-migration drops them. If deployment is rolled back before any data is written, the down-migration is clean.

**Step 4 — Rollback criteria (baseline values recorded BEFORE deployment):**

| Signal | Current baseline | Threshold | Action | Owner |
|---|---|---|---|---|
| Error rate | [recorded pre-deploy] | >2x baseline for 5 min | Automatic rollback | [named person with deploy access] |
| p95 latency | [recorded pre-deploy] | >3x baseline for 5 min | Investigate; rollback if not resolving | [named person with deploy access] |
| Support ticket spike | [recorded pre-deploy rate] | >3x rate within 1 hour | Investigate; rollback if product-related | [named person] |
| Health check | Non-200 | Any non-200 | Immediate rollback | [named person with deploy access] |

**Step 5 — Communication plan:**

| Audience | What they need | When | Channel |
|---|---|---|---|
| External partners | Breaking change details, response schema diff (`data` → `result.data`), migration guide, timeline | Before deployment | Email + partner portal |
| Support | FAQ for report scheduling feature, known issues, escalation paths | Before deployment | Briefing document |
| Engineering | Deploy time, metrics to watch, rollback plan, on-call contact | Before deployment | Team channel |
| Leadership | Release summary, risk assessment (HIGH for breaking change) | Before deployment | Status update |
| Customers | Release notes (scheduling feature not yet visible; partner API change) | After verified stable | In-app changelog + email |

**Step 6 — Decision:**

GO if: all gates pass, external partners notified, migration down-migration staged and verified.

NO-GO if: migration rollback not verified in staging, external partners not notified, any engineering gate fails.

"Tuesday" is a target, not a reason to override a failed gate.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Skill uses git log to enumerate changes — release-plan SKILL.md Step 1 specifies `git log --oneline --no-merges <last-release-tag>..HEAD` and requires categorising each change into the defined category table (Feature, Enhancement, Bug fix, Infrastructure, Migration, Security).
- [x] PASS: Skill evaluates all engineering gates with evidence requirements — release-plan SKILL.md Step 2 rules: "Check each gate by reading actual evidence... A gate without evidence is a gate that has not passed." Each gate is explicitly marked PASS/FAIL/N/A.
- [x] PASS: Skill recommends feature flag strategy for report scheduling — release-plan SKILL.md Step 3: "Default to feature flags for user-facing changes." Report scheduling is a new user-facing feature — feature flag is the explicitly preferred strategy.
- [x] PASS: Skill identifies breaking API change as high risk and flags partner communication before deployment — release-plan SKILL.md Step 1 requires identifying "which changes have the widest blast radius?" Step 5 communication plan explicitly includes external partners requiring "before deployment" timing. Anti-patterns: "We'll write the release notes later" is explicitly prohibited.
- [x] PASS: Skill verifies Postgres migration tested in staging with rollback verified — release-plan SKILL.md Step 2 engineering gates explicitly lists: "Database migrations tested in staging (with rollback verified)" as a named gate that must have evidence.
- [x] PASS: Skill records baseline metric values before deployment — release-plan SKILL.md Step 4 rules: "Record current baseline values for each metric BEFORE deployment." The output template shows "Current baseline | [value]" in the Rollback Criteria table.
- [x] PASS: Rollback criteria with specific thresholds and named rollback owner — release-plan SKILL.md Step 4 table specifies >2x error rate and >3x p95 latency thresholds. Step 4 rules: "Assign a rollback owner who has the authority and access to execute."
- [~] PARTIAL: Skill includes communication plan with audiences, content, and timing — release-plan SKILL.md Step 5 defines the full audience table with columns (Audience, What they need, When, Channel). The structure is present and complete. Maximum score is 0.5 per PARTIAL-prefixed criterion ceiling.
- [x] PASS: Output produces the full 6-section release plan format — release-plan SKILL.md Output section defines the template with all six sections: Scope, Readiness, Strategy, Rollback Criteria, Communication, Decision.

### Notes

The breaking API change criterion (4) is well-tested by this scenario — the skill's blast radius identification step and the communication plan's "before deployment" requirement for external partners both apply. The communication plan criterion (8) has a PARTIAL ceiling despite being fully present; this reflects the test author's judgment that a PARTIAL ceiling is appropriate for a criterion where depth of implementation varies.
