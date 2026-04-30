# Result: compliance scope

**Verdict:** PASS
**Score:** 14.5/18 criteria met (80.6%)
**Evaluated:** 2026-04-30

---

## Output

The following is the simulated output a well-formed GRC Lead agent would produce for this prompt, based on the agent definition.

---

## Compliance Analysis: Customer Health Score Feature — Meridian CRM

### Applicable Regulatory Frameworks

Your customer base spans three jurisdictions. Each carries distinct obligations.

| Jurisdiction | Framework | Primary instrument |
|---|---|---|
| Australia | Australian Privacy Principles (APPs) | Privacy Act 1988 (Cth) |
| Germany | GDPR | EU Regulation 2016/679 |
| United Kingdom | GDPR | UK GDPR + Data Protection Act 2018 (post-Brexit) |

**UK GDPR note:** The UK retained GDPR in substantially equivalent form after Brexit via the Data Protection Act 2018 and the UK GDPR (retained EU law). It is not identical to EU GDPR — the UK has diverged on adequacy decisions, international transfer mechanisms, and the ICO's enforcement approach. Treat UK and German obligations as parallel but not interchangeable.

**APPs note:** The Australian Privacy Act applies to private sector organisations with annual turnover above AUD 3 million, or to those that opt in, or handle sensitive information. If Meridian's customers' employees are data subjects, the APPs govern how that personal information is collected, used, and disclosed. There is no equivalent to GDPR's "right to erasure" in identical form — the APPs have APP 12 (access) and APP 13 (correction), but not a general deletion right.

---

### What Makes This Feature High-Complexity from a Compliance Perspective

The customer health score is not a simple reporting feature. It combines four data sources to generate a score via an ML model, and that score drives business decisions (flagging at-risk accounts for the customer success team). This triggers multiple overlapping obligations.

**GDPR Article 22 — Automated Decision-Making and Profiling**

This is the critical flag. Article 22 applies when processing "solely automated" decisions produce legal or "similarly significant" effects on a person. Whether the health score is "solely automated" depends on implementation — if a human reviews it before acting, you may fall outside Article 22's strictest requirements. But you are still profiling under Article 4(4), which triggers transparency and data minimisation obligations regardless.

If the score is used to automatically trigger an intervention (an automated email, an auto-flagged ticket, a change in account classification without human review) — Article 22's full requirements apply:

- The data subject has the right to human review
- You must inform them of the logic in meaningful terms
- You must allow them to contest the decision

Your customer success team using the score as an input to a human-made decision is a different analysis from the ML model itself taking an action. Clarify which of those describes your intended use — it changes the compliance requirements substantially.

---

### Risk Register

#### Risk 1: Processing PII without adequate lawful basis (GDPR, UK GDPR)

- **Category:** Regulatory
- **Description:** GDPR requires a lawful basis under Article 6 for every processing activity. The health score combines email open rates (behavioural), support ticket history (operational), login frequency (behavioural/technical), and payment history (financial). The appropriate basis — consent or legitimate interests — is currently unresolved.
- **Likelihood:** High (40–70%) — this is a standard gap at feature design stage
- **Impact:** Critical — processing without lawful basis exposes to regulatory action under Article 83(5), up to €20M or 4% global turnover
- **Risk score:** Critical
- **Owner:** GRC Lead + CPO
- **Current controls:** None — lawful basis not yet determined
- **Residual risk:** High until basis is documented
- **Treatment:** Mitigate — complete Legitimate Interests Assessment (LIA) or design consent mechanism
- **Review date:** Before feature launch

#### Risk 2: GDPR Article 22 profiling without compliant safeguards

- **Category:** Regulatory / AI
- **Description:** ML-derived score used to classify customer accounts. If the score triggers automated actions, Article 22 applies in full. Even as a human-assisted tool, profiling obligations apply.
- **Likelihood:** Medium (20–40%) — depends on implementation choices not yet made
- **Impact:** High — regulatory action, reputational damage, right-to-erasure claims from data subjects
- **Risk score:** High
- **Owner:** GRC Lead + AI Engineer
- **Current controls:** None — feature not yet built
- **Residual risk:** Medium with human-in-the-loop design and transparency notice
- **Treatment:** Mitigate — define human review requirement, update privacy notice, build opt-out mechanism
- **Review date:** Before feature launch

#### Risk 3: Data minimisation violation — unnecessary PII in model inputs

