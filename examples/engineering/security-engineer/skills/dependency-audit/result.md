# Dependency Audit

Scenario: Checking that the dependency-audit skill enforces reachability analysis per CVE rather than treating all vulnerabilities equally, and produces a prioritised action plan with owners and deadlines.

## Prompt

> Review the dependency-audit skill definition and verify it produces a triaged, evidence-based audit rather than a raw vulnerability list dump.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Both versions are identical. Let me assess the skill against the stated criteria.

---

## Assessment: `security-engineer:dependency-audit`

**Verdict: Passes the core test — the process structure prevents raw dumping — but has a few concrete defects worth fixing.**

### What works well

- **Step 3 (Reachability Analysis)** is marked MANDATORY and requires 3 explicit questions per CVE before categorization. This is the primary mechanism that stops the output being a raw list.
- **Step 4 (Triage Categories)** maps each vulnerability to one of four buckets with criteria, action, and timeline. "Accept" requires an owner and review date.
- **Step 5 (CVE Detail template)** requires import chain evidence (`file:line`) and an exploitability assessment — not just CVSS scores.
- The **output table** has "Reachable" and "Category" columns, not just CVE/CVSS/severity.
- Anti-pattern "Treating all CVEs as equal" is explicitly called out.

### Defects

**Bug — Step 2 silently truncates output:**
```bash
npm audit --json 2>/dev/null | head -100
```
This pipes valid JSON to `head -100`, which truncates mid-stream and produces unparseable JSON. It directly contradicts the rule two lines below it: *"Capture the full output — do not truncate vulnerability lists."* Drop the `| head -100`.

**Gap — Medium/Low and "Monitor" findings get no evidence requirement.** Step 5 only applies to HIGH/CRITICAL. A MEDIUM reachable vulnerability gets a table row but no import chain, no `file:line` reference, no exploitability note. The triage table says "Reachable: YES" but nothing enforces *how* reachability was determined for those items.

**Gap — No dev vs prod dependency distinction.** A CRITICAL CVE in a test runner or linter is categorically different risk from the same CVE in prod runtime code. The outdated package risk table mentions "dev-only" only in passing for Low, but the vulnerability triage has no such filter.

**Staleness — `safety check --json` is deprecated.** The `safety` CLI replaced this command with `safety scan` in v3. The current command may error or warn.

### Summary

| | |
|---|---|
| Triaged output? | **Yes** — mandatory reachability + 4-bucket classification enforces this |
| Evidence-based? | **Yes for HIGH/CRITICAL**, partial for MEDIUM/LOW — import chain evidence only required in Step 5 |
| Raw dump risk? | Low — anti-patterns section and Step 3 MANDATORY label actively prevent it |
| Blocking defect? | The `head -100` truncation bug in Step 2 |

