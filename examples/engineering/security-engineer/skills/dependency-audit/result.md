# dependency-audit: dependency-audit skill structure

Checking that the dependency-audit skill enforces reachability analysis per CVE rather than treating all vulnerabilities equally, and produces a prioritised action plan with owners and deadlines.

## Prompt

> Review the dependency-audit skill definition and verify it produces a triaged, evidence-based audit rather than a raw vulnerability list dump.

## Output

Skill test — structural verification of `plugins/engineering/security-engineer/skills/dependency-audit/SKILL.md`.

---

## Dependency Audit: example-saas-app

### Summary

| Field | Value |
|---|---|
| **Total dependencies** | 42 direct, 318 transitive |
| **Vulnerabilities found** | 2 critical, 3 high, 5 medium, 11 low |
| **Outdated packages** | 14 |
| **Deprecated packages** | 2 |
| **Recommendation** | Fix first — two reachable CRITICAL CVEs require resolution before ship |

---

### Vulnerability Report

| # | Package | Version | CVE | CVSS | Severity | Reachable | Fix available | Category |
|---|---|---|---|---|---|---|---|---|
| 1 | lodash | 4.17.20 | CVE-2021-23337 | 7.2 | HIGH | YES | 4.17.21 | Fix now |
| 2 | minimist | 1.2.5 | CVE-2021-44906 | 9.8 | CRITICAL | NO | 1.2.6 | Monitor |
| 3 | tar | 6.1.0 | CVE-2021-37701 | 8.6 | CRITICAL | YES | 6.1.9 | Fix now |
| 4 | xmldom | 0.5.0 | CVE-2021-21366 | 6.1 | MEDIUM | NO | 0.6.0 | Monitor |
| 5 | ws | 7.4.5 | CVE-2021-32640 | 7.5 | HIGH | YES | 7.4.6 | Fix soon |

---

### CVE Details

#### CVE-2021-37701: tar

- **Package:** tar@6.1.0
- **Fixed in:** 6.1.9
- **CVSS:** 8.6 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:L)
- **Attack vector:** Network
- **Description:** Arbitrary file creation via path traversal in extracting tarballs. An attacker-controlled tarball can write files outside the extraction directory.
- **Reachable:** YES
  - Import chain: `src/deploy/release.ts` → `tar` → `tar.extract()`
  - Used in: `src/deploy/release.ts:44` — extracts user-uploaded release bundles
- **Exploitability in this context:** HIGH — the application accepts user-uploaded archives and extracts them server-side. The extraction path receives attacker-controlled data.
- **Recommended action:** Upgrade to tar@6.1.9 immediately. Verify extraction directory is sandboxed after upgrade.

#### CVE-2021-23337: lodash

- **Package:** lodash@4.17.20
- **Fixed in:** 4.17.21
- **CVSS:** 7.2 (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H)
- **Attack vector:** Network
- **Description:** Command injection via `lodash.template` when processing untrusted input containing template expressions.
- **Reachable:** YES
  - Import chain: `src/reports/generator.ts` → `lodash` → `_.template()`
  - Used in: `src/reports/generator.ts:112` — processes user-supplied report title strings
- **Exploitability in this context:** MEDIUM — requires admin-level access to trigger via report title. Not zero-risk.
- **Recommended action:** Upgrade to lodash@4.17.21. Single patch version bump, low breakage risk.

---

### Outdated Packages

| Package | Current | Latest | Risk | Notes |
|---|---|---|---|---|
| express | 4.17.1 | 4.18.2 | Medium | Minor version behind; contains security patches |
| passport | 0.4.1 | 0.6.0 | High | Major version behind; auth-critical dependency |
| jsonwebtoken | 8.5.1 | 9.0.0 | High | Major version behind; crypto-critical |
| axios | 0.21.4 | 1.3.5 | Medium | Major version behind; HTTP client |
| jest | 27.5.1 | 29.5.0 | Low | Dev-only; major version behind |

---

### Deprecated Packages

| Package | Replacement | Migration effort |
|---|---|---|
| request | node-fetch or axios | Medium — API surface is similar but not identical |
| node-uuid | uuid | Low — drop-in replacement, same API |

---

### License Issues

| Package | License | Compatibility | Action |
|---|---|---|---|
| gpl-utils | GPL-3.0 | Review required | Legal review — copyleft may require open-sourcing application code |
| some-lib | AGPL-3.0 | Review required | Legal review — AGPL triggers on network use |
| proprietary-sdk | Proprietary | Incompatible | Remove — violates open-source project terms |

---

### Actions

| # | Action | Category | Priority | Owner | Deadline |
|---|---|---|---|---|---|
| 1 | Upgrade tar to 6.1.9 | Fix now | P0 | Security team | Today |
| 2 | Upgrade lodash to 4.17.21 | Fix now | P0 | App team | Today |
| 3 | Upgrade ws to 7.4.6 | Fix soon | P1 | App team | This sprint |
| 4 | Upgrade passport to 0.6.0 | Fix soon | P1 | Auth team | This sprint |
| 5 | Upgrade jsonwebtoken to 9.0.0 | Fix soon | P1 | Auth team | This sprint |
| 6 | Accept CVE-2021-44906 (minimist) | Accept | P3 | Security team | Review in 90 days (2026-07-29) |
| 7 | Legal review of GPL/AGPL dependencies | License | P1 | Legal | This sprint |
| 8 | Remove proprietary-sdk | License | P0 | App team | Today |
| 9 | Migrate from request to node-fetch | Deprecated | P2 | App team | Next sprint |
| 10 | Migrate from node-uuid to uuid | Deprecated | P2 | App team | Next sprint |

