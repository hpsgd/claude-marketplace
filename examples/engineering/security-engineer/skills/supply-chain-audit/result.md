# Supply chain audit skill structure

Checking that the supply-chain-audit skill assesses all four supply chain layers (source, build, dependency, artifact), maps findings to SLSA levels, and requires specific evidence rather than generic checklist completion.

## Prompt

> Review the supply-chain-audit skill definition and verify it produces a SLSA-aligned assessment with specific findings that can drive a hardening roadmap.

## Output

**Step 1 — Source integrity checks:**

| Control | How to Verify | Severity if Missing |
|---|---|---|
| Signed commits | `git log --format="%H %G?" -10` | MEDIUM |
| Branch protection | Check `.github/` for ruleset config, `CODEOWNERS` | HIGH |
| Code review requirement | Check PR merge rules — review count | HIGH |
| CODEOWNERS file | `find . -name "CODEOWNERS" -type f` | MEDIUM |
| Force push disabled | Branch protection settings | HIGH |
| Commit signing policy | CI enforcement of `commit.gpgSign` | LOW |

**Step 2 — Build integrity checks:**

| Control | How to Verify | Severity if Missing |
|---|---|---|
| Hosted runners | `grep -r "self-hosted" .github/workflows/ --include="*.yml"` | HIGH |
| Build defined in code | CI config in repo, not UI | HIGH |
| Build provenance | `grep -r "slsa\|provenance\|attest\|sigstore\|cosign" .github/workflows/` | HIGH |
| Build logs retained | Log storage configuration | MEDIUM |

**Step 3 — Dependency integrity checks:**

| Control | How to Verify | Severity if Missing |
|---|---|---|
| Lockfiles present and committed | `find . -maxdepth 3 \( -name "package-lock.json" -o -name "yarn.lock" -o -name "poetry.lock" ... \)` | CRITICAL |
| Lockfiles not gitignored | `grep -r "lock" .gitignore` | CRITICAL |
| Dependencies pinned to exact versions | `grep -E '"[~^*]' package.json` | HIGH |
| Dependency review on PRs | `grep -r "dependabot\|renovate\|snyk\|npm audit" .github/` | MEDIUM |
| Vulnerability scanning in CI | Same grep as above | HIGH |

**Step 4 — Artifact integrity checks:**

| Control | How to Verify | Severity if Missing |
|---|---|---|
| Container images signed | `grep -r "cosign\|notation\|sigstore" .github/workflows/` | HIGH |
| SBOMs generated | `grep -r "sbom\|spdx\|cyclonedx\|syft" .github/workflows/` | HIGH |
| Image tags immutable | Registry configuration | MEDIUM |
| Attestation published | In-toto/SLSA provenance in CI | HIGH |

**Step 5 — SLSA level assessment:**

| SLSA Level | Requirements | Current level criteria |
|---|---|---|
| Level 0 | No provenance, no lockfiles | — |
| Level 1 | Build defined in code, lockfiles present | — |
| Level 2 | Hosted runners, signed provenance | — |
| Level 3 | Hermetic build, non-falsifiable provenance | — |
| Level 4 | Reproducible + two-party review | — |

Current level = the highest level where ALL requirements are met.

**Rules:**

Lockfiles absent = automatic CRITICAL finding. No exceptions.

Actions pinned to SHA: `actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11` not `actions/checkout@v4`. Tags can be moved maliciously. Reference: GitHub Actions security hardening guide at `https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions`.

**Output format:** SLSA Level Achieved, Assessment by Area (four tables), Findings in SC-NNN format with severity/category/current state/risk/recommendation/effort/SLSA impact, Remediation Roadmap ordered by SLSA impact.

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8/8 criteria met (100%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Skill assesses source integrity including signed commits, branch protection, CODEOWNERS, and force push — supply-chain-audit SKILL.md Step 1 checks table covers all five controls: Signed commits, Branch protection, Code review requirement, CODEOWNERS file, Force push disabled — each with How to Verify and Severity if Missing.
- [x] PASS: Skill assesses build integrity including hosted runners, build in code, provenance, log retention — supply-chain-audit SKILL.md Step 2 checks table covers all four: Build runs on hosted infrastructure, Build is defined in code, Build provenance generated, Build logs retained.
- [x] PASS: Skill assesses dependency integrity including lockfiles, floating versions, dependency review, vulnerability scanning — supply-chain-audit SKILL.md Step 3 checks table covers all four. Lockfiles absent = CRITICAL. Floating ranges checked via grep. Dependency review and vulnerability scanning both listed.
- [x] PASS: Skill assesses artifact integrity including image signing, SBOM generation, immutable tags — supply-chain-audit SKILL.md Step 4 checks table: Container images signed (Cosign/Notation), SBOMs generated (SPDX/CycloneDX), Image tags are immutable, Attestation published.
- [x] PASS: Skill maps to SLSA levels 0-4, current level is highest where ALL requirements met — supply-chain-audit SKILL.md Step 5 defines all five levels with requirements. "Current level — the highest level where ALL requirements are met."
- [x] PASS: Skill provides specific bash commands for evidence collection — supply-chain-audit SKILL.md every step has an Evidence Collection bash block with specific commands (find, grep, git log); not just descriptions of what to look for.
- [x] PASS: Automatic CRITICAL finding if lockfiles absent — supply-chain-audit SKILL.md Rules: "Lockfiles are non-negotiable — any project without committed lockfiles gets an automatic CRITICAL finding. No exceptions."
- [x] PASS: CI/CD actions pinned to SHAs not tags, citing GitHub Actions security hardening guide — supply-chain-audit SKILL.md Rules: full SHA example given (`actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11`), with explicit link to the GitHub Actions security hardening guide.

### Notes

This is the only test in the set scoring 100%. The supply-chain-audit definition is the most comprehensive of the security skills — every step has a structured checks table, bash evidence commands, and explicit SLSA mapping. The Remediation Roadmap ordering by SLSA impact is a useful addition not tested by the criteria. No gaps identified.
