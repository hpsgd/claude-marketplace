# Release Checklist — v{X.Y.Z}

> Date: {Date} | Release Owner: {Name} | Status: {Planning/In Progress/Deployed/Rolled Back}

---

## 1. Release Info

| Field | Value |
|-------|-------|
| Version | v{X.Y.Z} |
| Planned date | {Date and time with timezone} |
| Release owner | {Name} |
| Scope summary | {One-paragraph description of what this release includes} |
| Change tickets | {Links to relevant issues/PRs} |
| Rollback plan | {Link to rollback-plan.md for this release} |

---

## 2. Pre-Deployment Checks

| # | Gate | Status | Evidence | Sign-off |
|---|------|--------|----------|----------|
| 1 | All CI checks pass on release branch | {Pass/Fail/N-A} | {Link to CI run} | {Name} |
| 2 | Code review approved | {Pass/Fail/N-A} | {Link to PR} | {Name} |
| 3 | QA sign-off | {Pass/Fail/N-A} | {Link to test report} | {Name} |
| 4 | Security scan clean | {Pass/Fail/N-A} | {Link to scan results} | {Name} |
| 5 | Database migrations tested | {Pass/Fail/N-A} | {Link to migration test} | {Name} |
| 6 | Performance regression check | {Pass/Fail/N-A} | {Link to benchmark} | {Name} |
| 7 | Rollback plan reviewed | {Pass/Fail/N-A} | {Link to rollback plan} | {Name} |
| 8 | Feature flags configured | {Pass/Fail/N-A} | {Link to flag config} | {Name} |

---

## 3. Deployment Steps

| Step | Action | Command / Link | Owner | Status |
|------|--------|---------------|-------|--------|
| 1 | Tag release | `git tag -a v{X.Y.Z} -m "Release v{X.Y.Z}"` | {Name} | {Done/Pending} |
| 2 | Deploy to staging | {Command or link to pipeline} | {Name} | {Done/Pending} |
| 3 | Run staging smoke tests | {Command or link} | {Name} | {Done/Pending} |
| 4 | Deploy to production | {Command or link to pipeline} | {Name} | {Done/Pending} |
| 5 | Run production smoke tests | {Command or link} | {Name} | {Done/Pending} |
| 6 | Enable feature flags | {Flag names and platform link} | {Name} | {Done/Pending} |

---

## 4. Post-Deployment Verification

| Check | Method | Expected Result | Actual Result | Status |
|-------|--------|----------------|---------------|--------|
| Health endpoint | `GET /health` | 200 OK | {Result} | {Pass/Fail} |
| Smoke test suite | {Link to test runner} | All pass | {Result} | {Pass/Fail} |
| Error rate | {Monitoring dashboard link} | No spike above {threshold}% | {Result} | {Pass/Fail} |
| Latency p95 | {Monitoring dashboard link} | Below {threshold}ms | {Result} | {Pass/Fail} |

**Monitoring window:** Observe for {30 minutes} after deployment before declaring success.

---

## 5. Rollback Trigger Criteria

Initiate rollback if any of the following occur within the monitoring window:

- [ ] Error rate exceeds {X}% of requests
- [ ] p95 latency exceeds {X}ms
- [ ] Health check fails for more than {X} consecutive minutes
- [ ] Critical bug reported by users
- [ ] Data integrity issue detected

---

## 6. Communication Status

| Audience | Channel | Status | Owner |
|----------|---------|--------|-------|
| Engineering team | {e.g. #engineering Slack} | {Notified/Pending} | {Name} |
| Product team | {e.g. #product Slack} | {Notified/Pending} | {Name} |
| Customer support | {e.g. email / Slack} | {Notified/Pending} | {Name} |
| External customers | {e.g. status page / changelog} | {Published/Pending} | {Name} |

---

## 7. Go/No-Go Decision

| Field | Value |
|-------|-------|
| Decision | {Go / No-Go} |
| Reasoning | {Summary of why the decision was made} |
| Decided at | {Date and time} |
| Approvers | {Names and roles} |
