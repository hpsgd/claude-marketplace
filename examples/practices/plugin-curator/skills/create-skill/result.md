# Output: create-skill new skill for existing agent

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16 / 17 criteria met (94.1%) |
| **Evaluated** | 2026-04-29 |
| **Source** | `plugins/practices/plugin-curator/skills/create-skill/SKILL.md` |

## Results

### Criteria

- [x] PASS: Step 1 reads the skill template and CLAUDE.md before creating anything — met: Lines 15-17 show explicit `Read` calls for `skill-template.md` and `CLAUDE.md` as the first mandatory step, before any directory creation or file writing
- [x] PASS: Step 2 reads the parent agent (coding-standards) and checks for existing sibling skills to understand boundaries and avoid duplication — met: Step 2 reads the parent agent definition; Step 3 requires checking sibling skills and mapping their scope boundaries before writing
- [x] PASS: SKILL.md frontmatter includes all required fields: name, description, argument-hint, user-invocable, and allowed-tools — met: Lines 57-65 show a complete frontmatter template with all five fields under a heading stating "all fields required"
- [x] PASS: Description is specific enough for auto-invocation — includes what it produces and when to use it, not just "helps review Go code" — met: Line 68 marks description "CRITICAL" and requires both what it produces and when to use it; Line 127 provides a concrete bad/good contrast
- [x] PASS: Skill body includes sequential mandatory steps, rules with anti-patterns, and a structured output format template — met: Lines 75-81 body structure table marks all three as Required; Anti-Patterns section at lines 122-129; Output Format at lines 131-150
- [x] PASS: Step 6 self-containment check is performed — met: Lines 94-99 define an explicit self-containment step with a four-row pass-criteria table (understandable, executable, complete, bounded)
- [x] PASS: README is updated to add review-go to the coding-standards skill list — met: Step 7 (lines 101-103) instructs adding the skill to the parent agent's row in `README.md` as a numbered mandatory step
- [~] PARTIAL: Examples in the skill use generic identifiers (e.g., `myservice`, `@org/shared`) — no private company names or internal package references — partially met: Line 87 lists "Generic examples only (no private references)" as a quality target and Step 8 includes it in the mental audit checklist, but only as a mental check with no mechanical verification (no grep or pattern scan)

### Output expectations

- [x] PASS: Output creates `plugins/practices/coding-standards/skills/review-go/SKILL.md` — met: Step 4 uses `plugins/{category}/{agent}/skills/{skill-name}` which maps correctly; the skill does not create a new top-level plugin
- [x] PASS: Output's frontmatter contains all required fields — met: Step 5 frontmatter template shows all five fields with "all fields required" instruction
- [x] PASS: Output's description is auto-invocation-friendly — met: Line 68 CRITICAL framing requires what the skill produces and when to use it; the bad/good contrast at line 127 reinforces this
- [x] PASS: Output's body covers the four areas from the prompt — met: Step 3 directs explicit domain research, the arguments enumerate all four areas (error handling, interface usage, goroutine safety, table-driven tests), and a well-formed execution following Steps 3-5 would incorporate them
- [x] PASS: Output includes mandatory sequential steps and a structured output format template with findings table — met: Body structure table at lines 75-81 marks both as Required
- [~] PARTIAL: Output includes a Rules / Anti-patterns section with named anti-patterns specific to Go — partially met: The skill requires a Rules/Anti-patterns section (body structure table) but does not drive Go-specific content; a well-formed execution would include Go-specific anti-patterns based on domain research, but the skill provides no guard against generic anti-patterns that happen not to be Go-specific
- [x] PASS: Output's self-containment is verified — met: Step 6 four-point check table is a mandatory step
- [x] PASS: Output updates README.md — met: Step 7 is a numbered mandatory step covering exactly this
- [x] PASS: Output's examples use generic identifiers — met: Line 87 and Step 8 checklist both state this requirement explicitly
- [~] PARTIAL: Output addresses Go-specific concurrency review patterns — partially met: Step 3 domain research would surface concurrency patterns, but the skill provides no prompt or checklist that specifically calls out mutex choice, channel direction, or context propagation as areas to cover; coverage depends entirely on agent judgment from the arguments

## Notes

The skill is structurally solid — every lifecycle stage from template reading through README update is covered. The description-specificity guidance is strong, with CRITICAL framing and a concrete bad/good contrast in Anti-Patterns.

The two partial gaps are related: the skill enforces the presence of sections (anti-patterns, examples) but not the specificity or domain-accuracy of their content. For a general-purpose create-skill, this is a reasonable boundary. A skill that writes other skills can't know in advance what domain-specific content to mandate. The gaps are minor quality ceilings, not structural failures.

One implementation note from the previous evaluation remains valid: Step 2's bash commands use literal placeholder syntax (`{agent-name}`) without explaining substitution from `$ARGUMENTS`. A contributor following the step literally would need to infer this.
