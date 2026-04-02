---
name: supply-chain-audit
description: "Audit the software supply chain for integrity risks — source, build, dependencies, and artifact provenance. Produces a SLSA-aligned assessment with findings and hardening recommendations. Use when assessing supply chain posture or after a dependency incident."
argument-hint: "[repository, pipeline, or system to audit]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Audit the software supply chain for $ARGUMENTS.

Follow every step below. The output must be a structured assessment with specific findings and remediation actions — not a generic checklist.

---

## Step 1: Assess Source Integrity

Evaluate how the source code is protected from tampering:

### Checks

| Control | How to Verify | Severity if Missing |
|---------|---------------|---------------------|
| **Signed commits** | Check `git log --show-signature` or `.gitsign` config | MEDIUM |
| **Branch protection** | Check for `CODEOWNERS`, branch protection rules, or `ruleset` config | HIGH |
| **Code review requirement** | Check PR merge rules — are reviews required? How many? | HIGH |
| **CODEOWNERS file** | Look for `CODEOWNERS` or `.github/CODEOWNERS` | MEDIUM |
| **Force push disabled** | Check branch protection settings | HIGH |
| **Commit signing policy** | Check for `commit.gpgSign` in `.gitconfig` or CI enforcement | LOW |

### Evidence Collection

```bash
# Check for CODEOWNERS
find . -name "CODEOWNERS" -type f

# Check for branch protection config (GitHub)
find . -path "*/.github/*" -name "*.yml" | head -20

# Check for signed commits
git log --format="%H %G?" -10

# Check for merge commit policy
grep -r "merge" .github/ --include="*.yml" -l
```

Document each control as PASS, FAIL, or PARTIAL with specific evidence.

---

## Step 2: Assess Build Integrity

Evaluate whether the build process can be tampered with:

### Checks

| Control | How to Verify | Severity if Missing |
|---------|---------------|---------------------|
| **Build runs on hosted infrastructure** | CI config uses hosted runners, not self-hosted | HIGH |
| **Build is defined in code** | CI/CD config is in the repo, not configured in the UI | HIGH |
| **Build is hermetic** | No network access during build (or explicitly declared dependencies) | MEDIUM |
| **Build is reproducible** | Same inputs produce same outputs (lockfiles, pinned versions) | MEDIUM |
| **Build provenance generated** | Attestation or SLSA provenance document created | HIGH |
| **Build logs retained** | Logs are stored and accessible for audit | MEDIUM |

### Evidence Collection

```bash
# Find CI/CD configuration files
find . -name "*.yml" -path "*/.github/workflows/*" -o -name ".gitlab-ci.yml" -o -name "Jenkinsfile" -o -name "azure-pipelines.yml" | head -20

# Check for self-hosted runners
grep -r "self-hosted" .github/workflows/ --include="*.yml"

# Check for build provenance generation
grep -r "slsa\|provenance\|attest\|sigstore\|cosign" .github/workflows/ --include="*.yml"

# Check for hermetic build indicators
grep -r "network.*none\|--network=none\|hermetic" .github/workflows/ --include="*.yml"
```

---

## Step 3: Assess Dependency Integrity

Evaluate how third-party dependencies are managed:

### Checks

| Control | How to Verify | Severity if Missing |
|---------|---------------|---------------------|
| **Lockfiles present and committed** | `package-lock.json`, `poetry.lock`, `go.sum`, `Cargo.lock` exist in repo | CRITICAL |
| **Lockfiles are not ignored** | Not listed in `.gitignore` | CRITICAL |
| **Dependencies pinned to exact versions** | No floating ranges (`^`, `~`, `*`) in lockfile | HIGH |
| **Dependency review on PRs** | GitHub Dependency Review Action or equivalent | MEDIUM |
| **Private registry configured** | `.npmrc`, `pip.conf`, or `nuget.config` points to approved registry | MEDIUM |
| **Typosquat check** | Package names verified against known typosquat lists | MEDIUM |
| **Vulnerability scanning** | Dependabot, Renovate, Snyk, or `npm audit` in CI | HIGH |
| **License compliance** | License checker in CI or documented policy | LOW |

### Evidence Collection

```bash
# Find lockfiles
find . -maxdepth 3 \( -name "package-lock.json" -o -name "yarn.lock" -o -name "pnpm-lock.yaml" -o -name "poetry.lock" -o -name "Pipfile.lock" -o -name "go.sum" -o -name "Cargo.lock" -o -name "composer.lock" \) -type f

# Check if lockfiles are gitignored
grep -r "lock" .gitignore 2>/dev/null

# Check for registry configuration
find . -maxdepth 2 \( -name ".npmrc" -o -name "pip.conf" -o -name "nuget.config" -o -name ".yarnrc.yml" \) -type f

# Check for dependency scanning in CI
grep -r "dependabot\|renovate\|snyk\|npm audit\|pip-audit\|cargo audit\|trivy" .github/ --include="*.yml" -l 2>/dev/null

# Check for floating versions in package.json
grep -E '"[~^*]' package.json 2>/dev/null | head -10
```

---

## Step 4: Assess Artifact Integrity

Evaluate how built artifacts are protected:

### Checks

