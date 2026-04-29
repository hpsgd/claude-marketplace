# Output: Research plan

**Verdict:** PARTIAL
**Score:** 13.5/16 criteria met (84%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Starts with a clear research question — met. Research Planning step 1 explicitly instructs reframing vague problems into specific answerable questions, using the checkout example almost verbatim: "What prevents users who reach the payment step from completing checkout?"
- [x] PASS: Prioritises existing data analysis before new primary research — met. Step 2 states this directly and the Research Plan Format places "Existing data analysis" as Phase 1.
- [x] PASS: Recommends specific participant counts — met. Step 5 gives "5-8 participants for usability testing (Nielsen's saturation point), 8-12 for interviews" with explicit reasoning.
- [x] PASS: Accounts for PM resource constraints — met. Step 4 names this exact scenario: "A PM doing research solo in a 2-week sprint gets a different plan than a dedicated research team with a quarter."
- [x] PASS: Distinguishes quant from qual — met. Step 3 states it directly: "Quantitative data answers WHERE and HOW MUCH... Qualitative data answers WHY."
- [~] PARTIAL: Includes recruitment screener or participant criteria — partially met. Step 7 instructs defining a screener with characteristics to consider (existing customer vs prospect, power user vs new user, plan tier, disqualifiers). Types of criteria are named but no screener template is provided; specificity of output depends on agent judgment rather than enforced structure. Score: 0.5.
- [x] PASS: Produces a plan with sequenced steps and time estimates — met. Step 6 defines sequencing; the Research Plan Format includes duration fields across a phased structure.

### Output expectations

- [x] PASS: Output reframes the research question — met. Research Planning step 1 models this transformation with the checkout example, producing a specific question grounded in available evidence.
- [x] PASS: Output sequences existing-data analysis first — met. Phase 1 in the format template is "Existing data analysis" before primary research; step 2 reinforces this.
- [x] PASS: Output recommends specific qualitative participant count — met. 5-8 for usability testing with Nielsen saturation reasoning is stated in step 5.
- [x] PASS: Output scopes to a 2-week sprint with a single PM — met. The definition explicitly scopes plans to available resources and calls out the PM-solo-sprint case.
- [x] PASS: Output distinguishes quant vs qual capability — met. Step 3 is dedicated to this and instructs stating it explicitly in the plan.
- [x] PASS: Output plan is sequenced with time estimates — met. The Research Plan Format includes duration fields per phase and step 6 instructs sequencing with each stage building on the previous.
- [x] PASS: Output recruitment criteria are specific — met. Step 7 requires specific characteristics and disqualifiers; the format template includes a recruitment criteria field.
- [x] PASS: Output suggests interview discussion guide themes — met via inference. The agent's methodology (evidence-first, behaviour over opinion, "WHY" requires qualitative) would produce question themes for what users tried to do, expected, hesitated at, and did instead. The definition does not name the themes explicitly but the research planning process would generate them as part of scoping the qualitative phase.
- [~] PARTIAL: Output addresses PM-doing-research bias caveat — partially met. Step 4 scopes the plan to PM capabilities but does not flag confirmation bias or leading-question guardrails for a PM who is also the design owner. The definition acknowledges the constraint but not the bias risk. Score: 0.5.
- [~] PARTIAL: Output recommends a quick post-research synthesis action — partially met. The Research Plan Format includes "Phase 3: Synthesis" with a "how findings will be consolidated and shared" field, but does not specify translation into hypothesis-driven design experiments with the design/engineering team. Synthesis is present; the specific workshop format and experimental outputs are not. Score: 0.5.

## Notes

The definition handles the core research planning scenario well. The Research Planning section maps to most criteria with unusual precision — the checkout-drop-off example in step 1 appears to have been written with this class of scenario in mind.

The two partial gaps are meaningful but narrow. The PM-as-interviewer bias risk is absent — this is a genuine omission given the scenario explicitly involves a PM with no researcher background conducting their own interviews. The definition's own principles ("Behaviour over opinion," "Evidence over intuition") make this a natural place to add a guardrail. The post-synthesis action gap is structural: synthesis is present as a phase but the definition does not specify what that output should be (hypothesis-driven experiments vs a research report).

The screener partial remains from the earlier evaluation — the definition names what to consider but provides no template, leaving specificity to agent judgment.
