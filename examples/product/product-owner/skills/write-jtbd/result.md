# Output: Write JTBD

**Verdict:** PARTIAL
**Score:** 15.5/18 criteria met (86%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires a core functional job statement in the canonical format: "When I [situation], I want to [motivation], so I can [outcome]" — met: Step 2 defines the exact three-part format and states "Write exactly one core functional job"
- [x] PASS: Skill requires emotional jobs AND social jobs — met: Step 3 covers both as separate required categories with their own templates, reinforced by "Do not skip emotional and social jobs"
- [x] PASS: Skill requires an outcome table with Importance, Current Satisfaction, and Opportunity Score columns — met: Step 4 defines the table with all three columns and an example row
- [x] PASS: Skill defines the Opportunity Score formula with underserved/overserved thresholds — met: formula is `Importance + max(Importance - Satisfaction, 0)`, thresholds stated as >12 (underserved) and <6 (overserved)
- [x] PASS: Skill requires hiring and firing criteria — met: Step 5 covers both directions, with a Push/Pull/Anxiety/Habit table for switching triggers and a top-5 firing moments list with sudden/gradual classification
- [x] PASS: Skill prohibits solution-specific job statements — met: the Rules section explicitly calls out `"I want to use the dashboard"` as wrong, with an explanation and a corrected alternative
- [~] PARTIAL: Skill requires at least 8 outcome statements for the core job — fully met (criterion has PARTIAL ceiling, scored at 0.5): Step 4 states "Write at least 8 outcomes for the core job" with the minimum count explicitly specified
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met: all three fields present in the frontmatter block

### Output expectations

- [x] PASS: Output's core functional job is in the canonical format — met: Step 2 mandates the three-part format with solution-agnostic rules; the output template shows the exact format; a well-formed agent following this skill would produce a portfolio-framed functional job statement for the given prompt
- [x] PASS: Output identifies the operations director as the JTBD performer with context — met: Step 1 requires "specific role + circumstance", triggering context, current solution, and emotional state in a performer table; the prompt's "operations directors" framing would produce the required specificity
- [x] PASS: Output produces emotional jobs AND social jobs — met: Step 3 requires both categories with distinct templates and an explicit "Do not skip" instruction; both would appear in output
- [x] PASS: Output's outcome table has at least 8 rows — met: Step 4 explicitly requires "at least 8 outcomes for the core job"; the output template includes the full table structure
- [~] PARTIAL: Output's Opportunity Scores are computed via the formula with math shown — partially met: the formula is defined in Step 4 and scores are included in the table, but the skill does not require showing the arithmetic inline per row; a compliant output would have correct scores but might not show the calculation — partially met: formula present, inline math not required
- [~] PARTIAL: Output's hiring criteria name concrete switching triggers — partially met: Step 5 models concrete examples (e.g. "My spreadsheet broke when we hit 10,000 rows") but does not require this level of specificity in the output; the output template uses "..." placeholders; a compliant output could produce vague hiring triggers and still satisfy the skill
- [x] PASS: Output's firing criteria name what causes operations directors to switch away — met: Step 5 requires the top 5 firing moments with sudden/gradual classification; the output template includes this section
- [x] PASS: Output is solution-agnostic — met: the Rules section prohibits solution references in two places; the skill would prevent outputs that reference product features as jobs
- [~] PARTIAL: Output addresses the data dimension explicitly — partially met: Step 4's outcome format would capture data-related outcomes if the agent applies the "reporting and analytics" context correctly, but the skill does not require data-specific outcome categories (freshness, accuracy, drill-down, export); whether this appears depends on context application, not on a skill requirement
- [~] PARTIAL: Output addresses team-level vs portfolio-level outcomes — partially met: Step 1 asks the agent to identify the performer's circumstance, which would surface portfolio scope for an operations director, but the skill does not explicitly require distinguishing portfolio vs team-level framing; this distinction may or may not appear in the output

## Notes

The existing result only scored the Criteria section (8 items). This evaluation adds the Output expectations section (10 items) as required by the test format.

The skill is methodologically strong. It references both Christensen and Ulwick, the Opportunity Score formula is precise, and the prohibition on solution-specific statements is reinforced in multiple places.

The main gaps are in the Output expectations section: the skill models concrete examples in its instructions but does not require that level of specificity in the output. An agent following the skill to the letter could produce vague hiring triggers, omit inline math for opportunity scores, and miss the portfolio/team distinction — all while remaining compliant with the skill definition.

One dependency worth noting: the final line references `templates/jtbd-canvas.md` as the output structure, but this is not validated within the skill definition. If that template is absent, the reference is a dead end.
