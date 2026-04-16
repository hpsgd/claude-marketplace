# Test: iterative-depth architecture decision analysis

Scenario: A team is deciding whether to extract their monolith's notification subsystem into a separate microservice. The iterative-depth skill is used to examine the decision from multiple angles.

## Prompt

/iterative-depth Should we extract the notification subsystem from our Rails monolith into a separate service? It currently handles email, push, and SMS. It has 8,000 lines, 3 engineers have touched it in the past 6 months, and it's the source of 40% of our production incidents. It handles email, push, and SMS. We deploy the whole monolith weekly.

## Criteria

- [ ] PASS: Step 1 produces a complete problem framing with problem statement, context, constraints, stakeholders, current state, and desired state
- [ ] PASS: Step 2 selects 3-5 lenses from the eight available and states which were chosen and why
- [ ] PASS: Lens selection includes at least one human lens (User or Business) and one system lens (Technical or Edge case) per the skill's selection rules
- [ ] PASS: Each lens analysis produces at least one finding not surfaced by any previous lens — not just restating earlier observations
- [ ] PASS: Contradictions between lenses are explicitly called out — not smoothed over
- [ ] PASS: Step 4 synthesis produces a convergent findings table, a tensions table with recommended resolutions, and a clear recommendation
- [ ] PASS: Revised problem framing at the end of Step 4 differs from the Step 1 framing in a meaningful way
- [ ] PARTIAL: Confidence level for the recommendation is stated with the evidence basis (not just "Medium confidence" but what data would raise or lower it)
