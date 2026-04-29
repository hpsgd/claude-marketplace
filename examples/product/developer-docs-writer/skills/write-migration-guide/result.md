# Result: Write migration guide

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/19 criteria met (92.1%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Before/after code per breaking change — Step 3 rules state "Every step must have a before/after code example. Prose alone is not sufficient for a migration guide"; reinforced again in the global Rules section
- [x] PASS: Rollback plan with point of no return — Step 6 is "Write rollback instructions (mandatory)" and explicitly requires a `#### Point of no return` subsection identifying which migration step makes rollback impossible
- [x] PASS: Deprecation timeline with actual dates — Step 5 rules state "Every deprecation needs a timeline with actual dates (or 'X months after release'), not 'eventually'"; "eventually deprecated" is implicitly rejected by this rule
- [x] PASS: Impact assessment — Step 2 "Assess impact (mandatory)" requires a table covering who is affected, what code changes, effort estimate, risk level, and who is NOT affected
- [x] PASS: Exhaustive breaking changes table — Step 4 rules state "EVERY breaking change gets its own row. Do not combine multiple changes into 'various API improvements'"
- [x] PASS: Verification steps — Step 7 "Add verification steps (mandatory)" requires automated verification code, a manual checklist, and a common post-migration issues table
- [~] PARTIAL: Coexistence guidance — Step 5 includes both "Running old and new simultaneously" and "Dual-write/dual-read guidance" as required subsections; the skill fully covers this but the PARTIAL prefix in the criterion caps the score at 0.5
- [x] PASS: Honest effort estimates — Rules section states "Effort estimates must be honest. Underestimating migration effort is a form of lying to your developers. Round up, not down."
- [x] PASS: Valid YAML frontmatter — frontmatter contains `name: write-migration-guide`, `description`, and `argument-hint` fields

### Output expectations

- [x] PASS: Breaking-changes table lists each change as a separate row — the skill's Step 4 template has one row per change and the Rules state "EVERY breaking change gets its own row"; a well-formed response would produce separate rows for each renamed field (with old→new names), the auth shift, and each removed endpoint by name
- [x] PASS: Auth migration section covers OAuth 2.0 setup — Step 3's before/after template plus the Step 1 "Key difference" rule would drive a response to explain the auth mechanism shift in detail; the skill does not restrict this to a single-line summary
- [x] PASS: Before/after code examples show the actual change per breaking change — Step 3 rules require full before/after code (not pseudo-code) per step, and Step 4's breaking-changes table includes an "Example" column; a conforming response would include both old and new field names shown in code
- [x] PASS: Deprecation timeline has actual dates — Step 5 rules explicitly reject "eventually"; the template provides a dated-row table format that requires real dates (e.g. v3 GA, deprecation warnings, v2 EOL)
- [x] PASS: Impact assessment names who is affected and who is NOT — Step 2 template includes both "Who is affected" and a "Who does NOT need to migrate" section; a conforming response would call out integrations using removed endpoints and API key auth, plus identify unaffected parties
- [x] PASS: Rollback plan documents the point of no return — Step 6 template requires a `#### Point of no return` subsection that names which migration step makes rollback impossible; removing the old auth credentials or migrating off the removed endpoints would be identified
- [~] PARTIAL: Coexistence guidance covers running v2 and v3 in parallel — Step 5 requires a "Running old and new simultaneously" section and "Dual-write/dual-read guidance"; the skill would produce this, but does not explicitly require addressing whether v2 API keys remain valid alongside new OAuth tokens during the transition, which is the specific coexistence question for this prompt
- [x] PASS: Verification steps let developers confirm migration success — Step 7 requires automated verification code, a manual checklist, and a troubleshooting table; a conforming response would include a `GET /v3/users` check returning the new schema, and 410 Gone for removed v2 endpoints post-sunset
- [x] PASS: Effort estimate is honest and non-trivial — the Rules section's "Underestimating migration effort is a form of lying" rule plus the impact assessment template's "be honest" note would drive a realistic range; auth rebuild + field renames would not be summarised as "quick"
- [~] PARTIAL: Deprecation header / Sunset header (RFC 8594) addressed — the skill's Step 5 mentions "Old version still works but logs warnings" in the timeline template, which implies some form of deprecation signal, but does not explicitly mention HTTP `Sunset` headers or RFC 8594; partial credit for the warning concept without the specific header guidance

## Notes

The skill is well-constructed. Every mandatory step is labelled "(mandatory)", which removes ambiguity for both model and evaluator. The "honest effort estimates" rule uses the word "lying" — deliberate language that signals intent rather than boilerplate. Step 5's dual-write guidance is a required subsection, not a passing mention. The PARTIAL on coexistence (criterion 7 / output criterion 7) reflects the rubric's prefix ceiling rather than a skill gap — the skill covers dual-write more thoroughly than most. The RFC 8594 Sunset header is a legitimate gap: the skill never mentions HTTP-level deprecation signalling, which is standard practice for REST APIs in a migration window.
