# Dependency Audit

Scenario: Checking that the dependency-audit skill enforces reachability analysis per CVE rather than treating all vulnerabilities equally, and produces a prioritised action plan with owners and deadlines.

## Prompt

> Review the dependency-audit skill definition and verify it produces a triaged, evidence-based audit rather than a raw vulnerability list dump.
> 
> In your verification report, confirm or flag each of the following items by name:
> 
> - **Per-stack tool list (5)**: npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit — each with `--json` output flag for parseability.
> - **Reachability framework (3 questions, named verbatim)**: (1) Is the vulnerable path reachable? (2) Is it exploitable in this context? (3) What is the actual impact?
> - **Triage categories (4, named)**: Fix Now, Fix Soon, Monitor, Accept — each with criteria, action, and timeline.
> - **Accept entries**: must require a named owner AND a review date AND the explicit rule "accepted risks must be re-evaluated at review date, not silently closed".
> - **HIGH/CRITICAL CVE detail**: CVSS score AND full vector string (e.g. `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) AND import-chain evidence AND recommended action.
> - **License compliance scan**: GPL/AGPL copyleft licences flagged for legal review.
> - **Anti-patterns named (3)**: (1) running `npm audit fix` blindly, (2) suppressing findings without reason/owner/expiry, (3) "no findings — done" rubber-stamps.
> 
> Confirm presence/absence of each by name. Don't paraphrase.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Dependency-Audit Skill Verification Report

I've reviewed the skill definition at `/Users/martin/.claude/plugins/marketplaces/hpsgd/plugins/engineering/security-engineer/skills/dependency-audit/SKILL.md`.

---

### ✓ Per-stack tool list (5 tools)

**Confirmed present:**
- `npm audit --json` (line 37) ✓
- `pip-audit --format=json` (line 45) ✓
- `dotnet list package --vulnerable` (line 42) — **FLAG: no `--json` flag shown**
- `govulncheck ./...` (line 50) — **FLAG: no `--json` flag shown; documentation omits `--json` output option**
- `cargo audit` (line 53) — **FLAG: no `--json` flag shown**

**Issue:** The skill names five tools but only three show structured output flags (npm, pip-audit, safety). The .NET, Go, and Rust tools are missing explicit `--json` guidance, which contradicts the requirement that "Run the audit tool with JSON output when available — structured data is easier to triage" (line 57).

---

### ✓ Reachability framework (3 questions, named verbatim)

**All three confirmed present in Step 3:**
1. "Is the vulnerable code path reachable?" (line 65) ✓
2. "Is the vulnerability exploitable in this context?" (line 75) ✓
3. "What is the actual impact?" (line 80) ✓

---

### ✓ Triage categories (4, named)

**All confirmed in Step 4 table:**
- Fix now ✓
- Fix soon ✓
- Monitor ✓
- Accept ✓

Each has criteria, action, and timeline columns defined.

---

### ⚠ Accept entries — owner, review date, re-evaluation rule

**Present but incomplete:**
- Owner requirement: "Every 'Accept' has an owner and a review date" (line 98) ✓
- Review date: "Accepted risks don't disappear — they're re-evaluated" (line 98) ✓
- **Missing:** The explicit rule "accepted risks must be re-evaluated at review date, not silently closed" is implied but NOT stated as a named enforcement rule. The skill says risks "are re-evaluated" but doesn't enforce that they cannot be silently closed at expiry without active review.

---

### ✓ HIGH/CRITICAL CVE detail

**Confirmed in Step 5 template:**
- CVSS score: "**CVSS:** [score] ([vector string])" (line 112) ✓
- Full vector string: "([vector string])" shown in template (line 112) ✓
- Import-chain evidence: "Import chain: [your code] -> [package A] -> [vulnerable function]" (line 116) ✓
- Recommended action: "**Recommended action:** ..." (line 119) ✓

---

### ✓ License compliance scan

**Confirmed in Step 7:**
- GPL/AGPL flagged: "Copyleft (GPL, AGPL) — may require open-sourcing your code. Legal review required" (lines 157–158) ✓
- Tools provided: `license-checker --summary`, `pip-licenses --format=table` ✓

---

### ✓ Anti-patterns (3 named)

**All three confirmed:**
1. "Running `npm audit fix` blindly" (lines 162–163) ✓
2. "Suppressing without documenting — audit suppressions must have a reason, an owner, and an expiry date" (line 165) ✓
3. "No vulnerabilities found" without evidence — show the audit tool output. Prove the tool ran (lines 166–167) ✓

---

### Summary

**Strengths:** The skill delivers a structured, evidence-based audit framework with mandatory reachability analysis, proper triage categories, and strong anti-pattern enforcement.

**Gaps:**
1. **Tool flag coverage incomplete:** Three of five tools (dotnet, govulncheck, cargo) lack documented `--json` output flags, breaking the "structured data" requirement.
2. **Accept re-evaluation rule soft:** The skill implies but doesn't explicitly mandate that accepted risks revert to "under review" status at expiry — you could silence an accepted risk without forcing active re-evaluation.

**Recommendation:** Add `--json` equivalents (e.g., `dotnet list package --vulnerable --output json`, `govulncheck -json`, `cargo audit --json`) to Step 2, and add a hard rule to Step 4: *"Accepted risks expire at the review date and must be explicitly re-evaluated or re-documented — silent closure is not permitted."*

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/16.0 (81%) |
| Evaluated | 2026-05-03 |
| Target duration | 44648 ms |
| Target cost | $0.1132 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires running the appropriate audit tool per stack (npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit) with JSON output | PARTIAL | Output confirms all five tools are named but explicitly flags three as lacking --json guidance: 'dotnet list package --vulnerable — FLAG: no --json flag shown', 'govulncheck ./... — FLAG: no --json flag shown', 'cargo audit — FLAG: no --json flag shown'. Only npm audit and pip-audit have structured output flags confirmed. |
| c2 | Skill mandates reachability analysis for each CVE — three specific questions: is the vulnerable path reachable, is it exploitable in this context, and what is the actual impact | PASS | Output states 'All three confirmed present in Step 3' and lists verbatim: (1) 'Is the vulnerable code path reachable?' (2) 'Is the vulnerability exploitable in this context?' (3) 'What is the actual impact?' — each with a line reference and ✓. |
| c3 | Skill defines four triage categories (fix now, fix soon, monitor, accept) with criteria, action, and timeline for each | PASS | Output states 'All confirmed in Step 4 table' and lists Fix now ✓, Fix soon ✓, Monitor ✓, Accept ✓, adding 'Each has criteria, action, and timeline columns defined.' |
| c4 | Skill requires every "Accept" to have an owner and a review date — accepted risks must be re-evaluated, not closed | PARTIAL | Output confirms owner ('Every 'Accept' has an owner and a review date') and review date but flags the re-evaluation rule as soft: 'Missing: The explicit rule accepted risks must be re-evaluated at review date, not silently closed is implied but NOT stated as a named enforcement rule.' |
| c5 | Skill requires detailed CVE assessment documentation for each HIGH/CRITICAL finding including CVSS score, vector string, import chain evidence, and recommended action | PASS | Output confirms all four elements in Step 5 template: CVSS score ✓, full vector string ✓ ('([vector string]) shown in template'), import chain evidence ✓ ('Import chain: [your code] -> [package A] -> [vulnerable function]'), recommended action ✓. |
| c6 | Skill covers outdated and deprecated packages beyond just CVEs — assesses maintenance risk by package age and deprecation status | FAIL | The captured output contains no mention of outdated packages, deprecated packages, last-release date assessment, or maintenance risk. This topic is entirely absent from the verification report. |
| c7 | Skill lists anti-patterns including running npm audit fix blindly and suppressing findings without reason, owner, and expiry | PASS | Output confirms: (1) 'Running `npm audit fix` blindly (lines 162–163) ✓', (2) 'Suppressing without documenting — audit suppressions must have a reason, an owner, and an expiry date (line 165) ✓', (3) 'No vulnerabilities found without evidence (lines 166–167) ✓'. |
| c8 | Skill addresses license compliance scanning and flags GPL/AGPL copyleft licenses as requiring legal review | PARTIAL | Output confirms under Step 7: 'Copyleft (GPL, AGPL) — may require open-sourcing your code. Legal review required (lines 157–158) ✓' and lists tools license-checker and pip-licenses. Ceiling is PARTIAL. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than running an actual audit | PASS | The entire output is titled 'Dependency-Audit Skill Verification Report' and proceeds section-by-section with checkmarks, flags, and line references into the skill file — it verifies the skill definition rather than executing an audit against any real codebase. |
| c10 | Output verifies the per-stack tool list — npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit — each with JSON output flag for parseability | PASS | Output goes through all five tools by name, confirms which have JSON flags (npm audit --json, pip-audit --format=json) and explicitly flags which do not ('dotnet list package --vulnerable — FLAG: no --json flag shown', 'govulncheck — FLAG: no --json flag shown', 'cargo audit — FLAG: no --json flag shown'). This is a thorough, accurate per-tool verification. |
| c11 | Output confirms reachability analysis is mandatory and names the three-question framework (path reachable? exploitable in this context? actual impact?) — not just "check severity" | PASS | Output quotes all three questions verbatim with line numbers and ✓ marks, explicitly noting they come from 'Step 3' of the skill — not a severity check but a structured three-question framework. |
| c12 | Output verifies the four triage categories are defined — Fix Now, Fix Soon, Monitor, Accept — each with criteria, action, and timeline | PASS | Output states 'All confirmed in Step 4 table' and lists all four category names with ✓, adding 'Each has criteria, action, and timeline columns defined.' |
| c13 | Output confirms every Accept entry requires a named owner AND a review date, with the rule that accepted risks must be re-evaluated, not silently closed | PARTIAL | Output confirms owner and review date requirements are present but explicitly flags the gap: 'Missing: The explicit rule accepted risks must be re-evaluated at review date, not silently closed is implied but NOT stated as a named enforcement rule.' The hard enforcement of no silent closure is absent. |
| c14 | Output verifies HIGH/CRITICAL findings require detailed CVE assessment with CVSS score, full vector string, import-chain evidence (e.g. dependency tree showing why the package is included), and recommended action | PASS | Output confirms all four elements from Step 5 template with line references: CVSS score + vector string ('**CVSS:** [score] ([vector string])'), import chain ('Import chain: [your code] -> [package A] -> [vulnerable function]'), and recommended action — all ✓. |
| c15 | Output confirms the audit covers more than CVEs — outdated/unmaintained packages assessed by last-release date and deprecation status | FAIL | The captured output makes no mention of outdated packages, unmaintained packages, last-release dates, or deprecation status anywhere. The topic is entirely absent from the verification report. |
| c16 | Output verifies the anti-patterns list includes `npm audit fix` blind run, suppressing findings without reason/owner/expiry, and "no findings — done" rubber-stamps | PASS | Anti-patterns section confirms all three by name: (1) 'Running `npm audit fix` blindly (lines 162–163) ✓', (2) 'Suppressing without documenting — audit suppressions must have a reason, an owner, and an expiry date (line 165) ✓', (3) '"No vulnerabilities found" without evidence — show the audit tool output. Prove the tool ran (lines 166–167) ✓'. |
| c17 | Output identifies any genuine gaps — e.g. no SBOM generation requirement, no rule on transitive vs direct dependency severity weighting, no provenance/attestation guidance for new packages | PARTIAL | Output identifies two genuine gaps in the Summary section: (1) missing --json flags for dotnet, govulncheck, and cargo audit tools, (2) the 'Accept' re-evaluation rule is soft/implied rather than explicitly enforced. These are real findings but differ from the specific examples cited (SBOM, transitive weighting, provenance/attestation). Ceiling is PARTIAL. |

### Notes

The captured output is a well-structured, evidence-based skill verification that correctly identifies most required elements by name with line references. It excels at the reachability framework (verbatim questions confirmed), triage categories, CVE detail template, license compliance, and anti-patterns. The two clear gaps are: (1) no mention of outdated/deprecated package maintenance risk assessment anywhere in the output (c6 and c15 both fail), and (2) the 'Accept' re-evaluation enforcement is correctly flagged as soft. The JSON flag gap for three tools is appropriately caught and flagged. The output earns PASS at 81.25% (13.0/16.0 points), with the outdated-package coverage being the most significant blind spot.
