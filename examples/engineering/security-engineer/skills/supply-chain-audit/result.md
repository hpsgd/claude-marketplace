# Supply Chain Audit

Scenario: Checking that the supply-chain-audit skill assesses all four supply chain layers (source, build, dependency, artifact), maps findings to SLSA levels, and requires specific evidence rather than generic checklist completion.

## Prompt

> Review the supply-chain-audit skill definition and verify it produces a SLSA-aligned assessment with specific findings that can drive a hardening roadmap.
> 
> Read the skill at `/Users/martin/Projects/turtlestack/plugins/engineering/security-engineer/skills/supply-chain-audit/SKILL.md` and verify each item by name. Quote skill text where present:
> 
> - **Source integrity controls**: signed commits, branch protection, code review requirements, CODEOWNERS, force-push prevention. Verify the skill uses `gh api repos/X/branches/main/protection` or equivalent to actually check these (not just CODEOWNERS file presence).
> - **Build integrity**: hosted vs self-hosted runners, build-defined-in-code, build provenance / SLSA attestations, AND **log retention** explicitly.
> - **Dependency integrity**: lockfiles committed, **no floating version ranges** (`^`, `~`, `*` flagged), Dependabot or PR dependency review, AND CI vulnerability scanning.
> - **Artifact integrity**: container image signing (cosign / sigstore), SBOM generation (Syft / cyclonedx), AND **immutable image tags** (no `:latest`).
> - **SLSA level mapping rule**: explicitly confirm "assessed level = highest where ALL requirements are met (not the average)" appears.
> - **CI action SHA-pinning** with citation to the [GitHub Actions security hardening guide](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions).
> - **All four supply-chain layers** (source, build, dependency, artifact) covered, none skippable.
> - Bash commands provided per layer for evidence collection.
> 
> Confirm presence/absence of each by name — do not paraphrase.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I've reviewed the skill against your checklist. Here are the findings:

## Verified Present ✓

| Item | Verified | Location |
|------|----------|----------|
| **Source integrity controls** | ✓ All named | Step 1, lines 15-29 (signed commits, branch protection, code review, CODEOWNERS, force-push prevention) |
| **Build integrity with log retention** | ✓ Explicit | Step 2, line 63: "Logs are stored and accessible for audit" |
| **Dependency integrity (lockfiles, no floating ranges, Dependabot, scanning)** | ✓ All explicit | Step 3, lines 91-97; evidence command line 116: `grep -E '"[~^*]' package.json` |
| **Artifact integrity (cosign/sigstore, Syft/CycloneDX, immutable tags)** | ✓ All explicit | Step 4, lines 129-133 |
| **SLSA level rule** | ✓ Explicit | Step 5, line 171: "**Current level** — the highest level where ALL requirements are met" |
| **CI action SHA-pinning** | ✓ With citation | Step 6, line 205: quoted rule + GitHub Actions guide link |
| **All four supply-chain layers** | ✓ Present | Steps 1-4 cover source, build, dependency, artifact |
| **Bash commands per layer** | ✓ Present | Lines 32-43 (source), 66-78 (build), 102-116 (dependency), 138-149 (artifact) |

## Gap Identified ⚠️

**Branch protection verification lacks GitHub API interrogation:**

The skill's evidence collection for Step 1 (lines 31-44) does NOT include `gh api repos/X/branches/main/protection` to actually query GitHub branch protection settings. Current commands only check for local config:

```bash
find . -path "*/.github/*" -name "*.yml" | head -20
grep -r "merge" .github/ --include="*.yml" -l
```

**Problem:** Many projects configure branch protection rules in GitHub UI, not in code. The skill would miss:
- Required number of reviewers
- Dismiss stale PR approvals
- Require code owner review
- Require up-to-date branches
- Restrict force pushes

**Missing command:**
```bash
gh api repos/{owner}/{repo}/branches/main/protection --jq '.required_pull_request_reviews, .restrictions, .enforce_admins'
```

---

## Summary

