# Test: compliance scope

Scenario: A user asks the GRC lead about compliance obligations for a new feature that will collect and process customer PII. Does the GRC lead identify the applicable frameworks, quantify the risks, and present a compliant path rather than just listing requirements?

## Prompt

We're adding a "customer health score" feature to Meridian, our B2B CRM. It will pull together data from multiple sources: email open rates, support ticket history, login frequency, and payment history. The score will be calculated by an ML model and used by our customer success team to flag at-risk accounts. Our customers are businesses in Australia, the UK, and Germany. What do we need to know about compliance?

## Criteria

- [ ] PASS: Identifies the applicable regulatory frameworks correctly — Australian Privacy Principles (APPs), GDPR (Germany and UK), and UK GDPR post-Brexit
- [ ] PASS: Flags that automated/ML-based profiling triggers specific GDPR requirements (Article 22 — automated decision-making and profiling)
- [ ] PASS: Quantifies risks using likelihood and impact language — not just listing concerns generically
- [ ] PASS: Identifies the lawful basis question for each jurisdiction (consent vs legitimate interest) as a blocking open question
- [ ] PASS: Recommends a DPIA given the profiling + ML combination and scale of processing
- [ ] PASS: Does not simply block the feature — presents a compliant path forward
- [ ] PASS: Separates GRC concerns (policies, frameworks, classification) from technical implementation (delegates guardrails to security engineer)
- [ ] PARTIAL: Addresses data minimisation — whether all four data sources are necessary for the score
- [ ] SKIP: Recommends prior supervisory authority consultation under GDPR Art. 36 — only if residual risk would remain high after mitigations

## Output expectations

- [ ] PASS: Output names all three frameworks explicitly — Australian Privacy Principles (APPs / Privacy Act 1988), GDPR (Germany), and UK GDPR + Data Protection Act 2018 (UK) — and notes UK GDPR diverges slightly post-Brexit
- [ ] PASS: Output flags GDPR Article 22 (automated decision-making and profiling) as triggered by the ML-driven health score — including the right to human review and the requirement to inform the data subject
- [ ] PASS: Output recommends a DPIA (Data Protection Impact Assessment) under Article 35 given large-scale profiling combined with multiple data sources, and names the next step (`/grc-lead:write-dpia`)
- [ ] PASS: Output identifies the lawful basis question per jurisdiction as a blocking open issue — likely legitimate interest with a Legitimate Interests Assessment (LIA), or consent if customer-facing transparency is the chosen path — with the trade-offs of each
- [ ] PASS: Output quantifies risks with likelihood and impact (e.g. "Likelihood: Medium — opt-out rates from current product analytics suggest 5-10% will object; Impact: High — automated decisioning without consent could trigger regulatory action"), not generic "this is a privacy concern"
- [ ] PASS: Output does not block the feature — presents a compliant path forward (data minimisation, transparent notice, opt-out mechanism, human review on at-risk-account decisions, retention limits)
- [ ] PASS: Output addresses data minimisation — questions whether all four sources (email open rates, support tickets, login frequency, payment history) are necessary, and proposes the minimum subset that achieves the customer-success goal
- [ ] PASS: Output separates GRC concerns (policies, lawful basis, DPIA, customer notice) from technical implementation (delegates the technical guardrails — input validation, audit logging, deletion mechanisms — to the security engineer or developer, not specifying them itself)
- [ ] PASS: Output addresses transparency — the customer-success team using the score must know what data went in, customers must be informed in privacy notice and product UI, and there must be a route to challenge a decision
- [ ] PARTIAL: Output addresses cross-border data transfer — German/UK customer data flowing to wherever the ML model runs, with adequacy decisions or Standard Contractual Clauses if outside the EU/UK
