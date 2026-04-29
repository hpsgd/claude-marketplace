# Output: Usability review

| | |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 14.5/17 criteria met (85%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill evaluates against Nielsen's 10 usability heuristics — met: Step 2 lists all 10 heuristics by name and number with explicit violation examples
- [x] PASS: Skill assigns severity ratings to each finding (Critical/Major/Minor/Enhancement) — met: Step 3 defines the scale and Step 2 template requires severity per finding
- [x] PASS: Skill requires a structured walkthrough of the interface before evaluation — met: Step 1 mandates scope definition, entry point, success state, and full annotated walkthrough before any heuristic evaluation
- [x] PASS: Skill produces a prioritised synthesis with the top issues identified — met: Step 4 explicitly requires "Top 3 Recommendations (by impact)" and a prioritised findings table
- [x] PASS: Each finding is tied to a specific heuristic violation — met: finding template requires "Heuristic: [number and name]" and rules state "every finding must map to a specific heuristic"
- [~] PARTIAL: Skill distinguishes between blocking and non-blocking issues — partially met: the severity scale implicitly covers this (Critical = "cannot complete the task", Enhancement = "not blocked"), but the skill never uses "blocking" / "non-blocking" terminology explicitly
- [x] PASS: Skill includes recommendations for each finding — met: finding template requires "Recommendation: [specific fix]" and rules explicitly ban vague feedback
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met: all three fields present in frontmatter

### Output expectations

- [x] PASS: Output would evaluate against all 10 heuristics by name — met: Step 2 table lists all 10 with names, numbers, check criteria, and common violations; the structure guarantees coverage by name
- [x] PASS: Output's structured walkthrough traces actual user paths — met: Step 1 requires tracing the full flow from entry point to success state including unhappy paths and "try to break the flow" instruction
- [x] PASS: Output's findings each have severity + heuristic citation + specific location — met: finding template mandates all three fields; rules require "every finding needs a location"
- [~] PARTIAL: Output's findings address the prompt's specific symptom — partially met: H6 (Recognition over recall) and H4 (Consistency) are both in the heuristics table and the skill evaluates $ARGUMENTS. However, the skill has no explicit instruction to cross-reference support-ticket signals against findings; the symptom-to-heuristic connection depends on agent inference rather than skill direction
- [x] PASS: Output's prioritised synthesis names top 3-5 issues — met: Step 4 calls for "Top 3 Recommendations (by impact)" with reasoning
- [x] PASS: Output's recommendations are concrete per finding — met: rules give an explicit bad-vs-good example ("Replace the 'Error 500' message with..." pattern) and ban "improve this" style feedback
- [x] PASS: Output distinguishes blocking from non-blocking — met: Critical = "Users cannot complete the task at all" (blocking) vs lower severities (friction, annoyance), which covers the distinction through severity even without explicit labels
- [ ] FAIL: Output addresses information architecture explicitly — not met: the skill has no mention of IA, navigation structure, sitemap, or information architecture. For a prompt about users unable to find things, this is a notable gap — the skill surfaces individual heuristic violations but does not prompt IA-level recommendations
- [~] PARTIAL: Output addresses search/find-as-fallback — partially met: H7 (Flexibility and efficiency) and H10 (Help and documentation) are in the heuristics table, and "searchable docs" in H10's common violations could surface settings search. However, there is no explicit instruction to consider global search or find-as-fallback as a recovery mechanism for navigation failure

## Notes

The skill is structurally strong. The four-step mandatory process (scope, evaluate, rate, synthesise) is well-sequenced, the finding template is complete, and the rules section actively prevents common quality failures (vague feedback, missing locations, manufactured findings).

The main gap is information architecture. The skill finds heuristic violations at the interaction level but does not prompt the agent to step back and evaluate whether the navigation structure itself is the problem. For the test prompt — users unable to find team, billing, and API keys — the root cause is almost certainly IA (wrong labels, wrong grouping, wrong hierarchy), not individual interaction bugs. The skill would surface H6 and H4 violations but may not produce the sitemap/navigation restructuring recommendations the prompt warrants.

The blocking/non-blocking distinction works implicitly through severity, which is functional but less explicit than it could be for teams who need to triage findings by task-criticality.
