# Test: Usability review

Scenario: Testing whether the usability-review skill requires Nielsen's heuristics with severity ratings, and produces a prioritised synthesis rather than a flat list of observations.

## Prompt


/ux-researcher:usability-review of our account settings area — users frequently contact support saying they can't find how to manage team members, billing, or their API keys.

## Criteria


- [ ] PASS: Skill evaluates against Nielsen's 10 usability heuristics — not a generic UX checklist
- [ ] PASS: Skill assigns severity ratings to each finding (e.g. Critical/Major/Minor/Enhancement or a numeric scale) — not a flat unrated list
- [ ] PASS: Skill requires a structured walkthrough of the interface before evaluation — scope is defined, paths are traced
- [ ] PASS: Skill produces a prioritised synthesis with the top issues identified — not just a complete catalogue of all findings
- [ ] PASS: Each finding is tied to a specific heuristic violation — not a general observation
- [ ] PARTIAL: Skill distinguishes between issues that affect task completion (blocking) and issues that affect experience quality (non-blocking) — partial credit if severity does this work implicitly
- [ ] PASS: Skill includes recommendations for each finding, not just problem statements
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output evaluates the account settings area against Nielsen's 10 heuristics by name — Visibility of system status, Match between system and real world, User control and freedom, Consistency and standards, Error prevention, Recognition rather than recall, Flexibility and efficiency, Aesthetic and minimalist design, Help users recognise/diagnose/recover from errors, Help and documentation
- [ ] PASS: Output's structured walkthrough traces the actual user paths from the prompt — finding team members, finding billing, finding API keys — showing the navigation each user would attempt, where they would get stuck, what they would see
- [ ] PASS: Output's findings each have a severity rating (Critical / Major / Minor / Enhancement) AND a heuristic violation cited (H4 Consistency, H6 Recognition vs Recall, etc.) AND a specific location (selector, page section, screen) — not a flat unrated list
- [ ] PASS: Output's findings address the prompt's specific symptom — users contacting support because they can't find team / billing / API keys — likely H6 (Recognition vs Recall) and H4 (Consistency) violations: settings buried under non-obvious labels, inconsistent placement across product
- [ ] PASS: Output's prioritised synthesis names the TOP 3-5 issues — not a complete catalogue — with reasoning that addresses the support-ticket signal (these are the issues actually causing user friction at scale)
- [ ] PASS: Output's recommendations are concrete per finding — not "improve discoverability" but "rename 'Account preferences' to 'Account settings' to match user mental model; move team management out of submenu to top-level Settings sidebar"
- [ ] PASS: Output distinguishes blocking issues (user genuinely cannot complete the task) from non-blocking issues (user can complete but with friction) — the prompt's "users contact support because they can't find" suggests blocking issues
- [ ] PASS: Output addresses information architecture explicitly — the prompt's symptoms point to IA / navigation problems, not micro-interaction issues; recommendations should include sitemap / navigation restructuring suggestions
- [ ] PASS: Output's findings each name the affected user task — "Affected task: invite a teammate" — so the team can validate the recommendation against the actual job-to-be-done
- [ ] PARTIAL: Output addresses search / find-as-fallback — when navigation fails, can users search settings? Is there a global settings search? This is a recovery mechanism Nielsen's H7 (flexibility / accelerators) addresses
