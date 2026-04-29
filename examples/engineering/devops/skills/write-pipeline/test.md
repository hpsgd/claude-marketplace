# Test: write-pipeline skill structure

Scenario: Checking that the write-pipeline skill produces a fail-fast pipeline with the correct stage order, dependency caching, pinned action versions, and secrets management — not a minimal hello-world workflow.

## Prompt

Review the write-pipeline skill definition and verify it produces CI/CD pipelines that meet production standards for speed, security, and reliability.

## Criteria

- [ ] PASS: Skill enforces the correct stage order — lint/format first, then build, then unit tests, then integration tests, then security scan, then deploy — with explicit fail-fast reasoning
- [ ] PASS: Skill requires pipeline to complete the fast path (lint + build + unit tests) in under 10 minutes
- [ ] PASS: Skill requires caching with keys derived from lockfile hashes — and flags below 80% cache hit rate as a sign of incorrect key strategy
- [ ] PASS: Skill requires GitHub Actions to be pinned to full commit SHAs not tags, citing the security risk of movable tags
- [ ] PASS: Skill limits deployment to the main branch only and after all checks pass
- [ ] PASS: Skill requires security scan stage — dependency audit at HIGH/CRITICAL level and SAST/container image scanning if applicable
- [ ] PASS: Skill prohibits watch mode in CI and requires CI=true or --run flag for test commands
- [ ] PARTIAL: Skill addresses monorepo CI with change detection, selective execution, and dependency graph awareness

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than producing a sample workflow
- [ ] PASS: Output verifies the stage order — lint/format → build → unit tests → integration tests → security scan → deploy — with fail-fast reasoning quoted or explained
- [ ] PASS: Output confirms the under-10-minute fast-path target (lint + build + unit tests) and that this is enforced, not aspirational
- [ ] PASS: Output verifies the cache-key-from-lockfile-hash rule and the 80% cache hit rate threshold flag
- [ ] PASS: Output confirms the security requirement to pin GitHub Actions to full commit SHAs (40-character hex), not tags or branches, with the supply-chain reasoning explicit
- [ ] PASS: Output verifies deploy-from-main-only after all checks pass, and that deployment from feature branches is rejected
- [ ] PASS: Output confirms the security scan stage covers dependency audit (HIGH/CRITICAL severity threshold) and SAST/container image scanning where applicable
- [ ] PASS: Output verifies the watch-mode prohibition — CI=true env var or --run flag for test commands, never default watch mode that hangs the runner
- [ ] PASS: Output confirms monorepo handling addresses change detection, selective execution, and dependency graph awareness
- [ ] PARTIAL: Output identifies any genuine gaps — e.g. no concurrency-control guidance (cancel-in-progress on PR push), no artifact retention policy, no required-status-check ruleset for branch protection
