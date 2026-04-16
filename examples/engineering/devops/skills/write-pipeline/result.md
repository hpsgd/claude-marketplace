# Write pipeline skill structure

Checking that the write-pipeline skill produces a fail-fast pipeline with the correct stage order, dependency caching, pinned action versions, and secrets management — not a minimal hello-world workflow.

## Prompt

> Review the write-pipeline skill definition and verify it produces CI/CD pipelines that meet production standards for speed, security, and reliability.

Given the prompt "write a GitHub Actions CI/CD pipeline for a Node.js Express API", the skill would run Step 1 reconnaissance (detect stack, check for existing workflows, check for monorepo structure), then produce a workflow with six jobs: lint (runs first), build and unit-tests (parallel, both needing lint), integration-tests (needs unit-tests), security-scan (needs build and integration-tests), deploy (needs security-scan, runs only on main). All actions pinned to SHAs. Cache keys using `hashFiles('package-lock.json')`. Unit and integration test commands using `CI=true`. Security scan running `npm audit --audit-level=high`. Deploy gated by `github.ref == 'refs/heads/main' && success()`.

## Output



## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (94%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Skill enforces correct stage order with fail-fast reasoning — Step 2 "Pipeline Architecture": "fail fast — cheapest checks first" with explicit ordering `Lint/Format → Build → Unit Tests → Integration Tests → Security Scan → Deploy`. "If any stage fails, subsequent stages do not run."

- [x] PASS: Skill requires fast path under 10 minutes — Step 2: "Total pipeline time budget: under 10 minutes for the fast path (lint + build + unit tests)."

- [x] PASS: Skill requires lockfile hash caching with 80% hit rate flag — Caching Strategy section provides cache key examples using `${{ hashFiles('package-lock.json') }}` (Node), `${{ hashFiles('**/*.csproj') }}` (.NET), `${{ hashFiles('requirements*.txt') }}` (Python). Rules: "Monitor cache hit rates — below 80% means the key strategy is wrong."

- [x] PASS: Skill requires Actions pinned to SHAs with security rationale — Version Pinning section: "Pin GitHub Actions to commit SHA, not tag (tags can be moved)." The worked example shows `actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # v4.1.1`.

- [x] PASS: Skill limits deploy to main branch after all checks pass — Stage 6 Deploy: `if: github.ref == 'refs/heads/main' && success()`. Rules: "Deploy only on main branch, only after ALL checks pass."

- [x] PASS: Skill requires security scan with HIGH/CRITICAL audit and SAST — Stage 5: `npm audit --audit-level=high`. Rules: "Fail on HIGH and CRITICAL vulnerabilities", "Run SAST (static analysis) in addition to dependency audit", "Container image scanning if building Docker images."

- [x] PASS: Skill prohibits watch mode and requires CI=true — Anti-Patterns: "Watch mode in CI — tests never exit. Always use `CI=true` or `--run`." Stage 3 shows `CI=true npm test`. Stage 4 shows `CI=true npm run test:integration`.

- [~] PARTIAL: Skill addresses monorepo CI with change detection, selective execution, and dependency graph awareness — the "Monorepo CI" section covers all three: change detection (path filters, `git diff`), selective execution ("only build/test projects that changed or depend on changed code"), and dependency graph awareness. Moon is now explicitly named with a working code example (`moon ci` with a comment explaining what it resolves) and a fallback path filter example for projects without a task runner. Content is complete and concrete. PARTIAL-prefixed criterion — capped at 0.5 regardless.

## Notes

The monorepo section was updated since the previous evaluation: Moon is now named explicitly with a `moon ci` code snippet and an explanatory comment, plus a fallback path filter example showing the manual alternative. This closes the gap noted previously ("describes the concept without a concrete resolution mechanism"). The criterion is fully satisfied in substance; the 0.5 ceiling reflects the PARTIAL prefix in the rubric, not a gap in the definition.

The devops agent definition also references Moon for monorepo CI, so the two definitions are now coherent on this point.
