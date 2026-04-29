# Test: Launch plan

Scenario: Testing whether the launch-plan skill determines a launch tier, produces a structured rollout strategy, and requires a post-launch review plan with success metrics.

## Prompt


/gtm:launch-plan for our mobile app — we're releasing native iOS and Android apps after 3 years of web-only. This is a significant milestone for us and for our customers who've been requesting it.

## Criteria


- [ ] PASS: Skill determines a launch tier before planning — a 3-year milestone mobile launch is not a silent rollout, and the tier determines resource allocation and communication scope
- [ ] PASS: Skill produces a pre-launch checklist — internal readiness, support preparation, documentation — not just external marketing
- [ ] PASS: Skill produces a rollout strategy — phased or full launch, criteria for advancing phases
- [ ] PASS: Skill requires a post-launch review plan with defined success metrics and a review date
- [ ] PASS: Skill includes a communication plan — who is told what, when, and through which channel
- [ ] PASS: All marketing copy and messaging is labelled DRAFT and flagged for human review
- [ ] PARTIAL: Skill includes a launch day checklist — specific actions on the day of release — partial credit if launch day is covered in the rollout strategy but not as a separate checklist
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output classifies this as Tier 1 (or equivalent top tier) launch — a 3-year-anticipated milestone with both iOS and Android, a customer-requested feature, and significant brand-level signal — explicitly rationalised
- [ ] PASS: Output's pre-launch checklist covers all four readiness streams — internal (engineering sign-off, beta complete, crash rate target met), support (mobile-specific runbooks, FAQs, ticket categories), documentation (mobile-specific user guides, app store listings), and marketing
- [ ] PASS: Output's rollout strategy is phased — e.g. "Week 1: TestFlight / Play internal track to 100 beta users; Week 2: 5% rollout via staged release; Week 3: 25%; Week 4: 100%" — with criteria to advance per phase (crash rate < X, App Store rating > Y, no Sev-1 issues)
- [ ] PASS: Output addresses both platforms separately — iOS (TestFlight, App Store review timing, App Store optimisation) and Android (internal testing track, staged rollout %, Play Store listing) — with platform-specific timing
- [ ] PASS: Output's post-launch review has defined success metrics — installs, MAU on mobile, % web users now also on mobile, crash-free rate, App Store rating ≥4.5 — and a review schedule (Day 7, Day 30, Day 90)
- [ ] PASS: Output's communication plan names audiences (existing customers, prospects, internal teams, support, sales, press) with timing and channel per audience — e.g. "existing customers: in-product banner + email Day 0; press: embargoed announcement Day -1"
- [ ] PASS: Output's launch day checklist has specific actions with timing — e.g. "T-1h: confirm app store listings live; T-0: send customer email; T+1h: monitor crash rate; T+4h: first social post"
- [ ] PASS: Output's marketing copy and announcement examples are labelled DRAFT — not approved final copy — with a flag for human review
- [ ] PASS: Output addresses rollback / kill-switch — what happens if a critical bug surfaces post-launch (Apple's expedited review process, Play Store percentage rollback, server-side feature flag)
- [ ] PARTIAL: Output addresses App Store / Play Store optimisation as part of pre-launch — keywords, screenshots, description, demo video — these affect organic discovery and rating
