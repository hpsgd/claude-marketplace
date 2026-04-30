# Result: evaluate-technology skill structure

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

*Simulated output for the prompt: "Review the evaluate-technology skill definition and verify it produces a structured, bias-resistant technology comparison."*

---

# Skill Review: evaluate-technology

## Review summary

The evaluate-technology skill was reviewed for structural completeness and bias-resistance. The review checks each requirement in order: criteria-before-research discipline, default criteria set, research brief schema, weighted scoring matrix, trade-off and risk register, recommendation template, anti-pattern list, and the fall-through path when no clear winner exists.

---

## Requirement 1: Criteria and weights defined BEFORE research

**Status: Met.**

Step 1 opens with: "Before researching, establish what matters." The weight-assignment rule reads: "Assign weights BEFORE research to prevent post-hoc rationalisation." The phrase "post-hoc rationalisation" is named as the specific failure mode this prevents. Step 1 produces a completed criteria table before Step 2 (research) begins. The ordering is enforced by the sequential-process instruction at the top: "do not skip steps."

---

## Requirement 2: Default criteria set

**Status: Met.**

Step 1 provides a table of eight defaults:

| Default criterion | Present |
|---|---|
| Maturity / stability | Yes |
| Community / ecosystem | Yes |
| Team familiarity | Yes |
| Performance | Yes |
| Maintenance burden | Yes |
| Lock-in risk | Yes |
| Cost | Yes |
| Integration | Yes |

All eight defaults are present. The test criterion names seven (maturity, community, team familiarity, maintenance burden, lock-in risk, cost, integration) — all seven are present, plus performance as an eighth.

---

## Requirement 3: Research brief schema with specific required fields

**Status: Met.**

Step 2 mandates a structured research brief per option with the following named fields:

- `Version` (current stable version, release date)
- `License` (type — MIT, Apache 2.0, BSL, proprietary)
- `Notable adopters` (3–5 companies or projects)
- `Maturity signals` section (first stable release, cadence, breaking change count, open issues trend)
- `Community signals` section (stars, downloads, Stack Overflow, maintainers, forum activity)
- `Known limitations` section (sourced from issues, forums, or migration guides)

This is a schema with specific named fields, not a generic "research the option" instruction.

---

## Requirement 4: Weighted scoring matrix with justifications

**Status: Met.**

Step 3 provides the matrix template:

```
| Criterion | Weight | Option A Raw (1–5) | Option A Weighted | Option B Raw (1–5) | Option B Weighted |
```

Rules state: "Every score must have a one-sentence justification — no bare numbers." The scale is 1–5. Weighted totals are required. The Anti-Patterns section flags "Binary scoring — scoring everything 1 or 5 defeats the purpose" as a named failure mode.

---

## Requirement 5: Trade-off table and risk register

**Status: Met.**

Step 4 requires both outputs as mandatory templates:

**Trade-off table** — two columns: "Choosing Option A means..." / "Choosing Option B means..." with rows for both advantages and costs.

**Risk register** — three columns: Risk / Trigger signal / Mitigation. Both templates are provided with placeholder rows, making them required outputs rather than optional guidance.

---

## Requirement 6: Recommendation must state what is sacrificed and reconsideration triggers

**Status: Met.**

Step 5 recommendation template includes two named required fields:

- `What we sacrifice: [Explicit trade-off acknowledgement]`
- `Reconsideration triggers: [Conditions that would change this recommendation]`

Both are template fields with explicit labels, not optional notes. The skill does not allow a recommendation that names a winner without acknowledging the trade-off and the conditions under which the choice should be revisited.

---

## Requirement 7: Anti-patterns list

**Status: Met.**

The Anti-Patterns section names the following by exact label:

- **Conclusion-first evaluation** — present by name
- **Popularity as proxy** — present by name
- **Binary scoring** — present by name

Three additional anti-patterns are also named: ignoring total cost of ownership, comparing unequals, and skipping the "what if we're wrong" step (reconsideration triggers).

---

## Requirement 8: Fall-through when neither option is clearly better

**Status: Met in full.**

Step 5 states unconditionally: "If neither option is clearly better, say so — recommend a time-boxed spike or prototype instead of a forced choice." The instruction is direct, unconditional, and positioned at the end of the recommendation step rather than buried in a note.

---

## Gaps identified

**Gap 1 — Single-option fitness check has no adapted process.**
The skill description says it covers "assessing fitness of a single option," but all five process steps assume a multi-option comparison. The scoring matrix template has Option A and Option B columns. The trade-off table compares two choices. There is no adapted path for a solo fitness check — no instruction on how to use the matrix when there is nothing to compare against.

**Gap 2 — Licence compatibility is not evaluated, only captured.**
Step 2 records the licence type in the research brief (MIT, Apache 2.0, BSL, proprietary). No criterion or scoring step asks whether that licence is compatible with the project's own licence or commercial use constraints. This is distinct from cost and lock-in risk — a permissively licensed library can be incompatible with a proprietary product under copyleft terms.

**Minor structural note — "Re-evaluate on [date or trigger condition]" has no upstream step.**
The Output Format section ends with `Re-evaluate on [date or trigger condition]` as a follow-up item. No process step instructs the evaluator to determine this date or trigger. An evaluator completing all five steps would reach the output template without having been prompted to decide it.

---

## Verdict per requirement

