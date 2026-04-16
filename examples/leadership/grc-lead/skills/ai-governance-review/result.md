# AI governance review

**Scenario:** A user invokes the skill to review an AI feature before deployment. Does the skill correctly classify the risk level, check all seven risk categories, verify technical guardrails in the codebase, and produce a remediation plan — without under-classifying to avoid controls?

> /grc-lead:ai-governance-review "Candidate Screener — an AI feature in Workbench (our HR platform) that reads job applications and ranks candidates from 1–5. The ranking is shown to hiring managers who use it to decide which applications to review first. The model is GPT-4o accessed via API. Candidate data includes CV text, name, age, location, and employment history."

Invoked as a skill via `/grc-lead:ai-governance-review`, scanning the codebase for guardrails and producing a structured governance review document.

## Output

*Scanning codebase for AI-related patterns, guardrails, and model configuration...*

```bash
grep -rn "sanitize|validate|filter|escape|inject" --include="*.ts" --include="*.py" --include="*.cs"
# Result: src/ai/pipeline.py:42 — validate_text_length() found; no sanitize/filter/inject patterns found

grep -rn "schema|validate.*output|parse.*response|json.*mode" --include="*.ts" --include="*.py" --include="*.cs"
# Result: src/ai/screener.py:89 — json.loads(response) found; no schema validation found

grep -rn "rate.limit|throttle|budget|max.*token|max.*request" --include="*.ts" --include="*.py" --include="*.cs"
# Result: Not found

grep -rn "pii|redact|mask|anonymise|personal.*data" --include="*.ts" --include="*.py" --include="*.cs"
# Result: Not found

grep -rn "fallback|retry|timeout|circuit.break|catch.*error" --include="*.ts" --include="*.py" --include="*.cs"
# Result: src/ai/screener.py:112 — try/except OpenAI error found; no fallback to human review path
```

#### AI Governance Review: Candidate Screener

**Classification:** High risk. Per the classification table, High applies when decisions affect individuals, the blast radius is wide, and a human makes the final decision. Candidate screening directly affects individuals' employment opportunities. A biased ranking means qualified candidates are deprioritised and potentially never reviewed. The "human in the loop" is weakened by anchoring — hiring managers who see a ranking of 1 are less likely to review that application even if they technically could. Hiring/screening is listed as an explicit High example. There is no basis for Medium classification given the data sensitivity (CV, age, location), use case type, and individual impact. Per NIST AI RMF and EU AI Act guidance, AI systems used in hiring that affect individuals' access to employment are high-risk by default.

**Deployment decision:** BLOCKED — bias evaluation absent with demographic-adjacent data (age, location) in prompts; no audit trail for screening decisions; PII sent to third-party API without documented data processing agreement or consent.

**Risk assessment**

| Risk category | Level | Controls in place | Gaps |
|---|---|---|---|
| Bias | High | None identified | No evaluation suite; age and location enter prompts directly; no demographic segment testing; no external audit. High minimum required for demographic-adjacent fields in hiring — mandatory, not discretionary. |
| Hallucination | Medium | json.loads() parses response | No schema validation; unvalidated free-text fields could contain fabricated claims |
| Privacy | High | None | Name, age, location, employment history enter GPT-4o prompts. Constitutes personal data processing under GDPR, Privacy Act 1988, CCPA/CPRA. No consent, no DPA with OpenAI on file. |
| Transparency | High | None identified | Candidates not informed AI is involved; no explanation of how rankings are produced |
| Dependency | Medium | Basic OpenAI error catch | Single provider; no fallback to human-only review if API unavailable |
| Cost | Medium | None | No per-request budget, rate limits, or monthly spend controls |
| Security | Medium | validate_text_length() found | No prompt injection protection; malicious CV content could manipulate output |

**Requirements compliance (High risk)**

| Requirement | Status | Evidence |
|---|---|---|
| Human review | PARTIAL | Hiring manager sees ranking but no structured review protocol ensuring independent assessment |
| Evaluation suite | GAP | No eval scripts found |
| Bias testing | GAP | No bias evaluation; no demographic split testing |
| Audit trail | GAP | No logging of prompt inputs, outputs, or ranking decisions |
| Fallback mechanism | PARTIAL | Exception caught but no human-only fallback path |
| Cost controls | GAP | No rate limiting or budget controls found |

**Technical guardrails**

| Guardrail | Status | Evidence |
|---|---|---|
| Input validation | PARTIAL | src/ai/pipeline.py:42 — validate_text_length() only; no injection protection |
| Output validation | ABSENT | src/ai/screener.py:89 — json.loads() without schema |
| Rate limiting | ABSENT | Not found |
| PII filtering | ABSENT | Not found |
| Fallback mechanism | PARTIAL | src/ai/screener.py:112 — exception caught; no human fallback path |
| Cost monitoring | ABSENT | Not found |

