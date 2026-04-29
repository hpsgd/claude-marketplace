# Output: Usability test plan

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16.5/17 criteria met (97%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill requires specific research questions before methodology selection — Step 1 defines 3-5 specific, answerable research questions with types and decision links before Step 2 (Methodology). The rules section reinforces: "Research questions drive everything. If you cannot connect a research question to a decision, remove it."
- [x] PASS: Skill requires participant screener criteria — Step 3 includes a Participants table with an explicit "Exclusions" row ("employees, recent participants, competitors") and a Screener Questions table with Accept/Reject columns per question.
- [x] PASS: Skill requires task scenarios written from the user's perspective — Step 4 names this as a rule: "Scenario, not instruction." It contrasts a correct example ("You need to change your billing address") against a wrong one ("Click Settings, then Billing, then Edit Address").
- [x] PASS: Skill requires success metrics defined per task — the task table in Step 4 requires a "Success criteria" column (observable outcome) and a "Time limit" per task. Step 6 defines task success rate, time on task, and error rate with explicit targets and measurement methods.
- [x] PASS: Skill includes a moderator guide with specific prompts and an intervention policy — Step 5 provides a full script: introduction, warm-up questions, three named follow-up probes, and an explicit intervention rule with timing and neutral wording ("If stuck for > [time limit]: offer one neutral prompt ('What are you looking for?')").
- [x] PASS: Skill specifies the number of participants with a rationale — Step 3 gives "5-8 for qualitative; 20+ for quantitative benchmarking" and cites Nielsen's research (5 participants catch approximately 85% of usability issues) as the basis.
- [x] PARTIAL: Skill covers logistics — all three named elements are fully present: session duration ("typically 45-60 for moderated, 15-30 for unmoderated"), recording consent (consent form template covering recording, data use, and withdrawal rights), and tools. Full coverage within the PARTIAL ceiling.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — all three fields are present and populated.

### Output expectations

- [x] PASS: Output's research questions would be specific and testable — the template explicitly requires a "What it will tell us / Decision this informs" column, and the rules section rejects questions not linked to a decision. Applied to the prompt ("Can a new user reach 'first project created' in under 10 minutes without help?"), the skill's structure produces testable, decision-linked questions.
- [x] PASS: Output's success metric ties to the prompt's threshold — Step 6's metrics table includes task success rate (target > 80%), time-on-task with a configurable target ("< [target]s"), and error rate per task. The skill's structure would produce a success criterion matching "reaches first project within 10 minutes" at a defined threshold.
- [x] PASS: Output's task scenarios are written from the user's perspective — Step 4 enforces scenario framing ("You want to invite a colleague to your project...") and explicitly prohibits instruction-style tasks. Applied to the onboarding prompt, output would follow the example form in the test's expected output.
- [x] PASS: Output's participant criteria specify who qualifies and who is excluded — the Participants table requires user type, experience level, demographics, and an Exclusions row. Screener questions require Accept/Reject columns. The structure produces criteria matching the expected form (role, company type, prior product exposure, exclusions).
- [x] PASS: Output specifies 5-8 participants with reasoning — the skill states "5-8 for qualitative" and cites Nielsen's research inline as the rationale. The citation is embedded in the body text, not decorative.
- [x] PASS: Output's moderator guide names specific prompts and a non-intervention policy — Step 5 provides named probes ("What did you expect to happen there?", "Was anything confusing or surprising?") and an explicit non-intervention rule with timing ("If stuck for > [time limit]: offer one neutral prompt").
- [x] PASS: Output's logistics cover session duration, recording consent, and tools — Step 7's logistics table includes all three items explicitly, with both moderated (45-60 min) and unmoderated (15-30 min) durations.
- [~] PARTIAL: Output's timeline includes recruitment lead time, session scheduling, conducting sessions, and synthesis — the logistics table includes a "Schedule" row ("Date range, sessions per day") and the recruitment section has a "Timeline" row. Synthesis timing is not broken out as a distinct phase in the template, only session scheduling is addressed. Partial credit: recruitment and session scheduling are covered but synthesis lead time is absent from the plan structure.
- [x] PASS: Output's pilot session is recommended before live participants — Step 7 includes a "Pilot session" row in the logistics table and the rules section states "An untested test plan wastes participants. Always run one pilot session."
- [x] PASS: Output addresses incentive — Step 3's recruitment table includes an "Incentive" row with a placeholder ("$50 gift card") and the skill's structure prompts the researcher to specify amount and form, flagging it as a named item in the plan.

## Notes

The skill is well-structured with tight internal logic. Research questions gate methodology, tasks must map to research questions, and metrics are defined pre-session — the sequence is enforced by step ordering and the rules section.

The one gap against output expectations is synthesis lead time. The logistics table asks for a "Schedule" row (session dates and cadence) but doesn't provide a dedicated row or template guidance for post-session synthesis time. For the onboarding test prompt, a researcher following the template would produce a schedule but might not reserve 1-2 days for analysis. This is a minor omission — the structure is otherwise complete.

The metrics section is thorough: per-task SEQ alongside post-test SUS is a combination most test plan templates don't include. The severity scale mirrors the usability-review skill, which is a deliberate consistency choice that pays off when teams use both skills together.