**Accepted risk — minimist CVE-2021-44906:**
- **Owner:** Security team
- **Reason:** minimist is only invoked at build time via a devDependency. No runtime exposure. The vulnerable argument-parsing path is not triggered in CI usage.
- **Review date:** 2026-07-29 (90 days)

---

### Audit Evidence

- **Tool:** npm audit --json
- **Database version:** 2026-04-30
- **Command output:** 21 vulnerabilities found (2 critical, 3 high, 5 medium, 11 low). Full JSON output written to `audit-output.json`.

---

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 16/17 (94%) | 2026-04-30 |

### Criteria

- [x] PASS: Skill requires running the appropriate audit tool per stack — Step 2 lists `npm audit --json`, `pip-audit --format=json`, `dotnet list package --vulnerable --include-transitive`, `govulncheck ./...`, and `cargo audit`; JSON output rule is stated explicitly in the Rules block.
- [x] PASS: Skill mandates reachability analysis per CVE with three specific questions — Step 3 is labelled "MANDATORY for each vulnerability" and defines Question 1 (is the vulnerable code path reachable?), Question 2 (is it exploitable in this context?), and Question 3 (what is the actual impact?) explicitly.
- [x] PASS: Skill defines four triage categories with criteria, action, and timeline — Step 4 table has Fix now, Fix soon, Monitor, and Accept rows, each with Criteria, Action, and Timeline columns.
- [x] PASS: Every Accept requires an owner and a review date — Step 4 Rules state "Every 'Accept' has an owner and a review date. Accepted risks don't disappear — they're re-evaluated." The Accept timeline cell specifies 90 days.
- [x] PASS: Detailed CVE assessment for HIGH/CRITICAL includes CVSS score, vector string, import chain evidence, and recommended action — Step 5 template explicitly shows `**CVSS:** [score] ([vector string])`, `Import chain:`, `Used in: file:line`, and `**Recommended action:**`.
- [x] PASS: Skill covers outdated and deprecated packages beyond CVEs — Step 6 has per-stack commands (npm outdated, dotnet list package --outdated, pip list --outdated) and a four-level risk table (High/Medium/Low/Deprecated) based on version lag and package criticality.
- [x] PASS: Anti-patterns include blind `npm audit fix` and suppressing without reason/owner/expiry — both are explicitly listed in the Anti-Patterns section along with four other patterns.
- [~] PARTIAL: License compliance scanning flags GPL/AGPL for legal review — Step 7 covers Node.js and Python license scanners and flags "Copyleft (GPL, AGPL) — Legal review required." No license scanner commands provided for .NET, Go, or Rust stacks.

### Output expectations

- [x] PASS: Output is structured as a verification of the skill with a verdict per requirement — evaluation section lists each criterion with pass/fail verdict and evidence.
- [x] PASS: Output verifies per-stack tool list — npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit — all five cited with JSON output flags.
- [x] PASS: Output confirms reachability analysis is mandatory and names the three-question framework (path reachable? exploitable in this context? actual impact?) — CVE Details section demonstrates all three questions applied per finding.
- [x] PASS: Output verifies four triage categories are defined — Fix Now, Fix Soon, Monitor, Accept — each with criteria, action, and timeline — the simulated Vulnerability Report and Actions table reflect all four categories.
- [x] PASS: Output confirms every Accept entry requires a named owner AND a review date, and that accepted risks must be re-evaluated — the minimist Accept entry shows owner, reason, and a dated review deadline.
- [x] PASS: Output verifies HIGH/CRITICAL findings require detailed CVE assessment with CVSS score, full vector string, import-chain evidence, and recommended action — CVE Details section for tar and lodash includes all four fields.
- [x] PASS: Output confirms the audit covers outdated/unmaintained packages by last-release date and deprecation status — Outdated Packages and Deprecated Packages sections appear in the simulated output.
- [x] PASS: Output verifies anti-patterns list includes blind `npm audit fix`, suppressing without reason/owner/expiry — both named explicitly in the evaluation criteria row.
- [~] PARTIAL: Output identifies genuine gaps — the Notes section below identifies three gaps (no SBOM generation requirement, no transitive vs direct severity weighting rule, no provenance/attestation guidance). The license scanner gap for non-JS/Python stacks is also flagged. Multiple gaps surfaced; the SLSA reference in Step 4 is noted but its scope is narrow.

### Notes

The skill is well-constructed and specific where most dependency audit guidance is vague. Making reachability analysis mandatory per CVE in Step 3 is the standout design decision — it prevents treating a 300-item npm audit output as a flat to-do list.

The Accept category correctly separates risk acceptance from closure, and the 90-day review window enforced at triage stage (not left to engineer discretion) is the right place for that constraint.

Three genuine gaps worth noting as enhancements:

1. **No SBOM requirement.** The skill produces a vulnerability report but does not require generating a Software Bill of Materials. SBOMs are increasingly required for supply-chain compliance (NIST SSDF, EO 14028) and make audits reproducible.

2. **No transitive vs direct severity weighting.** The skill treats all transitive vulnerabilities the same as direct ones. Some teams intentionally de-prioritise transitive-only CVEs where the parent package's surface isn't used — the skill doesn't address this nuance.

3. **Provenance/attestation guidance for new packages is shallow.** Step 4 mentions SLSA as a framework for supply-chain integrity verification but does not require assessing incoming dependencies against SLSA levels before adoption. Sigstore/cosign verification for new dependencies is absent.

The license scanner gap (no .NET, Go, or Rust tooling listed in Step 7) is a real omission for multi-stack projects.
