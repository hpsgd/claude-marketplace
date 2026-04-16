# Test: Plan release v3.1.0 with breaking API change

Scenario: Developer invokes the release-plan skill for v3.1.0, which includes a breaking change to the `/api/v2/reports` response schema, a new report scheduling feature, and a Postgres migration adding two tables.

## Prompt

Plan release v3.1.0. It includes: (1) a breaking change to `GET /api/v2/reports` — the `data` field is now nested under `result.data` instead of at the top level, (2) a new report scheduling feature behind feature flag `report-scheduling`, (3) a Postgres migration adding `scheduled_reports` and `schedule_executions` tables. Some API consumers are external partners who need advance notice. Target deploy: next Tuesday.

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
