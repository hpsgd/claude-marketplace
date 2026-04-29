# Output: Test strategy for new notifications microservice

**Verdict:** PARTIAL
**Score:** 15.5/19 criteria met (82%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent operates as the definition of WHAT to test — met. Definition explicitly states "You define WHAT to test. The QA Engineer implements HOW to test it" and "What You Don't Do: Implement automated tests."
- [x] PASS: Agent assesses the risk profile before defining test levels — met. Test Strategy section step 1 is "Determine risk profile — financial, safety, data integrity, reputation, legal/regulatory/compliance," and the classify table lists "Assess risk profile" as first step for test strategy definition.
- [x] PASS: Agent defines test levels covering unit, integration, and E2E — met. Test Level Assignment table in Output Format covers Acceptance/Integration/Unit, and the 3 amigos contribution explicitly names all three levels. The agent definition supports all three.
- [x] PASS: Agent applies the 3 amigos framing — met. Full "The 3 Amigos Pattern" section with explicit questions for product owner and architect, and numbered contributions for the QA Lead.
- [x] PASS: Agent identifies edge cases including concurrency, opt-out timing, channel fallback — met. All three map directly to categories in the Edge Case Checklist: Concurrency ("Duplicate submissions. Race conditions"), Error handling ("Network failure, timeout" covers channel fallback), and Data integrity (covers opt-out state integrity).
- [x] PASS: Agent sets specific, measurable quality gates for pre-merge and pre-release — met. Output Format requires "Quality Gates: Pre-merge: [checklist] / Pre-release: [checklist]." Test Strategy step 4 explicitly calls for gates at both checkpoints.
- [x] PASS: Agent flags testability concerns — met. 3 amigos contribution item 5: "Flag testability concerns — if something can't be tested, it needs to be redesigned before development starts." Principles section reinforces: "Testability is a design requirement."
- [~] PARTIAL: Agent assigns test levels to specific criteria with rationale — partially met. The Output Format includes a Test Level Assignment table with a Rationale column, and the template is present. However, the definition provides no heuristics for assigning levels (e.g., "unit when no external dependencies," "integration when crossing a service boundary"), so rationale depth depends entirely on model judgment rather than defined rules.

### Output expectations

- [~] PARTIAL: Output's risk assessment names duplicate-send (financial/reputational), opt-out violations (legal/regulatory — TCPA/GDPR), and provider outage as top risks — partially met. The risk profile methodology now explicitly lists "legal/regulatory/compliance" as a category, which maps to TCPA/GDPR. The definition does not pre-wire domain-specific notifications risks by name — the agent infers them from the prompt — making the output plausible but not guaranteed to name the specific regulatory frameworks.
- [x] PASS: Output's test levels table covers unit (logic, preference resolution), integration (internal REST API + external Sendgrid/Twilio/Firebase boundaries), and E2E — met. The test levels structure in Output Format plus the 3 amigos methodology supports a full levels table covering all three tiers for this scenario.
- [x] PASS: Output identifies integration test pattern — fakes/contract tests at provider boundaries, never live calls in CI — met. Testability concern instruction ("flag testability concerns — if something can't be tested, it needs to be redesigned") combined with the edge case checklist on external API error handling would produce the fake/contract test pattern for provider boundaries.
- [x] PASS: Output's edge case checklist covers concurrency, opt-out timing, and channel fallback — met. All three map directly to categories in the Edge Case Checklist: Concurrency, Error handling, and Data integrity/Backwards compatibility.
- [x] PASS: Output applies the 3 amigos lens with named specific questions for PO and architect — met. The 3 Amigos Pattern section provides explicit question frames for each role, and the agent's contribution list includes "Identify edge cases the product owner missed" and "Identify technical risks the architect missed." The agent would produce domain-specific questions derived from these frames.
- [x] PASS: Output sets specific quality gates pre-merge and pre-release — met. Quality Gates in Output Format explicitly separates pre-merge and pre-release. The Test Strategy methodology step 4 directs defining gates at both checkpoints. The agent would produce measurable gates including coverage thresholds.
- [x] PASS: Output addresses scaling from 50K to 500K notifications/day in the test strategy — met. Test Strategy step 6 now explicitly reads: "Cover stated growth or scale targets — if the prompt names launch volume and a future target, the strategy must validate the trajectory, not just the launch state." This directly directs the agent to address the 10x growth path in quality gates.
- [x] PASS: Output stays at strategy level, does not include implementation test code or specific test method names — met. The definition is unambiguous: "You don't implement tests — that's the QA Engineer" and "What You Don't Do: Implement automated tests."
- [x] PASS: Output identifies at least one specific gap — met. Test Strategy step 5 directs "Identify what can't be automated" and Decision Checkpoints include "Signing off on a feature without edge case coverage — document the gap." The agent would identify at least one named gap (e.g., no fake providers available, no contract tests with calling services).
- [~] PARTIAL: Output addresses observability requirements as a testability concern — partially met. The definition covers testability concerns as a design requirement and the 3 amigos contribution includes flagging them. However, observability (asserting delivery state vs request acceptance, queue hooks, provider callbacks) is not named as a distinct testability category. The agent may surface this from prompt inference but the definition does not guide the model toward it.

## Notes

The edit to the agent definition added two things. First, "legal/regulatory/compliance" was added to the risk profile categories in step 1 — this nudges the PARTIAL risk assessment criterion slightly toward a full pass but doesn't guarantee TCPA/GDPR by name. Second, step 6 was added to the Test Strategy section — "Cover stated growth or scale targets — if the prompt names launch volume and a future target, the strategy must validate the trajectory, not just the launch state" — which directly closes the previous FAIL on the 50K→500K scaling criterion.

Score moves from 14.5/19 (76%) to 15.5/19 (82%). Still PARTIAL. The two remaining gaps are rationale heuristics for test level assignment (no guidance on why unit vs integration vs E2E for a given criterion) and observability as a named testability concern (asserting delivery state rather than just request acceptance).