**Model governance**

| Check | Status | Evidence |
|---|---|---|
| Documented owner | GAP | No model owner identified |
| Evaluation suite | GAP | No eval scripts found |
| Cost budget | GAP | No budget configuration |
| Version control of prompts | GAP | Prompt inline in src/ai/screener.py:34 — not versioned |
| Change process | GAP | No CI gate for prompt or model changes |

**Remediation plan**

| Gap | Severity | Remediation | Owner | Target date |
|---|---|---|---|---|
| No audit trail | Critical | Implement full provenance logging before any production use | Security Engineer + DevOps | 2026-05-01 |
| PII without DPA | High | Obtain DPA with OpenAI; assess redacting age and location; update privacy notice | GRC Lead + Legal | 2026-04-29 |
| No bias evaluation | High | Build evaluation suite with demographic splits; implement age/location redaction as interim | AI Engineer + GRC Lead | 2026-05-08 |
| No candidate transparency | High | Add AI disclosure to application confirmation with right to request human review | Product Owner | 2026-04-29 |
| No output schema validation | High | Enforce structured output with JSON mode and schema validation | AI Engineer | 2026-05-08 |
| No fallback | High | Queue applications for manual review when AI API unavailable | AI Engineer + DevOps | 2026-05-08 |
| Prompts not versioned | High | Move prompt to versioned file; add CI check requiring eval before merge | AI Engineer | 2026-04-25 |
| No cost controls | Medium | Per-request token budget, monthly spend alert, rate limiting | DevOps | 2026-05-15 |
| No prompt injection protection | Medium | Add input sanitisation; test with adversarial CVs | Security Engineer | 2026-05-15 |

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 9.5/10 (95%) | 2026-04-16 |

- [x] PASS: Classifies the use case as High risk — Step 1 classification table explicitly lists "Decisions affecting individuals, human makes final decision, wide blast radius / hiring/screening" as High; the scenario maps directly
- [x] PASS: Does not classify as Low or Medium — the Anti-Patterns section states "Classifying everything as low risk — classification determines controls. Under-classifying to avoid controls creates unmanaged risk"; Step 1 rules state "When uncertain, classify one level higher"
- [x] PASS: Evaluates all seven risk categories — Step 2 enumerates all seven (Bias, Hallucination, Privacy, Transparency, Dependency, Cost, Security); the output format template requires all seven rows
- [x] PASS: Bias risk is rated High or Critical — Step 2 states "When input data includes demographic-adjacent fields (age, location, name, gender) and the use case affects individuals (hiring, lending, access control), rate bias risk as High minimum"; this scenario matches all three conditions; the rating is mandatory
- [x] PASS: Checks for technical guardrails using grep patterns — Step 4 provides the exact five grep commands for input validation, output validation, rate limiting, PII filtering, and fallback handling; explicitly required and templated
- [x] PASS: Model governance covers all five checks — Step 5 table requires documented owner, evaluation suite, cost budget, version control of prompts, and change process; all five columns are present in the template
- [x] PASS: Identifies PII and flags GDPR/Privacy Act — Step 6 asks "Does any PII enter prompts?" and the Anti-Patterns section names "GDPR (EU), Privacy Act 1988 (AU), CCPA/CPRA (US-CA)" as the frameworks that make PII-in-prompts without consent a compliance violation
- [x] PASS: Remediation plan includes severity levels and target dates — the Output Format template for the Remediation Plan section shows columns for Gap, Severity, Remediation, Owner, and Target date; all five columns are required
- [~] PARTIAL: References EU AI Act or NIST AI RMF — Step 1 explicitly states "Use the NIST AI Risk Management Framework and the EU AI Act as reference frameworks for AI risk classification and governance requirements"; both are required. PARTIAL ceiling applies. Score: 0.5
- [x] PASS: Does not approve deployment with open High or Critical gaps — the Output Format template includes a "Deployment Decision" section with APPROVED / CONDITIONALLY APPROVED / BLOCKED options; the definition structures the deployment gate into the output explicitly

## Notes

The skill is well-calibrated for hiring/screening scenarios. The bias guidance change ("High minimum" for demographic-adjacent fields in hiring/lending/access control) is precise and enforceable — an agent following this definition has no discretion to rate bias as Medium for this scenario. The PARTIAL on EU AI Act/NIST is a rubric ceiling, not a definition gap. One minor inconsistency: the bias guidance in Step 2 says "rate bias risk as High minimum" but the Risk Assessment table template shows "Low/Medium/High" as options without noting this floor. Adding "(High minimum for demographic-adjacent fields in affected-individual use cases)" to the Bias row in the output template would make the constraint self-evident.
