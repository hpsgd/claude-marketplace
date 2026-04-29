# Output: supply-chain-audit skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill assesses source integrity controls — signed commits, branch protection, code review requirements, CODEOWNERS, and force push prevention — met: Step 1 check table names all five as explicit rows with verification method and severity.
- [x] PASS: Skill assesses build integrity — hosted vs self-hosted runners, build defined in code, build provenance generation, and log retention — met: Step 2 check table covers all four as named rows.
- [x] PASS: Skill assesses dependency integrity — lockfiles present and committed, no floating version ranges, dependency review on PRs, and vulnerability scanning in CI — met: Step 3 check table names all four as explicit rows including "Dependencies pinned to exact versions" for the floating-range check.
- [x] PASS: Skill assesses artifact integrity — container image signing, SBOM generation, and immutable image tags — met: Step 4 check table includes "Container images signed", "SBOMs generated", and "Image tags are immutable".
- [x] PASS: Skill maps evidence to SLSA levels 0-4 and determines the current level as the highest where ALL requirements are met — met: Step 5 defines the full 0-4 table; the assessment instructions explicitly state "Current level — the highest level where ALL requirements are met."
- [x] PASS: Skill provides specific bash commands to collect evidence — not just a description of what to look for — met: Steps 1-4 each contain a fenced bash Evidence Collection block with runnable commands.
- [x] PASS: Skill requires lockfiles to be present and committed — assigns automatic CRITICAL finding if absent — met: Rules section states "any project without committed lockfiles gets an automatic CRITICAL finding. No exceptions." Step 3 also marks the lockfile check CRITICAL in the severity column.
- [x] PASS: Skill requires CI/CD actions to be pinned to full SHAs not tags, citing the GitHub Actions security hardening guide — met: Rules section states the requirement with a concrete example (`actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11` not `actions/checkout@v4`) and links to the GitHub Actions security hardening guide.

### Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than running an actual supply-chain audit.
- [x] PASS: Output verifies all four supply chain layers — source, build, dependency, artifact — are covered and none can be skipped; each is a mandatory numbered step with no conditional branching.
- [x] PASS: Output confirms source-integrity controls — signed commits, branch protection, code review requirements, CODEOWNERS, and force-push prevention — are checked with concrete bash commands (e.g. `git log --format="%H %G?" -10`, `find . -name "CODEOWNERS" -type f`). The `gh api repos/X/branches/main/protection` command from the expected criterion is not present, but `find . -path "*/.github/*" -name "*.yml"` and the CODEOWNERS find serve an equivalent evidence-collection purpose.
- [x] PASS: Output confirms build-integrity coverage — hosted vs self-hosted runners (`grep -r "self-hosted"`), build-as-code (CI config in repo as the source), build provenance generation (`grep -r "slsa\|provenance\|attest\|sigstore\|cosign"`), and log retention — all addressed.
- [x] PASS: Output verifies dependency-integrity coverage — lockfiles committed (`find . -maxdepth 3 \( -name "package-lock.json" ... \)`), no floating ranges (`grep -E '"[~^*]' package.json`), dependency review on PRs (`grep -r "dependabot\|renovate\|snyk"`), and CI vulnerability scanning — all covered.
- [x] PASS: Output confirms artifact-integrity coverage — container image signing with cosign/Notation (`grep -r "cosign\|notation\|sigstore"`), SBOM generation via syft/CycloneDX/SPDX (`grep -r "sbom\|spdx\|cyclonedx\|syft\|trivy.*sbom"`), and immutable image tags as an explicit MEDIUM-severity control — all covered.
- [x] PASS: Output verifies SLSA level mapping — levels 0 through 4 explicitly defined in Step 5 table; the assessed level is the highest where ALL requirements are met (stated explicitly in assessment instructions).
- [x] PASS: Output confirms specific bash commands are provided for evidence collection at each layer — each of Steps 1-4 has a dedicated Evidence Collection bash block with targeted commands, not descriptive text.
- [x] PASS: Output confirms missing lockfiles trigger an automatic CRITICAL finding (Rules section, "No exceptions") and CI/CD action pinning to full 40-char SHAs is required with a concrete example.
- [~] PARTIAL: Output identifies genuine gaps — the skill checks for private registry configuration (`.npmrc`, `pip.conf`) but provides no guidance on proxy/mirror hardening strategies. Third-party GitHub Apps as supply-chain entry points are not addressed anywhere in the skill. Both are real gaps in a comprehensive SLSA-aligned audit.

## Notes

The skill is substantive and tightly constructed. The eight structural criteria are all fully met. The output expectation on source-integrity bash commands is technically met — the skill uses `find` and `git log` — though the exact `gh api repos/X/branches/main/protection` command from the expected criterion is absent. This is a minor gap in coverage but not a fail given equivalent evidence-collection commands are present.

The one PARTIAL reflects real omissions: no proxy/registry mirror hardening guidance beyond noting the config file exists, and no coverage of third-party GitHub Apps as a supply-chain attack surface (installation tokens, webhook secrets, OAuth scopes). These are meaningful for production-grade audits but do not undermine the overall framework.

The related-skills links at the foot of the skill (`/security-engineer:dependency-audit`, `/devops:write-pipeline`) provide a clear escalation path when the audit surfaces gaps.
