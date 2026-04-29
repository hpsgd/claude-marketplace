# Output: Service blueprint

**Verdict:** PARTIAL
**Score:** 17.5/19 criteria met (92%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires a scope definition with a concrete start event and end outcome before mapping begins — Step 1 is mandatory and the scope table requires explicit Start point and End point fields with example concrete triggers
- [x] PASS: Skill maps all four required lanes: customer actions, frontstage employee actions, backstage employee actions, and support processes — Steps 2, 3, 5, and 6 each map one lane and are all marked mandatory
- [x] PASS: Skill explicitly draws the line of visibility separating what customers see from what they don't — Step 4 is a dedicated mandatory step with the visual separator and audit table
- [x] PASS: Skill includes a visibility audit — identifying what backstage work becomes visible to customers and whether that's intentional — Step 4 includes the visibility audit table and explicitly calls out "visibility breaches" with a rule to decide if intentional or accidental
- [x] PASS: Skill requires failure point analysis with location, failure mode, customer impact, frequency, and root cause — Step 7 table has columns for all five plus current mitigation
- [x] PASS: Skill requires each backstage action to have a trigger — no orphaned process steps — backstage rules state "Every backstage action must be triggered by something... No orphaned steps" and the table has a "Triggered by" column
- [~] PARTIAL: Skill requires duration estimates for backstage actions — duration is a required column in the backstage action table (Step 5), fully required per step; criterion is PARTIAL-prefixed so 0.5 credit applied even though the skill fully satisfies it
- [x] PASS: Skill produces prioritised improvement recommendations linked to specific failure points — Step 8 table links recommendations to failure point numbers (F#) and is explicitly prioritised by customer impact
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — frontmatter present with all three required fields

### Output expectations

- [x] PASS: Output's scope explicitly defines start and end — the scope table in Step 1 has Start point and End point as explicit rows with concrete example triggers; rules reinforce "Start and end must be concrete events"
- [x] PASS: Output's blueprint has all four lanes — the output format section confirms Customer Actions, Frontstage Employee Actions, Backstage Employee Actions, and Support Processes as separate sections
- [x] PASS: Output draws the line of visibility explicitly — the output format template includes the literal `───────────── LINE OF VISIBILITY ─────────────────────` separator between frontstage and backstage sections
- [x] PASS: Output's visibility audit identifies leaky abstractions — Step 4 rules explicitly address "visibility breaches" where backstage work leaks customer-visible, requiring a decision on whether intentional or accidental
- [x] PASS: Output's failure point analysis lists concrete failure modes — Step 7 table requires location, failure mode, customer impact, frequency, and root cause with a template row structure that maps to the expected specificity
- [x] PASS: Output's backstage actions each have a trigger — the backstage table's "Triggered by" column is mandatory, and the rules state no orphaned steps
- [x] PASS: Output's improvements are tied to specific failure points — Step 8 table has a "Failure point" column requiring the F# reference; rules state "Automate X is only a recommendation if you specify what and how"
- [x] PASS: Output covers the three named teams — the skill requires a "Role" column in both frontstage and backstage lanes, enforcing clear ownership per action; structurally enforced
- [ ] FAIL: Output's customer-action lane includes thinking/feeling/pain at each stage — the customer action lane (Step 2) captures only action, touchpoint, and channel; no emotional or cognitive dimension is required or mentioned anywhere in the skill; the related-skills note points to `/ux-researcher:journey-map` for the customer-facing layer but does not pull that emotional dimension into the blueprint lane itself
- [~] PARTIAL: Output addresses duration estimates per backstage action — duration is a required column in the backstage table (Step 5); criterion is PARTIAL-prefixed so 0.5 credit applied

## Notes

The only genuine gap is the emotional/cognitive dimension on the customer action lane. The customer action template in Step 2 captures behaviour only — what they do, what they touch, which channel. There is no prompt to record emotional state, anxiety, confusion, or sentiment at each stage. The skill references `/ux-researcher:journey-map` as a related skill for "the customer-facing layer," but does not instruct the agent to incorporate that emotional dimension into the blueprint's customer lane. For enterprise onboarding, where the customer's emotional state is a primary driver of churn risk, this is a real gap rather than a minor omission.

Duration in Step 5 is fully required as a column, not merely noted as important — the PARTIAL scores reflect test criterion type, not definition weakness.

The visibility audit design is strong: the "intentional or accidental" framing for visibility breaches is an above-average insight that goes beyond mechanical separation.
