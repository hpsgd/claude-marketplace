# Test: supply-chain-audit skill structure

Scenario: Checking that the supply-chain-audit skill assesses all four supply chain layers (source, build, dependency, artifact), maps findings to SLSA levels, and requires specific evidence rather than generic checklist completion.

## Prompt

Review the supply-chain-audit skill definition and verify it produces a SLSA-aligned assessment with specific findings that can drive a hardening roadmap.

Read the skill at `/Users/martin/Projects/turtlestack/plugins/engineering/security-engineer/skills/supply-chain-audit/SKILL.md` and verify each item by name. Quote skill text where present:

- **Source integrity controls**: signed commits, branch protection, code review requirements, CODEOWNERS, force-push prevention. Verify the skill uses `gh api repos/X/branches/main/protection` or equivalent to actually check these (not just CODEOWNERS file presence).
- **Build integrity**: hosted vs self-hosted runners, build-defined-in-code, build provenance / SLSA attestations, AND **log retention** explicitly.
- **Dependency integrity**: lockfiles committed, **no floating version ranges** (`^`, `~`, `*` flagged), Dependabot or PR dependency review, AND CI vulnerability scanning.
- **Artifact integrity**: container image signing (cosign / sigstore), SBOM generation (Syft / cyclonedx), AND **immutable image tags** (no `:latest`).
- **SLSA level mapping rule**: explicitly confirm "assessed level = highest where ALL requirements are met (not the average)" appears.
- **CI action SHA-pinning** with citation to the [GitHub Actions security hardening guide](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions).
- **All four supply-chain layers** (source, build, dependency, artifact) covered, none skippable.
- Bash commands provided per layer for evidence collection.

Confirm presence/absence of each by name — do not paraphrase.

## Criteria

- [ ] PASS: Skill assesses source integrity controls — signed commits, branch protection, code review requirements, CODEOWNERS, and force push prevention
- [ ] PASS: Skill assesses build integrity — hosted vs self-hosted runners, build defined in code, build provenance generation, and log retention
- [ ] PASS: Skill assesses dependency integrity — lockfiles present and committed, no floating version ranges, dependency review on PRs, and vulnerability scanning in CI
- [ ] PASS: Skill assesses artifact integrity — container image signing, SBOM generation, and immutable image tags
- [ ] PASS: Skill maps evidence to SLSA levels 0-4 and determines the current level as the highest where ALL requirements are met
- [ ] PASS: Skill provides specific bash commands to collect evidence — not just a description of what to look for
- [ ] PASS: Skill requires lockfiles to be present and committed — assigns automatic CRITICAL finding if absent
- [ ] PASS: Skill requires CI/CD actions to be pinned to full SHAs not tags, citing the GitHub Actions security hardening guide

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than running an actual supply-chain audit
- [ ] PASS: Output verifies all four supply chain layers are covered — source, build, dependency, artifact — and that none can be skipped
- [ ] PASS: Output confirms source-integrity controls — signed commits, branch protection, code review requirements, CODEOWNERS, and force-push prevention — are checked with concrete bash commands (e.g. `gh api repos/X/branches/main/protection`)
- [ ] PASS: Output confirms build-integrity coverage — hosted vs self-hosted runners, build-as-code, build provenance generation (SLSA attestations), and log retention
- [ ] PASS: Output verifies dependency-integrity coverage — lockfiles committed, no floating ranges (^, ~, *), Dependabot or equivalent dependency review on PRs, and CI vulnerability scanning
- [ ] PASS: Output confirms artifact-integrity coverage — container image signing (cosign / sigstore), SBOM generation (Syft / cyclonedx), and immutable image tags (no `:latest`)
- [ ] PASS: Output verifies SLSA level mapping — finds level 0 through 4 explicitly defined and the rule that the assessed level is the highest where ALL requirements are met (not the average)
- [ ] PASS: Output confirms specific bash commands are provided for evidence collection at each layer — not just descriptive text of what to look for
- [ ] PASS: Output confirms missing lockfiles trigger an automatic CRITICAL finding, and CI/CD action pinning to full 40-char SHAs (not tags) is required
- [ ] PARTIAL: Output identifies any genuine gaps — e.g. no rule on package registry mirror / proxy hardening, no guidance on assessing third-party GitHub Apps as supply-chain entry points
