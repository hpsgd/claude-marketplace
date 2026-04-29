# Output: learning capture after a mistake

**Verdict:** PARTIAL
**Score:** 13.5/16 criteria met (84%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Step 1 assigns a category (SYSTEM, METHOD, DOMAIN, or FEEDBACK) with reasoning — the skill mandates category assignment with reasoning as the mandatory Step 1 output
- [x] PASS: Step 2 writes the learning in the exact format — the skill's Step 2 specifies the full template including frontmatter (name, description, type) and all body fields
- [x] PASS: The learning is stated as an imperative rule — the skill's Rules section explicitly requires "Always X when Y" form, not narrative
- [x] PASS: The "Why" field explains the consequence of ignoring the rule — the skill's rules state "The 'why' must explain the consequence of ignoring it, not just restate the learning"
- [x] PASS: Step 3 assigns Critical severity — the severity table uses "Force-pushed to main and lost 3 commits" as the canonical Critical example, matching this scenario exactly
- [x] PASS: Step 4 failure capture is triggered — the scenario describes data loss, rework, and a platform team restore; Step 4 defines the five-field failure analysis format as required output
- [x] PASS: Output follows the "When capturing" format — the skill's Output Format section defines the exact template with Name, Category, Severity, Rule, and Saved-to fields
- [~] PARTIAL: Skill checks for existing learning before creating — the Rules section states "Never duplicate learnings. Before saving, check if an existing learning covers the same ground." The obligation is present but there is no procedural step, no tool call sequence, and no path list to implement it; the check depends entirely on the model remembering to apply the rule

### Output expectations

- [x] PASS: Classifies as SYSTEM with reasoning — force-push from the wrong directory is a tooling/environment context failure; the skill's SYSTEM definition ("Infrastructure, tooling, configuration, environment") maps directly; the definition requires reasoning alongside the label
- [x] PASS: "What happened" reproduces specific details — the skill's Step 2 template requires "the specific situation that triggered this learning"; the scenario's key details (command, wrong directory, payments-service vs my-feature-branch, 3 commits overwritten, platform team backup) are required inputs to the template
- [x] PASS: Learning stated as an imperative rule — the skill's Rules section and Step 2 template both require imperative form; the existing result's "Always run `git remote -v` and `git branch --show-current`..." satisfies this
- [x] PASS: "Why" explains consequence — data loss, need for backup restore, deploy freeze, and hours of rework follow directly from the skill's consequence-focused Why requirement
- [ ] FAIL: "How to apply" gives a concrete trigger pattern with shell helper or alias suggestion — the skill says "specific enough that future-you can act on it without remembering the context" but provides no example that would drive an alias or shell helper suggestion; a model following only the skill definition is unlikely to produce that level of specificity
- [x] PASS: CRITICAL severity with explicit reasoning — the severity table's canonical example matches the scenario; the Rules section reinforces "If it caused data loss, it's Critical"
- [x] PASS: Failure analysis is triggered with required fields — Step 4 defines root cause, what was tried, what worked, and prevention rule as required fields; the scenario qualifies as a notable failure
- [x] PASS: Saved to a path matching the convention — the skill says "Save to the project's memory system" and the output format includes "Saved to: [file path]"; the convention resolves to `~/.claude/learnings/<name>.md`
- [x] PASS: Frontmatter includes required fields — the Step 2 template specifies name, description, type; severity and category appear in the body; classification from Step 1 should inform type
- [~] PARTIAL: Output checks both learnings paths before creating — the "Never duplicate" obligation exists in the Rules section; the skill provides no procedural mechanism (no Glob/Grep step, no path enumeration) to make the check happen reliably before Step 2 executes

## Notes

The skill is structurally strong for the core capture flow. The severity table's use of a force-push scenario as its Critical canonical example is a good design choice — it eliminates ambiguity for exactly this class of incident.

Two meaningful gaps:

1. The "How to apply" field has no template or example in the skill. The test's Output expectation requires a concrete trigger pattern and an optional shell helper or alias suggestion. The skill's prose says "specific enough that future-you can act on it" but gives no example that would drive a tool or alias recommendation. A model following the skill would produce something, but a shell alias is not implied by the definition.

2. The duplicate-check rule is a stated obligation but has no procedural implementation — no tool call, no path list, no ordering before Step 2. The PARTIAL is appropriate: the intent is present; the execution path is absent.

One structural inconsistency worth noting (outside the rubric): the Step 2 template hardcodes `type: feedback` in the frontmatter regardless of the Step 1 classification. A SYSTEM learning would carry `type: feedback` in its frontmatter, conflicting with the SYSTEM value in the body. The template should use a dynamic type field or rename the frontmatter field to avoid the mismatch.
