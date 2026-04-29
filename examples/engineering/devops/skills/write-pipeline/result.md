# Result: write-pipeline skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill enforces the correct stage order with fail-fast reasoning — Step 2 states "fail fast — cheapest checks first" with the explicit sequence `Lint/Format → Build → Unit Tests → Integration Tests → Security Scan → Deploy`. "If any stage fails, subsequent stages do not run."
- [x] PASS: Skill requires the fast path to complete in under 10 minutes — Step 2: "Total pipeline time budget: under 10 minutes for the fast path (lint + build + unit tests)." Stage-level timeouts back this up: unit tests capped at 5 minutes, integration tests at 10 minutes.
- [x] PASS: Skill requires cache keys derived from lockfile hashes and flags below 80% hit rate — Caching Strategy provides working examples using `hashFiles('package-lock.json')`, `hashFiles('**/*.csproj')`, and `hashFiles('requirements*.txt')`. Rule: "Monitor cache hit rates — below 80% means the key strategy is wrong."
- [x] PASS: Skill requires GitHub Actions pinned to full commit SHAs, not tags — Version Pinning section: "Pin GitHub Actions to commit SHA, not tag (tags can be moved)." The worked example shows `actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1`.
- [x] PASS: Skill limits deployment to main branch only, after all checks pass — Stage 6 uses `if: github.ref == 'refs/heads/main' && success()`. Rule: "Deploy only on main branch, only after ALL checks pass." Anti-Patterns section reinforces: "Deploy from feature branches" is explicitly banned.
- [x] PASS: Skill requires a security scan stage covering HIGH/CRITICAL audit, SAST, and container image scanning — Stage 5 runs `npm audit --audit-level=high`, rules require SAST in addition to dependency audit, and container image scanning is required when building Docker images.
- [x] PASS: Skill prohibits watch mode and requires CI=true or --run — Anti-Patterns: "Watch mode in CI — tests never exit. Always use `CI=true` or `--run`." Stage 3 example shows `CI=true npm test`.
- [x] PASS: Skill addresses monorepo CI with change detection, selective execution, and dependency graph awareness — the Monorepo CI section covers all three: change detection (`git diff` or path filters), selective execution ("only build/test projects that changed or depend on changed code"), and dependency graph awareness (Moon cited with a `moon ci` example that resolves the graph automatically).

### Output expectations

- [x] PASS: Result is structured as a verification of the skill (verdict per criterion), not a sample pipeline workflow.
- [x] PASS: Stage order verified — `Lint/Format → Build → Unit Tests → Integration Tests → Security Scan → Deploy`. Fail-fast reasoning quoted from Step 2: "fail fast — cheapest checks first"; "If any stage fails, subsequent stages do not run."
- [x] PASS: Under-10-minute fast-path target confirmed and enforced. The budget is not aspirational — it is backed by unit test timeout (5 minutes max), integration test timeout (10 minutes max), and the Anti-Patterns rule that timeouts are mandatory on all jobs.
- [x] PASS: Cache-key-from-lockfile-hash rule confirmed across Node, .NET, and Python stacks. The 80% cache hit rate threshold is explicit: "below 80% means the key strategy is wrong."
- [x] PASS: SHA pinning confirmed with supply-chain reasoning. The skill requires a full 40-character commit SHA (not a tag), with the justification "tags can be moved." The example SHA `b4ffde65f46336ab88eb53be808477a3936bae11` is a real 40-character hex value.
- [x] PASS: Deploy-from-main-only confirmed. The `if: github.ref == 'refs/heads/main' && success()` gate is present in Stage 6. Feature branch deployments are rejected by the Anti-Patterns section.
- [x] PASS: Security scan stage confirmed — dependency audit at HIGH/CRITICAL (`--audit-level=high`), SAST required in addition to dependency audit, container image scanning specified for Docker builds.
- [x] PASS: Watch-mode prohibition confirmed. `CI=true` is shown in the unit test example; `--run` flag is named in the Anti-Patterns rule. Both mechanisms are addressed.
- [x] PASS: Monorepo handling confirmed — change detection, selective execution, and dependency graph awareness all present. Moon (`moon ci`) is cited as the recommended tool for automatic graph resolution.
- [~] PARTIAL: Gaps identified — partially met. Three production concerns are absent from the skill: (1) no concurrency control guidance (`cancel-in-progress: true` on PR push, which cancels superseded runs and prevents CI queue buildup), (2) no artifact retention policy (how long pipeline artifacts are kept, which has both cost and compliance implications), (3) no required-status-check ruleset guidance for branch protection (without it, the `if: github.ref == 'refs/heads/main'` gate can be bypassed by anyone with direct push access). The PARTIAL criterion is satisfied: gaps are identified.

## Notes

The skill is well-constructed. The stage ordering, fast-path budget, caching strategy, SHA pinning, and security requirements are all precise, justified, and backed by concrete examples rather than vague rules.

The three absent production concerns are worth noting for a future revision. Concurrency control (`cancel-in-progress: true`) prevents queued runs on rapid PR pushes from burning CI minutes on stale commits — a cheap and common fix. Artifact retention policies affect both cost (GitHub charges for storage above the free tier) and compliance (some teams have retention windows). Required-status-check rulesets are the enforcement mechanism that makes the `if: github.ref == 'refs/heads/main'` gate meaningful — without them, developers with direct push access can bypass the gate entirely.

The monorepo section covers all three required sub-topics but is honest about the path-filter fallback's limitation: "no dependency graph awareness." This transparency is a quality signal, not a gap.
