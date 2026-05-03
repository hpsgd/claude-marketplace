# Supply Chain Audit

Scenario: Checking that the supply-chain-audit skill assesses all four supply chain layers (source, build, dependency, artifact), maps findings to SLSA levels, and requires specific evidence rather than generic checklist completion.

## Prompt

> Review the supply-chain-audit skill definition and verify it produces a SLSA-aligned assessment with specific findings that can drive a hardening roadmap.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here is the assessment:

---

## Supply Chain Audit Skill Review

**File:** `/Users/martin/.claude/plugins/cache/turtlestack/security-engineer/1.7.6/skills/supply-chain-audit/SKILL.md`

---

### What works well

- Finding format is solid: ID, severity, evidence, risk, recommendation, effort, and SLSA impact — enough structure to translate directly to a backlog.
- Rules section is unusually concrete: lockfile non-negotiable CRITICAL, SHA-pinning mandate, SBOM-per-release, and the "findings must cite specific evidence" rule guards against generic output.
- Prioritisation logic (CRITICAL → SLSA-blocking → quick wins) produces an actionable roadmap order.
- Step 3 dependency evidence commands are detailed and cover all major ecosystems.

---

### Gap 1 — SLSA spec is outdated (blocker)

The level table maps to **SLSA v0.1 (draft)**, not **SLSA v1.0 (ratified 2023)**. Differences:

| Skill (v0.1) | SLSA v1.0 |
|---|---|
| Level 0 — No guarantees | Not a level in v1.0 |
| Level 1 — Build defined in code | L1 — Provenance exists |
| Level 2 — Hosted runners, signed provenance | L2 — Hosted build, signed provenance |
| Level 3 — Hardened, non-falsifiable provenance | L3 — Hardened build, non-falsifiable provenance |
| Level 4 — Reproducible, two-party review | **Removed in v1.0** |

A team using this output to target a SLSA level will be working from an obsolete map. The skill should reference the v1.0 Build Track (L1–L3) only, and note that Source Track is a separate ladder.

**Fix:** Replace the level table with SLSA v1.0 Build Track L1–L3 requirements. Remove L4. Distinguish Build Track from Source Track.

---

### Gap 2 — Several Step 1 controls are structurally unverifiable

`allowed-tools` is `Read, Bash, Glob, Grep` — no `WebFetch`. Branch protection rules, required reviewers, default token permissions, and force-push policy live in the **GitHub API**, not in repo files. The evidence commands in Step 1 can only find `CODEOWNERS` and CI YAML; they cannot verify the controls they claim to check.

Affected controls that will silently produce wrong results:

- Branch protection (no file to read — lives in GitHub settings)
- Code review requirement (same)
- Force push disabled (same)

**Fix:** Mark these controls as "requires GitHub API or manual verification" and note the tool limitation in the output format. Don't produce PASS/FAIL for controls the skill cannot actually observe.

---

### Gap 3 — SHA-pinning rule has no detection command

The Rules section (line 205) mandates that every CI action must be pinned to a SHA, not a tag — this is the single most-cited supply chain hardening control. But no bash command in Step 2 actually detects `uses: actions/checkout@v4` vs `uses: actions/checkout@b4ffde6...`.

This means a repo with dozens of floating tag references will produce no finding.

**Fix:** Add to Step 2 evidence collection:

```bash
# Detect CI actions pinned to tags instead of SHAs
grep -rn "uses:.*@" .github/workflows/ --include="*.yml" | grep -v "@[a-f0-9]\{40\}"
```

---

### Gap 4 — Platform monoculture

Every evidence command targets `.github/workflows/`. GitLab CI, Jenkins, Azure DevOps, and CircleCI repos will silently return empty results, and every Build/Artifact control will appear as FAIL rather than "not applicable." A multi-platform audit will misclassify posture.

**Fix:** Detect the CI platform early and branch evidence collection:

```bash
# Detect CI platform
ls .github/workflows/ 2>/dev/null && echo "GitHub Actions"
ls .gitlab-ci.yml 2>/dev/null && echo "GitLab CI"
ls Jenkinsfile 2>/dev/null && echo "Jenkins"
ls azure-pipelines.yml 2>/dev/null && echo "Azure DevOps"
```

---

### Gap 5 — Self-hosted runners incorrectly classified as HIGH

