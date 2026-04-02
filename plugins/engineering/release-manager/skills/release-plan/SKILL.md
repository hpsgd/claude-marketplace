---
name: release-plan
description: Plan a release — scope assessment, readiness gates, deployment strategy, communication plan, and go/no-go decision.
argument-hint: "[version, feature set, or release name to plan]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Plan a release for $ARGUMENTS.

## Release Planning Process (6 steps — sequential, do not skip)

The cardinal rule: **every release is reversible, communicated, and gated.** No release ships without passing all gates, having a rollback plan, and briefing support. Pressure does not override process.

### Step 1: Define Release Scope

Identify everything included in this release:

1. **List changes since last release** — use git log to enumerate:
   ```bash
   git log --oneline --no-merges <last-release-tag>..HEAD
   ```
2. **Categorise each change:**

   | Category | Includes |
   |---|---|
   | Features | New user-facing capabilities |
   | Enhancements | Improvements to existing features |
   | Bug fixes | Corrections to existing behaviour |
   | Infrastructure | CI/CD, deployment, config changes |
   | Migrations | Database schema changes, data migrations |
   | Security | Auth changes, dependency patches, vulnerability fixes |

3. **Identify dependencies** — does any change depend on a migration, config change, feature flag, or external service deployment?
4. **Flag risks** — which changes have the widest blast radius? Which touch auth, payments, or data?
5. **Confirm scope with product** — the release manager does not decide what ships. Confirm the scope matches what the product owner approved

### Step 2: Readiness Assessment (MANDATORY — every gate checked)

Evaluate every gate. A skipped gate is a failed gate.

**Engineering gates:**
- [ ] All items meet Definition of Done (code complete, tests pass, reviewed, docs updated)
- [ ] Verification tests pass in staging (full acceptance suite, exit 0)
- [ ] No open critical or high-severity bugs in this release
- [ ] Security review completed for auth/data changes (CVSS scores assessed)
- [ ] Database migrations tested in staging (with rollback verified)
- [ ] Performance benchmarks met (no regression from baseline)

**Operational gates:**
- [ ] Rollback plan documented and tested
- [ ] Monitoring and alerts in place for key metrics
- [ ] Support team briefed (FAQ, known issues, escalation paths)
- [ ] Release notes drafted (user-facing and internal)

**Communication gates:**
- [ ] Customer communication prepared (if user-facing changes)
- [ ] Documentation updated (user docs, API docs, changelog)
- [ ] GTM team notified (if launch activities are planned)

**Rules:**
- Check each gate by reading actual evidence (test output, review comments, migration logs) — not by asking "did someone do this?"
- A gate without evidence is a gate that has not passed
- If a gate is genuinely not applicable (e.g., no migrations in this release), mark it N/A with reasoning

### Step 3: Select Deployment Strategy

Choose a strategy based on the release content and risk profile:

| Strategy | When | Risk | Rollback speed |
|---|---|---|---|
| **Feature flag** | New features, uncertain impact | Lowest | Instant (toggle off) |
| **Percentage rollout** | User-facing changes, want to monitor | Low | Fast (reduce to 0%) |
| **Blue/green** | Infrastructure changes, zero-downtime required | Low | Fast (switch traffic) |
| **Canary** | High-risk changes, need real traffic validation | Medium | Moderate (redirect traffic) |
| **Big bang** | Small changes, internal tools, low risk | Higher | Slow (full redeploy) |

**Default to feature flags** for user-facing changes. Big bang only for low-risk internal changes.

If multiple strategies apply to different parts of the release, combine them. A release can use feature flags for user-facing features and big bang for internal tooling changes simultaneously.

### Step 4: Define Rollback Criteria

Define BEFORE deployment what triggers a rollback. These are non-negotiable:

| Signal | Threshold | Action |
|---|---|---|
| Error rate | >2x baseline for 5 minutes | Automatic rollback |
| p95 latency | >3x baseline for 5 minutes | Investigate, rollback if not resolving |
| Support ticket spike | >3x normal rate within 1 hour | Investigate, rollback if product-related |
| Health check failures | Any health endpoint returning non-200 | Immediate rollback |
| Data integrity | Any data corruption signal | Immediate rollback + incident response |

