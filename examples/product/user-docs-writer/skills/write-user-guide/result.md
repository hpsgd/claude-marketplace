# Output: Write user guide

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 7.5/8 criteria met (94%) |
| **Evaluated** | 2026-04-29 |

## Results

- [x] PASS: Skill requires a research step — Step 1 "Research the feature" is a mandatory first step requiring `Grep` and `Glob` searches for UI components, routes, and handlers; identification of all feature states; locating required permissions; checking existing docs; and ranking user tasks by frequency. Writing cannot begin until this step is complete.
- [x] PASS: Skill produces numbered steps for procedural tasks — Step 3 mandates a numbered format (`1. [action]`). The rules state "One action per step" and the template uses numbered lists throughout. Bullet points are not an acceptable substitute.
- [x] PASS: Each step includes what the user should see after completing it — the step template in Step 3 includes `**Expected result:** [What the user should see]` as a required field. The quality check table in Step 6 lists "Expected results: Does every step state what the user should see?" as a named pass/fail criterion.
- [x] PASS: Skill requires a troubleshooting section — Step 4 is a mandatory step with a Problem/Why/Fix structure. It requires at minimum: the most common error message, the most common user mistake, and environment differences. A minimum of 3 entries is required.
- [x] PASS: Skill uses only product terminology — the Rules section explicitly states "Use product language, not developer language" with examples ("Save your changes" not "persist the state"). The quality check in Step 6 includes "No jargon: Would a non-technical user understand every term?" as a required criterion.
- [x] PASS: Skill requires related content links at the end — Step 5 "Write related content and metadata" is a mandatory step producing a "Related guides" section with links for the next logical task, an alternative approach, and a deeper topic.
- [~] PARTIAL: Role-based or permissions context — the definition fully meets the intent. Step 1 research requires "Find the permissions or roles required to access the feature." The Step 2 header template includes `**Required role:**` as a named mandatory field. PARTIAL ceiling applies per the criterion's own notation (0.5), not due to any gap in the definition.
- [x] PASS: Valid YAML frontmatter — the skill has valid frontmatter with all three required fields: `name: write-user-guide`, `description`, and `argument-hint`. Additional fields `user-invocable` and `allowed-tools` are present and valid.

## Notes

The permissions criterion is fully met — Step 1 research explicitly requires locating required permissions, and Step 2's header template has a dedicated `**Required role:**` field. The PARTIAL score reflects the criterion's own ceiling, not a gap.

The six-step structure (research → header → steps → troubleshooting → related content → quality checks) is well-sequenced. The Step 6 quality checklist operationalises review as 10 binary checks rather than vague style guidance, which makes it harder to skip.

The rule "Never write 'simply,' 'just,' or 'easily'" targets a specific, common writer mistake. The cross-references to `/user-docs-writer:write-kb-article` and `/user-docs-writer:write-onboarding` at the end of the Rules section usefully route writers to the right skill when the use case doesn't fit a user guide.
