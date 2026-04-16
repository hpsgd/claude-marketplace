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
