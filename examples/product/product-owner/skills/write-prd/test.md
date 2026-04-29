# Test: Write PRD

Scenario: Testing whether the write-prd skill definition includes all required sections, RICE scoring, success metrics framework, and pre-mortem analysis.

## Prompt


/product-owner:write-prd for a bulk user import feature that lets admins upload a CSV to add multiple team members at once.

## Criteria


- [ ] PASS: Skill requires a problem statement section that is separate from the solution description
- [ ] PASS: Skill requires RICE scoring to justify prioritisation of the feature
- [ ] PASS: Skill requires three types of success metrics: leading indicators, lagging indicators, and guardrail metrics
- [ ] PASS: Skill requires a pre-mortem or risk analysis section — what could go wrong with this feature
- [ ] PASS: Skill requires explicit out-of-scope statements — not just what's included but what's excluded
- [ ] PASS: Skill produces a structured document with named sections that a team can review, not a prose narrative
- [ ] PARTIAL: Skill requires a rollout or release strategy section — partial credit if phasing is mentioned but not required as a structured section
- [ ] PASS: Skill requires success criteria to be measurable — "users can import" is not acceptable, "95% of CSV imports complete without error" is
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's problem statement is separate from the solution — describes the user pain (admins onboarding 50+ team members one at a time burns hours and is error-prone) before any reference to CSV upload as the solution
- [ ] PASS: Output's RICE score is shown numerically per cell — Reach (admins onboarding new teams per quarter, e.g. 200), Impact (1 — significant time saved per onboarding event), Confidence (% based on user-research signal strength), Effort (story points or weeks)
- [ ] PASS: Output's leading-indicator metrics are pre-launch / early signal — e.g. "% of admin users who try the bulk-import feature within 2 weeks of launch", "average time to first successful import"
- [ ] PASS: Output's lagging-indicator metrics measure the actual outcome — e.g. "average users added per onboarding event (target: 12+ vs current 3)", "admin NPS on team-onboarding question"
- [ ] PASS: Output's guardrail metrics name what must NOT regress — e.g. "no increase in import errors per imported user", "support ticket volume on user-management does not increase"
- [ ] PASS: Output's pre-mortem identifies at least 3-5 specific risks — e.g. "permission escalation via CSV row granting admin role", "performance under 1000-row imports", "duplicate-email handling when re-running an import" — with mitigation per risk
- [ ] PASS: Output's out-of-scope section is explicit — e.g. "v1 does NOT support: importing from external sources (Workday, Okta), updating existing user attributes, partial-roll-back if some rows fail" — so reviewers see the scope cliff
- [ ] PASS: Output's success criteria are measurable — "95% of imports under 100 rows complete without errors", "import of 1,000 rows completes within 30 seconds" — never "users can import"
- [ ] PASS: Output addresses the rollout strategy section — feature flag, beta cohort (e.g. 5 enterprise admins), staged GA — even if it's not the strongest section
- [ ] PARTIAL: Output references the related coordinator skill (`/coordinator:write-spec`) for the engineering-facing technical spec, since the PRD is the product-facing artefact and a separate technical spec follows
