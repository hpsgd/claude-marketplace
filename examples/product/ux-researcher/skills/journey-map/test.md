# Test: Journey map

Scenario: Testing whether the journey-map skill requires evidence sources, maps all journey dimensions (actions/thinking/feeling/pain), and identifies critical moments.

## Prompt


/ux-researcher:journey-map for the customer journey from first hearing about Clearpath through to becoming an active daily user — specifically for mid-market operations directors.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria


- [ ] PASS: Skill requires defining a scope with a concrete start trigger and end outcome before mapping begins
- [ ] PASS: Skill requires identifying evidence sources (interviews, analytics, support data) before mapping — not mapping from assumptions
- [ ] PASS: Skill maps all four customer dimensions per stage: actions, thinking, feeling, and pain points
- [ ] PASS: Skill requires touchpoints and channels to be specified for each stage — not just abstract stages
- [ ] PASS: Skill identifies critical moments — stages with the highest emotional intensity or biggest impact on outcome
- [ ] PASS: Skill produces improvement recommendations linked to specific stages or pain points — not generic UX advice
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's scope defines a concrete start trigger ("operations director hears about Clearpath via Google search / peer recommendation / paid ad") and end outcome ("uses Clearpath at least 5 days/week for portfolio reporting") — not abstract beginning / end
- [ ] PASS: Output names evidence sources for the map — sales call recordings, onboarding survey responses, support tickets, churn-interview notes, product analytics — not invented from assumptions
- [ ] PASS: Output maps all four customer dimensions per stage — Actions (what they DO), Thinking (what they're rationally weighing), Feeling (emotional state), Pain Points (frustrations, blockers) — every stage gets all four
- [ ] PASS: Output's touchpoints / channels per stage are specific — e.g. Awareness: Google search, LinkedIn ads, peer recommendations; Trial: signup form, in-product onboarding, sales engineering call — named, not generic "marketing channels"
- [ ] PASS: Output identifies critical moments — stages where emotional intensity is highest or where the journey can fork (e.g. "POC outcome decides purchase" or "first failed integration causes abandonment") — with reasoning
- [ ] PASS: Output's improvement recommendations are linked to specific stages or pain points — not generic UX advice; e.g. "Onboarding stage: integration failures are the #1 friction; build a connector validator" specifically tied to a mapped pain point
