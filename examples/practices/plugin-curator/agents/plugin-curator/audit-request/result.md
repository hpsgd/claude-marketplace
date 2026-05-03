# Audit Request

Scenario: User asks the plugin-curator agent to audit an existing agent definition for structural consistency, expecting a structured report against the template criteria.

## Prompt

> Can you audit the `qa` agent for me? I want to know if it's structurally consistent with the template — whether it's got all the required sections, the right model, no private references, that kind of thing. Just give me the full breakdown.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I found two QA agents: `qa-lead` and `qa-engineer`. Auditing both.

---

## Agent Audit: qa-lead

### Summary
- **Lines:** 207 (target: 150–300)
- **Quality score:** 12/15 criteria met (3 partial, 0 N/A)
- **Model:** sonnet (correct)

### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (150–300) | ✅ | 207 lines |
| 2 | Core statement | ✅ | "You define what quality means for each piece of work BEFORE development starts…" — second person, clear ownership, line 10 |
| 3 | Non-negotiable rules | ✅ | "Acceptance criteria are defined before development starts. Edge cases are identified before the happy path is built." — specific and falsifiable, line 12 |
| 4 | Pre-Flight | ✅ | "Read CLAUDE.md and .claude/CLAUDE.md. Check for installed rules in `.claude/rules/`" — line 18 |
| 5 | Mandatory methodology | ✅ | "Every acceptance criterion uses Gherkin format" and numbered mandatory steps across both 3 Amigos and Acceptance Criteria sections |
| 6 | Output format | ✅ | Acceptance Test Plan template at lines 91–115; second Output Format block at lines 153–172 |
| 7 | Failure caps | ✅ | 3 caps present at lines 175–178 |
| 8 | Decision checkpoints | ✅ | 5 triggers in table at lines 185–190 |
| 9 | Collaboration table | ✅ | 5 roles at lines 196–200 |
| 10 | Principles | ✅ | 5 domain-specific principles at lines 130–134: Shift left, behaviour not implementation, absence of evidence, edge cases, testability |
| 11 | What You Don't Do | ⚠️ | Section present (lines 202–207), but only 1/4 items names an owner: "that's the QA Engineer." The other three ("Make product decisions", "Make architecture decisions", "Skip the 3 amigos") drop the exclusion without naming who DOES own it |
| 12 | No private refs | ✅ | No private company names, internal packages, or project-specific references |
| 13 | Tool links | ⚠️ | Line 142: `[Playwright](https://playwright.dev)/Cypress` — Playwright is linked, Cypress is not. First and only mention of Cypress in this agent |
| 14 | Correct model | ✅ | `sonnet` — correct for specialist |
| 15 | Description precision | ⚠️ | Description covers role and domain but lacks the required "Use when {trigger conditions}" clause. Template format: "{Role} — {domain}. Use when {triggers}." |

### Recommended Actions
1. **What You Don't Do (Criterion 11):** Add owners to the three unattributed exclusions — e.g., "Make product decisions — that's the product-owner", "Make architecture decisions — that's the architect", "Skip the 3 amigos — if the QA Lead wasn't in the session, acceptance criteria are incomplete"
2. **Frontmatter description (Criterion 15):** Add an explicit "Use when…" clause, e.g., "Use when starting a new feature, running a 3 amigos session, or defining acceptance criteria for a sprint"
3. **Tool links (Criterion 13):** Link Cypress on first mention at line 142 — `[Cypress](https://www.cypress.io)`

---

## Agent Audit: qa-engineer

### Summary
- **Lines:** 347 (target: 150–300)
- **Quality score:** 12/15 criteria met (3 partial, 0 N/A)
- **Model:** sonnet (correct)

### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (150–300) | ⚠️ | 347 lines — 47 over the upper target. Bug Investigation (lines 233–263), E2E Acceptance Testing (lines 154–229), and Review Process (lines 96–121) are candidates to extract to dedicated skills |
| 2 | Core statement | ✅ | "You own product quality — not just 'does it work?' but 'does it work correctly, reliably, and as specified under all conditions?'" — second person, clear ownership, line 10 |
| 3 | Non-negotiable rules | ✅ | "No test passes without evidence. No approval without independent verification… You trust exit codes, not narratives." — specific and falsifiable, line 12 |
| 4 | Pre-Flight | ✅ | "Read CLAUDE.md and .claude/CLAUDE.md. Check for installed rules in `.claude/rules/`" — line 18 |
| 5 | Mandatory methodology | ✅ | "CRITICAL", "MANDATORY", "The Iron Law", "This is not a suggestion" — mandatory framing throughout |
| 6 | Output format | ✅ | Evidence Output Format at lines 264–291 with Evidence, Scenarios Verified, and Quality Score tables |
| 7 | Failure caps | ✅ | 3 caps at lines 305–307 |
| 8 | Decision checkpoints | ✅ | 5 triggers in table at lines 313–319 |
| 9 | Collaboration table | ✅ | 6 roles at lines 323–329 |
| 10 | Principles | ✅ | 7 domain-specific principles at lines 334–340: exit codes, behaviour not implementation, real over mocked, one assertion, deterministic, RED before GREEN, criteria immutable |
| 11 | What You Don't Do | ⚠️ | Lines 342–347: "Make product decisions — escalate to product-owner" ✅, "Make architecture decisions — escalate to architect" ✅, "Approve your own code — request review from another specialist" ⚠️ (vague — no specific agent named), "Skip tests under time pressure" ❌ (no owner named at all) |
| 12 | No private refs | ✅ | No private company names, internal packages, or project-specific references |
| 13 | Tool links | ⚠️ | Line 22 lists Vitest, Jest, pytest, Playwright, Cypress in prose without any hyperlinks — this is the first mention of all five. Vitest and Playwright are linked later (lines 42 and 172), but Jest and pytest are never linked at all |
| 14 | Correct model | ✅ | `sonnet` — correct for specialist |
| 15 | Description precision | ✅ | "QA engineer — test automation, E2E acceptance tests, quality gates, coverage analysis. Use for writing test suites, implementing acceptance tests, browser-based E2E tests, analysing failures, or assessing release readiness." — role, domain, and trigger conditions all present |

