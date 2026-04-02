# Rollback Plan — v{X.Y.Z}

> Release: v{X.Y.Z} | Date: {Date} | Owner: {Name}

## 1. Release Reference

| Field | Value |
|-------|-------|
| Version | v{X.Y.Z} |
| Deployment method | {e.g. Blue-green / Rolling / Canary / Feature flag} |
| Previous stable version | v{X.Y.Z-1} |
| Release checklist | {Link to release-checklist.md} |
| Artefact | {Container image tag, build ID, or commit SHA} |

## 2. Rollback Mechanism

| Aspect | Detail |
|--------|--------|
| Method | {e.g. Switch blue-green target / Redeploy previous image / Disable feature flag} |
| Estimated duration | {e.g. < 5 minutes} |
| Automation | {Link to rollback script/pipeline, or "Manual"} |
| Data changes | {Yes — see Section 5 / No — stateless deployment} |

## 3. Trigger Criteria

Initiate rollback if any condition is observed. **Decision authority:** {Name/Role}.

- [ ] Error rate exceeds {X}% for more than {Y} minutes
- [ ] p95 latency exceeds {X}ms sustained for {Y} minutes
- [ ] Health endpoint non-200 for {Y} consecutive checks
- [ ] Critical functionality broken or data integrity issue detected

## 4. Rollback Steps

| Step | Action | Command / Procedure | Verify |
|------|--------|-------------------|--------|
| 1 | Announce rollback | Post to {#channel} | Message confirmed |
| 2 | Disable feature flags | {Command or UI steps} | Flags disabled |
| 3 | Revert deployment | {e.g. `kubectl rollout undo deployment/{name}`} | Previous pods running |
| 4 | Verify health | `curl -s https://{host}/health` | Returns 200 |
| 5 | Run smoke tests | {Command or link} | All pass |

## 5. Database Rollback

{If none: "N/A — no database migrations in this release."}

| Aspect | Detail |
|--------|--------|
| Migration to reverse | {Migration name/number} |
| Reverse command | {e.g. `migrate down 1`} |
| Data loss risk | {Describe any unrecoverable data} |
| Pre-rollback backup | {e.g. `pg_dump` command} |

## 6. Verification

- [ ] Application version matches v{X.Y.Z-1}
- [ ] Health endpoint returns 200
- [ ] Smoke tests pass
- [ ] Error rate and latency returned to baseline

## 7. Communication

| Order | Audience | Channel | Message |
|-------|----------|---------|---------|
| 1 | Incident team | {PagerDuty / Slack #incidents} | Rollback initiated |
| 2 | Engineering | {Slack #engineering} | Rollback complete, investigating |
| 3 | Product / Support | {Slack #product} | Release rolled back, {reason} |
| 4 | External | {Status page} | Service restored |

## 8. Post-Rollback Actions

- [ ] Schedule retrospective within {48 hours}
- [ ] Create investigation ticket
- [ ] Identify fixes before re-attempting release
