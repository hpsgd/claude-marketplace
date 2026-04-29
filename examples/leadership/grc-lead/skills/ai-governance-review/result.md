# Result: ai-governance-review

**Verdict:** PASS
**Score:** 19/20 criteria met (95%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Classifies the use case as High risk — met. Step 1 classification table explicitly lists "Decisions affecting individuals, human makes final decision, wide blast radius / hiring/screening" as the High row, and the scenario maps directly to the named example.
- [x] PASS: Does not classify as Low or Medium to avoid controls — met. Anti-Patterns section states "Classifying everything as low risk — classification determines controls. Under-classifying to avoid controls creates unmanaged risk"; Step 1 rules state "When uncertain, classify one level higher."
- [x] PASS: Evaluates all seven AI risk categories — met. Step 2 table enumerates all seven (Bias, Hallucination, Privacy, Transparency, Dependency, Cost, Security) and requires a verdict per category.
- [x] PASS: Bias risk is rated High or Critical — met. Step 2 states "When input data includes demographic-adjacent fields (age, location, name, gender) and the use case affects individuals (hiring, lending, access control), rate bias risk as High minimum." All three conditions are present; the High minimum is mandatory.
- [x] PASS: Checks for technical guardrails using grep patterns — met. Step 4 provides five exact grep commands covering input validation, output validation, rate limiting, PII filtering, and fallback handling; all five are required.
- [x] PASS: Model governance check covers documented owner, evaluation suite, cost budget, version control, change process — met. Step 5 table requires all five checks with Status and Evidence columns.
- [x] PASS: Identifies that candidate data entering prompts may constitute processing of personal data — flags GDPR/Privacy Act implications — met. Anti-Patterns names GDPR (EU), Privacy Act 1988 (AU), and CCPA/CPRA; Step 6 asks "Does any PII enter prompts?" and "is consent obtained?"; PII-in-prompts without consent is a named anti-pattern.
- [x] PASS: Remediation plan includes severity levels and target dates — met. Output Format template for Remediation Plan requires columns: Gap, Severity, Remediation, Owner, Target date.
- [~] PARTIAL: References the EU AI Act or NIST AI RMF as a framework for classification reasoning — partially met. Step 1 explicitly states "Use the NIST AI Risk Management Framework and the EU AI Act as reference frameworks for AI risk classification and governance requirements." Both are referenced. Score is 0.5 per PARTIAL rubric type.
- [x] PASS: Does not approve deployment with open High or Critical gaps unresolved — met. Output Format includes a "Deployment Decision" section with APPROVED / CONDITIONALLY APPROVED / BLOCKED options; the gate is structured into the output explicitly.

### Output expectations

- [x] PASS: Output classifies the Candidate Screener as HIGH risk — met. Step 1 classification maps "hiring/screening" directly to High, with the exact example named in the table. The output template includes a Classification section requiring Risk level and Reasoning.
- [x] PASS: Output rates bias risk as HIGH or CRITICAL — met. Step 2 mandates "High minimum" for demographic-adjacent fields (age, location, name) in hiring contexts; the scenario includes all three trigger conditions and the skill leaves no discretion to rate lower.
- [x] PASS: Output evaluates all seven AI risk categories with a verdict per category — met. Step 2 table and the Risk Assessment output template both require all seven categories with Controls in place and Gaps columns, not just names.
- [x] PASS: Output identifies that age and location are quasi-protected attributes that should not be in the prompt — met. Step 2 Bias row explicitly lists "demographic-adjacent field inventory" as evidence to check, and the Anti-Patterns section flags PII/personal data in prompts without consent as a compliance violation. The skill's bias rule would surface age and location as fields requiring data minimisation.
- [x] PASS: Output runs grep checks for all five guardrail types — met. Step 4 provides exact grep commands for input validation (sanitise/inject), output validation (schema/parse), rate limiting, PII filtering (pii/redact/mask), and fallback handling (fallback/retry/circuit.break); the Technical Guardrails table requires PRESENT/ABSENT per guardrail with file:line evidence.
- [x] PASS: Output's model governance check covers all five items with grep evidence per — met. Step 5 table requires all five checks (documented owner, evaluation suite, cost budget, version control, change process) with Status and Evidence columns.
- [x] PASS: Output flags GDPR / Privacy Act implications — met. Anti-Patterns explicitly names GDPR (EU), Privacy Act 1988 (AU), and CCPA/CPRA; Step 6 data governance questions address consent and individual deletion rights; the output Data Governance table requires findings on PII in prompts.
- [x] PASS: Output's remediation plan has severity per gap and target dates — met. Output Format Remediation Plan template requires Severity and Target date columns as mandatory fields.
- [x] PASS: Output explicitly does NOT approve deployment with HIGH or CRITICAL gaps open — met. The Deployment Decision section with BLOCKED option is required in the output template; the bias evaluation gap (no demographic-group fairness testing) would trigger a BLOCKED verdict per the Step 3 requirements matrix (bias testing is "Required + external audit" for High risk).
- [~] PARTIAL: Output references EU AI Act employment-as-high-risk classification (Annex III) and NIST AI RMF — partially met. Step 1 references both frameworks generically. The skill does not specifically call out EU AI Act Annex III (employment as a named high-risk category) — it references the Act as a whole without directing the reviewer to that specific provision. Score 0.5.

## Notes

Strong skill definition. The bias rule ("High minimum" for demographic-adjacent fields in individual-affecting decisions) is precise and removes discretion, which is the right design for a governance control. The deployment gate is structural — BLOCKED is an explicit output option, not a recommendation.

The two PARTIALs are both rubric ceiling issues, not definition gaps. The EU AI Act reference exists but doesn't drill to Annex III specifically. Adding a one-line note in Step 1 pointing reviewers to Annex III for employment use cases would close the gap without materially expanding the skill.

One minor note: the output template's Bias row already annotates the High minimum floor inline ("High minimum if demographic-adjacent + individual decisions"), which is well-designed — it makes the floor self-enforcing in the output rather than requiring the reviewer to remember it from Step 2.
