# Evaluate Technology

Scenario: Checking that the evaluate-technology skill enforces an honest, evidence-based evaluation process — criteria defined before research, weighted scoring with justifications, and a clear recommendation with reconsideration triggers.

## Prompt

> Review the evaluate-technology skill definition and verify it produces a structured, bias-resistant technology comparison.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Good. Here's the review:

---

## Review: `architect:evaluate-technology`

The skill is well-structured overall — sequential steps, pre-committed weights before research, explicit anti-patterns, and required justifications per score. The bias-resistance foundations are solid. Seven gaps worth addressing:

---

### 1. Collision with `learned--evaluate-platforms-as-package` (high severity)

The skill evaluates in isolation or as X-vs-Y. Your own learned rule says infrastructure decisions (DB, auth, hosting, storage) cascade — changing one invalidates others. The skill has no mechanism for declaring "this evaluation depends on / affects evaluations X and Y." A user invoking this for infrastructure decisions gets 5 independent ADRs, not a coordinated platform decision.

**Fix:** Add a pre-check step: *"If this technology is infrastructure (DB, auth, hosting, storage, framework), list which other in-flight technology decisions it interacts with. If >1, consider evaluating as a platform bundle rather than in isolation."*

---

### 2. Unjustified numeric thresholds (collision with `learned--justify-numeric-thresholds`)

The 1–5 weight scale and 1–5 scoring scale are asserted without explanation. Why not 1–10? Why the same scale for both?

**Fix:** Add a one-sentence justification, e.g. *"1–5 because finer granularity creates false precision with qualitative scoring."* Or make the scale configurable.

---

### 3. Cross-option anchoring in Step 3

The side-by-side matrix invites relative scoring ("B looks strong next to A") rather than absolute scoring. There's no instruction to score each option independently before merging into the matrix.

**Fix:** Add to Step 3 rules: *"Score each option column independently before comparing — fill Option A fully before opening Option B's column."*

---

### 4. Asymmetric research depth

Step 2 includes `[tech] problems` and `[tech] limitations` search prompts for known weaknesses, but no equivalent prompt for the dispreferred option's strengths. This can create a skewed record where the preferred option gets a sympathetic brief.

**Fix:** Add: *"For each option, also search: `[tech] strengths`, `why [tech]`, `[tech] success stories` — apply equal effort to the case for and against each."*

---

### 5. Status quo bias in "Team familiarity"

This default criterion structurally advantages the incumbent technology and isn't flagged in anti-patterns. A greenfield decision and a migration decision should weight this differently.

**Fix:** Add to the anti-patterns section: *"Team familiarity bias — when evaluating a replacement for an existing tool, 'team familiarity' will mechanically favor the incumbent. Downweight it or add a parallel 'hiring pool / future familiarity' criterion to balance."*

---

### 6. Unverified scores have no quality floor

*"Score 3 if unverified, flag as unverified"* is good hygiene but has no cap. If 6 of 8 criteria are unverified, the weighted total is noise dressed as a number.

**Fix:** Add: *"If >3 criteria are unverified for any option, pause and do more research before scoring. A majority-unverified matrix should not drive a decision."*

---

### 7. "Notable adopters" conflicts with the "popularity as proxy" anti-pattern

Step 2 includes a "Notable adopters" field, but the anti-patterns section explicitly calls out popularity as a proxy for quality. The field is unlabeled as to its interpretive role.

**Fix:** Either remove the field, or add a label: *"(context only — do not treat as a quality signal; see anti-patterns)"*

---

### Summary

