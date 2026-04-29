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

## Output expectations

- [ ] PASS: Output's requirements table reproduces all four numeric thresholds from the prompt — >=90% accuracy, p95 < 2s latency, < $0.005/request, ~$225/month at 1,500/day volume — with no rounding or omission
- [ ] PASS: Output names at least 2 specific Fast-tier or low-cost candidate models (e.g. Claude Haiku, GPT-4o-mini, Gemini Flash) by name with provider, not abstract tier labels
- [ ] PASS: Output's eval dataset section specifies 50+ examples with the 60/25/15 happy/edge/adversarial split and describes what edge cases look like for ticket classification (multi-category tickets, very short tickets, non-English content, mislabelled prior categories)
- [ ] PASS: Output's per-model results table reports actual or projected numbers for all six dimensions (quality, latency, cost, reliability, context, safety) — not just quality and cost
- [ ] PASS: Output's cost calculation shows the math: input tokens × input price + output tokens × output price, multiplied by 1,500/day, landing under $225/month
- [ ] PASS: Output's comparison table includes a "All requirements met?" YES/NO row per candidate and selects the cheapest passing candidate (not the highest-quality)
- [ ] PASS: Output's fallback plan covers all four mandated scenarios — primary unavailable, latency degradation, cost spike, quality degradation — with a named fallback model, not generic "switch model" text
- [ ] PASS: Output specifies a re-evaluation schedule (e.g. quarterly) and trigger conditions (provider model deprecation, accuracy drift detected, volume change) — not a one-time evaluation
- [ ] PARTIAL: Output addresses class imbalance — billing/technical/account/feature-request likely don't appear at equal rates, and accuracy alone can hide poor performance on minority classes; per-class precision/recall or F1 should appear