### Recommended Actions
1. **Line count (Criterion 1):** Agent is 47 lines over target. The Bug Investigation section (lines 233–263) is the strongest candidate to extract to a `write-bug-report` skill — it's a self-contained methodology. The Review Process (lines 96–121) could become a `code-review` companion skill. Extracting either would bring the agent within range
2. **Tool links (Criterion 13):** Line 22 should link on first mention — add `[Vitest](https://vitest.dev)`, `[Jest](https://jestjs.io)`, `[pytest](https://pytest.org)`, `[Playwright](https://playwright.dev)`, `[Cypress](https://www.cypress.io)`. Alternatively, convert the enumeration in Step 2 Pre-Flight to a table where links appear there instead
3. **What You Don't Do (Criterion 11):** Fix the last two entries — "Approve your own code — request review from the qa-lead or a senior developer" (name a specific agent), and "Skip tests under time pressure — quality gates are owned by the QA Lead and CTO" (name owners)

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 12.5/16.5 (76%) |
| Evaluated | 2026-05-01 |
| Target duration | 148192 ms |
| Target cost | $0.3008 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Agent reads CLAUDE.md and marketplace.json as part of its mandatory pre-flight before beginning the audit | FAIL | The captured output contains no pre-flight step at all. It opens with 'I found two QA agents: qa-lead and qa-engineer. Auditing both.' and proceeds directly to tables. No mention of reading CLAUDE.md or marketplace.json. |
| c2 | Agent reads the agent template file before evaluating the qa agent definition | FAIL | No mention of reading an agent template file appears anywhere in the output. The 15-criterion table implies template knowledge was used, but no explicit read step is shown or referenced. |
| c3 | Audit output includes a criteria table covering all 15 quality criteria from the template | PASS | Both qa-lead and qa-engineer tables contain exactly 15 numbered rows (Line count, Core statement, Non-negotiable rules, Pre-Flight, Mandatory methodology, Output format, Failure caps, Decision checkpoints, Collaboration table, Principles, What You Don't Do, No private refs, Tool links, Correct model, Description precision). |
| c4 | Each criterion is scored as met, partially met, or missing — not left blank or assumed | PASS | Every row in both tables has a status symbol — either ✅ (met) or ⚠️ (partially met). No row is blank or marked 'N/A' without explanation. All 30 criterion rows across both audits are scored. |
| c5 | Non-passing criteria include specific evidence (file reference, line number, or exact quote) rather than vague descriptions | PASS | All ⚠️ rows cite specific lines: criterion 11 qa-lead 'Section present (lines 202–207), but only 1/4 items names an owner'; criterion 13 qa-lead 'Line 142: [Playwright]…/Cypress'; criterion 1 qa-engineer '347 lines — 47 over the upper target'; criterion 13 qa-engineer 'Line 22 lists Vitest, Jest, pytest, Playwright, Cypress in prose without any hyperlinks'. |
| c6 | Audit output includes a quality score (X/15 format) and line count | PASS | qa-lead summary: 'Lines: 207' and 'Quality score: 12/15 criteria met'. qa-engineer summary: 'Lines: 347' and 'Quality score: 12/15 criteria met'. Both numeric and exact. |
| c7 | Audit includes recommended actions prioritised by impact | PARTIAL | Recommended actions exist for both agents (3 each) and are numbered, implying an ordering. However, no explicit impact labels or severity tiers are stated. For qa-engineer, line count (a size issue) appears as #1 while a content gap (What You Don't Do) is #3, which inverts structural-before-style priority. |
| c8 | Boundary check — agent does not audit itself (plugin-curator is explicitly excluded from 'all' audits per the skill's anti-patterns) | PARTIAL | The output audits only qa-lead and qa-engineer; plugin-curator does not appear in the audit. The boundary is respected, earning the ceiling. |
| c9 | Output's audit table covers all 15 quality criteria from the agent template — not a subset, not a generic checklist | PASS | Both tables have 15 rows matching named template sections (Core statement, Pre-Flight, Failure caps, Decision checkpoints, Collaboration table, Principles, What You Don't Do, Description precision, etc.) — not a generic quality checklist. |
| c10 | Output scores each criterion as MET / PARTIALLY MET / MISSING (or equivalent ternary) — never blank, never 'assumed met' | PASS | ✅ and ⚠️ cover all 30 rows across both audits. No row is left blank or skipped. The ternary's third state (MISSING/❌) is not needed because no criterion is entirely absent in either agent, but the ternary capacity is demonstrated within criterion 11's evidence sub-items (✅, ⚠️, ❌). |
| c11 | Output's non-passing criteria each include specific evidence — file reference, line number, or exact quote from the qa agent definition — not vague descriptions like 'frontmatter could be better' | PASS | All partial-credit rows cite line numbers or exact quotes: criterion 15 qa-lead includes exact template format 'Use when {trigger conditions}'; criterion 11 qa-engineer quotes each 'What You Don't Do' entry individually with ✅/⚠️/❌ inline; criterion 13 qa-engineer lists all five tool names from line 22 and distinguishes which were eventually linked vs. never linked. |
| c12 | Output reports the quality score as `X/15` and the line count of the audited agent — both numeric, not approximate | PASS | qa-lead: '12/15 criteria met' and '207 lines'. qa-engineer: '12/15 criteria met' and '347 lines'. Both are exact integers, not ranges or approximations. |
| c13 | Output checks model correctness — qa is a specialist agent that should use `sonnet`, not `opus` — and flags as a finding if mismatched | PASS | Criterion 14 in both tables: qa-lead 'sonnet — correct for specialist' ✅; qa-engineer 'sonnet — correct for specialist' ✅. Model check is present and confirms the correct expected value. |
| c14 | Output's recommended actions are prioritised — structural gaps (missing required sections) before content gaps (sparse rules) before style issues (line length, banned words) — with severity per action | FAIL | No severity labels appear on any recommended action. For qa-engineer, action #1 is line count (a size/style issue), which should rank below structural or content gaps. No action carries a 'high/medium/low' or equivalent severity marker; the numbered list implies sequential priority but the ordering does not follow structural → content → style. |
| c15 | Output reads CLAUDE.md, marketplace.json, and the agent template before evaluating the qa agent — pre-flight is shown explicitly as a step or evidence in the output | FAIL | The output opens immediately with 'I found two QA agents' and presents audit tables. There is no explicit pre-flight step, no mention of reading CLAUDE.md, marketplace.json, or the agent template anywhere in the captured text. |
| c16 | Output checks for private references / company names that shouldn't appear in a public marketplace plugin definition | PASS | Criterion 12 appears in both tables labeled 'No private refs': qa-lead 'No private company names, internal packages, or project-specific references' ✅; qa-engineer identical finding ✅. |
| c17 | Output checks tool-link conventions — third-party tools mentioned in prose have markdown hyperlinks on first mention | PASS | Criterion 13 in both tables explicitly checks this: qa-lead flags Cypress unlinked on first mention at line 142; qa-engineer flags Jest and pytest as never linked, with specific line references and recommended URL fixes. |
| c18 | Output's recommendations are concrete — each action specifies what to add or change, not 'improve this section' | PARTIAL | Actions are highly concrete: qa-lead #3 specifies exact markdown '[Cypress](https://www.cypress.io)' at line 142; qa-engineer #2 gives full URLs for all five tools; qa-lead #2 provides the exact 'Use when…' clause wording. Ceiling is PARTIAL; the content meets the standard well. |

### Notes

The output delivers a genuinely strong audit on criteria content — 15-item tables, line-specific evidence, X/15 scoring, model checks, private-ref checks, and tool-link checks are all present and well-executed for both qa-lead and qa-engineer. The critical failure is the complete absence of any pre-flight documentation: there is no indication that CLAUDE.md, marketplace.json, or the agent template were read before the audit began (c1, c2, c15 all fail). Recommended actions also lack explicit severity labels and do not follow the structural → content → style priority order required by c14. These four FAIL criteria drag the score into PARTIAL territory despite an otherwise detailed and specific audit.
