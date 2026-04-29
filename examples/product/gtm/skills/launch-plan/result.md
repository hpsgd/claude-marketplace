# Output: Launch plan

**Verdict:** PASS
**Score:** 13/13 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill determines a launch tier before planning — Step 1 is an explicit tier classification table (Major/Standard/Minor) that gates checklist scope; a 3-year milestone mobile launch unambiguously maps to Tier 1
- [x] PASS: Skill produces a pre-launch checklist — Step 2 covers internal readiness (technical readiness section), support preparation, and documentation (all tiers)
- [x] PASS: Skill produces a rollout strategy — Step 3 lists five rollout strategies with risk levels and a documented plan template including kill switch and rollback trigger
- [x] PASS: Skill requires a post-launch review plan with defined success metrics and a review date — Step 6 is a 7-day review with a metrics table (baseline, Day 1, Day 3, Day 7, target) and Step 7 mandates a scheduled date in every output
- [x] PASS: Skill includes a communication plan — Step 5 table maps six audiences (internal team, support, existing users, social, partners, press/analysts) to channel, timing, and message
- [x] PASS: All marketing copy and messaging is labelled DRAFT and flagged for human review — Rules section states "All output is DRAFT until human-reviewed. Label every output with 'DRAFT — requires human review' at the top and bottom."
- [x] PASS: Skill includes a launch day checklist — Step 4 is a dedicated launch day run-of-show with morning/launch/afternoon sequences as its own section, not folded into the rollout strategy
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — frontmatter at lines 2-6 contains all three required fields

### Output expectations

- [x] PASS: Output classifies this as Tier 1 with explicit rationale — Tier 1 maps to "New product, major feature"; the output format template mandates "Launch Tier: [1/2/3] — [rationale]", so the rationale is structural, not optional
- [x] PASS: Output's communication plan names audiences with timing and channel per audience — Step 5 table includes existing users (email, launch time), press (email, pre-launch embargo), internal (Slack, pre-launch morning), support (briefing, 1 week pre-launch), social followers, and partners
- [x] PASS: Output's launch day checklist has specific actions with timing — Step 4 structures actions by morning/launch/afternoon time blocks with a run-of-show table in the output format
- [x] PASS: Output's marketing copy and announcement examples are labelled DRAFT — the Rules section explicitly mandates "DRAFT — requires human review" labelling; applies to all output including copy examples
- [x] PASS: Output addresses rollback / kill-switch — Step 2 technical readiness requires "Rollback procedure documented"; Step 3 rollout template has explicit "Kill switch: [feature flag name]" and "Rollback trigger: [specific condition]" fields

## Notes

The skill is a well-constructed generic launch framework that meets all current criteria cleanly. Tier classification, pre-launch checklists, rollout template, communication plan, launch day run-of-show, DRAFT labelling, and rollback/kill-switch coverage are all present and substantive.

One observation: the launch day run-of-show uses time blocks (morning/launch/afternoon) rather than explicit T-relative timing (T-1h, T+1h). The output format table shows `[HH:MM]` placeholders, which is close to what the criterion describes. This is a presentation style difference rather than a structural gap.

The skill is platform-agnostic — it would not naturally produce iOS/Android split treatment or App Store-specific pre-launch tasks for a mobile launch. Those gaps are not tested by the current criteria but would be worth noting for a future revision.
