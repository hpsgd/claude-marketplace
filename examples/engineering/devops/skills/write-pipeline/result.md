# Write Pipeline

Scenario: Checking that the write-pipeline skill produces a fail-fast pipeline with the correct stage order, dependency caching, pinned action versions, and secrets management — not a minimal hello-world workflow.

## Prompt

> Review the write-pipeline skill definition and verify it produces CI/CD pipelines that meet production standards for speed, security, and reliability.
> 
> Read the skill via the loaded plugin (it is available as `/devops:write-pipeline` in this session). The skill source is at `${CLAUDE_PLUGIN_ROOT}/skills/write-pipeline/SKILL.md` or equivalently `/Users/martin/Projects/turtlestack/plugins/engineering/devops/skills/write-pipeline/SKILL.md`. Read it and verify the following items by name. Quote skill text where present:
> 
> - **Stage order (6)**: lint/format → build → unit tests → integration tests → security scan → deploy. Fail-fast reasoning explicit.
> - **Fast-path target**: lint + build + unit tests under **10 minutes**, enforced.
> - **Cache key from lockfile hash**, plus **80% cache hit rate** threshold flag.
> - **GitHub Actions pinned to full 40-char commit SHAs** (not tags), supply-chain reasoning cited.
> - **Deploy restricted to `main` branch** after ALL checks pass.
> - **Security scan stage**: dependency audit at HIGH/CRITICAL, SAST, container image scanning.
> - **Test commands**: `CI=true` or `--run` flag — no default watch mode.
> - **Monorepo (3)**: change detection, selective execution, dependency graph awareness.
> - **Identified gaps**: any of — `concurrency: cancel-in-progress`, artifact retention, required-status-check ruleset.
> 
> Confirm or flag each by name.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Verification Report: `/devops:write-pipeline` Skill

**Overall:** 8 of 9 items confirmed. 3 identified gaps (expected) found.

---

### ✓ Confirmed Items

**1. Stage order (6) + fail-fast reasoning**
- Quoted (L27–29): `Lint/Format → Build → Unit Tests → Integration Tests → Security Scan → Deploy`
- Reasoning explicit (L25): "fail fast — cheapest checks first"

**2. Fast-path target: <10 min**
- Quoted (L31): "Total pipeline time budget: under 10 minutes for the fast path (lint + build + unit tests)."

**3. Cache key from lockfile hash + 80% hit rate threshold**
- Hash quoted (L134): `key: node-${{ hashFiles('package-lock.json') }}`
- Threshold quoted (L159): "Monitor cache hit rates — below 80% means the key strategy is wrong"

**4. GitHub Actions pinned to 40-char SHA + supply-chain reasoning**
- SHA example (L224): `actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11`
- Reasoning (L233): "Pin GitHub Actions to commit SHA, not tag (tags can be moved)"

**5. Deploy restricted to `main` + all checks pass**
- Quoted (L114): `if: github.ref == 'refs/heads/main' && success()`
- Rule (L119): "Deploy only on main branch, only after ALL checks pass"

**6. Security scan: dependency audit + SAST + container scanning**
- Dependency audit (L100–101): `npm audit --audit-level=high` or `trivy fs . --severity HIGH,CRITICAL`
- SAST requirement (L107): "Run SAST (static analysis) in addition to dependency audit"
- Container scanning (L108): "Container image scanning if building Docker images"

**7. Test commands: `CI=true` or `--run` flag**
- Examples (L68, 81): `CI=true npm test`, `CI=true npm run test:integration`
- Rule (L72): "Run in run mode, never watch mode (`CI=true` or explicit `--run` flag)"
- Anti-pattern (L240): "Watch mode in CI — tests never exit. Always use `CI=true` or `--run`"

**8. Monorepo (3 elements): change detection + selective execution + dependency graph**
- All three elements quoted (L183–189):
  1. Change detection: "determine which projects changed using path filters or `git diff`"
  2. Selective execution: "only build/test projects that changed or depend on changed code"
  3. Dependency graph: "if project A depends on project B and B changed, test A too. Use [Moon](https://moonrepo.dev) (`moon ci`) or similar"

---

### ✗ Identified Gaps

**9. Expected gaps (production hardening items not present):**

- **`concurrency: cancel-in-progress`** — Not mentioned. Prevents wasting CI minutes on redundant runs when new commits push during pipeline execution.
- **Artifact retention policy** — Not specified. Artifacts are mentioned (L61 "Build output is cached or uploaded as an artifact") but no guidance on retention/cleanup (e.g., `retention-days: 30`).
- **Required status check ruleset** — Not mentioned. GitHub branch protection rules (enforce all checks pass before merge) are operational, not technical pipeline config, but should be documented.

---

### Summary

The skill is **production-ready for the core 6-stage pipeline, caching, and monorepo awareness**. The three gaps are operational/defensive hardening items that don't affect correctness but reduce CI cost and visibility. They're discoverable items, not oversights — each deserves its own decision based on repo usage patterns.

