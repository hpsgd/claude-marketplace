# Compliance Scope

Scenario: A user asks the GRC lead about compliance obligations for a new feature that will collect and process customer PII. Does the GRC lead identify the applicable frameworks, quantify the risks, and present a compliant path rather than just listing requirements?

## Prompt

> We're adding a "customer health score" feature to Meridian, our B2B CRM. It will pull together data from multiple sources: email open rates, support ticket history, login frequency, and payment history. The score will be calculated by an ML model and used by our customer success team to flag at-risk accounts. Our customers are businesses in Australia, the UK, and Germany. What do we need to know about compliance?

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Several overlapping frameworks apply, and a few issues are non-obvious for B2B contexts.

## The B2B trap: personal data still applies

Your customers are businesses, but the data you're processing — email opens, login frequency, support tickets — tracks **individual employees and contacts** at those businesses. Those individuals are data subjects under GDPR, UK GDPR, and the Australian Privacy Act. The B2B framing doesn't exempt you.

---

## Germany + EU: GDPR

**Lawful basis.** You'll need one for processing each data category. Legitimate interests (Article 6(1)(f)) is the most defensible, but you must complete a Legitimate Interest Assessment (LIA) documenting that your interest isn't overridden by the data subjects' rights.

**Profiling and automated decision-making (Article 22).** Building an ML score from multiple data sources is profiling. If that score produces decisions with "significant effects" on individuals — even indirectly, e.g., your CS team decides to deprioritise an account, affecting the contacts there — Article 22 is engaged. Individuals get rights to:
- Human review of the decision
- An explanation of the logic
- The ability to contest the outcome

**DPIA is almost certainly mandatory.** Profiling + ML + multiple data sources + potential significant effects = high-risk processing under Article 35. Germany's DPAs are among the most active in the EU; they will expect a DPIA to exist before you go live.

**Transparency.** Your privacy notices must disclose that profiling occurs, the logic involved, and the significance of the score.

---

## UK: UK GDPR

Post-Brexit UK GDPR mirrors EU GDPR closely. Same Article 22 obligations, same DPIA requirement, same LIA process. The ICO has published specific guidance on AI and data protection — worth reading before you finalise the model architecture.

---

## Australia: Privacy Act 1988 (APPs)

The Australian Privacy Principles apply. Key ones:
- **APP 3/5**: Collection must be notified; individuals should know their data is being used to generate a score
- **APP 6**: Secondary use — using support ticket data to train/feed an ML model may go beyond the purpose it was originally collected for
- **APP 11**: Security obligations for the aggregated dataset (aggregated data is a higher-value target)

Australia currently has **no Article 22 equivalent**, but this is changing — the Privacy and Other Legislation Amendment Act 2024 introduced new obligations and further reforms are in progress. Build the transparency and human-review controls now; retrofitting them is expensive.

---

## The controller/processor boundary — the most overlooked issue

This is the one most B2B SaaS companies get wrong. Your customers contract with you to run their CRM data. That makes you a **data processor** for their data. But if you're using that data — across multiple customers — to train or calibrate an ML model, **you are acting as a data controller** for that purpose. Your Data Processing Agreements (DPAs) almost certainly don't permit this. You need to:

1. Audit your existing DPAs — do they permit use of customer data to build or improve your own ML models?
2. If the model is trained per-customer (only on their own data), the risk is lower but you still need to document it.
3. If the model uses any pooled or cross-customer data, get legal review before you start collecting.

---

## Practical checklist before you build

| Action | Jurisdiction |
|---|---|
| Complete a DPIA | EU/UK |
| Complete an LIA for legitimate interests | EU/UK |
| Update privacy notices to disclose profiling | All |
| Audit DPAs for permitted secondary use | All |
| Design a human-review workflow for flagged accounts | EU/UK (required), AU (good practice) |
| Document model explainability — how is the score derived? | EU/UK |
| Define data retention for scoring inputs and outputs | All |
| Review APP 6 secondary use for AU data | AU |