The Build Integrity table marks self-hosted runners as a HIGH finding regardless of configuration. SLSA v1.0 does not prohibit self-hosted runners — it requires tamper-resistance. A properly isolated, ephemeral self-hosted runner can satisfy L2 and potentially L3. Marking all self-hosted as HIGH will generate false positives and erode trust in findings.

**Fix:** Change to "Self-hosted runners without ephemeral/isolated configuration" as HIGH. A self-hosted runner with ephemeral instances and no persistent state is not a gap.

---

### Summary

| Issue | Impact on stated purpose |
|---|---|
| SLSA v0.1 level table | Blocker — hardening roadmap targets wrong spec |
| Unverifiable Step 1 controls | Structural gap — produces false confidence |
| Missing SHA-pin detection | Missing the most important finding in practice |
| GitHub-only evidence commands | Wrong findings on non-GitHub repos |
| Self-hosted = HIGH (unconditional) | False positives erode roadmap credibility |

The skill produces well-structured output and the finding/roadmap format is genuinely good. The two changes that most directly affect whether the output drives real hardening: update the SLSA level table to v1.0, and add the SHA-pinning grep.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 11.0/17.5 (63%) |
| Evaluated | 2026-05-01 |
| Target duration | 128436 ms |
| Target cost | $0.4587 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill assesses source integrity controls — signed commits, branch protection, code review requirements, CODEOWNERS, and force push prevention | PASS | Gap 2 explicitly lists 'Branch protection rules, required reviewers, default token permissions, and force-push policy' as controls Step 1 attempts to assess, along with 'CODEOWNERS and CI YAML' as findable artifacts. |
| c2 | Skill assesses build integrity — hosted vs self-hosted runners, build defined in code, build provenance generation, and log retention | PARTIAL | Gap 5 confirms self-hosted runners are in the Build Integrity table. The SLSA comparison table in Gap 1 shows 'Hosted runners, signed provenance' and 'Build defined in code' as mapped concepts. Log retention is never mentioned anywhere in the output. |
| c3 | Skill assesses dependency integrity — lockfiles present and committed, no floating version ranges, dependency review on PRs, and vulnerability scanning in CI | PARTIAL | 'lockfile non-negotiable CRITICAL' and 'Step 3 dependency evidence commands are detailed and cover all major ecosystems' confirm lockfile and broad dependency coverage. Floating version ranges (^, ~, *), Dependabot/PR dependency review, and CI vulnerability scanning are not explicitly verified. |
| c4 | Skill assesses artifact integrity — container image signing, SBOM generation, and immutable image tags | PARTIAL | 'SBOM-per-release' is cited in 'What works well.' Container image signing (cosign/sigstore) and immutable image tags (no :latest) are not mentioned anywhere in the output. |
| c5 | Skill maps evidence to SLSA levels 0-4 and determines the current level as the highest where ALL requirements are met | PARTIAL | Gap 1 shows the level table L0–L4 exists in the skill. The 'all requirements met (not the average)' assessment rule is never mentioned or verified in the output. |
| c6 | Skill provides specific bash commands to collect evidence — not just a description of what to look for | PASS | 'Step 3 dependency evidence commands are detailed and cover all major ecosystems.' Gap 3 notes a specific missing bash command for SHA-pinning detection, implying the reviewer verified command presence vs absence across the skill. |
| c7 | Skill requires lockfiles to be present and committed — assigns automatic CRITICAL finding if absent | PASS | Explicitly stated in 'What works well': 'lockfile non-negotiable CRITICAL' directly confirms an automatic CRITICAL finding is assigned when lockfiles are absent. |
| c8 | Skill requires CI/CD actions to be pinned to full SHAs not tags, citing the GitHub Actions security hardening guide | PARTIAL | Gap 3 confirms 'The Rules section (line 205) mandates that every CI action must be pinned to a SHA, not a tag.' The GitHub Actions security hardening guide is not mentioned as the citation source. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than running an actual supply-chain audit | PASS | The output is titled 'Supply Chain Audit Skill Review,' reads the skill file at a specific path, and discusses gaps in the skill definition itself — not findings from a real repository audit. |
| c10 | Output verifies all four supply chain layers are covered — source, build, dependency, artifact — and that none can be skipped | PARTIAL | All four layers are touched implicitly: source (Gap 2), build (Gaps 4–5), dependency (Step 3, lockfiles), artifact (SBOM). However, the output never explicitly states all four layers are present in the skill or that none can be skipped. |
| c11 | Output confirms source-integrity controls — signed commits, branch protection, code review requirements, CODEOWNERS, and force-push prevention — are checked with concrete bash commands (e.g. `gh api repos/X/branches/main/protection`) | FAIL | Gap 2 explicitly states the opposite: 'allowed-tools is Read, Bash, Glob, Grep — no WebFetch. Branch protection rules, required reviewers… live in the GitHub API, not in repo files. The evidence commands in Step 1 can only find CODEOWNERS and CI YAML; they cannot verify the controls they claim to check.' The `gh api` approach is never mentioned as a solution the skill uses. |
| c12 | Output confirms build-integrity coverage — hosted vs self-hosted runners, build-as-code, build provenance generation (SLSA attestations), and log retention | PARTIAL | Gap 5 confirms self-hosted runners in Build Integrity table. SLSA v0.1 table in Gap 1 references 'Build defined in code' and 'signed provenance.' Log retention is absent from the output entirely. |
| c13 | Output verifies dependency-integrity coverage — lockfiles committed, no floating ranges (^, ~, *), Dependabot or equivalent dependency review on PRs, and CI vulnerability scanning | PARTIAL | 'lockfile non-negotiable CRITICAL' and 'Step 3 dependency evidence commands are detailed and cover all major ecosystems' confirm lockfile coverage. Floating ranges (^, ~, *), Dependabot/PR review, and CI vulnerability scanning are not explicitly verified in the output. |
| c14 | Output confirms artifact-integrity coverage — container image signing (cosign / sigstore), SBOM generation (Syft / cyclonedx), and immutable image tags (no `:latest`) | PARTIAL | 'SBOM-per-release' confirmed in 'What works well.' Container image signing tools (cosign/sigstore/Syft/cyclonedx) and immutable image tags (no :latest) are not mentioned anywhere in the output. |
| c15 | Output verifies SLSA level mapping — finds level 0 through 4 explicitly defined and the rule that the assessed level is the highest where ALL requirements are met (not the average) | PARTIAL | Gap 1 explicitly shows the L0–L4 table from the skill. The criterion requirement that 'assessed level = highest where ALL requirements are met (not the average)' is not verified or even mentioned in the output. |
| c16 | Output confirms specific bash commands are provided for evidence collection at each layer — not just descriptive text of what to look for | PARTIAL | Step 3 (dependency layer) confirmed to have 'detailed' bash commands. Gap 3 reveals the build layer is missing a SHA-pinning detection command. Gap 2 reveals source-layer commands cannot verify what they claim. Not all layers confirmed to have working bash commands. |
| c17 | Output confirms missing lockfiles trigger an automatic CRITICAL finding, and CI/CD action pinning to full 40-char SHAs (not tags) is required | PASS | 'lockfile non-negotiable CRITICAL' confirms automatic CRITICAL for missing lockfiles. Gap 3 confirms 'The Rules section (line 205) mandates that every CI action must be pinned to a SHA, not a tag' and provides a regex for 40-char SHAs in the fix command. |
| c18 | Output identifies any genuine gaps — e.g. no rule on package registry mirror / proxy hardening, no guidance on assessing third-party GitHub Apps as supply-chain entry points | PARTIAL | Five genuine gaps identified: SLSA v0.1 vs v1.0 (blocker), unverifiable Step 1 controls, missing SHA-pinning detection command, GitHub-only evidence commands (platform monoculture), and self-hosted runner misclassification. None match the specific examples in the criterion (package registry, GitHub Apps), but they are real and actionable. |

### Notes

The output is a thoughtful skill review that correctly identifies several real structural weaknesses (SLSA version drift, tool-limitation blind spots, missing SHA-pin grep, platform monoculture, self-hosted false positives). Its strongest contributions are on build and tooling gaps. However, it falls short on the verification criteria that require confirming all four supply-chain layers have working bash commands at each layer — critically, c11 fails because Gap 2 reveals source-integrity controls are structurally unverifiable with available tools rather than confirmed as working. Artifact-integrity coverage is thin (only SBOM mentioned; image signing and immutable tags absent). The 'all requirements met' SLSA assessment rule is never confirmed. These gaps push the score to PARTIAL territory at 62.9%.
