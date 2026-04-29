# Output: dependency-audit skill structure

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16/16.5 criteria met (97%) |
| **Evaluated** | 2026-04-29 |
| **Source** | `plugins/engineering/security-engineer/skills/dependency-audit/SKILL.md` |

## Results

### Criteria

- [x] PASS: Skill requires running the appropriate audit tool per stack — Step 2 lists `npm audit --json`, `pip-audit --format=json`, `dotnet list package --vulnerable --include-transitive`, `govulncheck ./...`, `cargo audit` with JSON output rule stated explicitly
- [x] PASS: Skill mandates reachability analysis per CVE with three specific questions — Step 3 is labelled "MANDATORY for each vulnerability" and defines Question 1 (is the vulnerable code path reachable?), Question 2 (is it exploitable in this context?), and Question 3 (what is the actual impact?) explicitly
- [x] PASS: Skill defines four triage categories — Fix now, Fix soon, Monitor, Accept — each with Criteria, Action, and Timeline columns in the Step 4 table
- [x] PASS: Every "Accept" requires owner and review date — Step 4 Rules: "Every 'Accept' has an owner and a review date. Accepted risks don't disappear — they're re-evaluated." 90-day review window in the Accept timeline cell
- [x] PASS: Detailed CVE assessment for HIGH/CRITICAL includes CVSS score, vector string, import chain evidence, and recommended action — Step 5 template includes `**CVSS:** [score] ([vector string])`, `Import chain: [your code] -> [package A] -> [vulnerable function]`, `Used in: file:line`, and `**Recommended action:**`
- [x] PASS: Skill covers outdated and deprecated packages beyond CVEs — Step 6 is a dedicated section with per-stack commands and a four-level risk table (High/Medium/Low/Deprecated) based on version lag and package criticality
- [x] PASS: Anti-patterns include blind `npm audit fix` and suppressing without reason/owner/expiry — both explicitly listed in the Anti-Patterns section
- [~] PARTIAL: License compliance scanning flags GPL/AGPL for legal review — Step 7 covers Node.js and Python license scanners and explicitly flags "Copyleft (GPL, AGPL) — Legal review required." No license scanner commands for .NET, Go, or Rust stacks. Criterion is PARTIAL-prefixed so capped at 0.5

### Output expectations

- [x] PASS: Output structured as verification of the skill with verdict per requirement — the evaluation format uses a table of criterion/result/evidence rows
- [x] PASS: Output verifies per-stack tool list — npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit — each with JSON output flag — all five stacks cited with their JSON flags in the evaluation table
- [x] PASS: Output confirms reachability analysis is mandatory and names the three-question framework — criterion 2 row states "MANDATORY for each vulnerability" and names all three questions explicitly
- [x] PASS: Output verifies four triage categories with criteria, action, and timeline — criterion 3 row confirms the Step 4 table structure with all four categories and all three column types
- [x] PASS: Output confirms every Accept entry requires named owner AND review date, and that accepted risks must be re-evaluated — criterion 4 row quotes the rule directly and notes the 90-day window
- [x] PASS: Output verifies HIGH/CRITICAL findings require detailed CVE assessment with CVSS score, full vector string, import-chain evidence, and recommended action — criterion 5 row cites the exact template fields
- [x] PASS: Output confirms the audit covers outdated/unmaintained packages by last-release date and deprecation status — criterion 6 row cites the four-level risk table and per-stack commands
- [x] PASS: Output verifies anti-patterns list includes blind `npm audit fix`, suppressing without reason/owner/expiry — criterion 7 row cites both explicitly
- [~] PARTIAL: Output identifies genuine gaps — the Notes section flags the missing license scanner commands for .NET, Go, and Rust stacks. It does not call out missing SBOM generation requirement, no rule on transitive vs direct dependency severity weighting, and no provenance/attestation guidance for new packages. One of three expected gap categories noted; partial credit warranted

## Notes

The skill is well-constructed and specific where most dependency audit guidance is vague. The reachability analysis in Step 3 is the standout design decision — making it mandatory per CVE prevents treating a 300-item npm audit output as a flat to-do list.

The Accept category correctly distinguishes risk acceptance from closure. The 90-day review window enforced at triage stage, not left to engineer discretion, is the right place for that constraint.

Genuine gaps not called out in the prior evaluation: the skill has no requirement to produce an SBOM (Software Bill of Materials), no guidance on weighting transitive vs direct dependency severity differently, and no provenance or attestation guidance (e.g. SLSA levels, Sigstore) for evaluating new packages before adoption. The SLSA reference in Step 4 mentions it as a framework for verifying supply-chain integrity but does not require SLSA level assessment of incoming dependencies. These are worth noting as enhancements rather than failures — the skill is functional without them.
