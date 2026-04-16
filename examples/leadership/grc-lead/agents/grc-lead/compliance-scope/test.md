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
