# Test: Write onboarding

Scenario: Testing whether the write-onboarding skill defines a value path before writing content, includes an "aha moment" confirmation step, and measures progress toward first value.

## Prompt


/user-docs-writer:write-onboarding for new Clearpath users — the in-product onboarding experience that takes someone from account creation to completing their first project milestone.

A few specifics for the response:

- Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
- Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
- For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
- When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
- Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Criteria


- [ ] PASS: Skill requires defining the value path first — the minimum steps to reach first value — before writing any content
- [ ] PASS: Skill requires an "aha moment" step that explicitly confirms the user has reached first value — not just "completed setup"
- [ ] PASS: Skill requires a welcome step that contextualises what the user will achieve, not just a greeting
- [ ] PASS: Each onboarding step includes the benefit to the user, not just the instruction — why this step matters
- [ ] PASS: Skill requires progress indicators so users know how far they are through onboarding
- [ ] PARTIAL: Skill addresses what happens if a user skips or abandons onboarding mid-flow — partial credit if this is mentioned but not required as a design consideration
- [ ] PASS: Skill uses plain language only — no technical terms or internal product jargon
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output defines the value path explicitly — the minimum sequence from sign-up to first project milestone — naming each step and why it leads to value, BEFORE writing any UI copy or interaction details
- [ ] PASS: Output's welcome step contextualises what the user will achieve — "In the next 5 minutes you'll set up your first project and complete your first milestone, so you can see how Clearpath tracks status across your work"
- [ ] PASS: Output's per-step copy includes the BENEFIT — e.g. "Add your first task — this is what you'll mark complete to see your milestone update"; not just "click here to add a task"
- [ ] PASS: Output's progress indicator is named and specified — e.g. "1 of 5: Set up your project" — visible across all steps so users know where they are and how far to go
- [ ] PASS: Output addresses skip / abandon paths — what happens if the user skips milestone setup (re-engagement nudge in the empty-state of the project view, in-product tip on next visit) and how to resume
- [ ] PASS: Output uses plain language only — no jargon like "milestone", "objective" if those aren't customer-facing terms; if Clearpath uses these as product terms, they're explained on first mention
- [ ] PASS: Output's onboarding length is appropriate — short enough not to lose users (≤5 steps to first value), long enough to cover the value path; explicit reasoning for the count
- [ ] PARTIAL: Output addresses celebration / reinforcement at the aha moment — making the moment of first value visible (animation, congratulatory message, share-with-team prompt) so users feel the win rather than just completing the flow
