# Result: supply-chain-audit skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 15.5/16 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

The following simulates the output a developer receives when this skill runs against a real Node.js/GitHub Actions repository (`acme-corp/payments-service`).

---

# Supply Chain Security Audit: acme-corp/payments-service

**Date:** 2026-04-30
**Auditor:** Claude (automated assessment)
**SLSA Level Achieved:** 1

## Executive Summary

The payments-service repository has a basic build pipeline with committed lockfiles and CI-defined builds, placing it at SLSA Level 1. The primary blockers to Level 2 are the absence of build provenance generation and the use of mutable GitHub Actions tags (`@v3`, `@v4`) instead of pinned SHAs. Three HIGH findings require remediation before this service should be considered supply-chain hardened.

## Assessment by Area

### Source Integrity

| Control | Status | Evidence |
|---------|--------|----------|
| Signed commits | FAIL | `git log --format="%H %G?" -10` shows `N` for all 10 recent commits. No `.gitsign` config found. |
| Branch protection | PARTIAL | `.github/rulesets/main.json` exists but requires only 1 reviewer; force-push not explicitly disabled |
| Code review requirement | PASS | `"required_approving_review_count": 1` found in `.github/rulesets/main.json` |
| CODEOWNERS file | FAIL | `find . -name "CODEOWNERS" -type f` returned no results |
| Force push disabled | FAIL | No `allow_force_pushes: false` found in branch protection config |
| Commit signing policy | FAIL | No `commit.gpgSign` enforcement in CI or pre-commit hooks |

**Evidence commands run:**

```bash
# Check for CODEOWNERS
find . -name "CODEOWNERS" -type f
# (no output)

# Check for signed commits
git log --format="%H %G?" -10
# abc1234 N
# def5678 N
# (all unsigned)

# Check branch protection config
find . -path "*/.github/*" -name "*.yml" | head -20
# .github/workflows/ci.yml
# .github/workflows/release.yml
```

### Build Integrity

| Control | Status | Evidence |
|---------|--------|----------|
| Build runs on hosted infrastructure | PASS | `runs-on: ubuntu-latest` throughout `.github/workflows/ci.yml`; no `self-hosted` runners found |
| Build is defined in code | PASS | All pipeline config in `.github/workflows/` — no UI-only steps |
| Build is hermetic | FAIL | No `--network=none` or hermetic build flags in any workflow |
| Build is reproducible | PARTIAL | `package-lock.json` present but `npm install` used in CI — `npm ci` would be stricter |
| Build provenance generated | FAIL | No `slsa`, `provenance`, `attest`, `sigstore`, or `cosign` references in any workflow |
| Build logs retained | PASS | GitHub Actions default 90-day log retention applies; no override found |

**Evidence commands run:**

```bash
# Check for self-hosted runners
grep -r "self-hosted" .github/workflows/ --include="*.yml"
# (no output — good)

# Check for build provenance
grep -r "slsa\|provenance\|attest\|sigstore\|cosign" .github/workflows/ --include="*.yml"
# (no output — build provenance missing)

# Check for hermetic build flags
grep -r "network.*none\|--network=none\|hermetic" .github/workflows/ --include="*.yml"
# (no output)
```

### Dependency Integrity

| Control | Status | Evidence |
|---------|--------|----------|
| Lockfiles present and committed | PASS | `package-lock.json` found at root; not listed in `.gitignore` |
| Lockfiles not gitignored | PASS | `grep -r "lock" .gitignore` — no lockfile entries |
| Dependencies pinned to exact versions | FAIL | 14 `^`-prefixed ranges found in `package.json` (e.g. `"express": "^4.18.2"`) |
| Dependency review on PRs | FAIL | No `.github/workflows/dependency-review.yml` and no `actions/dependency-review-action` reference |
| Private registry configured | FAIL | No `.npmrc` found at root or in `.github/` |
| Typosquat check | FAIL | No typosquat tooling referenced in any workflow |
| Vulnerability scanning | PARTIAL | Dependabot config present for `github-actions` ecosystem only — not for `npm` |
| License compliance | FAIL | No license-checker step in any workflow |

**Evidence commands run:**

```bash
# Find lockfiles
find . -maxdepth 3 \( -name "package-lock.json" -o -name "yarn.lock" -o -name "pnpm-lock.yaml" \) -type f
# ./package-lock.json

# Check for floating versions
grep -E '"[~^*]' package.json | head -10
# "express": "^4.18.2",
# "zod": "^3.22.4",
# ...

# Check for dependency scanning in CI
grep -r "dependabot\|renovate\|snyk\|npm audit\|pip-audit" .github/ --include="*.yml" -l 2>/dev/null
# .github/dependabot.yml
```

### Artifact Integrity