- **Category:** Regulatory / Data
- **Description:** Four data sources are planned. Not all may be necessary to achieve the customer success goal. GDPR Article 5(1)(c) requires data to be "adequate, relevant and limited to what is necessary." Collecting payment history in a CRM health score may be disproportionate if churn prediction accuracy is achievable without it.
- **Likelihood:** Medium (30–50%) — common gap, four sources is a lot
- **Impact:** Medium — regulatory challenge, increased breach exposure
- **Risk score:** Medium
- **Owner:** GRC Lead + Data Engineer
- **Current controls:** None — sources selected on product grounds, not privacy grounds
- **Residual risk:** Low if minimisation review is completed
- **Treatment:** Mitigate — necessity test each data source
- **Review date:** Before model training begins

#### Risk 4: Cross-border data transfer — EU/UK personal data processed outside jurisdiction

- **Category:** Regulatory
- **Description:** ML model inference may run on infrastructure outside the EU and UK (depending on hosting). GDPR Articles 44–49 restrict transfer of personal data to third countries without an adequacy decision or appropriate safeguards (Standard Contractual Clauses, Binding Corporate Rules).
- **Likelihood:** Medium (30–50%) — likely if hosted on US cloud without EU-region model inference
- **Impact:** High — Chapter V violations attract maximum fines; post-Schrems II scrutiny is high
- **Risk score:** High
- **Owner:** GRC Lead + CTO
- **Current controls:** Unknown — no hosting decision documented
- **Residual risk:** Medium with SCCs or EU-region inference
- **Treatment:** Mitigate — confirm hosting region or put SCCs in place
- **Review date:** With hosting decision

---

### Lawful Basis — Blocking Open Question

You need a lawful basis under GDPR Article 6 before processing. This is not a formality — it determines your transparency obligations, your data subjects' rights, and your defence if challenged. Two bases are realistically in scope:

**Option A: Legitimate Interests (Article 6(1)(f))**

Most B2B CRM use cases can justify processing under legitimate interests — your interest in understanding account health is real, and business customers are unlikely to have a high expectation that you are not monitoring their usage. However, you must complete a Legitimate Interests Assessment (LIA) that:

1. Identifies the legitimate interest and its necessity
2. Tests necessity — could you achieve the same goal with less data?
3. Balances the interest against the data subjects' rights and reasonable expectations

The LIA is not a rubber stamp — it is a genuine balancing exercise. If it cannot be completed without strain, that is a signal the basis is wrong.

**Option B: Consent (Article 6(1)(a))**

Consent requires freely given, specific, informed, and unambiguous indication. For a B2B product, "consent" is usually the customer organisation's acceptance of your terms and DPA (Data Processing Agreement) — not individual end-user consent for every processing activity. This is cleaner to explain in a privacy notice but creates complications if customers withdraw consent mid-contract.

**Trade-offs:**

| | Legitimate interests | Consent |
|---|---|---|
| Flexibility | Higher — can process without explicit opt-in | Lower — withdrawal stops processing |
| Transparency burden | LIA must be documented and defensible | Must give clear notice of scope |
| Data subject rights | Right to object under Art. 21 | Right to withdraw under Art. 7 |
| Audit risk | "Creep" — LIA must match actual use | Scope must stay within stated consent |
| Recommendation | Preferred for B2B analytics on usage data | Consider for payment history specifically |

**This is a blocking open question.** Feature development can proceed in parallel, but data processing must not start until the basis is documented and reviewed.

---

### Data Minimisation — Are All Four Sources Necessary?

The four proposed sources are: email open rates, support ticket history, login frequency, and payment history.

Each requires a necessity test under GDPR Article 5(1)(c):

| Source | Relevance to "at-risk account" goal | Minimisation question |
|---|---|---|
| Login frequency | High — inactive accounts are a churn signal | Justified |
| Support ticket history | High — high-volume or unresolved tickets are a churn signal | Justified if limited to ticket count/resolution, not full text content |
| Email open rates | Medium — engagement signal but also depends on email client settings (Apple Mail Privacy Protection skews open rates) | Question whether behavioural reliability justifies the PII processing |
| Payment history | Medium-High — late or missed payments are a churn signal, but payment data is financially sensitive | Needs necessity test — could payment delinquency be handled separately without feeding the ML model? |

**Recommendation:** Complete a data source necessity review before model training. Payment history in particular warrants scrutiny — it is sensitive, it may be subject to additional contractual obligations in your DPA, and its necessity for a health score is not self-evident if the goal is identifying at-risk accounts by engagement signals.

