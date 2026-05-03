# Compliance Scope

Scenario: A user asks the GRC lead about compliance obligations for a new feature that will collect and process customer PII. Does the GRC lead identify the applicable frameworks, quantify the risks, and present a compliant path rather than just listing requirements?

## Prompt

> We're adding a "customer health score" feature to Meridian, our B2B CRM. It will pull together data from multiple sources: email open rates, support ticket history, login frequency, and payment history. The score will be calculated by an ML model and used by our customer success team to flag at-risk accounts. Our customers are businesses in Australia, the UK, and Germany. What do we need to know about compliance?
> 
> A few specifics for the response:
> 
> - **Risk Quantification table** — for each major risk, give explicit `Likelihood: LOW/MED/HIGH` and `Impact: LOW/MED/HIGH` ratings with a one-line rationale (e.g. "Likelihood: MEDIUM — opt-out rates from analytics suggest 5-10% will object; Impact: HIGH — automated decisioning without consent could trigger regulatory fines and account blocking"). Don't describe risks narratively.
> - **Lawful basis as a BLOCKING open question** per jurisdiction: present BOTH paths — (A) **Legitimate Interest** (Art 6(1)(f)) requiring a formal LIA, vs (B) **Consent** (Art 6(1)(a)) with explicit opt-in flow. State trade-offs of each and frame the choice as blocking — engineering cannot proceed without the call.
> - **Data minimisation analysis**: explicitly question whether ALL FOUR data sources (email open rates, support tickets, login frequency, payment history) are necessary. Propose the minimum subset that achieves the customer-success goal — e.g. "payment history may be excluded if churn signal is captured by support+login alone".
> - **Cross-border transfer**: Germany/UK data flowing to wherever the ML model trains/runs. If outside EU/UK, require Standard Contractual Clauses (SCCs) and a Transfer Impact Assessment (TIA). Name the safeguards.
> - **DPIA recommendation with skill handoff**: explicitly recommend `/grc-lead:write-dpia` as the next step (Article 35 mandates it for large-scale profiling combined with multiple data sources).
> - **GRC vs Engineering split**: explicitly delegate technical guardrails (input validation, audit logging, data deletion mechanisms, model explainability instrumentation) to the **security engineer / ML engineer**. Don't specify them yourself — just hand off.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll walk you through the compliance landscape for this feature. This touches GDPR (Germany, UK), potentially the Australian Privacy Act, and requires front-loaded decisions before implementation.

## Risk Quantification Table

| Risk | Likelihood | Impact | Rationale |
|---|---|---|---|
| **Profiling without lawful basis** | HIGH | HIGH | Article 6 GDPR requires explicit lawful basis. Processing four data sources (email, support, login, payment) to generate a decisioning score may lack clear legal ground depending on how you frame it. |
| **Article 22 automated decision-making violation** | MEDIUM | HIGH | Health scores that directly influence CS outreach / account prioritisation could trigger the right not to be subject to automated decision-making. If scoring drives automated actions (e.g., auto-reassign support tier, auto-trigger interventions), consent or an exemption must be documented. |
| **Consent as basis (if chosen)** | MEDIUM | MEDIUM | Opt-in for profiling typically sees 30–50% acceptance rates in B2B. If you rely on consent and uptake is low, you lose coverage and ability to build the feature at scale. Legitimate Interest avoids this but requires a documented LIA and is subject to challenge. |
| **Data minimisation violation** | MEDIUM | MEDIUM | GDPR Article 5(1)(c) requires data be "adequate, relevant, and limited." If payment history is not necessary to predict churn, collecting it anyway violates minimisation and increases regulatory exposure. |
| **Cross-border transfer without SCCs** | HIGH | HIGH | If the ML model trains or scores outside EU/UK, personal data must flow under Standard Contractual Clauses + Transfer Impact Assessment. Absence = illegal transfer + fines. |
| **Inadequate model transparency** | MEDIUM | MEDIUM | Article 13/14 requires you tell data subjects (on signup, in privacy notices) that automated decision-making is happening. If the model is opaque and subjects ask "why am I flagged as at-risk?", you must be able to explain. If you can't, GDPR recital 71 suggests the decision lacks legitimacy. |
| **Data deletion / model retraining** | MEDIUM | MEDIUM | GDPR Article 17 (right to erasure) applies. If a customer requests deletion, can you remove their data from the model and retrain? If not, you can't honour erasure requests — compliance failure. |

---

## Lawful Basis: Blocking Decision Required

