# Test: Model evaluation for support ticket classification

Scenario: Developer invokes the model-evaluation skill to select a model for classifying incoming support tickets into categories (billing, technical, account, feature request) with a target accuracy of 90%+ and a cost budget of $0.005 per request.

## Prompt

Evaluate models for support ticket classification. We receive ~1,500 tickets/day. Each ticket is 50-500 words. We need to classify into: billing, technical, account, feature-request. Requirements: >= 90% accuracy, p95 latency < 2s, cost < $0.005/request (~$225/month at volume), context window of at least 1K tokens is fine.

## Criteria

- [ ] PASS: Skill defines hard pass/fail requirements before evaluating any model — quality threshold, latency budget, cost budget, context window, reliability, and safety refusal rate
- [ ] PASS: Skill recommends an eval set of at least 50 examples covering happy path (60%), edge cases (25%), and adversarial inputs (15%)
- [ ] PASS: Skill identifies Fast-tier (Haiku-class) models as candidates given the mechanical classification task — does not default to Capable-tier
- [ ] PASS: Skill specifies temperature 0 for deterministic classification and running at least 3 passes to measure consistency
- [ ] PASS: Skill produces a side-by-side comparison table with all six dimensions: quality, latency, cost, reliability, context window, safety
- [ ] PASS: Skill includes a mandatory fallback plan covering model unavailability, cost spike, and quality degradation scenarios
- [ ] PASS: Skill documents trade-offs accepted by the selected model — not just which model was chosen
- [ ] PARTIAL: Skill recommends scheduling a re-evaluation (quarterly or on trigger conditions) — not a one-time evaluation
- [ ] PASS: Output follows the full model evaluation format: requirements, candidates, eval dataset, results per model, comparison, decision, fallback plan