| Gap | Severity | Action |
|---|---|---|
| Platform interdependency (learned rule) | High | Add bundle pre-check |
| Unjustified 1–5 scale (learned rule) | Medium | Add justification or make configurable |
| Cross-option anchoring | Medium | Score independently before comparing |
| Asymmetric research depth | Medium | Add strengths search prompts |
| Status quo / familiarity bias | Medium | Add to anti-patterns |
| Unverified score quality floor | Low | Cap at >3 unverified |
| Notable adopters conflict | Low | Label as context-only |

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 7.0/15.0 (47%) |
| Evaluated | 2026-04-30 |
| Target duration | 145539 ms |
| Target cost | $0.4292 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires evaluation criteria and weights to be defined BEFORE research begins — explicitly to prevent post-hoc rationalisation | PASS | Opening paragraph: 'pre-committed weights before research, explicit anti-patterns, and required justifications per score. The bias-resistance foundations are solid.' |
| c2 | Skill provides a default criteria set including maturity, community, team familiarity, maintenance burden, lock-in risk, cost, and integration | FAIL | The output mentions 'team familiarity' only in the context of Gap #5 (status quo bias). It never confirms or enumerates the full default criteria set; the other seven defaults (maturity, community, maintenance burden, lock-in risk, cost, integration, performance) are not mentioned. |
| c3 | Skill mandates a research brief per option with specific fields: current version, license, notable adopters, maturity signals, community signals, known limitations | PARTIAL | Gap #7 references 'Notable adopters' field in Step 2; Gap #4 references '[ tech] limitations' search prompts. However, 'current version,' 'license,' 'maturity signals,' and 'community signals' are never explicitly named as required schema fields. |
| c4 | Skill requires a weighted scoring matrix with raw and weighted scores per criterion, and a one-sentence justification for every score | PASS | Opening confirms 'weighted scoring with justifications.' Gap #2 discusses 'The 1–5 weight scale and 1–5 scoring scale' and references one-sentence justifications per score implicitly in the context of requiring them. |
| c5 | Skill requires an explicit trade-off table and a risk register with trigger signals and mitigations | FAIL | Neither a trade-off table nor a risk register with trigger signals and mitigations is mentioned anywhere in the output. The word 'risk' does not appear in the captured output. |
| c6 | Skill's recommendation section requires stating what is sacrificed by the chosen option and what conditions would trigger reconsideration | PARTIAL | Opening says 'a clear recommendation with reconsideration triggers.' Reconsideration triggers are confirmed but 'what is sacrificed' is never mentioned as a required output element. |
| c7 | Skill lists anti-patterns including conclusion-first evaluation, popularity as proxy, and binary scoring | PARTIAL | Gap #7 explicitly names 'popularity as a proxy for quality' from the anti-patterns section. 'Conclusion-first evaluation' and 'binary scoring' are never named as anti-patterns in the skill's anti-patterns list; they appear only tangentially in gap discussions. |
| c8 | Skill handles the case where neither option is clearly better — recommends a time-boxed spike rather than forcing a choice | FAIL | No mention anywhere in the output of a time-boxed spike, a tie-handling fallback, or what happens when neither option is clearly better. |
| c9 | Output is structured as a review of the skill (verdict per requirement) rather than running an example evaluation | PARTIAL | The output is clearly a review of the skill, not an example evaluation. However, it is structured as a gap analysis (7 issues found) rather than a systematic verdict per requirement — it does not confirm what the skill correctly does for each requirement before flagging gaps. |
| c10 | Output verifies that criteria and weights are required BEFORE research, citing the explicit 'post-hoc rationalisation' anti-pattern guard | PARTIAL | Opening states 'pre-committed weights before research' confirming the timing requirement. However, the phrase 'post-hoc rationalisation' is never cited; the anti-pattern guard is not explicitly named. |
| c11 | Output confirms the default criteria set includes all eight defaults (maturity, community, team familiarity, performance, maintenance burden, lock-in risk, cost, integration) | FAIL | Only 'team familiarity' is mentioned (Gap #5). The other seven defaults are never enumerated or confirmed as present in the skill. |
| c12 | Output verifies the research brief schema names specific required fields (current version, license, notable adopters, maturity/community signals, known limitations) — not just 'research the option' | PARTIAL | Gap #7 names 'Notable adopters' as a Step 2 field. Gap #4 references limitations search prompts. 'Current version,' 'license,' 'maturity signals,' and 'community signals' are not verified as named schema fields. |
| c13 | Output confirms scoring uses a 1-5 scale with one-sentence justification per score and a weighted total — and that the skill rejects binary scoring as an anti-pattern | PARTIAL | Gap #2 explicitly names '1–5 weight scale and 1–5 scoring scale'; opening confirms 'weighted scoring with justifications.' Binary scoring as a named anti-pattern in the skill is never explicitly confirmed. |
| c14 | Output verifies the recommendation must include reconsideration triggers and explicit acknowledgement of what is sacrificed — not just naming a winner | PARTIAL | Opening confirms 'a clear recommendation with reconsideration triggers.' The requirement to acknowledge 'what is sacrificed' is never verified. |
| c15 | Output confirms the skill includes a fall-through option (time-boxed spike) when neither option is clearly better, instead of forcing a recommendation | FAIL | No mention of a time-boxed spike, fall-through option, or tie-handling anywhere in the output. |
| c16 | Output verifies the anti-patterns list calls out conclusion-first evaluation, popularity-as-proxy, and binary scoring by name | PARTIAL | Gap #7 explicitly names 'popularity as a proxy for quality' from the skill's anti-patterns section. 'Conclusion-first evaluation' and 'binary scoring' are not verified as named anti-patterns in the skill's anti-patterns list. |
| c17 | Output identifies any genuine gaps in the skill — e.g. no guidance on how to evaluate when only one option is being assessed (fitness check), missing licence-compatibility consideration, or no exit-cost / reversibility metric beyond lock-in risk | PARTIAL | The output identifies 7 genuine gaps: platform interdependency, unjustified numeric thresholds, cross-option anchoring, asymmetric research depth, status quo/familiarity bias, unverified score quality floor, and the notable-adopters conflict with anti-patterns. These are substantive, non-trivial gaps even if they don't match the specific examples listed in the criterion. |

### Notes

The captured output is a thoughtful gap analysis that correctly identifies several real weaknesses in the skill (asymmetric research depth, anchoring, status quo bias, threshold justification). However, it fundamentally fails the verification task: the criteria require the reviewer to confirm what the skill DOES correctly (default criteria set, all research brief fields, trade-off table, risk register, time-boxed spike fallback, all named anti-patterns) before flagging gaps. The output skips systematic verification and jumps straight to criticism. As a result it fails to confirm 8 of the 17 criteria entirely (c2, c5, c8, c11, c15 are complete misses) and only partially addresses most others. The most significant absences: no confirmation of the 8-criterion default set, no acknowledgment of the trade-off table or risk register requirement, no mention of the time-boxed spike fallback, and no explicit verification that conclusion-first evaluation and binary scoring are named anti-patterns.