The `head -100` truncation is the only thing I'd call blocking. The evidence gap for lower-severity findings is worth tightening. Want me to patch those two issues in the marketplace version?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 11.0/16.0 (69%) |
| Evaluated | 2026-05-01 |
| Target duration | 50950 ms |
| Target cost | $0.1205 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires running the appropriate audit tool per stack (npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit) with JSON output | PARTIAL | Output mentions 'npm audit --json 2>/dev/null' (in Step 2 bug) and 'safety check --json' (deprecated). Only 2 of 5 required tools are referenced; pip-audit, dotnet list package --vulnerable, govulncheck, and cargo audit are absent. |
| c2 | Skill mandates reachability analysis for each CVE — three specific questions: is the vulnerable path reachable, is it exploitable in this context, and what is the actual impact | PASS | Output states: 'Step 3 (Reachability Analysis) is marked MANDATORY and requires 3 explicit questions per CVE before categorization.' |
| c3 | Skill defines four triage categories (fix now, fix soon, monitor, accept) with criteria, action, and timeline for each | PASS | Output states: 'Step 4 (Triage Categories) maps each vulnerability to one of four buckets with criteria, action, and timeline.' |
| c4 | Skill requires every "Accept" to have an owner and a review date — accepted risks must be re-evaluated, not closed | PASS | Output states: '"Accept" requires an owner and review date.' The requirement for both owner and review date directly supports re-evaluation rather than silent closure. |
| c5 | Skill requires detailed CVE assessment documentation for each HIGH/CRITICAL finding including CVSS score, vector string, import chain evidence, and recommended action | PARTIAL | Output confirms 'Step 5 (CVE Detail template) requires import chain evidence (file:line) and an exploitability assessment — not just CVSS scores.' CVSS and import chain confirmed, but 'full vector string' is not mentioned. |
| c6 | Skill covers outdated and deprecated packages beyond just CVEs — assesses maintenance risk by package age and deprecation status | PASS | Output references 'the outdated package risk table' when discussing a gap around dev-only packages, confirming the skill includes a dedicated risk table for outdated/deprecated packages beyond CVEs. |
| c7 | Skill lists anti-patterns including running npm audit fix blindly and suppressing findings without reason, owner, and expiry | PARTIAL | Output confirms 'Anti-pattern "Treating all CVEs as equal" is explicitly called out' and refers to an 'anti-patterns section'. Only one anti-pattern is named; npm audit fix blindly and suppressing-without-reason are not confirmed. |
| c8 | Skill addresses license compliance scanning and flags GPL/AGPL copyleft licenses as requiring legal review | FAIL | The captured output contains no mention of license compliance, GPL/AGPL, or copyleft licensing anywhere. |
| c9 | Output is structured as a verification of the skill (verdict per requirement) rather than running an actual audit | PASS | Output opens with 'Assessment: security-engineer:dependency-audit', reviews named steps of the skill, lists defects, and closes with a structured verdict table — clearly a skill review, not an audit run. |
| c10 | Output verifies the per-stack tool list — npm audit, pip-audit, dotnet list package --vulnerable, govulncheck, cargo audit — each with JSON output flag for parseability | PARTIAL | Output references 'npm audit --json' and 'safety check --json' but does not mention pip-audit, dotnet list package --vulnerable, govulncheck, or cargo audit. |
| c11 | Output confirms reachability analysis is mandatory and names the three-question framework (path reachable? exploitable in this context? actual impact?) — not just "check severity" | PARTIAL | Output confirms Step 3 'is marked MANDATORY and requires 3 explicit questions per CVE' but never names the three questions (path reachable? exploitable in context? actual impact?). |
| c12 | Output verifies the four triage categories are defined — Fix Now, Fix Soon, Monitor, Accept — each with criteria, action, and timeline | PARTIAL | Output confirms 'four buckets with criteria, action, and timeline' but only names 'Accept' explicitly. Fix Now, Fix Soon, and Monitor are not named. |
| c13 | Output confirms every Accept entry requires a named owner AND a review date, with the rule that accepted risks must be re-evaluated, not silently closed | PARTIAL | Output states '"Accept" requires an owner and review date.' Owner and review date confirmed; the explicit rule that accepted risks must be re-evaluated rather than silently closed is not stated. |
| c14 | Output verifies HIGH/CRITICAL findings require detailed CVE assessment with CVSS score, full vector string, import-chain evidence (e.g. dependency tree showing why the package is included), and recommended action | PARTIAL | Output confirms 'import chain evidence (file:line) and an exploitability assessment — not just CVSS scores.' Import chain and CVSS confirmed; 'full vector string' is not mentioned. |
| c15 | Output confirms the audit covers more than CVEs — outdated/unmaintained packages assessed by last-release date and deprecation status | PASS | Output references 'the outdated package risk table' in the defects section on dev vs prod distinction, confirming coverage of outdated packages beyond CVEs. |
| c16 | Output verifies the anti-patterns list includes `npm audit fix` blind run, suppressing findings without reason/owner/expiry, and "no findings — done" rubber-stamps | FAIL | Output only confirms 'Treating all CVEs as equal' anti-pattern. None of the three specific anti-patterns (npm audit fix blind run, suppressing findings without reason/owner/expiry, no-findings rubber-stamp) are verified. |
| c17 | Output identifies any genuine gaps — e.g. no SBOM generation requirement, no rule on transitive vs direct dependency severity weighting, no provenance/attestation guidance for new packages | PARTIAL | Output identifies four genuine gaps: head -100 truncation bug, no evidence requirement for MEDIUM/LOW/Monitor findings, no dev vs prod dependency distinction, and deprecated safety check --json command. These are different examples than listed but the criterion uses 'e.g.' suggesting illustrative, not exhaustive. |

### Notes

The captured output is a well-structured skill review that correctly confirms the core triage mechanisms (mandatory 3-question reachability, four-bucket classification, Accept requiring owner+date, outdated package risk table). Its main weaknesses are: failing to verify the full per-stack tool list (only npm audit and safety check are mentioned, three other stacks are absent); not naming the three specific reachability questions or the four category names beyond 'Accept'; not verifying the specific anti-patterns required by c16 (npm audit fix, suppressing findings, rubber-stamps); and complete silence on license compliance (c8). The bugs it identifies (head -100 truncation, deprecated safety command, MEDIUM evidence gap, dev/prod distinction) are genuine and well-reasoned, earning partial credit on c17.