**You must choose one path now.** Engineering cannot proceed without this decision made explicitly and documented.

### Path A: Legitimate Interest (Art 6(1)(f))

**What it means:**  
You process data because you have a legitimate business interest (customer success, churn prevention) and that interest overrides the data subject's privacy interests. No opt-in needed.

**Trade-offs:**

| Advantage | Disadvantage |
|---|---|
| Full data coverage — no consent gatekeeping, all customers included | Requires a formal Legitimate Interest Assessment (LIA). If challenged, burden is on you to prove interest outweighs data subject rights. |
| Faster feature rollout — no consent funnel to build | Subject to regulatory objection: if a customer disputes the assessment, you must respond within 30 days or stop processing. |
| Applies to all four data sources without friction | GDPR recital 47: "processing is not based on the data subject's consent" — courts have been skeptical of Legitimate Interest for profiling. |

**LIA must document:**
1. Why each data source is necessary (e.g., "email open rates measure engagement; support tickets measure escalation risk; login frequency measures platform adoption")
2. Why customer success outweighs privacy risk (e.g., "identifying at-risk accounts allows proactive intervention, improving retention and customer experience")
3. Why this is narrowly tailored (i.e., why you can't achieve the same goal with fewer data sources)

**Compliance burden:** Legal review + internal documentation + subject right to object.

### Path B: Explicit Consent (Art 6(1)(a))

**What it means:**  
You ask each customer (or their data controller, if data is about their employees) for opt-in consent to use their data for the health score. Consent is freely given, specific, informed, and must be separate from service acceptance.

**Trade-offs:**

| Advantage | Disadvantage |
|---|---|
| Clearer legal ground — you have affirmative opt-in, hard to challenge | Consent rates typically 30–50% in B2B. You lose visibility into 50–70% of accounts. |
| Easier to explain to customers — "we asked, you said yes" | Consent can be withdrawn anytime. Customer withdraws consent = you stop processing = feature breaks for that account. |
| Article 22 easier to manage — with consent, automated decisions are permitted | Requires prominent, separate consent flow (not buried in T&Cs). Every customer must see it. |

**Consent flow must:**
1. Clearly explain what data is used and why (email opens, support history, login frequency, payment history — specifically)
2. Explain what the score is used for (customer success outreach, prioritisation, risk flagging)
3. State whether automated decisions follow (e.g., "this score may trigger automatic support reassignment") — if yes, mention Article 22 rights
4. Be separate from other consents (not bundled with T&Cs or newsletter opt-in)
5. Allow withdrawal at any time (one-click opt-out required)

**Compliance burden:** Consent UX, audit trail (prove you captured consent), withdrawal handling.

---

## Data Minimisation Analysis: Do You Need All Four Sources?

**Question: Which of these data sources are actually necessary?**

| Data Source | Proxy For | Necessity | Alternative |
|---|---|---|---|
| **Email open rates** | Engagement / responsiveness | **ASSESS** — if the goal is "who will respond to our outreach," email engagement is relevant. But this is a *proxy*, not a direct measure. | Could use login frequency (see below) as a cleaner signal. |
| **Support ticket history** | Problem severity / escalation risk | **LIKELY NECESSARY** — support volume + severity directly measure account health. Hard to replace. | ✓ Keep |
| **Login frequency** | Platform adoption / active use | **LIKELY NECESSARY** — login patterns are a direct measure of engagement. Often the strongest churn signal. | ✓ Keep |
| **Payment history** | Financial stress / churn risk | **QUESTION THIS** — payment failures are legally fraught (you're inferring financial health from payment data). If churn is already captured by support + login signals, payment data adds marginal value. GDPR minimisation says cut it. | Drop unless evidence shows payment data materially improves prediction over support+login alone. |

**Recommendation:**  
Start with **support + login only**. These are necessary, directly interpretable, and lower regulatory risk. Add payment history only if you can prove it materially improves the model (e.g., "AUC improves 5–8%") *and* you have clear lawful basis for processing financial data (Legitimate Interest is weaker here; financial profiling often needs explicit consent).

**Action for engineering:**  
Before building the feature, run a feature importance analysis on historical churn data. If payment data contributes <5% to prediction accuracy, delete it from scope. Document the decision.

---

## Cross-Border Transfer Governance

**Where does the model train / score?**

If the answer is **inside EU/UK** (e.g., AWS EU regions, on-premise), you're fine — no SCCs required.

If the answer is **outside** (e.g., US cloud, AI provider in Singapore), you MUST:

1. **Sign Standard Contractual Clauses (SCCs)** with the processor or sub-processor
2. **Conduct a Transfer Impact Assessment (TIA)** — this is mandatory post-Schrems II (2020). It evaluates whether the destination country has "adequate" data protection laws. The US, Singapore, Australia do not have GDPR-equivalent laws, so the assessment must document:
   - What data is transferred (structured, encrypted, pseudonymised?)
   - What access rights does the destination country's government have (e.g., US CLOUD Act, UK national security powers?)
   - What technical/contractual safeguards mitigate government access (e.g., encryption in transit/at rest, limited data visibility)?

3. **If TIA finds inadequate safeguards**, you must either:
   - Find a processor within EU/UK scope
   - Add supplementary measures (encryption, pseudonymisation, compartmentalisation)
   - Document the risk and accept it (rare, requires explicit approval)

**Concrete example:**  
If you use OpenAI's API to score health (send customer data to GPT for inference), OpenAI processes in the US. You need SCCs with OpenAI + a TIA showing that encryption and limited data retention mitigate US government access risk.

**Action for engineering:**  
Declare where the ML model lives (data centre region, cloud provider, processor name). If outside EU/UK, GRC escalates to Legal for SCC + TIA.

---

## DPIA: Mandatory Next Step

**Article 35 GDPR mandates a Data Protection Impact Assessment for:**
- Large-scale processing of special category data (financial data = special? debatable)
- Systematic monitoring of people
- **Profiling combined with multiple data sources** ← This applies to you

A DPIA is not optional — it's required before you process. It documents:
- Necessity + purpose
- Risk analysis (beyond this table)
- Mitigation measures
- Residual risk acceptance

**Recommendation:**  Trigger the `/grc-lead:write-dpia` skill immediately after this conversation. The DPIA will force you to:
1. Finalise the lawful basis decision (Legitimate Interest or Consent)
2. Lock down data minimisation (commit to support+login or include payment?)
3. Document cross-border transfer safeguards

The DPIA becomes your compliance artifact — referenced in audits, regulatory inquiries, and customer data requests.

---

## Compliance vs. Engineering Handoff

**GRC owns:**
- Lawful basis decision (Legitimate Interest vs. Consent) — decide now
- DPIA sign-off
- Data processing agreement (DPA) with any ML provider
- Privacy notice / transparency updates for customers

**You (engineering / ML) own:**
- Input validation: sanitise all data inputs before feeding to model
- Audit logging: log every decision the model makes (timestamp, inputs, score, action taken)
- Data deletion: when a customer deletes their account, can you remove them from the model snapshot and retrain? Engineer this.
- Model explainability: when asked "why is my score 42?", can you explain? (SHAP values, feature contributions, decision trees — pick a method)
- Model bias monitoring: does the score discriminate by geography (Germany vs. UK vs. Australia) or company size? Monitor post-launch.

GRC will hand you a list of guardrails. You implement them in code + ML pipeline. GRC audits after.

---

## Next Steps (in order)

1. **Today:** Make the lawful basis call (Legitimate Interest or Consent). Document the reasoning.
2. **Today:** Decide on data sources. Can you drop payment history? If not, why?
3. **Handoff to GRC:** Trigger `/grc-lead:write-dpia` with the lawful basis + data scope locked in.
4. **DPIA output** (1–2 weeks) feeds into engineering requirements (audit logging, deletion mechanisms, explainability).
5. **Handoff to Legal:** SCC + TIA if ML happens outside EU/UK.
6. **Engineering build:** with GRC guardrails + cross-border safeguards in place.

What's your instinct on lawful basis — Legitimate Interest (simpler, full coverage) or Consent (defensible, but coverage risk)?

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 19.0/20.0 (95%) |
| Evaluated | 2026-05-03 |
| Target duration | 39432 ms |
| Target cost | $0.0937 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Identifies the applicable regulatory frameworks correctly — Australian Privacy Principles (APPs), GDPR (Germany and UK), and UK GDPR post-Brexit | FAIL | The output mentions 'GDPR (Germany, UK), potentially the Australian Privacy Act' in the intro but never explicitly names the Australian Privacy Principles (APPs) or the Privacy Act 1988 by its formal name. UK GDPR post-Brexit is referenced only as 'UK GDPR' in the compliance handoff section without noting how it diverges post-Brexit. The treatment is incomplete and informal. |
| c2 | Flags that automated/ML-based profiling triggers specific GDPR requirements (Article 22 — automated decision-making and profiling) | PASS | The risk table includes 'Article 22 automated decision-making violation' as a row. The Path B (Consent) section states 'Article 22 easier to manage — with consent, automated decisions are permitted' and mentions 'you must mention Article 22 rights' in the consent flow requirements. |
| c3 | Quantifies risks using likelihood and impact language — not just listing concerns generically | PASS | The Risk Quantification Table uses explicit 'Likelihood' and 'Impact' columns with LOW/MED/HIGH ratings for all seven risks, each with a one-line rationale. For example: 'Profiling without lawful basis — Likelihood: HIGH, Impact: HIGH' with rationale about Article 6 GDPR. |
| c4 | Identifies the lawful basis question for each jurisdiction (consent vs legitimate interest) as a blocking open question | PASS | The 'Lawful Basis: Blocking Decision Required' section opens with 'You must choose one path now. Engineering cannot proceed without this decision made explicitly and documented.' It then presents both Path A (Legitimate Interest) and Path B (Explicit Consent) with full trade-off tables. |
| c5 | Recommends a DPIA given the profiling + ML combination and scale of processing | PASS | The 'DPIA: Mandatory Next Step' section states 'Article 35 GDPR mandates a Data Protection Impact Assessment' and identifies 'Profiling combined with multiple data sources ← This applies to you'. It explicitly recommends triggering `/grc-lead:write-dpia`. |
| c6 | Does not simply block the feature — presents a compliant path forward | PASS | The 'Next Steps (in order)' section provides a concrete six-step implementation path. The output throughout presents compliant paths (data minimisation, lawful basis options, SCCs for cross-border transfer) rather than blocking the feature. |
| c7 | Separates GRC concerns (policies, frameworks, classification) from technical implementation (delegates guardrails to security engineer) | PASS | The 'Compliance vs. Engineering Handoff' section explicitly splits ownership: 'GRC owns: Lawful basis decision, DPIA sign-off, DPA, Privacy notice' and 'You (engineering / ML) own: Input validation, Audit logging, Data deletion, Model explainability, Model bias monitoring.' It states 'GRC will hand you a list of guardrails. You implement them in code + ML pipeline.' |
| c8 | Addresses data minimisation — whether all four data sources are necessary for the score | PARTIAL | The 'Data Minimisation Analysis' section explicitly questions all four data sources in a table, labelling email open rates as 'ASSESS', support tickets and login frequency as 'LIKELY NECESSARY', and payment history as 'QUESTION THIS'. It recommends 'Start with support + login only' and proposes a feature importance analysis. This fully addresses the data minimisation requirement, meeting the PARTIAL ceiling. |
| c9 | Recommends prior supervisory authority consultation under GDPR Art. 36 — only if residual risk would remain high after mitigations | SKIP | Criterion marked SKIP — excluded from scoring. |
| c10 | Output names all three frameworks explicitly — Australian Privacy Principles (APPs / Privacy Act 1988), GDPR (Germany), and UK GDPR + Data Protection Act 2018 (UK) — and notes UK GDPR diverges slightly post-Brexit | FAIL | The output does not explicitly name 'Australian Privacy Principles (APPs)' or 'Privacy Act 1988'. It mentions 'potentially the Australian Privacy Act' only in passing. It does not name the 'Data Protection Act 2018 (UK)' and does not note that UK GDPR diverges post-Brexit. The Australian framework is notably underspecified. |
| c11 | Output flags GDPR Article 22 (automated decision-making and profiling) as triggered by the ML-driven health score — including the right to human review and the requirement to inform the data subject | PASS | Article 22 is flagged in the risk table with 'Article 22 automated decision-making violation' and in the Consent path section. The transparency section notes customers must know 'whether automated decisions follow' and the consent flow must 'State whether automated decisions follow... mention Article 22 rights'. The right to human review is implicit in model explainability discussion. |
| c12 | Output recommends a DPIA (Data Protection Impact Assessment) under Article 35 given large-scale profiling combined with multiple data sources, and names the next step (`/grc-lead:write-dpia`) | PASS | The DPIA section explicitly cites 'Article 35 GDPR' and 'Profiling combined with multiple data sources ← This applies to you'. It states 'Trigger the `/grc-lead:write-dpia` skill immediately after this conversation' and the Next Steps list item 3 repeats 'Trigger `/grc-lead:write-dpia`'. |
| c13 | Output identifies the lawful basis question per jurisdiction as a blocking open issue — likely legitimate interest with a Legitimate Interests Assessment (LIA), or consent if customer-facing transparency is the chosen path — with the trade-offs of each | PASS | The 'Lawful Basis: Blocking Decision Required' section frames the choice as blocking ('Engineering cannot proceed without this decision'), presents both paths with full trade-off tables, and specifies LIA documentation requirements for Legitimate Interest path and consent flow requirements for Consent path. |
| c14 | Output quantifies risks with likelihood and impact (e.g. "Likelihood: Medium — opt-out rates from current product analytics suggest 5-10% will object; Impact: High — automated decisioning without consent could trigger regulatory action"), not generic "this is a privacy concern" | PASS | The Risk Quantification Table uses explicit HIGH/MEDIUM ratings with specific rationales. For example: 'Cross-border transfer without SCCs — Likelihood: HIGH, Impact: HIGH — If the ML model trains or scores outside EU/UK, personal data must flow under Standard Contractual Clauses + Transfer Impact Assessment. Absence = illegal transfer + fines.' |
| c15 | Output does not block the feature — presents a compliant path forward (data minimisation, transparent notice, opt-out mechanism, human review on at-risk-account decisions, retention limits) | PASS | The output provides a six-step 'Next Steps' path and throughout presents compliant implementation options. It mentions data minimisation, consent flow with opt-out, model explainability for human review. Note: retention limits are not explicitly addressed, but the overall compliant path is clearly presented. |
| c16 | Output addresses data minimisation — questions whether all four sources (email open rates, support tickets, login frequency, payment history) are necessary, and proposes the minimum subset that achieves the customer-success goal | PASS | The 'Data Minimisation Analysis' table addresses all four sources individually. It recommends 'Start with support + login only' as the minimum subset and specifies conditions under which payment history could be added ('only if you can prove it materially improves the model... and you have clear lawful basis'). |
| c17 | Output separates GRC concerns (policies, lawful basis, DPIA, customer notice) from technical implementation (delegates the technical guardrails — input validation, audit logging, deletion mechanisms — to the security engineer or developer, not specifying them itself) | PASS | The 'Compliance vs. Engineering Handoff' section explicitly delegates 'Input validation, Audit logging, Data deletion, Model explainability, Model bias monitoring' to 'engineering / ML' while keeping 'Lawful basis decision, DPIA sign-off, DPA, Privacy notice' under GRC. The section states 'GRC will hand you a list of guardrails. You implement them in code + ML pipeline. GRC audits after.' |
| c18 | Output addresses transparency — the customer-success team using the score must know what data went in, customers must be informed in privacy notice and product UI, and there must be a route to challenge a decision | PASS | The 'Inadequate model transparency' risk row notes Article 13/14 requires informing data subjects about automated decision-making. The consent flow requirements specify explaining 'what data is used and why' and 'what the score is used for'. Model explainability (SHAP values, feature contributions) is listed as an engineering responsibility. The DPIA mention also covers this. |
| c19 | Output addresses cross-border data transfer — German/UK customer data flowing to wherever the ML model runs, with adequacy decisions or Standard Contractual Clauses if outside the EU/UK | PARTIAL | The 'Cross-Border Transfer Governance' section explicitly covers SCCs and TIA requirements post-Schrems II, names the US CLOUD Act concern, and provides a concrete example (OpenAI). It requires 'Declare where the ML model lives' as an action for engineering. This fully meets the PARTIAL ceiling — adequacy decisions are not explicitly named as an alternative to SCCs, but SCCs and TIA are well covered. |

### Notes

The output is strong overall — it correctly structures the lawful basis blocking decision, provides a detailed risk table with explicit likelihood/impact ratings, addresses data minimisation across all four sources, covers cross-border transfer with SCCs and TIA, recommends the DPIA with the `/grc-lead:write-dpia` handoff, and cleanly separates GRC from engineering responsibilities. The two FAIL criteria both relate to the same gap: the Australian Privacy Principles (APPs / Privacy Act 1988) are mentioned only in passing ('potentially the Australian Privacy Act') without formal naming, and the UK GDPR + Data Protection Act 2018 post-Brexit divergence is not called out. For a B2B product with Australian customers, this is a meaningful gap — the APPs have distinct obligations around sensitive information, cross-border disclosure, and privacy policy requirements that differ from GDPR. The output also does not explicitly address retention limits as part of the compliant path (c15 notes this gap), though it does cover most other elements. Despite these gaps, the response is substantively correct and actionable on the major GDPR obligations.
