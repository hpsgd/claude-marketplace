# Test: Release coordination with migrations and feature flags

Scenario: User needs to coordinate a release that includes database migrations, a new feature behind a feature flag, a dependency security patch, and a rollback plan — with support team briefing before go-live.

## Prompt

We need to release v2.4.0 this Thursday. It includes:
1. A database migration adding two new columns to the `subscriptions` table and a new `subscription_events` table
2. A new billing dashboard feature (currently behind a feature flag `billing-dashboard-v2`)
3. A security patch for CVE-2024-38372 in one of our dependencies
4. Some internal refactoring of the subscription service

The migration has been tested on staging. The security patch bumps a minor version. Can you help coordinate the release, define the go/no-go criteria, and prepare a rollback plan?

## Criteria

- [ ] PASS: Agent checks all engineering gates (tests, staging verification, security review, migration rollback verified) before issuing a go/no-go
- [ ] PASS: Agent recommends feature flag strategy for the billing dashboard feature — not big-bang deployment
- [ ] PASS: Agent defines rollback criteria with specific thresholds (error rate >2x baseline, p95 latency >3x baseline) and assigns a rollback owner
- [ ] PASS: Agent confirms support team must be briefed BEFORE deployment, not after
- [ ] PASS: Agent categorises each change by risk: migration (medium-high), security patch (low-medium), feature flag (low), refactoring (low)
- [ ] PASS: Agent records current baseline metric values before deployment so rollback thresholds can be evaluated post-deploy
- [ ] PASS: Agent identifies the migration as requiring special attention — rollback of a migration that has already altered production data is different from code rollback
- [ ] PARTIAL: Agent produces a structured output with Scope table, Readiness gates, Strategy, Rollback Criteria, Communication plan, and Decision
- [ ] PASS: Agent refuses to override a failed engineering gate under time pressure
