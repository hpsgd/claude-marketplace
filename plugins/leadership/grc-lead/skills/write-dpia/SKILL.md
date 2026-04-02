---
name: write-dpia
description: "Write a Data Protection Impact Assessment (DPIA) for high-risk personal data processing. Required by GDPR Article 35 when processing is likely to result in high risk to individuals. Produces a structured assessment with risks, mitigations, and DPO review."
argument-hint: "[processing activity or feature involving personal data]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Write DPIA

Write a [Data Protection Impact Assessment](https://gdpr-info.eu/art-35-gdpr/) (DPIA) for $ARGUMENTS. A DPIA is mandatory under GDPR Article 35 when processing is likely to result in high risk to the rights and freedoms of individuals — including profiling, large-scale processing of special categories, and systematic monitoring of public areas.

## Step 1: Describe the Processing

Before assessing risk, fully document what the processing involves:

```markdown
### Processing Description

| Aspect | Detail |
|---|---|
| **What personal data** | [List specific data categories — name, email, location, health, financial, behavioural, etc.] |
| **Whose data** | [Data subjects — customers, employees, children, patients, public] |
| **Purpose** | [Why this processing is needed — be specific, not "business purposes"] |
| **How processed** | [Collection method, storage, analysis, automated decisions, profiling] |
| **Retention period** | [How long data is kept and deletion/anonymisation policy] |
| **Recipients** | [Who receives the data — internal teams, processors, third countries] |
| **Data flows** | [Source → processing → storage → output — include cross-border transfers] |
```

Scan the codebase for data models, API schemas, and configuration that reveal what data is collected and how it flows. Use `Glob` and `Grep` to find relevant schemas, models, and privacy-related configuration.

**Output:** Completed processing description table with data flow diagram.

## Step 2: Assess Necessity and Proportionality

Evaluate whether the processing is justified under [GDPR Article 5](https://gdpr-info.eu/art-5-gdpr/) principles:

```markdown
### Necessity and Proportionality

| Principle | Assessment | Evidence |
|---|---|---|
| **Lawful basis** | [Which Art. 6 basis — consent, contract, legitimate interest, etc.] | [Where this is documented/implemented] |
| **Purpose limitation** | [Is data used only for the stated purpose?] | [Code paths that access the data] |
| **Data minimisation** | [Is every field necessary? Could any be removed?] | [Fields collected vs fields actually used] |
| **Accuracy** | [How is data kept accurate? Can subjects correct it?] | [Update mechanisms, validation] |
| **Storage limitation** | [Is retention period justified? Is deletion automated?] | [TTL configs, cleanup jobs, retention policies] |
| **Integrity and confidentiality** | [Encryption at rest/transit, access controls, audit logging] | [Security measures in place] |
```

For each principle, provide a verdict: **Met**, **Partially met** (with remediation needed), or **Not met** (blocks processing).

**Output:** Proportionality assessment table with verdicts and evidence.

## Step 3: Identify Risks to Individuals

Assess risks from the **individual's perspective**, not the organisation's. Consider what harm could occur if data is lost, stolen, misused, or inaccurate.

```markdown
### Risk Assessment

| # | Risk | Description | Likelihood | Severity | Overall Risk |
|---|---|---|---|---|---|
| R1 | [Risk name] | [What could happen to the individual] | [Low/Medium/High] | [Low/Medium/High] | [Low/Medium/High/Very High] |
| R2 | ... | ... | ... | ... | ... |
```

**Risk categories to evaluate** (assess each — mark N/A if genuinely not applicable):

- **Unauthorised access** — data breach exposing personal data
- **Excessive collection** — collecting more data than necessary
- **Function creep** — data used for purposes beyond original consent
- **Inaccurate decisions** — automated decisions based on wrong/incomplete data
- **Lack of transparency** — individuals unaware of processing
- **Inability to exercise rights** — cannot access, correct, or delete data
- **Re-identification** — pseudonymised data linked back to individuals
- **Cross-border exposure** — data transferred to jurisdictions with weaker protections
- **Discriminatory effects** — processing that disproportionately impacts protected groups

**Likelihood × Severity matrix:**

| | Low severity | Medium severity | High severity |
|---|---|---|---|
| **High likelihood** | Medium | High | Very High |
| **Medium likelihood** | Low | Medium | High |
| **Low likelihood** | Low | Low | Medium |

**Output:** Completed risk table with all applicable categories assessed.

## Step 4: Define Mitigation Measures

For every risk rated Medium or above, define specific mitigations:

```markdown
### Mitigation Measures

| # | Measure | Risk(s) addressed | Implementation status | Residual risk |
|---|---|---|---|---|
| M1 | [Specific technical or organisational measure] | R1, R3 | [Implemented / In progress / Planned] | [Must be lower than inherent risk] |
| M2 | ... | ... | ... | ... |
```

**Mitigation categories:**

- **Technical** — encryption, pseudonymisation, access controls, automated deletion, audit logging
- **Organisational** — policies, training, DPIAs for changes, breach procedures
- **Contractual** — data processing agreements, standard contractual clauses for transfers
- **Rights mechanisms** — subject access request process, consent management, opt-out capability

Every risk must map to at least one mitigation. Every mitigation must reduce residual risk below the inherent risk level.

**Output:** Mitigation table with residual risk ratings demonstrating risk reduction.

## Step 5: Obtain DPO Opinion

Provide an assessment section for DPO review:

```markdown
### DPO Review

| Item | Assessment |
|---|---|
| **DPIA required?** | [Yes — state which Art. 35 trigger applies] |
| **Processing lawful?** | [Yes/No — cite lawful basis and evidence] |
| **Proportionate?** | [Yes/No — are all principles met?] |
| **Risks adequately mitigated?** | [Yes/No — are all residual risks acceptable?] |
| **DPO recommendation** | [Proceed / Proceed with conditions / Do not proceed] |
| **Conditions (if any)** | [What must be done before processing begins] |
| **Review date** | [When this DPIA should be reviewed — max 12 months] |

**DPO signature:** _______________  **Date:** _______________
```

**Output:** DPO review section with clear recommendation.

## Step 6: Determine Supervisory Authority Consultation

Assess whether [Article 36](https://gdpr-info.eu/art-36-gdpr/) prior consultation is required:

```markdown
### Supervisory Authority Consultation

| Question | Answer |
|---|---|
| **Any residual risks rated High or Very High after mitigation?** | [Yes/No] |
| **Can residual risk be further reduced?** | [Yes/No — what has been tried] |
| **Prior consultation required?** | [Yes — if residual risk remains high despite mitigations / No] |
| **Supervisory authority** | [Relevant DPA — e.g., ICO, CNIL, BfDI] |
| **Consultation timeline** | [Must consult before processing begins; DPA has 8 weeks to respond] |
```

Prior consultation is required when: residual risk remains high despite mitigations **and** the controller cannot sufficiently reduce the risk.

**Output:** Consultation determination with rationale.

## Rules

- **Process before technology.** Describe what you are doing with personal data before discussing how you implement it technically. The DPIA assesses the processing activity, not the software.
- **Always take the individual's perspective.** "We might get fined" is not a risk. "An individual's health data could be exposed, causing distress and discrimination" is a risk.
- **Risks must be specific, not generic.** "Data breach" is not a risk assessment. "Unauthorised access to customer financial records via unencrypted API responses, leading to identity theft" is a risk assessment.
- **Residual risk must be lower than inherent risk.** If a mitigation doesn't reduce the risk level, it's not effective — find a better mitigation or escalate to DPO.
- **Never skip the necessity assessment.** If the processing isn't necessary and proportionate, no amount of mitigation makes it lawful. Step 2 can stop the entire DPIA.
- **DPIAs are living documents.** Set a review date. Processing changes require DPIA updates.

## Output Format

```markdown
# DPIA: [Processing Activity Name]

**Version:** [number]  |  **Date:** [date]  |  **Owner:** [role]  |  **Status:** [Draft/Under review/Approved]

## 1. Processing Description
[From Step 1 — data, subjects, purpose, flows, retention, recipients]

## 2. Necessity and Proportionality
[From Step 2 — principle-by-principle assessment with verdicts]

## 3. Risk Assessment
[From Step 3 — risk table with likelihood, severity, overall rating]

## 4. Mitigation Measures
[From Step 4 — measure table with residual risk ratings]

## 5. DPO Review
[From Step 5 — recommendation and conditions]

## 6. Supervisory Authority Consultation
[From Step 6 — determination and rationale]

## Appendices
- A. Data flow diagram
- B. Legal basis analysis
- C. Third-party processor list
```

## Related Skills

- `/grc-lead:compliance-audit` — audit GDPR compliance across the system. Use to validate that DPIA mitigations are implemented organisation-wide.
- `/grc-lead:risk-assessment` — broader risk methodology. The DPIA risk approach aligns with the organisation's risk framework.
