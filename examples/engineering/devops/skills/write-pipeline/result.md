# Result: write-pipeline skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated invocation: `/devops:write-pipeline` applied to the `write-pipeline` SKILL.md definition, verifying it meets production CI/CD standards.

---

### Skill verification: write-pipeline

**Stack identified from SKILL.md:** GitHub Actions (primary), with stack-agnostic guidance for Node.js, .NET, and Python.

---

#### Stage order and fail-fast reasoning

The skill mandates this sequence in Step 2:

```
Lint/Format → Build → Unit Tests → Integration Tests → Security Scan → Deploy
```

Rationale quoted directly: "fail fast — cheapest checks first." If any stage fails, subsequent stages do not run. The ordering minimises wasted CI time by front-loading the fastest checks — lint completes in under 60 seconds, build next, then unit tests. Integration tests and security scans only run after cheap gates pass.

**Verdict: ENFORCED** — the sequence is explicit, the fail-fast rule is stated, and each stage's purpose is justified.

---

#### Fast-path time budget

From Step 2: "Total pipeline time budget: under 10 minutes for the fast path (lint + build + unit tests)."

Enforced by stage-level timeouts:

| Stage | Timeout |
|---|---|
| Lint | <60 seconds (flagged as broken if exceeded) |
| Unit Tests | 5 minutes max |
| Integration Tests | 10 minutes max |
| All jobs | Mandatory timeout — "No timeout" is listed as an Anti-Pattern |

The budget is not aspirational. The Anti-Patterns section explicitly bans running without timeouts.

**Verdict: ENFORCED**

---

#### Cache key strategy and hit-rate threshold

Cache key examples from the Caching Strategy section:

```yaml
# Node.js
key: node-${{ hashFiles('package-lock.json') }}

# .NET
key: nuget-${{ hashFiles('**/*.csproj') }}

# Python
key: pip-${{ hashFiles('requirements*.txt') }}
```

Rule quoted: "Cache key MUST include a hash of the lockfile/dependency manifest." Monitoring rule: "Monitor cache hit rates — below 80% means the key strategy is wrong."

**Verdict: ENFORCED** — lockfile-hash keys are required, the 80% threshold is explicit.

---

#### GitHub Actions SHA pinning

From the Version Pinning section:

```yaml
# Pin action versions to full SHA (not tags)
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1
```

Rule: "Pin GitHub Actions to commit SHA, not tag (tags can be moved)." The example SHA is a real 40-character hex value. Supply-chain justification is stated: tags are movable, so a tag pin is not a security guarantee.

**Verdict: ENFORCED** — full SHA pinning required, justification present.

---

#### Deploy gate: main branch only, after all checks pass

From Stage 6:

```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main' && success()
  run: ./scripts/deploy.sh
```

Rule: "Deploy only on main branch, only after ALL checks pass." Anti-Patterns section reinforces: "Deploy from feature branches" is explicitly banned.

**Verdict: ENFORCED**

---

#### Security scan stage

Stage 5 requirements:

```yaml
- name: Security Scan
  run: |
    npm audit --audit-level=high
    # or: trivy fs . --severity HIGH,CRITICAL
```

Rules:
- Fail on HIGH and CRITICAL vulnerabilities
- Run SAST in addition to dependency audit
- Container image scanning required when building Docker images
- Suppression file allowed for acknowledged false positives (with expiry dates)

**Verdict: ENFORCED** — all three sub-requirements (dependency audit at HIGH/CRITICAL, SAST, container scanning) are present.

---

#### Watch mode prohibition

From Anti-Patterns: "Watch mode in CI — tests never exit. Always use `CI=true` or `--run`."

Stage 3 example:

```yaml
- name: Unit Tests
  run: CI=true npm test -- --coverage
```

Both mechanisms addressed: `CI=true` environment variable and explicit `--run` flag.

**Verdict: ENFORCED**

---

#### Monorepo CI handling

The Monorepo CI section covers all three required sub-topics:

1. **Change detection** — `git diff` or GitHub Actions path filters
2. **Selective execution** — "only build/test projects that changed or depend on changed code"
3. **Dependency graph awareness** — Moon (`moon ci`) resolves the dependency graph automatically

Example:

```yaml
# Moon handles change detection + dependency graph resolution
- name: Run affected checks
  run: moon ci
```

The skill is transparent about the path-filter fallback's limitation: "no dependency graph awareness." This is a quality signal — it distinguishes between full graph resolution (Moon) and manual path listing.

**Verdict: ENFORCED** — all three sub-topics addressed.

---

#### Production gaps identified

Three production concerns are absent from the skill:

1. **Concurrency control** — no guidance on `cancel-in-progress: true` for PR push workflows. Without this, rapid pushes queue multiple runs against stale commits, burning CI minutes unnecessarily.

2. **Artifact retention policy** — no guidance on how long pipeline artifacts (coverage reports, build outputs) are retained. GitHub charges for storage above the free tier; compliance teams may have mandatory retention windows.

3. **Required-status-check rulesets** — the `if: github.ref == 'refs/heads/main' && success()` gate is the right implementation, but without branch protection rules enforcing required status checks, a developer with direct push access can bypass the gate entirely. The skill does not mention this enforcement layer.

---

### Summary

