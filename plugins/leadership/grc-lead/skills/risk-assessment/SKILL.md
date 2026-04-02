---
name: risk-assessment
description: Conduct a risk assessment — identify, analyse, and evaluate risks with quantified likelihood, impact, and treatment plans.
argument-hint: "[system, project, initiative, or change to assess]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Conduct a risk assessment for $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Scope Definition

Define what is being assessed. A risk assessment without boundaries is a worry list.

1. **Subject** — what system, project, initiative, or change?
2. **Boundaries** — what is included? (components, data, processes, teams)
3. **Exclusions** — what is explicitly out of scope?
4. **Time horizon** — when do these risks materialise? (immediate, 3 months, 12 months)
5. **Stakeholders** — who is affected if these risks materialise?

### Step 2: Risk Identification

Systematically identify risks across ALL categories. Do not skip a category because you think it does not apply — document "no identified risks" with reasoning.

| Category | What to look for |
|---|---|
| **Regulatory** | Non-compliance with GDPR, Privacy Act, SOC 2, ISO 27001, industry-specific regulations |
| **Operational** | Process failures, key person dependency, system outages, supply chain disruption |
| **AI/ML** | Bias, hallucination, privacy leakage, prompt injection, model dependency, cost spikes |
| **Data** | Breach, loss, corruption, unauthorised access, inadequate retention/deletion |
| **Financial** | Budget overruns, vendor lock-in, uncontrolled AI spend, licensing costs |
| **Reputational** | Customer trust, public incidents, regulatory action, negative media |
| **Vendor/Third-party** | Provider outage, security posture, contract terms, data residency |

**For each risk identified, assign a unique ID** (e.g., `R-001`).

### Step 3: Risk Analysis

Quantify every risk. "There is a data breach risk" is not useful. "Likelihood: Medium (25%), Impact: Critical" enables decisions.

**Likelihood:**

| Level | Probability | Description |
|---|---|---|
| **Low** | < 10% | Unlikely under current conditions |
| **Medium** | 10–40% | Plausible given known conditions |
| **High** | 40–70% | Probable given current trends or known weaknesses |
| **Very High** | > 70% | Expected to occur without intervention |

**Impact:**

| Level | Description |
|---|---|
| **Low** | Minimal disruption, no data exposure, cosmetic or informational |
| **Medium** | Limited data exposure, feature degradation, contained impact |
| **High** | Significant data exposure, major feature compromise, reputational damage, regulatory scrutiny |
| **Critical** | Data breach, financial loss, complete service compromise, regulatory violation, legal action |

**Risk matrix:**

| | Low Impact | Medium Impact | High Impact | Critical Impact |
|---|---|---|---|---|
| **Very High likelihood** | Medium | High | Critical | Critical |
| **High likelihood** | Low | Medium | High | Critical |
| **Medium likelihood** | Low | Medium | Medium | High |
| **Low likelihood** | Low | Low | Medium | Medium |

### Step 4: Existing Controls Assessment

For each risk, document what mitigations are already in place:

| Question | Evidence to check |
|---|---|
| What controls exist? | Grep for auth middleware, encryption config, access controls, monitoring, CI gates |
| Are controls automated or manual? | Automated controls are reliable. Manual controls are aspirational until audited |
| When were controls last verified? | A control that was verified 2 years ago is a control that might not work |
| Are controls documented? | Undocumented controls are invisible to new team members |

### Step 5: Residual Risk Calculation

Residual risk = inherent risk after existing controls are applied.

For each risk:
1. Start with the inherent risk score (Step 3)
2. Assess control effectiveness: **Full** (reduces risk by 2 levels), **Partial** (reduces by 1 level), **None** (no reduction)
3. Calculate residual risk score

If residual risk is still High or Critical, the risk needs additional treatment.

### Step 6: Risk Treatment

Every risk needs a treatment decision. "We'll deal with it later" is not a treatment.

| Treatment | When to use | Requirements |
|---|---|---|
| **Accept** | Residual risk is Low or Medium AND cost of mitigation exceeds impact | Owner, justification, review date (maximum 6 months), conditions for re-evaluation |
| **Mitigate** | Controls can reduce risk to acceptable level | Action plan with owner, timeline, success criteria, verification method |
| **Transfer** | Risk can be shifted to a third party | Insurance, contractual indemnity, or SLA with penalties. Verify the transfer is real |
| **Avoid** | Risk is unacceptable and no mitigation is sufficient | Change plans to eliminate the risk source entirely |

**Acceptance rules:**
- Every accepted risk has an owner (a person, not a team)
- Every accepted risk has an expiry date (maximum 6 months)
- Critical risks cannot be accepted without coordinator approval
- Acceptance is documented with reasoning — "low priority" is not a justification

### Step 7: Risk Register Compilation

Compile all findings into the risk register format.

## Anti-Patterns (NEVER do these)

- **Risks without quantification** — "there is a risk" without likelihood and impact is a worry, not a risk assessment
- **Accepted risks without owner or expiry** — unowned risks are orphaned risks. Risks without review dates are permanently ignored risks
- **Missing residual risk** — reporting inherent risk without accounting for existing controls overstates the risk posture
- **Controls without verification** — "we have encryption" without evidence it is configured correctly is a false control
- **One-time assessment** — risk assessments are living documents. If the system changes, the risks change. Define review triggers
- **Treating all risks equally** — the risk matrix exists to prioritise. Critical risks get immediate action, low risks get monitoring

## Output Format

```markdown
# Risk Assessment: [subject]

## Scope
- **Subject:** [what is being assessed]
- **Boundaries:** [what is included]
- **Exclusions:** [what is out of scope]
- **Time horizon:** [when risks materialise]
- **Assessment date:** [date]
- **Assessor:** [who performed this assessment]

## Risk Register

### R-001: [descriptive name]

- **Category:** [Regulatory / Operational / AI / Data / Financial / Reputational / Vendor]
- **Description:** [what could happen — specific, not generic]
- **Likelihood:** [Low / Medium / High / Very High] ([percentage estimate])
- **Impact:** [Low / Medium / High / Critical]
- **Inherent risk:** [Low / Medium / High / Critical] (from matrix)
- **Current controls:** [what mitigations exist today]
- **Control effectiveness:** [Full / Partial / None]
- **Residual risk:** [Low / Medium / High / Critical]
- **Treatment:** [Accept / Mitigate / Transfer / Avoid]
- **Treatment detail:** [specific action or justification]
- **Owner:** [person accountable]
- **Review date:** [when to reassess — maximum 6 months]

## Risk Summary

| Risk | Category | Inherent | Residual | Treatment | Owner |
|---|---|---|---|---|---|
| R-001 | [cat] | [level] | [level] | [action] | [person] |

## Prioritised Actions
1. [Critical/High residual risks — immediate action required]
2. [Medium residual risks — planned mitigation]
3. [Accepted risks — monitoring schedule]

## Review Schedule
- **Next review:** [date]
- **Review triggers:** [system changes, incidents, regulatory updates, 6-month maximum]
```

## Related Skills

- `/grc-lead:compliance-audit` — when risks have regulatory exposure, audit compliance against the relevant framework.
- `/grc-lead:ai-governance-review` — when AI/ML risks are identified, run a specialised governance review.