The skill is **SLSA-aligned and production-ready** with one surgical gap: add `gh api` branch protection interrogation to actually verify GitHub's configured protection rules, not just file presence. All other layers (source integrity rules, build provenance, dependency lockfiles with floating-range detection, artifact signing, SBOM, immutable tags) are explicitly specified with finding format, prioritization rules, and bash evidence commands.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.5 (89%) |
| Evaluated | 2026-05-03 |
| Target duration | 32228 ms |
| Target cost | $0.0609 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill assesses source integrity controls — signed commits, branch protection, code review requirements, CODEOWNERS, and force push prevention | PASS | Table row: 'Source integrity controls ✓ All named \| Step 1, lines 15-29 (signed commits, branch protection, code review, CODEOWNERS, force-push prevention)' — all five items explicitly named and confirmed present. |
| c2 | Skill assesses build integrity — hosted vs self-hosted runners, build defined in code, build provenance generation, and log retention | PASS | Table row: 'Build integrity with log retention ✓ Explicit \| Step 2, line 63: "Logs are stored and accessible for audit"' — log retention explicitly quoted; row title confirms hosted/self-hosted, build-as-code, and provenance are ✓ within the same entry. |
| c3 | Skill assesses dependency integrity — lockfiles present and committed, no floating version ranges, dependency review on PRs, and vulnerability scanning in CI | PASS | Table row: 'Dependency integrity (lockfiles, no floating ranges, Dependabot, scanning) ✓ All explicit \| Step 3, lines 91-97; evidence command line 116: grep -E \'"[~^*]\' package.json' — all four sub-items named and confirmed with specific command. |
| c4 | Skill assesses artifact integrity — container image signing, SBOM generation, and immutable image tags | PASS | Table row: 'Artifact integrity (cosign/sigstore, Syft/CycloneDX, immutable tags) ✓ All explicit \| Step 4, lines 129-133' — all three items with specific tool names confirmed. |
| c5 | Skill maps evidence to SLSA levels 0-4 and determines the current level as the highest where ALL requirements are met | PASS | Table row: 'SLSA level rule ✓ Explicit \| Step 5, line 171: "**Current level** — the highest level where ALL requirements are met"' — the deterministic rule is confirmed as explicitly stated in the skill. |
| c6 | Skill provides specific bash commands to collect evidence — not just a description of what to look for | PASS | Table row: 'Bash commands per layer ✓ Present \| Lines 32-43 (source), 66-78 (build), 102-116 (dependency), 138-149 (artifact)' — specific line-number ranges cited for every layer. |
| c7 | Skill requires lockfiles to be present and committed — assigns automatic CRITICAL finding if absent | FAIL | The output confirms lockfiles are checked ('Dependency integrity … ✓ All explicit') but never mentions that absence triggers an automatic CRITICAL severity finding. The CRITICAL designation is not referenced anywhere in the captured output. |
| c8 | Skill requires CI/CD actions to be pinned to full SHAs not tags, citing the GitHub Actions security hardening guide | PASS | Table row: 'CI action SHA-pinning ✓ With citation \| Step 6, line 205: quoted rule + GitHub Actions guide link' — both the SHA-pinning requirement and the guide citation are confirmed present. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than running an actual supply-chain audit | PASS | Output opens with 'I've reviewed the skill against your checklist' and is structured as a verification table (Verified Present ✓ / Gap Identified ⚠️) with per-requirement verdicts — not an execution of an audit. |
| c10 | Output verifies all four supply chain layers are covered — source, build, dependency, artifact — and that none can be skipped | PASS | Table row: 'All four supply-chain layers ✓ Present \| Steps 1-4 cover source, build, dependency, artifact' — all four named and confirmed. The summary also states 'All other layers … are explicitly specified.' |
| c11 | Output confirms source-integrity controls — signed commits, branch protection, code review requirements, CODEOWNERS, and force-push prevention — are checked with concrete bash commands (e.g. `gh api repos/X/branches/main/protection`) | FAIL | The output explicitly identifies this as a gap: 'Branch protection verification lacks GitHub API interrogation … does NOT include gh api repos/X/branches/main/protection … Current commands only check for local config.' The output confirms the opposite of what this criterion requires. |
| c12 | Output confirms build-integrity coverage — hosted vs self-hosted runners, build-as-code, build provenance generation (SLSA attestations), and log retention | PASS | Table row: 'Build integrity with log retention ✓ Explicit \| Step 2, line 63: "Logs are stored and accessible for audit"' confirms log retention; the row's ✓ covers hosted/self-hosted, build-as-code, and provenance as named in the row header. |
| c13 | Output verifies dependency-integrity coverage — lockfiles committed, no floating ranges (^, ~, *), Dependabot or equivalent dependency review on PRs, and CI vulnerability scanning | PASS | Table row: 'Dependency integrity (lockfiles, no floating ranges, Dependabot, scanning) ✓ All explicit \| Step 3, lines 91-97; evidence command line 116: grep -E \'"[~^*]\' package.json' — all four sub-items confirmed with a specific regex command for floating range detection. |
| c14 | Output confirms artifact-integrity coverage — container image signing (cosign / sigstore), SBOM generation (Syft / cyclonedx), and immutable image tags (no `:latest`) | PASS | Table row: 'Artifact integrity (cosign/sigstore, Syft/CycloneDX, immutable tags) ✓ All explicit \| Step 4, lines 129-133' — all three items named with correct tool names confirmed. |
| c15 | Output verifies SLSA level mapping — finds level 0 through 4 explicitly defined and the rule that the assessed level is the highest where ALL requirements are met (not the average) | PARTIAL | The output quotes 'the highest level where ALL requirements are met' confirming the deterministic rule, but does not explicitly state that levels 0, 1, 2, 3, and 4 are each individually defined in the skill, and the '(not the average)' qualification is not referenced. |
| c16 | Output confirms specific bash commands are provided for evidence collection at each layer — not just descriptive text of what to look for | PASS | Table row: 'Bash commands per layer ✓ Present \| Lines 32-43 (source), 66-78 (build), 102-116 (dependency), 138-149 (artifact)' — concrete line ranges cited for every layer, with sample command shown for dependency layer. |
| c17 | Output confirms missing lockfiles trigger an automatic CRITICAL finding, and CI/CD action pinning to full 40-char SHAs (not tags) is required | PARTIAL | SHA-pinning is confirmed ('CI action SHA-pinning ✓ With citation \| Step 6, line 205'). The automatic CRITICAL severity for absent lockfiles is never mentioned anywhere in the output — only that lockfiles are checked, not the severity assigned when absent. |
| c18 | Output identifies any genuine gaps — e.g. no rule on package registry mirror / proxy hardening, no guidance on assessing third-party GitHub Apps as supply-chain entry points | PARTIAL | The output identifies one genuine gap: 'Branch protection verification lacks GitHub API interrogation' with specific missing commands and consequences listed. It does not identify the exemplar gaps (registry mirror/proxy hardening, third-party GitHub Apps) but the criterion only requires 'any genuine gaps' and the ceiling is PARTIAL. |

### Notes

The output is a well-structured skill verification that correctly confirms most supply-chain audit requirements. It earns full credit for source controls (c1), build integrity (c2), dependency and artifact integrity (c3, c4), SLSA rule (c5), bash commands (c6, c16), SHA-pinning (c8), structural framing (c9), and four-layer coverage (c10). Two criteria fail outright: c11 because the output explicitly reports the gh api branch-protection command is MISSING (the skill uses local file checks only), and c7/c17 because the automatic CRITICAL severity for absent lockfiles is never confirmed anywhere in the output despite lockfile checking being confirmed. c15 earns partial credit because the 'levels 0-4 explicitly defined' and the '(not the average)' qualifications are not verified, only the rule text is quoted. The single identified gap (missing gh api interrogation) satisfies c18 at its PARTIAL ceiling.