| Requirement | Status |
|---|---|
| Stage order with fail-fast reasoning | Enforced |
| Fast-path under 10 minutes | Enforced with timeouts |
| Cache keys from lockfile hashes, 80% threshold | Enforced |
| GitHub Actions pinned to full commit SHAs | Enforced |
| Deploy from main only, after all checks | Enforced |
| Security scan (audit + SAST + container) | Enforced |
| Watch mode prohibited, CI=true or --run | Enforced |
| Monorepo: change detection + selective execution + graph | Enforced |
| Concurrency control (cancel-in-progress) | Absent |
| Artifact retention policy | Absent |
| Required-status-check ruleset guidance | Absent |

---

## Criteria

- [x] PASS: Skill enforces the correct stage order with fail-fast reasoning — Step 2 states "fail fast — cheapest checks first" with the explicit sequence `Lint/Format → Build → Unit Tests → Integration Tests → Security Scan → Deploy`. "If any stage fails, subsequent stages do not run."
- [x] PASS: Skill requires the fast path to complete in under 10 minutes — Step 2: "Total pipeline time budget: under 10 minutes for the fast path (lint + build + unit tests)." Stage-level timeouts back this up: unit tests capped at 5 minutes, integration tests at 10 minutes.
- [x] PASS: Skill requires cache keys derived from lockfile hashes and flags below 80% hit rate — Caching Strategy provides working examples using `hashFiles('package-lock.json')`, `hashFiles('**/*.csproj')`, and `hashFiles('requirements*.txt')`. Rule: "Monitor cache hit rates — below 80% means the key strategy is wrong."
- [x] PASS: Skill requires GitHub Actions pinned to full commit SHAs, not tags — Version Pinning section: "Pin GitHub Actions to commit SHA, not tag (tags can be moved)." The worked example shows `actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1`.
- [x] PASS: Skill limits deployment to main branch only, after all checks pass — Stage 6 uses `if: github.ref == 'refs/heads/main' && success()`. Rule: "Deploy only on main branch, only after ALL checks pass." Anti-Patterns section reinforces: "Deploy from feature branches" is explicitly banned.
- [x] PASS: Skill requires a security scan stage covering HIGH/CRITICAL audit, SAST, and container image scanning — Stage 5 runs `npm audit --audit-level=high`, rules require SAST in addition to dependency audit, and container image scanning is required when building Docker images.
- [x] PASS: Skill prohibits watch mode and requires CI=true or --run — Anti-Patterns: "Watch mode in CI — tests never exit. Always use `CI=true` or `--run`." Stage 3 example shows `CI=true npm test`.
- [x] PASS: Skill addresses monorepo CI with change detection, selective execution, and dependency graph awareness — the Monorepo CI section covers all three: change detection (`git diff` or path filters), selective execution ("only build/test projects that changed or depend on changed code"), and dependency graph awareness (Moon cited with a `moon ci` example that resolves the graph automatically).

## Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample workflow.
- [x] PASS: Output verifies the stage order — `Lint/Format → Build → Unit Tests → Integration Tests → Security Scan → Deploy` — with fail-fast reasoning quoted from Step 2.
- [x] PASS: Under-10-minute fast-path target confirmed and enforced — backed by unit test timeout (5 minutes max), integration test timeout (10 minutes max), and the Anti-Patterns rule that timeouts are mandatory on all jobs.
- [x] PASS: Cache-key-from-lockfile-hash rule confirmed across Node, .NET, and Python stacks. The 80% cache hit rate threshold is explicit.
- [x] PASS: SHA pinning confirmed with supply-chain reasoning. The skill requires a full 40-character commit SHA (not a tag), with the justification "tags can be moved."
- [x] PASS: Deploy-from-main-only confirmed. The `if: github.ref == 'refs/heads/main' && success()` gate is present in Stage 6. Feature branch deployments are rejected by the Anti-Patterns section.
- [x] PASS: Security scan stage confirmed — dependency audit at HIGH/CRITICAL (`--audit-level=high`), SAST required in addition to dependency audit, container image scanning specified for Docker builds.
- [x] PASS: Watch-mode prohibition confirmed. `CI=true` is shown in the unit test example; `--run` flag is named in the Anti-Patterns rule. Both mechanisms are addressed.
- [x] PASS: Monorepo handling confirmed — change detection, selective execution, and dependency graph awareness all present. Moon (`moon ci`) is cited as the recommended tool for automatic graph resolution.
- [~] PARTIAL: Gaps identified — partially met. Three production concerns are absent: (1) no concurrency control guidance (`cancel-in-progress: true` on PR push), (2) no artifact retention policy, (3) no required-status-check ruleset guidance for branch protection.

## Notes

The skill is well-constructed. Stage ordering, fast-path budget, caching strategy, SHA pinning, and security requirements are all precise, justified, and backed by concrete examples rather than vague rules.

The three absent production concerns are worth a future revision. Concurrency control (`cancel-in-progress: true`) prevents queued runs on rapid PR pushes from burning CI minutes on stale commits — cheap and common. Artifact retention policies affect both cost (GitHub charges for storage above the free tier) and compliance. Required-status-check rulesets are the enforcement mechanism that makes the `if: github.ref == 'refs/heads/main'` gate meaningful — without them, developers with direct push access can bypass it.

The monorepo section is transparent about the path-filter fallback's limitation ("no dependency graph awareness"), which is a quality signal.
