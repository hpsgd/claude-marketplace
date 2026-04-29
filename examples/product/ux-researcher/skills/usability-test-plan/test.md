# Test: Usability test plan

Scenario: Testing whether the usability-test-plan skill requires defined research questions, participant criteria, task scenarios, and success metrics — not just a list of questions to ask.

## Prompt


/ux-researcher:usability-test-plan for testing our new onboarding flow before we ship it — we want to know if new users can get to their first project within 10 minutes without help.

## Criteria


- [ ] PASS: Skill requires specific research questions (what will we learn?) before methodology selection — not "we'll run usability tests and see what happens"
- [ ] PASS: Skill requires participant screener criteria — who qualifies to participate, who should be excluded
- [ ] PASS: Skill requires task scenarios written from the user's perspective, not the product's perspective (e.g. "You've just joined a new company..." not "Navigate to onboarding")
- [ ] PASS: Skill requires success metrics defined per task — completion rate, time-on-task, or error rate — not just "did they complete it"
- [ ] PASS: Skill includes a moderator guide with specific prompts and a policy on when to intervene
- [ ] PASS: Skill specifies the number of participants with a rationale — not an arbitrary number
- [ ] PARTIAL: Skill covers logistics — session duration, recording consent, tools — partial credit if logistics are mentioned but not all required elements are present
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's research questions are specific and testable — e.g. "Can a new user reach 'first project created' in under 10 minutes without help?" "Where in the flow do users hesitate longest?" — not "are users happy with the onboarding"
- [ ] PASS: Output's success metric ties to the prompt's threshold — completion rate of "reaches first project within 10 minutes" with a target (e.g. 80% of participants), plus time-on-task percentiles, and a per-step error rate
- [ ] PASS: Output's task scenarios are written from the user's perspective — "You've just signed up for Clearpath as a project manager at a consulting firm. Your goal is to set up your first client project so you can show your team status updates by tomorrow's standup." — NOT "Click on the onboarding wizard and complete each step"
- [ ] PASS: Output's participant criteria specify who qualifies — e.g. "Project managers or team leads at consulting / agency / professional services companies, 5-50 employee company, never used Clearpath before" — and exclusions (existing customers, internal employees, friends-of-the-team)
- [ ] PASS: Output specifies 5-8 participants per round (or equivalent qualitative number) with reasoning — Nielsen's "5 users find 80% of usability issues" cited or equivalent — not arbitrary
- [ ] PASS: Output's moderator guide names specific prompts — "What were you expecting to happen there?" "Tell me what's going through your head right now." — and a clear non-intervention policy ("don't help unless they're stuck for >2 minutes")
- [ ] PASS: Output's logistics cover session duration (typically 45-60 min), recording consent (signed before session, GDPR-aware), and tools (e.g. Maze for unmoderated, Lookback / Zoom for moderated)
- [ ] PASS: Output's timeline includes recruitment lead time (typically 1-2 weeks), session scheduling, conducting sessions (1-2/day), and synthesis (1-2 days)
- [ ] PASS: Output's pilot session is recommended before live participants — running 1 internal pilot to debug the test setup, task wording, and timing
- [ ] PARTIAL: Output addresses incentive — typical $50-100 USD equivalent per participant for a 60-min session, with the budget implication flagged for the requester
