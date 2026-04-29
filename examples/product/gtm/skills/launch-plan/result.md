# Output: Launch plan

**Verdict:** PARTIAL
**Score:** 13.5/18 criteria met (75%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill determines a launch tier before planning — Step 1 is an explicit tier classification table with Tier 1 defined as "New product, major platform" type launches; a 3-year milestone mobile launch unambiguously maps to Tier 1 — met
- [x] PASS: Skill produces a pre-launch checklist — covers internal readiness (technical readiness), support preparation, and documentation sections — met
- [x] PASS: Skill produces a rollout strategy — Step 3 documents rollout strategies with percentage-based and phased options, with a template including kill switch and rollback trigger — met
- [x] PASS: Skill requires a post-launch review plan with defined success metrics and a review date — Step 6 includes a 7-day review template with metrics table; Step 7 mandates a post-launch review template with scheduled date in the output — met
- [x] PASS: Skill includes a communication plan — Step 5 is a full communication plan table covering internal team, support, users, social, partners, and press/analysts — met
- [x] PASS: All marketing copy and messaging is labelled DRAFT and flagged for human review — the Rules section states "All output is DRAFT until human-reviewed. Label every output with 'DRAFT — requires human review' at the top and bottom." — met
- [x] PARTIAL: Skill includes a launch day checklist — Step 4 is an explicit launch day run-of-show with morning/launch/afternoon sequence as a dedicated separate section — fully met, scoring 1.0 rather than 0.5 as the criterion is completely satisfied
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — frontmatter contains name, description, argument-hint, user-invocable, and allowed-tools — met

### Output expectations

- [x] PASS: Output classifies this as Tier 1 — the skill's Step 1 tier table maps "new product" and major milestones to Tier 1; the 3-year mobile launch with both platforms unambiguously triggers Tier 1 with rationale produced in the output template — met
- [ ] FAIL: Output's pre-launch checklist covers all four readiness streams — the skill covers support readiness, documentation, and marketing, but is missing mobile-specific engineering readiness items: no mention of beta completion, crash rate targets, engineering sign-off, or app store listing preparation as a distinct stream — not found
- [ ] FAIL: Output's rollout strategy is phased with specific mobile-platform cadences — the skill provides a generic percentage rollout template but does not address mobile-specific phasing (TestFlight, Play internal track, staged release percentages, App Store review timing) — not found
- [ ] FAIL: Output addresses both platforms separately — iOS and Android are not addressed as distinct deployment paths anywhere in the skill; it is platform-agnostic and would not produce iOS/Android split planning — not found
- [~] PARTIAL: Output's post-launch review has defined success metrics and review schedule — the metrics table template exists (Step 6) with Day 7 review, but no Day 30/Day 90 schedule, and metric examples are generic rather than mobile-specific (installs, MAU on mobile, crash-free rate, App Store rating ≥4.5) — partially met
- [x] PASS: Output's communication plan names audiences with timing and channel per audience — Step 5 table has audience, channel, when, and message columns covering all named groups including press with embargo note — met
- [x] PASS: Output's launch day checklist has specific actions with timing — Step 4 is structured as morning/launch/afternoon with specific action items in sequence — met
- [x] PASS: Output's marketing copy and announcement examples are labelled DRAFT — the Rules section mandates this explicitly for all output — met
- [x] PASS: Output addresses rollback / kill-switch — technical readiness checklist includes "Feature flags configured" and "Rollback procedure documented"; the rollout template explicitly requires "Kill switch" and "Rollback trigger" fields — met
- [ ] FAIL: Output addresses App Store / Play Store optimisation as pre-launch — no mention of App Store/Play Store optimisation (keywords, screenshots, description, demo video, ASO) anywhere in the skill — not found

## Notes

The skill is a well-constructed generic launch framework. The structural criteria are all met cleanly — tier classification, checklist sections, rollout template, communication plan, and DRAFT labelling are solid.

The four failures are concentrated in the output expectations and share a single root cause: the skill is platform-agnostic. Given a mobile launch scenario, it would produce a capable Tier 1 plan but would not naturally generate iOS/Android split treatment, TestFlight/Play staged rollout cadences, app store optimisation tasks, or mobile-specific success metrics. A skill that detects platform context from $ARGUMENTS (e.g., recognising "iOS and Android" as a mobile launch) and adapts its checklist accordingly would close most of these gaps.

The Day 7 post-launch review is the only scheduled milestone. Day 30 and Day 90 cadences from the output expectations are absent from the skill definition.
