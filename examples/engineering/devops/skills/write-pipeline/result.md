# Write Pipeline

Scenario: Checking that the write-pipeline skill produces a fail-fast pipeline with the correct stage order, dependency caching, pinned action versions, and secrets management — not a minimal hello-world workflow.

## Prompt

> Review the write-pipeline skill definition and verify it produces CI/CD pipelines that meet production standards for speed, security, and reliability.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've reviewed the write-pipeline skill definition. Here's my assessment against production standards:

## ✅ **Strengths**

**Speed:**
- Explicit time budgets (10 min fast path, 5-10 min per stage)
- Fail-fast ordering with cheapest checks first
- Solid caching strategy with hash-based keys
- Monorepo change detection to avoid rebuilding everything
- Matrix builds with fail-fast enabled

**Security:**
- Secrets management section (minimal scope, environment-specific, masking)
- Version pinning guidance (SHA for actions, digest for images)
- Mentions security scanning (npm audit, SAST with trivy)

## ⚠️ **Gaps for Production**

**Security:**
- **No concrete scanning strategy** — mentions `npm audit` and `trivy` but doesn't explain how to integrate or handle failures
- **Missing supply chain security** — no SBOM, artifact signing, provenance, or attestations
- **Lightweight dependency scanning** — `npm audit` alone doesn't catch transitive vulnerabilities deeply; needs lockfile scanning tools
- **No container scanning** — if building Docker, should scan images before push
- **No license compliance** — missing FOSSA/SPDX for license checks
- **No code review gates** — doesn't mention branch protection or approval requirements

**Reliability:**
- **Rollback is mentioned but not specified** — "documented or automated" is vague. Needs concrete rollback strategy (blue-green, canary, feature flags)
- **No post-deployment health checks** — only mentions "smoke test" with no implementation detail
- **No monitoring integration** — doesn't connect pipeline to observability systems
- **No deployment approval gates** — production deployments need manual review rules
- **Missing error recovery** — no retry logic, circuit breaker, or graceful degradation
- **No alerting strategy** — failure notifications should go to oncall, not email spam

## **Recommendations**

To reach production-grade standards, expand the skill with:

1. **Security section enhancements:**
   - Code scanning (Semgrep, CodeQL)
   - Dependency scanning (using tool-specific depth, not just `npm audit`)
   - Secrets scanning (truffleHog, git-secrets in pre-commit)
   - SBOM generation and supply chain integrity
   - Container scanning with severity thresholds

2. **Reliability section with:**
   - Concrete rollback strategies (blue-green, canary w/ monitoring)
   - Post-deployment health check templates
   - Integration with observability (metric collection on deploy)
   - Approval gates for production with manual review config

3. **Anti-patterns to strengthen:**
   - Add "no auto-rollback without verification" (auto-rollback can hide signal)
   - "No secrets in build args" needs container-specific implementation

