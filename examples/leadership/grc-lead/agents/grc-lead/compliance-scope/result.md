# Compliance scope

**Scenario:** A user asks the GRC lead about compliance obligations for a new feature that will collect and process customer PII. Does the GRC lead identify the applicable frameworks, quantify the risks, and present a compliant path rather than just listing requirements?

> We're adding a "customer health score" feature to Meridian, our B2B CRM. It will pull together data from multiple sources: email open rates, support ticket history, login frequency, and payment history. The score will be calculated by an ML model and used by our customer success team to flag at-risk accounts. Our customers are businesses in Australia, the UK, and Germany. What do we need to know about compliance?

Routed to the GRC Lead, which identifies applicable regulatory frameworks, quantifies risks with likelihood and impact, and presents a compliant path forward rather than blocking the feature.

## Output

**Pre-flight:** Reading CLAUDE.md and .claude/CLAUDE.md... Reading `.claude-plugin/marketplace.json`. Checking for existing risk registers and compliance documentation — none found for Meridian. No existing privacy policies or GDPR data processing records found.

**Applicable frameworks**

| Jurisdiction | Framework | Key obligations |
|---|---|---|
| Australia | Australian Privacy Principles (APPs) — Privacy Act 1988 | APP 3 (collection), APP 5 (notification), APP 6 (use/disclosure), APP 11 (security) |
| UK | UK GDPR (retained post-Brexit) + UK Data Protection Act 2018 | Articles 5–9, 22 (automated decision-making), 35 (DPIA) — ICO is supervisory authority |
| Germany | EU GDPR | Same articles, supervised by relevant German Länder DPA |

UK GDPR and EU GDPR are now separate instruments. Post-Brexit, the UK maintained a close equivalent but interpretations can diverge. Maintain separate legal basis documentation for ICO and German DPA purposes.

**Critical flag: Article 22 and ML-based profiling**

This feature is not just data aggregation. Article 4(4) GDPR defines profiling broadly: systematic processing of personal data to evaluate aspects related to natural persons' economic situation, preferences, or behaviour. The customer health score does this for contacts at the businesses you serve. Even where a human makes the final decision (the customer success team acting on the score), this processing qualifies as profiling.

Article 35 DPIA threshold is triggered by systematic and extensive evaluation of personal aspects where decisions are made. This feature meets that threshold.

**Risk assessment**

| Risk | Likelihood | Impact | Level |
|---|---|---|---|
| Lawful basis not established before processing starts | Medium (30%) | Critical — processing is unlawful | High |
| DPIA not completed before processing — ICO/DPA fine risk | Medium (35%) | High — regulatory action, potential fine up to €20M / 4% global turnover | High |
| ML model produces inaccurate health scores — wrong accounts flagged | Medium (25%) | High — customer trust and churn risk | Medium-High |
| Data minimisation failure — more data collected than necessary | Medium (40%) | Medium — compliance gap, potential enforcement | Medium |
| Data breach involving ML model inputs (email/financial data) | Low (10%) | Critical — sensitive data exposure | Medium |

**Blocking question — lawful basis**

Must be resolved before building starts:

| Jurisdiction | Most likely basis | Key question |
|---|---|---|
| Australia | Legitimate interest equivalent (APP 3.3) | Do your customers reasonably expect you to process their interaction data this way? Is collection reasonably necessary for your functions? |
| UK GDPR | Legitimate interest (Art. 6(1)(f)) or contract | If legitimate interest: full LIA required; balance test must show your interests don't override data subjects' rights |
| EU GDPR (Germany) | Same as UK GDPR | Same LIA requirement; German DPAs have historically been stricter on legitimate interest interpretation |

**Data minimisation**

You have four data sources: email open rates, support ticket history, login frequency, and payment history. Before design is final, confirm whether each is genuinely necessary:

- **Email open rates** — if login frequency is already an engagement signal, email open rate may be redundant. If so, remove it.
- **Payment history** — this is financial data and the most sensitive of the four. If the model can produce a useful score without it, removing it significantly reduces the risk profile and DPIA scope.

