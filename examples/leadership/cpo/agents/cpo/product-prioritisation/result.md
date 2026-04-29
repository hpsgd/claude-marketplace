# Result: Product prioritisation

**Verdict:** PASS
**Score:** 16.5/17.5 criteria met (94%)
**Evaluated:** 2026-04-29

## Criteria

- [x] PASS: Challenges the mobile app request as a solution rather than a validated problem — met. The definition instructs "Think in problems, not features. Always reframe feature requests as customer problems" and "Challenge the solution, validate the problem." The prioritisation framework includes Evidence strength as a factor and the quality gate requires "Problem validated — evidence that users actually have this problem."
- [x] PASS: Identifies the address validation dropout as the highest-priority item due to quantified frequency (47 tickets, 30% dropoff) and direct impact on activation — met. Problem severity and Problem frequency are both weighted High in the prioritisation framework. The principle "Onboarding is the highest-leverage investment. 70% of new users churn in the first 3 months" maps directly to a 30% first-booking dropout.
- [x] PASS: Applies problem frequency and severity weighting — does not treat all three requests as equal — met. The prioritisation framework table uses explicit High/Medium/Low weights and the Evidence strength factor distinguishes between 47 quantified tickets and two anecdotal prospects.
- [x] PASS: Escalates the PostgreSQL upgrade to the CTO rather than making a technical timeline decision — met. Escalation protocol explicitly covers "Timeline estimates for engineering work" and "What You Don't Do" lists "Estimate engineering effort — that's the CTO's team."
- [x] PASS: Does not approve the mobile app without evidence of user need at scale — cites the 94% low-engagement principle or equivalent — met. The definition states "94% of features see low engagement. Fewer, better features beat a feature graveyard" and the decision checkpoint lists "Approving a feature without evidence of user need" as a mandatory STOP.
- [x] PASS: Produces a clear prioritisation with reasoning, not just a ranked list — met. The "Assess Before Acting" protocol requires identifying the user problem, checking evidence, and classifying work before any decision.
- [~] PARTIAL: References the need for a success metric on the address validation fix — partially met. The mandatory quality gate "Success metric defined — how will we know this worked? What number changes?" covers this, but the definition frames it as a gate to confirm before approval rather than a direct output of the prioritisation step itself. Score: 0.5.
- [x] PASS: Does not make the business priority call unilaterally on scope conflicts — presents trade-offs clearly — met. Decision checkpoint requires stopping before scope changes mid-sprint; escalation rules cover cross-team resource conflicts.

## Output expectations

- [x] PASS: Output explicitly challenges the mobile app request as a solution-not-problem — met. The definition drives "Why does the customer need this?" before "How do we build this?" and the User Segment factor ("Is this for our best-fit segment or a fringe case?") would surface the two-prospect limitation.
- [x] PASS: Output prioritises the address-validation drop-off as #1 due to quantified impact — met. Onboarding principle plus high-weighted frequency/severity factors plus 47-ticket evidence strength makes this the clear #1.
- [x] PASS: Output applies frequency × severity reasoning — does NOT treat the three requests as equal — met. The prioritisation framework with explicit weights drives differentiated treatment.
- [x] PASS: Output escalates the PostgreSQL upgrade to the CTO — met. Explicit escalation rule covers technical timeline decisions. Definition also requires asking the CTO what product work would be displaced, which is the right framing.
- [x] PASS: Output does NOT approve the mobile app build without further evidence — met. The 94% principle and the mandatory STOP decision checkpoint both block unconditional approval.
- [x] PASS: Output's prioritisation is presented with reasoning per item — met. "Assess Before Acting" requires evidence review and classification before any decision, producing per-item rationale.
- [x] PASS: Output recommends a specific success metric on the address-validation fix — met. The quality gate "Success metric defined — how will we know this worked? What number changes?" is mandatory for every product decision.
- [x] PASS: Output proposes a cheap discovery action on the mobile request — met. The definition's evidence-over-opinion principle and standard challenge "How do you know this problem exists at scale?" produce a discovery recommendation before committing engineering time.
- [x] PASS: Output presents the trade-off honestly to stakeholders — naming who is unhappy with the recommended sequence — met. The definition requires presenting trade-offs clearly and not making unilateral calls on scope conflicts.
- [~] PARTIAL: Output addresses what happens if the PostgreSQL upgrade and the address-validation fix conflict for engineering time — partially met. The definition escalates timeline decisions to the CTO and surfaces trade-offs, but does not explicitly instruct the agent to propose sequencing or parallelisation plans when engineering capacity is shared. The conflict would be named but a concrete plan is not mechanised. Score: 0.5.

## Notes

The agent definition handles this scenario well. The 94% principle appears in two places (Principles and Decision Checkpoints), making the mobile app treatment reliable. The prioritisation framework with explicit High weights for frequency and severity is the load-bearing mechanism for ranking the address validation fix first.

The two PARTIAL marks are edge cases. The success metric quality gate is strong enough to produce the right output in practice — the gap is sequencing (gate before approval vs. output of prioritisation). The PostgreSQL/activation conflict is surfaced but not resolved by the definition; the agent would name it and escalate rather than propose a sequencing plan, which partially satisfies the criterion.
