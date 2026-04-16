# Test: supply-chain-audit skill structure

Scenario: Checking that the supply-chain-audit skill assesses all four supply chain layers (source, build, dependency, artifact), maps findings to SLSA levels, and requires specific evidence rather than generic checklist completion.

## Prompt

Review the supply-chain-audit skill definition and verify it produces a SLSA-aligned assessment with specific findings that can drive a hardening roadmap.

## Criteria

- [ ] PASS: Skill assesses source integrity controls — signed commits, branch protection, code review requirements, CODEOWNERS, and force push prevention
- [ ] PASS: Skill assesses build integrity — hosted vs self-hosted runners, build defined in code, build provenance generation, and log retention
- [ ] PASS: Skill assesses dependency integrity — lockfiles present and committed, no floating version ranges, dependency review on PRs, and vulnerability scanning in CI
- [ ] PASS: Skill assesses artifact integrity — container image signing, SBOM generation, and immutable image tags
- [ ] PASS: Skill maps evidence to SLSA levels 0-4 and determines the current level as the highest where ALL requirements are met
- [ ] PASS: Skill provides specific bash commands to collect evidence — not just a description of what to look for
- [ ] PASS: Skill requires lockfiles to be present and committed — assigns automatic CRITICAL finding if absent
- [ ] PASS: Skill requires CI/CD actions to be pinned to full SHAs not tags, citing the GitHub Actions security hardening guide
