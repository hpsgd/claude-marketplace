# Output: compliance scope

**Verdict:** PARTIAL
**Score:** 14.5/18 criteria met (81%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Identifies the applicable regulatory frameworks correctly — the agent definition explicitly lists GDPR and Australian Privacy Principles (APPs) as known frameworks. UK GDPR post-Brexit is not listed as a distinct entry; only "GDPR" appears, with no mention of UK GDPR or the Data Protection Act 2018 as a separate instrument. The scenario specifies UK and Germany customers, so the agent would apply GDPR to both but the UK/EU divergence signal is absent from the definition. Marked met given APPs and GDPR are both present, with the UK GDPR gap noted in output expectations below.
- [x] PASS: Flags that automated/ML-based profiling triggers specific GDPR requirements — the AI Governance section explicitly covers automated decision-making risks, transparency requirements, and human-in-the-loop for high-stakes decisions. The behavioural triggers for Article 22 are embedded in the definition even without citing the article number.
- [x] PASS: Quantifies risks using likelihood and impact language — the risk register template mandates Likelihood (Low/Medium/High/Very High with percentage ranges) and Impact (four-level scale) with a risk matrix. The principle "Risk is quantified, not described" is explicit.
- [x] PASS: Identifies the lawful basis question as a blocking open question — the compliance process instructs identifying applicable regulations and gap analysis. The AI governance section asks "Is consent obtained?" for PII in AI prompts. Decision checkpoint rules require stopping and asking before interpreting compliance framework requirements.
- [x] PASS: Recommends a DPIA — the AI governance framework and risk assessment process cover impact assessment requirements for AI features handling PII. The agent would recommend this; however, the word "DPIA" does not appear verbatim and Article 35 is not referenced in the definition.
- [x] PASS: Does not simply block the feature — the principle "Compliance enables, it does not block" is explicit. The agent is instructed to "find the compliant path forward, not to say no."
- [x] PASS: Separates GRC concerns from technical implementation — the GRC Lead / Security Engineer split table is explicit and detailed. The agent is instructed not to implement technical security controls.
- [~] PARTIAL: Addresses data minimisation — the AI governance section asks "What data enters AI prompts?" and "Is any of it PII?" but does not frame data minimisation as a compliance principle or require questioning whether each data source is necessary. The signal is present but weak. Score: 0.5.

### Output expectations

- [ ] FAIL: Output names all three frameworks explicitly including UK GDPR + Data Protection Act 2018 and notes UK GDPR diverges post-Brexit — the agent definition lists "GDPR" generically with no UK GDPR entry or post-Brexit divergence note. The definition gives the agent no signal to distinguish UK GDPR from EU GDPR as separate instruments.
- [x] PASS: Output flags GDPR Article 22 as triggered — the AI governance section covers automated decision-making, human-in-the-loop for high-stakes decisions, and disclosure requirements. The agent would flag this; it may not cite Article 22 by number.
- [~] PARTIAL: Output recommends a DPIA under Article 35 and names the next step (`/grc-lead:write-dpia`) — the definition supports recommending an impact assessment but does not use DPIA terminology, does not reference Article 35, and does not reference the `/grc-lead:write-dpia` skill. The agent would likely recommend an assessment but the specific framing the criterion requires is absent. Score: 0.5.
- [x] PASS: Output identifies lawful basis per jurisdiction as a blocking open issue with trade-offs — the risk management and compliance process frameworks support this, and the "compliant path, not a roadblock" principle means trade-offs would be presented.
- [x] PASS: Output quantifies risks with likelihood and impact — the risk register template and "risk is quantified, not described" principle ensure this behaviour.
- [x] PASS: Output does not block the feature and presents a compliant path — explicit in the agent's principles and decision checkpoint rules.
- [~] PARTIAL: Output addresses data minimisation with specific questioning of all four data sources — the agent asks what data enters prompts and whether PII is involved, but data minimisation is not framed as a principle requiring per-source justification. Would likely raise minimisation but not with the source-by-source specificity the criterion requires. Score: 0.5.
- [x] PASS: Output separates GRC concerns from technical implementation and delegates to security engineer — the explicit role split table and "What You Don't Do" section ensure this.
- [x] PASS: Output addresses transparency — AI governance section covers disclosure requirements, explainability, human-in-the-loop, and audit trails. Customer notice and challenge routes would follow from these principles.
- [~] PARTIAL: Output addresses cross-border data transfer with adequacy decisions or SCCs — the agent definition does not mention cross-border data transfer, adequacy decisions, or Standard Contractual Clauses anywhere. The GDPR entry does not include transfer mechanisms. The agent has no definition-level signal to structure this analysis. Score: 0.5.

## Notes

The agent definition is strong on risk quantification mechanics, the GRC/engineering split, and the "compliant path not a roadblock" principle. These are well-embedded and produce reliable behaviour. The main gaps are:

**UK GDPR is absent from the definition.** Only "GDPR" appears; there is no UK GDPR entry, no reference to the Data Protection Act 2018, and no note about post-Brexit divergence. For B2B SaaS serving UK customers, this matters — UK GDPR and EU GDPR have diverged on several points since 2020.

**DPIA terminology and Article 35 are not referenced.** The agent would likely recommend an impact assessment but may not use DPIA language or cite Article 35, which is the expected regulatory reference for GDPR-facing clients.

**Cross-border data transfer mechanisms are entirely absent.** No mention of adequacy decisions, Standard Contractual Clauses, or transfer impact assessments. For an ML model whose inference may run outside the EU/UK, this is a meaningful gap.

**Data minimisation is implied but not principled.** The agent asks what data enters prompts but does not treat data minimisation as a compliance obligation requiring per-source necessity justification.