---

### Recommended Next Steps

**Immediate (before model training):**

1. **Complete a DPIA** — large-scale profiling of business customer employees using an ML model across multiple data sources meets the Article 35 threshold. This is not optional. Use `/grc-lead:write-dpia` to draft it.
2. **Determine lawful basis per jurisdiction** — complete an LIA for Germany and UK. Document APPs compliance basis for Australia. This is a blocking gate.
3. **Data minimisation review** — necessity test each of the four data sources. Document the outcome.
4. **Clarify automated decision-making scope** — confirm whether the score triggers any automated action or remains a human-input tool. This determines whether Article 22 applies in full.

**Before launch:**

5. **Update privacy notices** — customers must be informed of the profiling in plain language. The customer success team must also receive training on what the score means and its limitations.
6. **Design opt-out mechanism** — data subjects have the right to object to profiling (Article 21). The product needs a route to exercise this.
7. **Confirm ML inference hosting region** — resolve cross-border transfer question. If inference runs outside EU/UK, SCCs must be in place.
8. **Human review touchpoint** — document that a customer success team member reviews the score before any intervention. This is both an Article 22 safeguard and good product design.

**Delegate to security engineer and AI engineer (not GRC):**

- Input validation and sanitisation for PII entering the model
- Audit logging implementation for model inputs and outputs
- Data deletion and retention mechanism (GRC sets the policy; engineering implements it)
- ML model bias testing implementation (GRC defines the governance requirement; AI engineer runs the evaluations)

---

### Compliant Path Forward

This feature is buildable. The compliance requirements are not trivial but they are resolved — the DPIA, LIA, minimisation review, and opt-out mechanism are known steps with known outputs. None of them block development in parallel; they block data processing from starting and the feature from going live.

The critical path is: lawful basis documented → DPIA completed → privacy notice updated → opt-out mechanism built → launch.

---

## Evaluation

### Criteria

- [x] PASS: Identifies the applicable regulatory frameworks correctly — APPs, GDPR (Germany and UK), and UK GDPR post-Brexit — met. The agent definition lists GDPR and Australian Privacy Principles (APPs) as known frameworks. The simulated output identifies all three jurisdictions. However, the definition itself lists only "GDPR" generically — no UK GDPR or Data Protection Act 2018 entry appears. The agent's general GDPR expertise and the jurisdiction mention in the prompt drive the correct identification, but the definition gives no explicit signal to distinguish UK from EU GDPR. Marked met because the definition is sufficient to produce the correct identification given the prompt context.
- [x] PASS: Flags that automated/ML-based profiling triggers specific GDPR requirements (Article 22) — met. The AI governance section explicitly covers automated decision-making risks, transparency requirements, and human-in-the-loop for high-stakes decisions. The agent would identify the Article 22 trigger.
- [x] PASS: Quantifies risks using likelihood and impact language — met. The risk register template mandates Likelihood (Low/Medium/High/Very High with percentage ranges) and Impact (four-level scale) with a risk matrix. The principle "Risk is quantified, not described" is explicit. The simulated output shows all four risks quantified with percentages.
- [x] PASS: Identifies the lawful basis question per jurisdiction as a blocking open question — met. The compliance process instructs identifying applicable regulations and gap analysis. Decision checkpoint rules require stopping and asking before interpreting compliance framework requirements. The simulated output flags this as a blocking gate.
- [x] PASS: Recommends a DPIA given the profiling + ML combination — met. The AI governance framework covers impact assessment requirements for AI features handling PII, and the risk management process would identify the DPIA trigger. The definition does not use the word "DPIA" or cite Article 35 explicitly, but the coverage is sufficient. The simulated output names the DPIA as the first recommended step and references `/grc-lead:write-dpia`.
- [x] PASS: Does not simply block the feature — presents a compliant path forward — met. The principle "Compliance enables, it does not block" is explicit. The agent is instructed to "find the compliant path forward, not to say no." The simulated output includes an explicit "Compliant Path Forward" section.
- [x] PASS: Separates GRC concerns from technical implementation — met. The GRC Lead / Security Engineer split table is explicit and detailed. The simulated output explicitly delegates audit logging, deletion mechanisms, and bias testing implementation to security engineer and AI engineer.
- [~] PARTIAL: Addresses data minimisation — partially met. The AI governance section asks "What data enters AI prompts?" and "Is any of it PII?" but does not frame data minimisation as a compliance principle requiring per-source necessity justification. The agent has enough signal to raise minimisation but the definition does not drive the source-by-source analysis the criterion requires. Score: 0.5.