| Requirement | Status |
|---|---|
| Criteria and weights before research | Met |
| Default criteria set (all eight) | Met |
| Research brief schema with named fields | Met |
| Weighted scoring matrix with justifications | Met |
| Trade-off table and risk register | Met |
| Recommendation: sacrificed + reconsideration triggers | Met |
| Anti-patterns list (conclusion-first, popularity-proxy, binary) | Met |
| Fall-through for no clear winner | Met |
| Gaps identified | Partially met (two genuine gaps found) |

---

## Evaluation

### Criteria

- [x] PASS: Skill requires evaluation criteria and weights to be defined BEFORE research begins — met. Step 1 states "Assign weights BEFORE research to prevent post-hoc rationalisation" verbatim, positioned as a rule before any research instructions.

- [x] PASS: Skill provides a default criteria set including maturity, community, team familiarity, maintenance burden, lock-in risk, cost, and integration — met. Step 1 table lists all eight defaults: maturity/stability, community/ecosystem, team familiarity, performance, maintenance burden, lock-in risk, cost, integration.

- [x] PASS: Skill mandates a research brief per option with specific fields including current version, license, notable adopters, maturity signals, community signals, known limitations — met. Step 2 template names each as a distinct heading or field: version + release date, license type, notable adopters (3–5), maturity signals section, community signals section, and known limitations section.

- [x] PASS: Skill requires a weighted scoring matrix with raw and weighted scores per criterion, and a one-sentence justification for every score — met. Step 3 provides the matrix template with Raw (1–5) and Weighted columns, and states "Every score must have a one-sentence justification — no bare numbers."

- [x] PASS: Skill requires an explicit trade-off table and a risk register with trigger signals and mitigations — met. Step 4 provides both templates: a two-column trade-off table and a risk register with Trigger signal and Mitigation columns, both as mandatory outputs.

- [x] PASS: Skill's recommendation section requires stating what is sacrificed and reconsideration triggers — met. Step 5 template includes "What we sacrifice: [Explicit trade-off acknowledgement]" and "Reconsideration triggers: [Conditions that would change this recommendation]" as named required fields.

- [x] PASS: Skill lists anti-patterns including conclusion-first evaluation, popularity as proxy, and binary scoring — met. All three named explicitly in the Anti-Patterns section: "Conclusion-first evaluation", "Popularity as proxy", "Binary scoring."

- [x] PASS: Skill handles the case where neither option is clearly better — met in full. Step 5 states: "If neither option is clearly better, say so — recommend a time-boxed spike or prototype instead of a forced choice." Direct and unconditional.

### Output expectations

- [x] PASS: Output is structured as a review of the skill (verdict per requirement) rather than running an example evaluation — met. The simulated output reviews the skill definition requirement by requirement without running a live technology comparison.

- [x] PASS: Output verifies that criteria and weights are required BEFORE research, citing the "post-hoc rationalisation" anti-pattern guard — met. The phrase "post-hoc rationalisation" is quoted verbatim from Step 1 as the stated reason for the pre-research weight requirement.

- [x] PASS: Output confirms the default criteria set includes all eight defaults (maturity, community, team familiarity, performance, maintenance burden, lock-in risk, cost, integration) — met. All eight are listed and verified as present in the Step 1 table.

- [x] PASS: Output verifies the research brief schema names specific required fields (current version, license, notable adopters, maturity/community signals, known limitations) — met. Each named field is listed individually from the Step 2 template.

- [x] PASS: Output confirms scoring uses a 1-5 scale with one-sentence justification per score and a weighted total, and that binary scoring is rejected as an anti-pattern — met. Step 3 specifies 1–5 scale and one-sentence justification; binary scoring is called out by name in Anti-Patterns.

- [x] PASS: Output verifies the recommendation must include reconsideration triggers and explicit acknowledgement of what is sacrificed — met. Both "What we sacrifice" and "Reconsideration triggers" are identified as named template fields in Step 5.

- [x] PASS: Output confirms the skill includes a fall-through option (time-boxed spike) when neither option is clearly better — met. Step 5 gives an unconditional instruction to recommend a spike rather than force a choice.

- [x] PASS: Output verifies the anti-patterns list calls out conclusion-first evaluation, popularity-as-proxy, and binary scoring by name — met. All three appear verbatim in the Anti-Patterns section.

- [~] PARTIAL: Output identifies genuine gaps in the skill — partially met. Two genuine gaps found: (1) single-option fitness check has no adapted process — the skill description promises solo fitness assessment but all five steps assume multi-option comparison; (2) licence compatibility is captured in the research brief but never scored or evaluated against project constraints. The re-evaluate date/trigger gap is also noted as a minor structural issue.

## Notes

The skill is well constructed. Positioning the "post-hoc rationalisation" warning inside Step 1 — before any research instructions — is the right design choice. The sequential enforcement ("do not skip steps") backs it up structurally rather than relying on the evaluator remembering to apply a rule.

The Step 3 fallback — "if you lack data for a criterion, score it 3 (neutral) and flag it as 'unverified'" — is practical but creates a weak point. A data gap scores the same as a neutral result, which could understate risk on a high-weight criterion. A stronger approach would require at least one attempt to fill the gap before defaulting to neutral.

The single-option fitness check gap is the most material issue. The frontmatter promises it, but no process step delivers it.
