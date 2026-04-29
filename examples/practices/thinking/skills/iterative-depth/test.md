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

## Output expectations

- [ ] PASS: Output's problem framing reproduces the prompt's specific facts — 8,000 lines, 3 engineers in 6 months, 40% of incidents originate here, weekly monolith deploys, three channels (email/push/SMS) — and ties them to the decision
- [ ] PASS: Output selects 3-5 lenses and names them — e.g. Technical (extraction cost vs benefit), Operational (deploy independence, blast radius), Team (cognitive load, expertise), Business (incident reduction value), User (delivery reliability) — and explains why each was chosen for THIS decision
- [ ] PASS: Output's lens selection includes at least one human lens (Team or Business or User) AND one system lens (Technical or Operational or Edge case) per the skill's selection rules
- [ ] PASS: Output addresses the 40% incident origination directly — does extracting the service reduce the blast radius (yes — incidents stay isolated to notifications) or just shift the failure surface (now needs reliable inter-service comms)
- [ ] PASS: Output's lens analyses produce DIFFERENT findings — the technical lens surfaces e.g. "service extraction cost ~3 engineer-months", the operational lens surfaces "deploy frequency could go from weekly to daily for notifications", the team lens surfaces "ownership clarification" — not all converging on the same point
- [ ] PASS: Output's contradiction-surfacing step calls out tensions between lenses explicitly — e.g. "the team lens favours extraction (clear ownership), the operational lens cautions extraction (operational complexity for the same 3 engineers)"
- [ ] PASS: Output's synthesis produces a convergent findings table (where lenses agree), a tensions table (where lenses disagree, with proposed resolution path), and a clear recommendation
- [ ] PASS: Output's recommendation considers the alternative of fixing-in-place — extracting is one option, addressing the 40% incident root causes within the monolith is another, and the synthesis weighs both rather than only debating extraction
- [ ] PASS: Output's revised problem framing differs from the Step 1 framing — e.g. shifts from "should we extract?" to "what's driving the 40% incidents, and is extraction the leverage point?"
- [ ] PARTIAL: Output's confidence level is stated with the evidence basis — e.g. "MEDIUM confidence; would rise to HIGH if we had a 2-week incident root-cause analysis showing they're notifications-internal vs HIGH if they're integration boundaries"