**Rules:**
- Record current baseline values for each metric BEFORE deployment
- Specify which rollback mechanism applies (feature flag toggle, traffic switch, full redeploy)
- Assign a rollback owner who has the authority and access to execute
- Test the rollback mechanism before you need it

### Step 5: Communication Plan

Identify who needs to know what and when:

| Audience | What they need | When | Channel |
|---|---|---|---|
| **Support team** | FAQ, known issues, escalation paths, expected behaviour changes | Before deployment | Briefing + document |
| **Engineering** | Deploy time, what to monitor, rollback plan, on-call expectations | Before deployment | Team channel |
| **GTM / Marketing** | Feature availability, timing for announcements, any launch coordination | Before deployment | Coordination meeting |
| **Customers** | What changed, what they need to do (if anything), where to get help | After deployment verified stable | Release notes / email / in-app |
| **Leadership** | Release summary, risk assessment, go/no-go decision | Before deployment | Status update |

**Rules:**
- Support is briefed BEFORE deployment, never after
- Customer communication goes out AFTER deployment is verified stable, never before
- Internal engineering notification includes the rollback plan and on-call contact

### Step 6: Go/No-Go Decision

Make the call based on gates and evidence:

**GO:** All engineering, operational, and communication gates pass. Rollback plan verified. Team available to monitor post-deployment.

**NO-GO:** Any engineering gate fails. No rollback plan. Support team not briefed. Deploying into a known-bad state (existing incident in progress).

**CONDITIONAL GO:** Some non-engineering gates have known acceptable risks. Document the risk, get CTO approval, proceed with enhanced monitoring. Engineering gate failures are never conditionally acceptable.

## Anti-Patterns (NEVER do these)

- **Releasing without a rollback plan** — if you cannot reverse it, you cannot ship it. A rollback plan designed during an incident is a rollback plan that fails
- **Skipping support briefing** — support will be blindsided by customer questions. They are the first line of defence and need answers ready
- **Bundling hotfixes with feature releases** — hotfixes are minimal and urgent. Combining them with a feature release defeats the purpose of both
- **Deploying during an active incident** — deploying into a known-bad state compounds risk. Wait for resolution
- **Overriding gates under pressure** — time pressure does not make failing tests pass. If it is not ready, it is not ready
- **"We'll write the release notes later"** — release notes written after the fact are incomplete. Draft them during planning when context is fresh

## Output

Deliver a release plan in this format:

```markdown
## Release: [version/name]

### Scope
| Change | Category | Risk | PRs |
|---|---|---|---|
| [description] | Feature/Fix/Infra | Low/Med/High | #123 |

### Readiness
| Gate | Status | Evidence |
|---|---|---|
| Tests pass | PASS/FAIL | [command + exit code] |
| Security review | PASS/FAIL/N/A | [reviewer + date] |
| Migrations tested | PASS/FAIL/N/A | [staging verification] |
| Performance baseline | PASS/FAIL | [benchmark results] |
| Rollback tested | PASS/FAIL | [method + verification] |
| Support briefed | PASS/FAIL | [date + document link] |
| Docs updated | PASS/FAIL/N/A | [what was updated] |

### Strategy: [Feature flag / Percentage rollout / Blue-green / Canary / Big bang]
Reasoning: [why this strategy fits this release]

### Rollback Criteria
| Signal | Current baseline | Threshold | Action | Owner |
|---|---|---|---|---|
| Error rate | [value] | >2x for 5 min | Automatic rollback | [name] |
| p95 latency | [value] | >3x for 5 min | Investigate + rollback | [name] |

### Communication
| Audience | Status | Date |
|---|---|---|
| Support | Briefed/Pending | [date] |
| Engineering | Notified/Pending | [date] |
| Customers | Drafted/Pending | [date] |

### Decision: [GO / NO-GO / CONDITIONAL GO]
Reasoning: [why, citing gate results]
```

## Related Skills

- `/release-manager:rollback-assessment` — before releasing, define the rollback plan. Every release plan should have a corresponding rollback assessment.

Track [DORA metrics](https://dora.dev/) across releases: deployment frequency, lead time, change failure rate, and time to restore. These are the industry-standard measures of release process health.

Use the release checklist template (`templates/release-checklist.md`) and rollback plan template (`templates/rollback-plan.md`) for consistent output structure.