**Recommendation:** Add a brief section on GitHub branch protection rules (required checks, dismiss stale reviews, require code owner approval) so teams know what operational rules to enforce alongside this pipeline.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-03 |
| Target duration | 22912 ms |
| Target cost | $0.0560 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill enforces the correct stage order — lint/format first, then build, then unit tests, then integration tests, then security scan, then deploy — with explicit fail-fast reasoning | PASS | Output quotes L27–29: 'Lint/Format → Build → Unit Tests → Integration Tests → Security Scan → Deploy' and L25: 'fail fast — cheapest checks first' |
| c2 | Skill requires pipeline to complete the fast path (lint + build + unit tests) in under 10 minutes | PASS | Output quotes L31: 'Total pipeline time budget: under 10 minutes for the fast path (lint + build + unit tests).' |
| c3 | Skill requires caching with keys derived from lockfile hashes — and flags below 80% cache hit rate as a sign of incorrect key strategy | PASS | Output quotes L134: 'key: node-${{ hashFiles('package-lock.json') }}' and L159: 'Monitor cache hit rates — below 80% means the key strategy is wrong' |
| c4 | Skill requires GitHub Actions to be pinned to full commit SHAs not tags, citing the security risk of movable tags | PASS | Output quotes SHA example at L224 and supply-chain reasoning at L233: 'Pin GitHub Actions to commit SHA, not tag (tags can be moved)' |
| c5 | Skill limits deployment to the main branch only and after all checks pass | PASS | Output quotes L114: 'if: github.ref == 'refs/heads/main' && success()' and L119: 'Deploy only on main branch, only after ALL checks pass' |
| c6 | Skill requires security scan stage — dependency audit at HIGH/CRITICAL level and SAST/container image scanning if applicable | PASS | Output quotes L100–101 for dependency audit at HIGH/CRITICAL ('npm audit --audit-level=high' / 'trivy fs . --severity HIGH,CRITICAL'), L107 for SAST, and L108 for container image scanning |
| c7 | Skill prohibits watch mode in CI and requires CI=true or --run flag for test commands | PASS | Output quotes L68/81 ('CI=true npm test', 'CI=true npm run test:integration'), L72 rule, and L240 anti-pattern: 'Watch mode in CI — tests never exit. Always use CI=true or --run' |
| c8 | Skill addresses monorepo CI with change detection, selective execution, and dependency graph awareness | PARTIAL | Output quotes all three elements at L183–189: change detection via path filters/git diff, selective execution of changed projects, and dependency graph awareness (Moon ci). Ceiling capped at PARTIAL. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample workflow | PASS | Output is explicitly titled 'Verification Report' with numbered confirmed items and identified gaps section — no sample workflow generated |
| c10 | Output verifies the stage order — lint/format → build → unit tests → integration tests → security scan → deploy — with fail-fast reasoning quoted or explained | PASS | Under '1. Stage order (6) + fail-fast reasoning', output quotes the full 6-stage order from L27–29 and cites the fail-fast reasoning from L25 |
| c11 | Output confirms the under-10-minute fast-path target (lint + build + unit tests) and that this is enforced, not aspirational | PASS | Output quotes L31 with 'Total pipeline time budget: under 10 minutes for the fast path' — 'budget' framing indicates a hard constraint, confirmed as a skill requirement |
| c12 | Output verifies the cache-key-from-lockfile-hash rule and the 80% cache hit rate threshold flag | PASS | Output quotes both the lockfile hash key (L134) and the 80% threshold flag (L159) with direct text from the skill |
| c13 | Output confirms the security requirement to pin GitHub Actions to full commit SHAs (40-character hex), not tags or branches, with the supply-chain reasoning explicit | PASS | Output cites L224 with a full 40-char SHA example and L233 supply-chain reasoning: 'tags can be moved' |
| c14 | Output verifies deploy-from-main-only after all checks pass, and that deployment from feature branches is rejected | PASS | Output quotes the conditional 'github.ref == refs/heads/main && success()' which implicitly rejects feature branches, plus the rule 'Deploy only on main branch, only after ALL checks pass' |
| c15 | Output confirms the security scan stage covers dependency audit (HIGH/CRITICAL severity threshold) and SAST/container image scanning where applicable | PASS | Output confirms all three sub-components with direct quotes: HIGH/CRITICAL audit commands (L100–101), SAST (L107), and container image scanning conditioned on Docker usage (L108) |
| c16 | Output verifies the watch-mode prohibition — CI=true env var or --run flag for test commands, never default watch mode that hangs the runner | PASS | Output quotes the watch-mode prohibition from three locations (L68, L72, L240) including the explicit anti-pattern note about tests never exiting |
| c17 | Output confirms monorepo handling addresses change detection, selective execution, and dependency graph awareness | PASS | Output quotes all three elements from L183–189 with specific skill text for each: path filters/git diff, selective build/test, and Moon ci for dependency graph traversal |
| c18 | Output identifies any genuine gaps — e.g. no concurrency-control guidance (cancel-in-progress on PR push), no artifact retention policy, no required-status-check ruleset for branch protection | PARTIAL | Output identifies all three example gaps explicitly: 'concurrency: cancel-in-progress — Not mentioned', artifact retention 'Not specified', and required-status-check ruleset 'Not mentioned'. Ceiling capped at PARTIAL. |

### Notes

The captured output is a thorough, well-structured verification report that addresses every criterion with direct line-number citations and quoted text from the skill source. All 16 PASS-ceiling criteria are met with specific evidence. Both PARTIAL-ceiling criteria (c8 monorepo and c18 gaps) are fully supported by the evidence but correctly capped at 0.5 each per the scoring rules. The output achieves a perfect 17/17 against the weighted maximum, earning a clean PASS verdict. Notably, the response goes beyond minimal confirmation — it quotes anti-patterns, provides multi-source corroboration for several criteria, and offers a concrete recommendation for the identified gaps.