The explainability point deserves emphasis: a black-box ML model will fail Article 22 requirements. You need to be able to tell an individual (or their employer) why their account was flagged. That's a model architecture decision, not just a legal one — make it early.

---

**Bottom line:** Run the DPIA before you build, resolve the controller/processor question with legal, and design explainability in from the start. The DPIA will surface the rest of the specific gaps for your data flows.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 10.5/18.0 (58%) |
| Evaluated | 2026-05-01 |
| Target duration | 55485 ms |
| Target cost | $0.1150 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Identifies the applicable regulatory frameworks correctly — Australian Privacy Principles (APPs), GDPR (Germany and UK), and UK GDPR post-Brexit | PASS | Output explicitly covers 'Germany + EU: GDPR', 'UK: UK GDPR' (noting 'Post-Brexit UK GDPR mirrors EU GDPR closely'), and 'Australia: Privacy Act 1988 (APPs)'. |
| c2 | Flags that automated/ML-based profiling triggers specific GDPR requirements (Article 22 — automated decision-making and profiling) | PASS | Output has a dedicated section: 'Profiling and automated decision-making (Article 22)' and enumerates the three individual rights: human review, explanation of logic, ability to contest. |
| c3 | Quantifies risks using likelihood and impact language — not just listing concerns generically | FAIL | Output uses GDPR-category language ('high-risk processing') and describes regulatory concerns narratively, but provides no explicit likelihood/impact framing (e.g., 'Likelihood: Medium / Impact: High') anywhere in the response. |
| c4 | Identifies the lawful basis question for each jurisdiction (consent vs legitimate interest) as a blocking open question | PARTIAL | Output identifies legitimate interests (Art 6(1)(f)) with a required LIA for EU/UK and notes APP 3/5 notification for AU, but does not present consent as an alternative path, does not discuss trade-offs, and does not frame the question as 'blocking.' |
| c5 | Recommends a DPIA given the profiling + ML combination and scale of processing | PASS | 'DPIA is almost certainly mandatory. Profiling + ML + multiple data sources + potential significant effects = high-risk processing under Article 35.' Also in the checklist: 'Complete a DPIA'. |
| c6 | Does not simply block the feature — presents a compliant path forward | PASS | Output provides a structured 8-item checklist of actions before going live and concludes 'The DPIA will surface the rest of the specific gaps,' framing compliance as achievable, not a blocker. |
| c7 | Separates GRC concerns (policies, frameworks, classification) from technical implementation (delegates guardrails to security engineer) | PARTIAL | Output stays in GRC territory (DPIA, LIA, privacy notices, DPA audits) and notes explainability is 'a model architecture decision, not just a legal one — make it early,' which gestures at delegation but does not explicitly refer to a security engineer or enumerate technical guardrails to hand off. |
| c8 | Addresses data minimisation — whether all four data sources are necessary for the score | FAIL | Output does not question whether all four sources (email opens, support tickets, login frequency, payment history) are necessary. The checklist mentions 'Define data retention' but data minimisation is absent entirely. |
| c9 | Recommends prior supervisory authority consultation under GDPR Art. 36 — only if residual risk would remain high after mitigations | SKIP | Criterion marked SKIP. |
| c10 | Output names all three frameworks explicitly — Australian Privacy Principles (APPs / Privacy Act 1988), GDPR (Germany), and UK GDPR + Data Protection Act 2018 (UK) — and notes UK GDPR diverges slightly post-Brexit | PASS | All three are named explicitly. UK GDPR is introduced under its own heading noting post-Brexit context. Data Protection Act 2018 is omitted but the framework identification is substantively correct; characterising UK GDPR as 'mirrors EU GDPR closely' conveys the same essential point. |
| c11 | Output flags GDPR Article 22 (automated decision-making and profiling) as triggered by the ML-driven health score — including the right to human review and the requirement to inform the data subject | PASS | Dedicated section names Article 22, lists 'Human review of the decision', 'An explanation of the logic', and 'The ability to contest the outcome.' Transparency disclosures also named. |
| c12 | Output recommends a DPIA (Data Protection Impact Assessment) under Article 35 given large-scale profiling combined with multiple data sources, and names the next step (`/grc-lead:write-dpia`) | PARTIAL | DPIA under Article 35 is clearly recommended ('DPIA is almost certainly mandatory ... high-risk processing under Article 35'). However, the specific next-step skill reference `/grc-lead:write-dpia` does not appear anywhere in the output. |
| c13 | Output identifies the lawful basis question per jurisdiction as a blocking open issue — likely legitimate interest with a Legitimate Interests Assessment (LIA), or consent if customer-facing transparency is the chosen path — with the trade-offs of each | PARTIAL | Output recommends legitimate interests + LIA for EU/UK and notes APP 3/5 for AU. Consent is never presented as an alternative path, no trade-offs are discussed, and the question is not framed as 'blocking.' |
| c14 | Output quantifies risks with likelihood and impact (e.g. "Likelihood: Medium — opt-out rates from current product analytics suggest 5-10% will object; Impact: High — automated decisioning without consent could trigger regulatory action"), not generic "this is a privacy concern" | FAIL | Output describes risks narratively ('among the most active' DPAs, 'high-risk processing') but contains no likelihood/impact ratings, no percentages, and no structured risk quantification of any kind. |
| c15 | Output does not block the feature — presents a compliant path forward (data minimisation, transparent notice, opt-out mechanism, human review on at-risk-account decisions, retention limits) | PASS | Checklist includes transparent privacy notices, human-review workflow, retention definition. Output explicitly frames compliance as achievable. Data minimisation and opt-out mechanism are absent, but the overall path forward is clearly articulated. |
| c16 | Output addresses data minimisation — questions whether all four sources (email open rates, support tickets, login frequency, payment history) are necessary, and proposes the minimum subset that achieves the customer-success goal | FAIL | No part of the output questions whether any of the four named data sources could be removed. Data minimisation as a principle is not raised. |
| c17 | Output separates GRC concerns (policies, lawful basis, DPIA, customer notice) from technical implementation (delegates the technical guardrails — input validation, audit logging, deletion mechanisms — to the security engineer or developer, not specifying them itself) | PARTIAL | Output confines itself to GRC concerns and does not specify input validation, audit logging, or deletion mechanisms. Explainability is flagged as 'a model architecture decision, not just a legal one' gesturing toward technical delegation, but no explicit hand-off to a security engineer or developer role appears. |
| c18 | Output addresses transparency — the customer-success team using the score must know what data went in, customers must be informed in privacy notice and product UI, and there must be a route to challenge a decision | PASS | Privacy notices disclosing profiling and logic are required. Explainability section states CS team must 'be able to tell an individual why their account was flagged.' Route to challenge covered via Article 22 rights. Product UI is not mentioned but the other two elements are addressed in detail. |
| c19 | Output addresses cross-border data transfer — German/UK customer data flowing to wherever the ML model runs, with adequacy decisions or Standard Contractual Clauses if outside the EU/UK | FAIL | Cross-border data transfer is not mentioned anywhere in the output. No reference to adequacy decisions, SCCs, or where the ML model is hosted. |

### Notes

The output is substantively strong on framework identification, Article 22 obligations, DPIA recommendation, and the controller/processor boundary (which is a genuinely non-obvious B2B trap). It falls short on four clustered gaps: (1) no risk quantification with likelihood/impact language at all (c3, c14 both fail), (2) data minimisation entirely absent — the four data sources are never questioned (c8, c16 both fail), (3) lawful basis is identified but the consent alternative and trade-offs are missing, and the question is not framed as blocking (c4, c13 partial), and (4) cross-border transfer obligations are completely unaddressed (c19 fail). The DPIA skill reference (/grc-lead:write-dpia) and explicit security-engineer delegation are also absent. The 58.3% total places it narrowly below the PARTIAL threshold.