| Control | How to Verify | Severity if Missing |
|---------|---------------|---------------------|
| **Container images signed** | [Cosign](https://docs.sigstore.dev/cosign/signing/overview/) or Notation signatures | HIGH |
| **SBOMs generated** | SPDX or CycloneDX SBOM per release | HIGH |
| **Deployment requires verified signature** | Admission controller or policy engine validates signatures | HIGH |
| **Artifact stored in trusted registry** | ECR, GCR, ACR, or self-hosted with access controls | MEDIUM |
| **Image tags are immutable** | Tags cannot be overwritten (or digests used instead of tags) | MEDIUM |
| **Attestation published** | [In-toto](https://in-toto.io/) attestation or [SLSA](https://slsa.dev/) provenance attached to artifact | HIGH |

### Evidence Collection

```bash
# Check for image signing in CI
grep -r "cosign\|notation\|sigstore" .github/workflows/ --include="*.yml" 2>/dev/null

# Check for SBOM generation
grep -r "sbom\|spdx\|cyclonedx\|syft\|trivy.*sbom" .github/workflows/ --include="*.yml" 2>/dev/null

# Check for Dockerfile
find . -maxdepth 3 -name "Dockerfile*" -type f

# Check for registry push configuration
grep -r "docker push\|docker/build-push\|ecr\|gcr\|acr" .github/workflows/ --include="*.yml" 2>/dev/null
```

---

## Step 5: Determine SLSA Level Achieved

Based on the evidence collected, determine the [SLSA](https://slsa.dev/) level:

| SLSA Level | Requirements | Key Evidence |
|------------|-------------|--------------|
| **Level 0** | No guarantees | No build provenance, no lockfiles |
| **Level 1** | Documentation of the build process | Build defined in code, lockfiles present |
| **Level 2** | Hosted build service, signed provenance | CI runs on hosted runners, provenance generated |
| **Level 3** | Hardened build, non-falsifiable provenance | Hermetic build, isolated build environment, tamper-proof provenance |
| **Level 4** | Hermetic + reproducible, two-party review | All of Level 3 + reproducible builds + enforced code review |

### Assessment

For each level, document:
1. **Requirements met** — specific evidence from Steps 1-4
2. **Requirements not met** — specific gaps with remediation steps
3. **Current level** — the highest level where ALL requirements are met

---

## Step 6: Produce Findings and Recommendations

### Finding Format

For each finding:

| Field | Content |
|-------|---------|
| **ID** | SC-[NNN] |
| **Title** | Short description |
| **Severity** | CRITICAL / HIGH / MEDIUM / LOW |
| **Category** | Source / Build / Dependency / Artifact |
| **Current state** | What was found (with evidence) |
| **Risk** | What could happen if not addressed |
| **Recommendation** | Specific action to take |
| **Effort** | S / M / L |
| **SLSA impact** | Which SLSA level this blocks |

### Prioritisation

Order findings by:
1. CRITICAL severity first (these block production readiness)
2. Then by SLSA impact (findings that unlock the next SLSA level)
3. Then by effort (quick wins first)

---

## Rules

- **Lockfiles are non-negotiable** — any project without committed lockfiles gets an automatic CRITICAL finding. No exceptions.
- **Every CI/CD action must be pinned to a SHA, not a tag** — tags can be moved maliciously. `actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11` not `actions/checkout@v4`. Reference the [GitHub Actions security hardening guide](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions).
- **SBOMs should be generated for every release artifact** — without an SBOM, you cannot respond to a vulnerability disclosure (you do not know if you are affected).
- **Findings must cite specific evidence** — "dependency scanning is missing" is not a finding. "No `npm audit`, `pip-audit`, Snyk, or Dependabot configuration found in `.github/workflows/` or `dependabot.yml`" is a finding.
- **Do not recommend tools without justification** — if recommending Cosign for image signing, explain why it fits this project's stack and CI platform.
- Reference [SLSA](https://slsa.dev/) framework for supply chain levels and [Sigstore](https://www.sigstore.dev/) for keyless signing.

---

## Output Format

```markdown
# Supply Chain Security Audit: [Repository / System]

**Date:** [YYYY-MM-DD]
**Auditor:** Claude (automated assessment)
**SLSA Level Achieved:** [0-4]

## Executive Summary

[2-3 sentences: current posture, most critical gaps, recommended priority.]

## Assessment by Area

### Source Integrity
| Control | Status | Evidence |
|---------|--------|----------|
| Signed commits | PASS/FAIL/PARTIAL | [specific evidence] |
| Branch protection | PASS/FAIL/PARTIAL | [specific evidence] |
| ... | ... | ... |

### Build Integrity
| Control | Status | Evidence |
|---------|--------|----------|
| ... | ... | ... |

### Dependency Integrity
| Control | Status | Evidence |
|---------|--------|----------|
| ... | ... | ... |

### Artifact Integrity
| Control | Status | Evidence |
|---------|--------|----------|
| ... | ... | ... |

## SLSA Level Assessment

| Level | Status | Blocking Gaps |
|-------|--------|---------------|
| Level 1 | MET/NOT MET | [gaps] |
| Level 2 | MET/NOT MET | [gaps] |
| Level 3 | MET/NOT MET | [gaps] |
| Level 4 | MET/NOT MET | [gaps] |

## Findings

### SC-001: [Title]
- **Severity:** CRITICAL
- **Category:** Dependency
- **Current state:** [evidence]
- **Risk:** [what could happen]
- **Recommendation:** [specific action]
- **Effort:** S
- **SLSA impact:** Blocks Level 1

### SC-002: [Title]
...

## Remediation Roadmap

| Priority | Finding | Effort | SLSA Impact |
|----------|---------|--------|-------------|
| 1 | SC-001: [title] | S | Blocks L1 |
| 2 | SC-003: [title] | M | Blocks L2 |
| ... | ... | ... | ... |
```

---

## Related Skills

- `/security-engineer:dependency-audit` — deep-dive into dependency vulnerabilities. Use after this audit identifies dependency gaps.
- `/devops:write-pipeline` — harden the CI/CD pipeline based on audit findings. Pin actions to SHAs, add SBOM generation, add image signing.