Would you like me to draft enhancements to the skill definition, or audit a specific pipeline configuration against these standards?

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 7.5/17.0 (44%) |
| Evaluated | 2026-04-30 |
| Target duration | 25295 ms |
| Target cost | $0.0427 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill enforces the correct stage order — lint/format first, then build, then unit tests, then integration tests, then security scan, then deploy — with explicit fail-fast reasoning | PARTIAL | Output states 'Fail-fast ordering with cheapest checks first' and 'Matrix builds with fail-fast enabled' under strengths, but does not verify the specific stage sequence (lint → build → unit → integration → security → deploy) or quote any fail-fast reasoning from the skill. |
| c2 | Skill requires pipeline to complete the fast path (lint + build + unit tests) in under 10 minutes | PASS | Output explicitly states 'Explicit time budgets (10 min fast path, 5-10 min per stage)' under strengths, confirming the skill contains this requirement. |
| c3 | Skill requires caching with keys derived from lockfile hashes — and flags below 80% cache hit rate as a sign of incorrect key strategy | PARTIAL | Output mentions 'Solid caching strategy with hash-based keys' confirming the lockfile-hash key requirement, but makes no mention of the 80% cache hit rate threshold flag anywhere in strengths or gaps. |
| c4 | Skill requires GitHub Actions to be pinned to full commit SHAs not tags, citing the security risk of movable tags | PARTIAL | Output mentions 'Version pinning guidance (SHA for actions, digest for images)' confirming SHA pinning exists, but does not confirm 'full commit SHAs not tags' specifically nor does it quote or reference the supply-chain / movable-tag security risk. |
| c5 | Skill limits deployment to the main branch only and after all checks pass | FAIL | No mention anywhere in the output of deploy-from-main-only constraints, branch restrictions, or requiring all checks to pass before deployment. |
| c6 | Skill requires security scan stage — dependency audit at HIGH/CRITICAL level and SAST/container image scanning if applicable | PARTIAL | Output acknowledges 'Mentions security scanning (npm audit, SAST with trivy)' as a strength but then flags 'No concrete scanning strategy' as a gap. No mention of HIGH/CRITICAL severity threshold requirement. |
| c7 | Skill prohibits watch mode in CI and requires CI=true or --run flag for test commands | FAIL | No mention of watch mode, CI=true environment variable, --run flag, or hang-prevention for test commands anywhere in the output. |
| c8 | Skill addresses monorepo CI with change detection, selective execution, and dependency graph awareness | PARTIAL | Output lists 'Monorepo change detection to avoid rebuilding everything' as a strength, partially covering the criterion. Selective execution is implied. Dependency graph awareness is not mentioned. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample workflow | PARTIAL | Output is clearly a review of the skill (no sample workflow produced), organized into Strengths and Gaps sections. However, it is not structured as 'verdict per requirement' — it groups themes rather than confirming or denying individual skill requirements one by one. |
| c10 | Output verifies the stage order — lint/format → build → unit tests → integration tests → security scan → deploy — with fail-fast reasoning quoted or explained | PARTIAL | Output says 'Fail-fast ordering with cheapest checks first' but does not verify the explicit stage sequence (lint → build → unit → integration → security → deploy) nor quote or explain fail-fast reasoning from the skill text. |
| c11 | Output confirms the under-10-minute fast-path target (lint + build + unit tests) and that this is enforced, not aspirational | PARTIAL | Output confirms 'Explicit time budgets (10 min fast path)' exists in the skill, but does not distinguish whether this is enforced (e.g., pipeline fails if exceeded) or merely an aspirational target. |
| c12 | Output verifies the cache-key-from-lockfile-hash rule and the 80% cache hit rate threshold flag | PARTIAL | Output confirms 'Solid caching strategy with hash-based keys' but makes no mention of the 80% cache hit rate threshold, either as a confirmed strength or a gap. |
| c13 | Output confirms the security requirement to pin GitHub Actions to full commit SHAs (40-character hex), not tags or branches, with the supply-chain reasoning explicit | PARTIAL | Output notes 'Version pinning guidance (SHA for actions, digest for images)' but does not confirm 40-character hex format, 'not tags or branches' specificity, or any supply-chain reasoning from the skill. |
| c14 | Output verifies deploy-from-main-only after all checks pass, and that deployment from feature branches is rejected | FAIL | No mention of branch-restricted deployment, main-branch-only deploy, or rejection of feature-branch deployments anywhere in the output. |
| c15 | Output confirms the security scan stage covers dependency audit (HIGH/CRITICAL severity threshold) and SAST/container image scanning where applicable | PARTIAL | Output mentions 'npm audit, SAST with trivy' as what the skill 'mentions' and notes 'No concrete scanning strategy' as a gap. HIGH/CRITICAL severity threshold is never referenced. |
| c16 | Output verifies the watch-mode prohibition — CI=true env var or --run flag for test commands, never default watch mode that hangs the runner | FAIL | No reference to watch mode, CI=true, --run flag, or runner-hang scenarios anywhere in the output. |
| c17 | Output confirms monorepo handling addresses change detection, selective execution, and dependency graph awareness | PARTIAL | Output confirms 'Monorepo change detection to avoid rebuilding everything' covering change detection and implicit selective execution, but dependency graph awareness is not mentioned. |
| c18 | Output identifies any genuine gaps — e.g. no concurrency-control guidance (cancel-in-progress on PR push), no artifact retention policy, no required-status-check ruleset for branch protection | PARTIAL | Output identifies several genuine gaps (vague rollback strategy, missing post-deployment health checks, no deployment approval gates, no monitoring integration, no alerting strategy) but none match the specific examples cited (cancel-in-progress, artifact retention, required-status-checks). Ceiling is PARTIAL. |

### Notes

The captured output reads as a competent high-level review that identifies real strengths and gaps, but it is too shallow and thematically organized to satisfy the detailed verification criteria. It confirms the 10-minute fast-path budget and hash-based caching, and acknowledges SHA pinning and security scanning, but consistently fails to confirm the specifics that matter: exact stage order, 80% cache-hit threshold, 40-char SHA pinning with movable-tag reasoning, HIGH/CRITICAL severity thresholds, the watch-mode/CI=true prohibition, and deploy-from-main-only restrictions. Four criteria (c5, c7, c14, c16) are completely absent. The review also does not structure itself as a per-requirement verdict — it reads more like a consultant's summary than a systematic audit checklist.
