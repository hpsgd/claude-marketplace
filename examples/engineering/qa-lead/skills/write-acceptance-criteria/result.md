# Result: Write acceptance criteria for bulk user import

**Verdict:** PARTIAL
**Score:** 17.5/19 criteria met (92.1%)
**Evaluated:** 2026-04-29

## Results

### Criteria section

- [x] PASS: Skill decomposes the story into business rules before writing scenarios — Step 2 uses Example Mapping and explicitly requires listing all business rules before writing scenarios. Rule sources list includes permissions, validation constraints, and limits/thresholds, covering all four rules needed for this story.

- [x] PASS: Each business rule has at least 2 concrete examples — Step 3 states "Every rule needs at least 2 examples. One example is a demo. Two examples define a pattern." The Rules section repeats this as a hard constraint, not a guideline.

- [x] PASS: Scenarios use business language — Step 3 rules: "Business language, not technical language." A direct contrast is given: "Then the user sees an error message" (correct) vs "Then the API returns 422" (wrong). The skill explicitly prohibits technical-level assertions.

- [x] PASS: Every Given establishes state, every When is a single action, every Then verifies one observable outcome — Step 3: "Given sets up state, When triggers action, Then observes outcome. Do not put assertions in Given. Do not put setup in Then." Combined with "One behaviour per scenario," this structure is enforced.

- [x] PASS: Edge cases are mandatory and covered — Step 3's scenario coverage table marks "Edge case: Boundary values, empty states, maximums — Yes, always." Step 6's edge case audit explicitly requires "empty/null input, maximum/minimum values." These categories cover all four specified edge cases (empty CSV, all-invalid CSV, exactly 1000, 1001 rows).

- [x] PASS: Error cases are covered — Step 3 coverage table requires "Permission denied" (when rule involves permissions) and "Validation error" (when rule involves input). Step 6 edge case audit includes "error states." Both non-admin access and malformed file fall within these required categories.

- [x] PASS: Non-functional criteria are included with thresholds — Step 4 provides a non-functional criteria table with Category, Criterion, Threshold, and How to test. Rules section states: "'It works' is not sufficient. 'It works within 500ms for 95% of requests' is an acceptance criterion."

- [~] PARTIAL: Open questions are flagged explicitly — Step 2 states "If you discover a red card (unanswered question), flag it explicitly. Do not invent an answer." The output format includes a dedicated Open Questions table. However, the skill doesn't proactively prompt for the specific class of privilege-escalation question (what if importing a CSV grants the admin role to another user?). It surfaces questions the practitioner discovers — not questions they might miss.

- [x] PASS: Test level mapping assigns each criterion to unit, integration, or E2E with rationale — Step 5 is dedicated to this, providing a mapping table with Criterion / Level / Rationale and three explicit assignment rules.

### Output expectations section

- [x] PASS: Output identifies the four business rules — Step 2's Example Mapping structure, combined with the rule sources list (permissions, validation constraints, limits/thresholds), would produce separate Rule blocks for admin-only access, max 1,000 rows, duplicate skipping, and invalid row collection. The "at least 2 examples per rule" constraint is enforced.

- [x] PASS: Permission scenarios cover both happy path and non-admin 403 behaviour — Step 3's coverage table requires "Permission denied" for any rule involving permissions, and the business language rule means this would be expressed as "the user sees a permission denied message," not an HTTP code.

- [x] PASS: Boundary scenarios for row limit cover exactly 1,000, 1,001, and 0 rows — Step 3 requires edge cases ("Boundary values, empty states, maximums — Yes, always") and Step 6's audit explicitly requires "empty/null input, maximum/minimum values." All three boundary scenarios fall within these mandatory categories.

- [x] PASS: Invalid-row handling scenarios cover bad email format, invalid role, and all-invalid CSV — Step 3 requires validation error scenarios for input-validation rules ("yes if the rule involves input"). Step 6 edge case audit adds "empty/null input" covering the all-invalid case. All three sub-cases are within scope of the skill's mandatory coverage.

- [~] PARTIAL: Duplicate handling scenarios cover existing-user skip, summary counts, and intra-upload duplicates — existing-user skipping and summary counts are directly addressed by Rule 2 (duplicates already in system) with required 2+ examples. However, the skill does not specifically prompt for the intra-upload duplicate case (two rows in the same CSV upload with the same email). This is a distinct edge case not surfaced by the skill's rule-discovery prompts or edge case audit list.

- [x] PASS: Given/Then steps speak in business terms, never HTTP codes or internal paths — Step 3's business language rule is explicit with contrast examples. This governs every scenario the skill produces.

- [x] PASS: Non-functional criterion sets a specific time budget with UX rationale — Step 4 requires thresholds as specific values and includes a "How to test" column. The skill's Rules section enforces "It works within 500ms for 95% of requests" as the model — a specific budget tied to observable UX expectation.

- [x] PASS: Malformed-file scenario covers corrupt file format with expected behaviour — Step 6's edge case audit lists "special characters" and error states. Step 3 requires "Validation error" scenarios. Malformed/corrupt file format is within scope of these mandatory categories, and the skill's business-language rule ensures the outcome is stated from the user's perspective.

- [~] PARTIAL: Open-questions section explicitly raises the privilege-escalation concern — the Open Questions output format and Red card mechanism are present. The specific question (admin importing a CSV that grants admin to others) would surface only if the practitioner identifies it as a Red card. The skill doesn't prompt for this category of question systematically (e.g., "for stories involving role assignment, always ask whether the operation can escalate privileges").

- [x] PASS: Test-level mapping assigns each criterion with rationale — Step 5 is entirely dedicated to this, with three explicit assignment rules and a populated example table. The row-limit check (unit), permission denied (integration), and full import flow (E2E) pattern is directly supported by the skill's guidance.

## Notes

The skill is substantively strong. The six-step process handles complexity without story-specific prompting, and the business-language and test-level guidance is better than most comparable definitions.

Both gaps — intra-upload duplicate detection and privilege-escalation open questions — stem from the same root: the skill surfaces unknowns the practitioner already sees, but doesn't prompt for blind spots in specific problem classes. The Example Mapping Red card mechanism is designed for group discovery sessions; solo use doesn't get the same coverage. Adding a "common questions for stories involving role assignment / bulk data import" heuristic section would close both gaps without adding structural weight.
