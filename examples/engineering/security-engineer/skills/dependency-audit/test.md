# Test: dependency-audit skill structure

Scenario: Checking that the dependency-audit skill enforces reachability analysis per CVE rather than treating all vulnerabilities equally, and produces a prioritised action plan with owners and deadlines.

## Prompt

Review the dependency-audit skill definition and verify it produces a triaged, evidence-based audit rather than a raw vulnerability list dump.

## Criteria

- [ ] PASS: Skill requires running the appropriate audit tool per stack (npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit) with JSON output
- [ ] PASS: Skill mandates reachability analysis for each CVE — three specific questions: is the vulnerable path reachable, is it exploitable in this context, and what is the actual impact
- [ ] PASS: Skill defines four triage categories (fix now, fix soon, monitor, accept) with criteria, action, and timeline for each
- [ ] PASS: Skill requires every "Accept" to have an owner and a review date — accepted risks must be re-evaluated, not closed
- [ ] PASS: Skill requires detailed CVE assessment documentation for each HIGH/CRITICAL finding including CVSS score, vector string, import chain evidence, and recommended action
- [ ] PASS: Skill covers outdated and deprecated packages beyond just CVEs — assesses maintenance risk by package age and deprecation status
- [ ] PASS: Skill lists anti-patterns including running npm audit fix blindly and suppressing findings without reason, owner, and expiry
- [ ] PARTIAL: Skill addresses license compliance scanning and flags GPL/AGPL copyleft licenses as requiring legal review
