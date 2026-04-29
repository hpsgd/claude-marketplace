# Output: Design a prompt for extracting action items from meeting transcripts

**Verdict:** PARTIAL
**Score:** 14.5/18 criteria met (80.6%)
**Evaluated:** 2026-04-29

## Results

### Criteria (skill definition)

- [x] PASS: Skill defines all six task properties before writing a single word of prompt — Step 1 table covers Input, Output, Format, Constraints, Volume, and Latency explicitly, with the instruction to write all six before proceeding
- [x] PASS: Skill specifies evaluation criteria (accuracy, format compliance, hallucination rate, latency, cost) with pass thresholds BEFORE designing the prompt — Step 2 mandates this and provides a table with all five criteria and pass thresholds
- [x] PASS: Skill specifies using JSON mode or function calling for structured output — Step 5 contains a table explicitly labelling "Output as JSON" in prompt text as "Never" and specifying JSON mode and function calling as the correct approaches
- [x] PASS: Skill starts with a minimal prompt and adds instructions only when eval failures demand it — Step 3 states "Start with the minimal prompt that could work. Run eval. Add instructions only for failure modes" and the anti-patterns section reinforces this
- [x] PASS: Skill designs at least 5 test cases covering 2 happy paths, 2 edge cases, 1 adversarial — Step 4 mandates exactly this breakdown with minimum counts per category
- [x] PASS: Skill includes context grounding — Step 6 marks context grounding as MANDATORY and provides a template for fallback when context is insufficient, directly applicable to the no-action-items case
- [x] PASS: Skill specifies version control strategy — Step 7 defines file location convention, naming convention, changelog format with eval results per version, and a deployment rule
- [x] PASS: Skill includes output validation rules — Step 5 specifies schema validation on every response, length validation, and an explicit catch for validation failures (log raw response, return graceful error); all three sub-criteria present
- [x] PASS: Output follows the full format — the Output Format section includes all required sections: task definition, eval criteria, prompt v1.0, output schema, test results table, safety measures, version history

### Output expectations (simulated output)

- [x] PASS: Output's task definition restates the four input/output specifics — the skill's Step 1 demands exact values for all six properties; a compliant output carries forward 3,000-word ceiling, 200/day, p95 < 5s, and $0.03/request from the prompt rather than generic placeholders
- [x] PASS: Output's schema names all four required fields with correct types — Step 1 and Step 5 require an explicit schema; a compliant output would define owner (string), description (string), due_date (ISO date string | null), confidence (float 0-1)
- [x] PASS: Output's prompt instructs return of empty array for no-action-item transcripts and a test case verifies it — Step 6's mandatory context grounding and Step 4's edge case requirement together guarantee this; T3 in the test table models exactly this fallback pattern
- [x] PASS: Output's prompt delimits the transcript with explicit boundaries — Step 6 explicitly requires input delimiting via XML tags, triple quotes, or structural separation as part of injection resistance
- [x] PASS: Output's adversarial test case uses an embedded prompt injection attempt — Step 4's T5 entry specifies "Ignore previous instructions" as the adversarial pattern, with expected output of a normal response that ignores the injection
- [~] PARTIAL: Output addresses ambiguous ownership with a defined behaviour — the skill requires 2 edge cases covering unusual inputs and the `owner` field makes ambiguous ownership a natural edge case for this scenario; however, the skill does not mandate it by name, so inclusion depends on the practitioner's domain awareness rather than the skill's explicit requirements
- [~] PARTIAL: Output includes a test case for relative date resolution — the `due_date` field with nullable ISO string makes date-ambiguity an obvious edge case, but the skill's framework does not enumerate it; a careful practitioner would include it, the skill does not guarantee it
- [~] PARTIAL: Output names a specific model and shows a cost calculation — the skill requires cost as an evaluation criterion with a pass threshold, but does not mandate naming a model or deriving a token-count estimate; the output format has no cost-calculation section
- [~] PARTIAL: Output's eval set matches 50 examples and describes sourcing — the skill explicitly states "minimum 50 examples" which a compliant output would reference; however, describing how those 50 are sourced (real, synthetic, or mix) is not part of the skill's requirements, so the count is addressed but sourcing narrative is not guaranteed

## Notes

The skill definition is strong across all nine structural criteria — all pass cleanly. The four partial credits in the output expectations reflect domain-specific depth the skill's framework enables but does not prescribe. Ambiguous ownership, relative date resolution, model-specific cost arithmetic, and eval sourcing narrative are all things a careful practitioner would include, but nothing in the skill forces them. The skill's general-purpose design is the right call; closing these gaps would require either domain-specific extensions or richer worked examples in the output format template.

One minor structural note: the skill defines six task properties in Step 1 but the output format template adds a seventh (Cost budget) not in the Step 1 table. Cost is covered in Step 2's evaluation criteria, so nothing is missing in practice, but the property count mismatch across the skill is a small consistency issue.
