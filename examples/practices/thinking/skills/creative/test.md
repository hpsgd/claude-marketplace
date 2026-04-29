# Test: creative onboarding flow ideation

Scenario: A product team wants fresh ideas for reducing drop-off during user onboarding. They're stuck on a linear wizard approach and want genuinely different alternatives.

## Prompt

/creative We're losing 60% of new users before they complete our 7-step onboarding wizard for Nexus, our project management tool. The current flow is: account setup → invite team → create first project → add tasks → connect integrations → set notifications → take a tour. Most users drop off at step 3. What are some genuinely different approaches?

## Criteria

- [ ] PASS: Step 1 analyses the problem before generating ideas — identifies who has the problem, consequences, and constraints
- [ ] PASS: Step 2 produces all three reframes (user story, constraint, analogy) and states which was selected for ideation and why
- [ ] PASS: Step 3 applies all five mandatory diversity techniques (inversion, extreme scale, remove constraints, cross-domain transfer, worst idea first) producing at least one option from each
- [ ] PASS: At least 5 options pass all three quality tests — distinct, feasible, and specific enough to act on
- [ ] PASS: Step 4 evaluates each option with genuine pros, biggest risk, effort estimate, and reversibility
- [ ] PASS: A wild card option is included in the output — unconventional but argued seriously
- [ ] PASS: Recommended path specifies what to do first as a concrete immediate action
- [ ] PARTIAL: Options named with descriptive memorable names (not "Option 1", "Option 2")

## Output expectations

- [ ] PASS: Output addresses step 3 (create first project) explicitly as the dropoff hotspot — at least 2 of the generated options target reducing friction at that specific step, not generic onboarding ideas
- [ ] PASS: Output's inversion option flips the wizard premise (e.g. "no onboarding wizard at all — drop the user into a sample project pre-populated with their email contacts") rather than a slight tweak
- [ ] PASS: Output's extreme-scale option imagines onboarding for 10x or 0.1x users (e.g. "1,000 simultaneous account-creators in a workshop" or "single user, no team yet") and surfaces a different design implication
- [ ] PASS: Output's remove-constraints option drops one of the 7 steps as non-essential (e.g. "skip integrations and notifications for week 1, prompt later in-app") with reasoning
- [ ] PASS: Output's cross-domain transfer option borrows a pattern from outside SaaS onboarding — e.g. how Duolingo's progressive disclosure works, how IKEA furniture instructions order steps, how a Mario tutorial level introduces mechanics
- [ ] PASS: Output's worst-idea option is genuinely bad (e.g. "force users to invite 5 colleagues before they can do anything") and explains what the failure mode reveals — not a softened "it could work in some scenarios"
- [ ] PASS: Output produces at least 5 distinct, feasible, specific options — each has a memorable name (not "Option 1, 2, 3"), a specific mechanism, a primary risk, and an effort estimate
- [ ] PASS: Output's wild-card option is non-obvious but argued seriously — e.g. "make onboarding optional, run a Loom walkthrough instead of a wizard" — not a joke entry
- [ ] PASS: Output's recommended path names a concrete first action — "ship the sample-project-on-signup version as a 1-week experiment, measure step-3 completion against control" — not "consider trying X"
- [ ] PARTIAL: Output addresses the 60% dropoff with a hypothesis about WHY users abandon at step 3 — is creating-a-project blocked by team-not-set-up-yet, or is it the cognitive load of a real first project — and matches options to that hypothesis
