# Test: dependency-audit skill structure

Scenario: Checking that the dependency-audit skill enforces reachability analysis per CVE rather than treating all vulnerabilities equally, and produces a prioritised action plan with owners and deadlines.

## Prompt

Review the dependency-audit skill definition and verify it produces a triaged, evidence-based audit rather than a raw vulnerability list dump.

In your verification report, confirm or flag each of the following items by name:

- **Per-stack tool list (5)**: npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit — each with `--json` output flag for parseability.
- **Reachability framework (3 questions, named verbatim)**: (1) Is the vulnerable path reachable? (2) Is it exploitable in this context? (3) What is the actual impact?
- **Triage categories (4, named)**: Fix Now, Fix Soon, Monitor, Accept — each with criteria, action, and timeline.
- **Accept entries**: must require a named owner AND a review date AND the explicit rule "accepted risks must be re-evaluated at review date, not silently closed".
- **HIGH/CRITICAL CVE detail**: CVSS score AND full vector string (e.g. `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`) AND import-chain evidence AND recommended action.
- **License compliance scan**: GPL/AGPL copyleft licences flagged for legal review.
- **Anti-patterns named (3)**: (1) running `npm audit fix` blindly, (2) suppressing findings without reason/owner/expiry, (3) "no findings — done" rubber-stamps.

Confirm presence/absence of each by name. Don't paraphrase.

## Criteria

- [ ] PASS: Skill requires running the appropriate audit tool per stack (npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit) with JSON output
- [ ] PASS: Skill mandates reachability analysis for each CVE — three specific questions: is the vulnerable path reachable, is it exploitable in this context, and what is the actual impact
- [ ] PASS: Skill defines four triage categories (fix now, fix soon, monitor, accept) with criteria, action, and timeline for each
- [ ] PASS: Skill requires every "Accept" to have an owner and a review date — accepted risks must be re-evaluated, not closed
- [ ] PASS: Skill requires detailed CVE assessment documentation for each HIGH/CRITICAL finding including CVSS score, vector string, import chain evidence, and recommended action
- [ ] PASS: Skill covers outdated and deprecated packages beyond just CVEs — assesses maintenance risk by package age and deprecation status
- [ ] PASS: Skill lists anti-patterns including running npm audit fix blindly and suppressing findings without reason, owner, and expiry
- [ ] PARTIAL: Skill addresses license compliance scanning and flags GPL/AGPL copyleft licenses as requiring legal review

## Output expectations

- [ ] PASS: Output is structured as a verification of the skill (verdict per requirement) rather than running an actual audit
- [ ] PASS: Output verifies the per-stack tool list — npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit — each with JSON output flag for parseability
- [ ] PASS: Output confirms reachability analysis is mandatory and names the three-question framework (path reachable? exploitable in this context? actual impact?) — not just "check severity"
- [ ] PASS: Output verifies the four triage categories are defined — Fix Now, Fix Soon, Monitor, Accept — each with criteria, action, and timeline
- [ ] PASS: Output confirms every Accept entry requires a named owner AND a review date, with the rule that accepted risks must be re-evaluated, not silently closed
- [ ] PASS: Output verifies HIGH/CRITICAL findings require detailed CVE assessment with CVSS score, full vector string, import-chain evidence (e.g. dependency tree showing why the package is included), and recommended action
- [ ] PASS: Output confirms the audit covers more than CVEs — outdated/unmaintained packages assessed by last-release date and deprecation status
- [ ] PASS: Output verifies the anti-patterns list includes `npm audit fix` blind run, suppressing findings without reason/owner/expiry, and "no findings — done" rubber-stamps
- [ ] PARTIAL: Output identifies any genuine gaps — e.g. no SBOM generation requirement, no rule on transitive vs direct dependency severity weighting, no provenance/attestation guidance for new packages