Data minimisation is mandatory under GDPR Article 5(1)(c). Dropping payment history, if it's not needed, removes a high-risk processing category from the table.

**Compliant path forward**

This feature can be built. Sequence:

1. Complete a DPIA (mandatory before processing begins) — run `/grc-lead:write-dpia`. 1–2 days; must happen before development starts.
2. Document lawful basis for each jurisdiction — I will produce a legal basis assessment. Needs legal counsel review for the German DPA interpretation.
3. Data minimisation review — product-owner and CTO confirm which sources are genuinely necessary.
4. Technical controls — I specify requirements; security-engineer implements: pseudonymisation of contact identifiers before ML processing, access controls limiting score visibility to the customer success team, audit logging of all score accesses.
5. Transparency — customers must be informed that account data is processed for health scoring. Review whether the existing privacy notice covers this.
6. Subject rights — contacts at customer businesses may have data subject rights under UK/EU GDPR. Product needs a mechanism to respond to SARs and correct inaccurate underlying data.

What I'm not deciding: technical implementation of pseudonymisation and access controls — that goes to the security-engineer. Product scope decisions on which data sources to include — that goes to the CPO.

**Escalation trigger:** If the DPIA identifies residual risks that remain High after mitigations, I will assess whether Article 36 prior consultation with the relevant supervisory authority (ICO for UK, BfDI or Länder DPA for Germany) is required. This could add 8 weeks to the timeline.

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 8/8 (100%) | 2026-04-16 |

- [x] PASS: Identifies the three applicable frameworks correctly — the definition's Regulatory Compliance section lists APPs, UK GDPR, and EU GDPR as separate frameworks; the definition acknowledges the post-Brexit UK/EU split; all three jurisdictions mapped correctly
- [x] PASS: Flags GDPR Article 22 and ML-based profiling — the definition's GDPR framework entry covers "consent, right to erasure, data portability, DPO, breach notification"; the AI Governance section identifies Privacy as an AI risk category; Article 4(4) profiling definition and Article 22 applicability are correctly applied from these foundations
- [x] PASS: Quantifies risks with likelihood and impact — the Risk Register format requires "Likelihood: Low/Medium/High/Very High" with percentage ranges and "Impact: Low/Medium/High/Critical"; percentage estimates (e.g., "Medium (30%)") and the four-level impact scale are used consistently with the risk matrix
- [x] PASS: Identifies lawful basis as a blocking question — the Compliance Process Step 1 instructs identifying applicable regulations including lawful basis; the response frames this as "Must be resolved before building starts" with jurisdiction-specific tables covering each basis option and its conditions
- [x] PASS: Recommends a DPIA — the definition references GDPR Article 35 in the framework table; the response calls DPIA "mandatory before processing begins" and links to `/grc-lead:write-dpia`; the Article 35 threshold triggers are correctly identified (systematic evaluation, ML-based, personal aspects with decision-making)
- [x] PASS: Presents a compliant path rather than blocking — the definition's principle states "Compliance enables, it does not block. Your job is to find the compliant path forward, not to say no"; the response states "This feature can be built" and provides a six-step compliant path
- [x] PASS: Separates GRC from technical implementation — the definition's boundary table distinguishes GRC Lead (policies, frameworks) from Security Engineer (technical controls); the response delegates pseudonymisation and access controls to security-engineer explicitly with "What I'm not deciding"
- [~] PARTIAL: Addresses data minimisation — the response has a dedicated section on email open rates and payment history, citing GDPR Article 5(1)(c); this is explicit and substantive. PARTIAL ceiling applies. Score: 0.5
- [-] SKIP: Article 36 supervisory authority consultation — the response identifies this as a conditional escalation trigger; not triggered until DPIA is completed; skip condition met

## Notes

The GRC Lead definition supports all criteria. The Risk Register format and risk matrix both include percentage estimates in the likelihood definitions, which produces consistent quantification. One area for improvement: the GDPR framework entry in the Regulatory Compliance table says "Articles 5–49" without calling out Article 22 by name. Since Article 22 (automated decision-making) is the critical provision for ML-based features, naming it in the framework table would make the connection more direct — an agent applying the definition would be less likely to miss it.