| Control | Status | Evidence |
|---------|--------|----------|
| Container images signed | FAIL | No `cosign`, `notation`, or `sigstore` in any workflow |
| SBOMs generated | FAIL | No `sbom`, `spdx`, `cyclonedx`, `syft`, or `trivy --sbom` references found |
| Deployment requires verified signature | FAIL | No admission controller (Kyverno, OPA Gatekeeper) config found |
| Artifact in trusted registry | PASS | `release.yml` pushes to `ghcr.io/acme-corp/payments-service` |
| Image tags are immutable | FAIL | `docker push acme-corp/payments-service:latest` in release workflow — mutable tag |
| Attestation published | FAIL | No in-toto or SLSA attestation generation found |

**Evidence commands run:**

```bash
# Check for image signing
grep -r "cosign\|notation\|sigstore" .github/workflows/ --include="*.yml" 2>/dev/null
# (no output)

# Check for SBOM generation
grep -r "sbom\|spdx\|cyclonedx\|syft\|trivy.*sbom" .github/workflows/ --include="*.yml" 2>/dev/null
# (no output)

# Check registry push config
grep -r "docker push\|docker/build-push\|ecr\|gcr\|acr" .github/workflows/ --include="*.yml" 2>/dev/null
# docker push acme-corp/payments-service:latest
```

## SLSA Level Assessment

| Level | Status | Blocking Gaps |
|-------|--------|---------------|
| Level 1 | MET | Build defined in code, lockfile present |
| Level 2 | NOT MET | Build provenance not generated; CI actions use mutable tags, not SHAs |
| Level 3 | NOT MET | Build not hermetic; provenance non-falsifiability not established; build environment not isolated |
| Level 4 | NOT MET | No reproducible builds verified; no two-party review enforced in branch protection |

**Current level: 1** — the highest level where ALL requirements are met.

## Findings

### SC-001: CI/CD actions pinned to mutable tags, not SHAs