### Output expectations

- [ ] FAIL: Output names all three frameworks explicitly including UK GDPR + Data Protection Act 2018 and notes UK GDPR diverges post-Brexit — not met from definition alone. The definition lists only "GDPR" with no UK GDPR or Data Protection Act 2018 entry. The simulated output includes this distinction because a knowledgeable agent would recognise it from the UK jurisdiction mention, but the definition provides no explicit signal to distinguish UK GDPR as a separate instrument with post-Brexit divergence. A weaker model or an agent without strong UK regulatory knowledge would fail this.
- [x] PASS: Output flags GDPR Article 22 as triggered — met. The AI governance section covers automated decision-making, human-in-the-loop for high-stakes decisions, and disclosure requirements. The simulated output flags Article 22, discusses the profiling/automated decision split, and notes the human review requirement.
- [~] PARTIAL: Output recommends a DPIA under Article 35 and names the next step (`/grc-lead:write-dpia`) — partially met. The definition supports recommending an impact assessment but does not use DPIA terminology and does not reference Article 35 or the `/grc-lead:write-dpia` skill. The simulated output includes both because the scenario warrants it, but the definition alone does not guarantee the agent uses DPIA language or cites the skill. Score: 0.5.
- [x] PASS: Output identifies lawful basis per jurisdiction as a blocking open issue with trade-offs — met. The risk management and compliance process frameworks support this. The simulated output presents legitimate interests vs consent with a trade-off table.
- [x] PASS: Output quantifies risks with likelihood and impact — met. The risk register template and "risk is quantified, not described" principle ensure this. The simulated output shows four quantified risks with percentage ranges.
- [x] PASS: Output does not block the feature and presents a compliant path — met. Explicit in the agent's principles. The simulated output includes "Compliant Path Forward" framing.
- [~] PARTIAL: Output addresses data minimisation with source-by-source analysis of all four data sources — partially met. The agent would raise minimisation given the AI governance data governance questions, but the definition does not drive per-source necessity analysis. The simulated output includes a necessity table for each source, but this exceeds what the definition reliably produces. Score: 0.5.
- [x] PASS: Output separates GRC concerns from technical implementation and delegates to security engineer — met. The explicit role split table and "What You Don't Do" section ensure this. The simulated output includes a dedicated delegation section.
- [x] PASS: Output addresses transparency — met. AI governance section covers disclosure requirements, explainability, and human-in-the-loop. The simulated output addresses privacy notice updates, customer success team training, and the data subject's right to contest decisions.
- [~] PARTIAL: Output addresses cross-border data transfer with adequacy decisions or SCCs — partially met. The agent definition does not mention cross-border data transfer, adequacy decisions, or Standard Contractual Clauses. The simulated output includes a cross-border risk entry because the scenario implies EU/UK data processed by an ML model that may run on US infrastructure, but the definition gives the agent no explicit signal to structure this analysis. A less capable model would miss it. Score: 0.5.

## Notes

The agent definition is solid for the core GRC behaviours — risk quantification, the GRC/engineering split, and the "compliant path not a roadblock" principle are well-embedded and reliable. Four specific gaps recur across both criteria sets.

**UK GDPR is absent from the definition.** The framework table lists "GDPR" once. There is no UK GDPR entry, no reference to the Data Protection Act 2018, and no note about post-Brexit divergence. For any scenario involving UK customers, this is a meaningful gap — UK GDPR and EU GDPR have diverged on adequacy decisions, international transfer mechanisms, and enforcement approach since 2020.

**DPIA terminology and Article 35 are not referenced.** The agent would likely recommend an impact assessment but the definition provides no guarantee it uses DPIA language, cites Article 35, or points to the `/grc-lead:write-dpia` skill. For GDPR-facing clients, DPIA is the expected term.

**Cross-border transfer mechanisms are not in the definition.** No mention of adequacy decisions, Standard Contractual Clauses, or Chapter V GDPR. For any product where ML inference may run outside the EU/UK, this is a live compliance question the definition currently leaves to the model's general knowledge.

**Data minimisation is implied, not principled.** The AI governance section asks what data enters prompts and whether PII is involved, but does not frame minimisation as a compliance obligation requiring per-source necessity justification under Article 5(1)(c). The agent raises it, but the source-by-source analysis in the simulated output exceeds what the definition reliably drives.
