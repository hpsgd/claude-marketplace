# Output: Journey map

**Verdict:** PARTIAL
**Score:** 14/18 criteria met (77.8%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires defining a scope with a concrete start trigger and end outcome before mapping begins — met. Step 1 is mandatory; its table includes Start point and End point fields with an explicit rule that both "must be concrete events, not states."
- [x] PASS: Skill requires identifying evidence sources (interviews, analytics, support data) before mapping — not mapping from assumptions — met. Step 2 (Evidence sources) is mandatory and precedes Step 3. Stages without data must be labelled "hypothesis" and the rules state: "If evidence is sparse, the journey map is a hypothesis to be validated, not a fact to be acted on."
- [x] PASS: Skill maps all four customer dimensions per stage: actions, thinking, feeling, and pain points — met. Step 3's per-stage table has Actions, Thinking, Feeling, and Pain points as distinct required rows.
- [x] PASS: Skill requires touchpoints and channels to be specified for each stage — not just abstract stages — met. Step 3's first table row is Touchpoints, with channel examples (website, app, email, docs, support, social media).
- [x] PASS: Skill identifies critical moments — stages with the highest emotional intensity or biggest impact on outcome — met. Step 4 is a mandatory section requiring Moment of truth, Biggest drop-off, and Delight opportunity, each with stage, description, impact, and evidence.
- [x] PASS: Skill produces improvement recommendations linked to specific stages or pain points — not generic UX advice — met. Step 5's Recommendations table has a "Stage affected" column and requires specific improvements. The rules section explicitly states "'Improve the onboarding' is not an opportunity."
- [~] PARTIAL: Skill includes wait times and gaps as explicit journey stages — partially met. Step 3 includes a Duration field (time spent within a stage) and lists "delays" as an example pain point, but the skill never requires wait times or gaps between stages to be modelled as their own explicit steps. The partial-credit condition in the criterion ("if pain points capture this but wait times are not explicitly required as steps") matches exactly.
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — met. Frontmatter contains all three required fields plus user-invocable and allowed-tools.

### Output expectations

- [x] PASS: Output's scope defines a concrete start trigger and end outcome — met. The skill mandates Step 1 with Start point and End point fields and the rule "must be concrete events, not states." Applied to the Clearpath scenario, this would produce specific trigger (e.g. peer recommendation / Google search) and outcome (e.g. daily active use for portfolio reporting), not abstract states.
- [x] PASS: Output names evidence sources for the map — met. Step 2 is mandatory before any stage mapping, and its template explicitly lists sales/CS conversations, analytics, user interviews, support tickets, and session recordings as sources. The skill enforces naming evidence before mapping — invented sources are disallowed by the rules ("stages with no data are hypothesis").
- [ ] FAIL: Output's stages cover the full journey — at least 6 stages — not guaranteed. The skill's guidance says "Typical journeys have 4–7 stages," which permits a 4-stage output. For the Clearpath mid-market director journey spanning Awareness through Daily Use, a 4-stage map would collapse meaningful inflection points. The skill does not require a minimum stage count and the lower bound of its guidance falls below the 6-stage criterion.
- [x] PASS: Output maps all four customer dimensions per stage — met. Step 3's per-stage table mandates Actions, Thinking, Feeling, and Pain points for every stage with no exceptions.
- [x] PASS: Output's touchpoints/channels per stage are specific — met. Step 3 requires Touchpoints as the first row with channel examples. The skill's specificity rules and evidence-over-assumption requirement would produce named channels (e.g. LinkedIn ads, signup form, sales call) rather than generic labels.
- [x] PASS: Output identifies critical moments — met. Step 4 is mandatory and requires Moment of truth, Biggest drop-off, and Delight opportunity with stage, description, impact, and evidence. This would produce reasoned critical moments for the Clearpath scenario (e.g. POC outcome, first integration failure).
- [x] PASS: Output's improvement recommendations are linked to specific stages or pain points — met. Step 5 requires a "Stage affected" column in the recommendations table. The rules ban vague improvements ("Improve the onboarding" is explicitly rejected). The skill would produce stage-pinned, specific recommendations.
- [ ] FAIL: Output addresses wait times explicitly — not guaranteed. The skill's Duration field captures time within a stage but does not require modelling wait times between stages as explicit steps. The Clearpath scenario involves meaningful delays (IT approval, 7-14 day eval window, 2-week integration wait) that would likely surface only as pain points in adjacent stages, not as named stages in their own right.
- [ ] FAIL: Output addresses cross-functional handoffs — not met. The skill has no structural requirement to identify handoff moments (sales → CSM, CSM → support, marketing → product). Touchpoints and pain points might capture handoff friction incidentally, but the skill does not require mapping handoffs as journey moments where experience can break down.
- [~] PARTIAL: Output addresses moments of doubt or churn risk — partially met. Step 3 includes a "Drop-off risk" field (High/Medium/Low) with a prompt for what causes users to leave at each stage. Step 4 identifies the "Biggest drop-off" as a critical moment. This captures churn risk structurally, though it does not explicitly name it as "moments of doubt" or require the map to surface pre-purchase doubt (mid-trial without value) as a distinct retention investment opportunity.

## Notes

The skill is well-constructed for its core purpose. The mandatory step sequencing (scope → evidence → stages → critical moments → synthesis) enforces rigour. The evidence-labelling requirement (evidence-based vs hypothesis per stage) is the skill's strongest quality gate.

Three output-level gaps are worth noting. First, stage count: the "4–7 stages" guidance permits outputs too compressed for complex B2B journeys like the Clearpath scenario. A minimum of 6 stages for enterprise journeys, or a prompt to expand when the journey spans more than 30 days, would close this. Second, inter-stage wait times: the Duration field captures time within a stage but not delays between stages. For mid-market operations software with IT procurement and integration cycles, these gaps are often the most painful part of the journey. Third, cross-functional handoffs: the skill models individual stages well but does not prompt for handoff moments between teams — a known failure point in B2B customer journeys. Adding a "Handoff from / to" field in Step 3 or a handoff row in Step 4 would address this without major restructuring.