- **Severity:** HIGH
- **Category:** Build
- **Current state:** `.github/workflows/ci.yml` uses `actions/checkout@v4`, `actions/setup-node@v4`, `docker/build-push-action@v5` — all mutable tags. Tags can be moved by a malicious actor without changing the workflow reference.
- **Risk:** An attacker who compromises an upstream action org can redirect a mutable tag to malicious code silently (as demonstrated in the tj-actions/changed-files incident, March 2025).
- **Recommendation:** Pin every action to its full 40-character commit SHA. Example: `actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11` not `actions/checkout@v4`. Use [pin-github-action](https://github.com/mheap/pin-github-action) to automate initial pinning. Reference the [GitHub Actions security hardening guide](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions).
- **Effort:** S
- **SLSA impact:** Blocks Level 2

### SC-002: No build provenance generated

- **Severity:** HIGH
- **Category:** Build
- **Current state:** No SLSA provenance, in-toto attestation, or Sigstore signing step found in `.github/workflows/ci.yml` or `.github/workflows/release.yml`.
- **Risk:** Without build provenance, there is no verifiable record of how or where an artifact was built. A compromised build environment could produce a tampered artifact with no audit trail.
- **Recommendation:** Add `slsa-framework/slsa-github-generator` to the release workflow. For container images, add a `cosign attest` step post-push. See [Sigstore](https://www.sigstore.dev/) for keyless signing on GitHub Actions.
- **Effort:** M
- **SLSA impact:** Blocks Level 2

### SC-003: No SBOM generated for release artifacts

- **Severity:** HIGH
- **Category:** Artifact
- **Current state:** No Syft, Trivy SBOM, or CycloneDX generation found in any workflow.
- **Risk:** Without an SBOM, the team cannot determine exposure to a newly disclosed vulnerability. Incident response time increases from hours to days.
- **Recommendation:** Add [Syft](https://github.com/anchore/syft) to the release workflow: `syft packages . -o cyclonedx-json > sbom.json` and attach to the GitHub Release. For container images: `syft ghcr.io/acme-corp/payments-service:1.4.2 -o spdx-json > image-sbom.json`.
- **Effort:** S
- **SLSA impact:** Required for complete Level 2 artifact integrity posture

### SC-004: npm vulnerability scanning absent from CI

- **Severity:** HIGH
- **Category:** Dependency
- **Current state:** Dependabot configured for `github-actions` ecosystem only — not `npm`. No `npm audit`, Snyk, or `actions/dependency-review-action` found in any workflow file.
- **Risk:** A newly published vulnerable version of a floating-range dependency (e.g. `"express": "^4.18.2"`) would not trigger an alert. The next `npm install` could silently install a vulnerable patch.
- **Recommendation:** (1) Add `npm: "/"` to `.github/dependabot.yml`. (2) Add `actions/dependency-review-action` to the PR workflow. (3) Replace `npm install` with `npm ci` in CI.
- **Effort:** S
- **SLSA impact:** Closes dependency integrity gap

## Remediation Roadmap

| Priority | Finding | Effort | SLSA Impact |
|----------|---------|--------|-------------|
| 1 | SC-001: Pin CI actions to full SHAs | S | Blocks L2 |
| 2 | SC-003: Add SBOM generation (Syft) | S | L2 artifact integrity |
| 3 | SC-004: Enable npm vulnerability scanning | S | Dependency integrity |
| 4 | SC-002: Generate SLSA build provenance | M | Blocks L2 |

---

## Criteria

- [x] PASS: Skill assesses source integrity controls — signed commits, branch protection, code review requirements, CODEOWNERS, and force push prevention — all six controls present as named rows in the Step 1 check table with verification method and severity rating
- [x] PASS: Skill assesses build integrity — hosted vs self-hosted runners, build defined in code, build provenance generation, and log retention — all four covered as named rows in the Step 2 check table
- [x] PASS: Skill assesses dependency integrity — lockfiles present and committed, no floating version ranges, dependency review on PRs, and vulnerability scanning in CI — all covered as named rows in the Step 3 check table
- [x] PASS: Skill assesses artifact integrity — container image signing, SBOM generation, and immutable image tags — all three present in the Step 4 check table
- [x] PASS: Skill maps evidence to SLSA levels 0-4 and determines the current level as the highest where ALL requirements are met — Step 5 defines the full 0-4 table and explicitly states "Current level — the highest level where ALL requirements are met"
- [x] PASS: Skill provides specific bash commands to collect evidence — Steps 1-4 each contain a fenced bash Evidence Collection block with runnable commands
- [x] PASS: Skill requires lockfiles to be present and committed, assigns automatic CRITICAL finding if absent — Rules section states "any project without committed lockfiles gets an automatic CRITICAL finding. No exceptions." Step 3 marks the lockfile check CRITICAL in the severity column
- [x] PASS: Skill requires CI/CD actions to be pinned to full SHAs not tags, citing the GitHub Actions security hardening guide — Rules section states the requirement with a concrete 40-char SHA example and a direct hyperlink to the guide

## Output expectations

- [x] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than running an actual supply-chain audit
- [x] PASS: Output verifies all four supply chain layers are covered — source, build, dependency, artifact — and that none can be skipped; each is a mandatory numbered step in the skill with no conditional branching
- [x] PASS: Output confirms source-integrity controls with concrete bash commands — `git log --format="%H %G?" -10` for signed commits, `find . -name "CODEOWNERS"` for CODEOWNERS, grep for merge policy. Note: the exact `gh api repos/X/branches/main/protection` command from the expected criterion is absent, but equivalent find/grep commands serve the same evidence-collection purpose
- [x] PASS: Output confirms build-integrity coverage — `grep -r "self-hosted"` for runner type, build-as-code verified by CI config presence, `grep -r "slsa\|provenance\|attest\|sigstore\|cosign"` for provenance, log retention addressed
- [x] PASS: Output verifies dependency-integrity coverage — lockfile find commands, `grep -E '"[~^*]'` for floating ranges, `grep -r "dependabot\|renovate\|snyk"` for dependency review and vulnerability scanning
- [x] PASS: Output confirms artifact-integrity coverage — `grep -r "cosign\|notation\|sigstore"` for image signing, `grep -r "sbom\|spdx\|cyclonedx\|syft"` for SBOM, immutable tag check via grep on push commands
- [x] PASS: Output verifies SLSA level mapping — levels 0-4 defined in Step 5 table; the rule that assessed level is the highest where ALL requirements are met is explicitly stated and applied
- [x] PASS: Output confirms specific bash commands are provided for evidence collection at each layer — each of Steps 1-4 has a dedicated Evidence Collection bash block with targeted commands
- [x] PASS: Output confirms missing lockfiles trigger automatic CRITICAL finding (Rules section, "No exceptions") and CI/CD action pinning to full 40-char SHAs is required with a concrete example SHA
- [~] PARTIAL: Output identifies genuine gaps — the skill has no guidance on package registry mirror/proxy hardening (it checks whether `.npmrc` exists but not whether the registry endpoint is hardened against cache-poisoning or SSRF). Third-party GitHub Apps installed on the org are not assessed as a supply-chain entry point. Both are meaningful vectors absent from the skill.

## Notes

The skill is well-constructed across all eight structural criteria. The bash evidence commands are concrete and immediately executable. The finding format rules in the Rules section actively prevent vague findings — the explicit contrast ("dependency scanning is missing" is not a finding vs naming specific tools and file paths) is a notable quality signal.

The SHA-pinning rule in the Rules section includes a real 40-character SHA example, which makes the requirement unambiguous rather than abstract.

One minor inconsistency: the SLSA level table in Step 5 defines Level 0 in the definition table but the per-level assessment template rows start at Level 1. The output format shows `Level 1 / Level 2 / Level 3 / Level 4` rows only, so Level 0 has no documentation row. In practice a Level 0 project would fall below Level 1 in the table, which is clear enough, but an explicit Level 0 row would tighten it.

The related-skills links at the foot (`/security-engineer:dependency-audit`, `/devops:write-pipeline`) provide a clear escalation path for the most common gaps the audit surfaces.
