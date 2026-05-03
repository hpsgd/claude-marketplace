# Test: Plan release v3.1.0 with breaking API change

Scenario: Developer invokes the release-plan skill for v3.1.0, which includes a breaking change to the `/api/v2/reports` response schema, a new report scheduling feature, and a Postgres migration adding two tables.

## Prompt

Plan release v3.1.0. It includes: (1) a breaking change to `GET /api/v2/reports` — the `data` field is now nested under `result.data` instead of at the top level, (2) a new report scheduling feature behind feature flag `report-scheduling`, (3) a Postgres migration adding `scheduled_reports` and `schedule_executions` tables. Some API consumers are external partners who need advance notice. Target deploy: next Tuesday.

A few specifics for the response:

- **Show the git log enumeration** at the top: `git log v3.0.0..HEAD --oneline` (or equivalent). If git history isn't available in the workspace, simulate the output based on the prompt's three changes, label each commit with category (feat / fix / breaking / migration / infra), and state the assumption.
- **Engineering gates table**: each gate marked **PASS / FAIL / N/A** (not PENDING) with linked evidence stub (e.g. `CI build: [link]`, `Staging migration log: [link]`, `Rollback rehearsal: [PASS — log link]`). Eight gates minimum: build green, tests green, migration tested in staging, rollback verified in staging, feature flag default-off confirmed, breaking-change docs published, partner notice sent, runbook updated.
- **Versioning strategy**: present BOTH options for the breaking change — (A) parallel `/api/v3/reports` route running alongside v2, (B) coordinated `/api/v2/reports` cutover with the new shape. State which you recommend AND why the other was rejected.
- **Partner notice ≥1 week ahead** (not 5 days): schedule the notice for at least 7 days before deploy. Include a deprecation header in v2 responses NOW pointing to the new shape, plus a migration guide URL.
- **Rollout in stages** for the feature flag: internal (dogfood, day 0-1) → beta (10% of customers, day 2-4) → general (100%, day 5+). Three stages explicitly named.
- **GO/NO-GO with explicit conditions**: e.g. "GO **conditional** on partner sign-off received by Monday EOD. If unresponsive partners > 1, NO-GO and reschedule to the following Tuesday."
- **All 8 gates marked PASS / FAIL / N/A** — no PENDING. If a gate's evidence isn't available yet (e.g. partner notice not sent), mark it FAIL with a note "must complete before deploy" rather than PENDING.
- **Baseline metrics recorded BEFORE deploy**: capture current baseline values (e.g. `Current baseline: 5xx rate 0.3%, p95 latency 280ms on /api/v2/reports`). Express rollback thresholds as multiples of baseline ("rollback if 5xx > 2× baseline (0.6%) for >5 min").
- **Named rollback owner PER signal**: e.g. `API errors → on-call backend (Alex)`, `Migration corruption → DBA on-call (Sam)`, `Partner integration breakage → integrations lead (Jordan)`. Not generic "the team" or "DBA on standby".
- **Three communication audiences explicit**: (1) external partners — ≥7 days ahead, email + deprecation header, (2) internal engineering — release notes day-of, (3) support team — runbook + script delivered Friday before deploy window with talking points for likely customer questions.

## Criteria

- [ ] PASS: Skill uses git log to enumerate all changes since the last release and categorises each (feature, enhancement, bug fix, infrastructure, migration, security)
- [ ] PASS: Skill evaluates all engineering gates with evidence requirements — marks each as PASS/FAIL/N/A, not just "assumed passed"
- [ ] PASS: Skill recommends feature flag strategy for the report scheduling feature — not big-bang
- [ ] PASS: Skill identifies the breaking API change as high risk and flags that external partners require advance communication BEFORE deployment
- [ ] PASS: Skill verifies the Postgres migration has been tested in staging with rollback verified
- [ ] PASS: Skill records current baseline metric values (error rate, p95 latency) to be used as rollback decision thresholds post-deploy
- [ ] PASS: Rollback criteria are defined with specific thresholds and a named rollback owner for each signal
- [ ] PARTIAL: Skill includes a communication plan showing which audiences receive what information and when
- [ ] PASS: Output produces the full release plan format: Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and a GO/NO-GO Decision with reasoning

## Output expectations

- [ ] PASS: Output uses `git log` (with the previous tag → HEAD range) to enumerate every commit in the release and categorises each as feature / enhancement / fix / infra / migration / breaking
- [ ] PASS: Output classifies the breaking API change as HIGH risk and requires advance partner notification with a concrete lead time (e.g. ≥1 week, deprecation header sent in current responses, migration guide provided)
- [ ] PASS: Output proposes a versioning approach for the breaking change — either a new `/api/v3/reports` route running in parallel, or `/api/v2/reports` carrying the new shape with a coordinated cutover, with reasoning for the chosen path
- [ ] PASS: Output's report scheduling rollout uses the `report-scheduling` feature flag, kept off at deploy and rolled out in stages (internal → beta → general), not big-bang on top of the breaking change
- [ ] PASS: Output's migration verification confirms staging applied both `scheduled_reports` and `schedule_executions` tables, plus a rollback rehearsal showing the down-migration ran cleanly without losing other data
- [ ] PASS: Output's engineering gates table marks each as PASS / FAIL / N/A with linked evidence (CI build URL, staging screenshot, migration log) — not assumed-passed
- [ ] PASS: Output records baseline metrics (error rate, p95 latency on `/api/v2/reports`) BEFORE the deploy, with the threshold values written into the rollback criteria — e.g. "rollback if 5xx rate > 2x baseline of 0.3% for >5 min"
- [ ] PASS: Output names a rollback owner per signal (API errors → on-call backend, migration corruption → DBA on-call) — not a generic "team" owner
- [ ] PASS: Output's communication plan has separate audiences and timing — external partners receive the breaking change notice ≥1 week ahead, internal teams get the release notes day-of, support gets the script before deploy window
- [ ] PARTIAL: Output's GO/NO-GO decision states explicit conditions — "GO conditional on partner sign-off received by Monday EOD; otherwise NO-GO and reschedule" — not a bare GO/NO-GO label
