# Plugin curator audit request

User asks the plugin-curator agent to audit an existing agent definition for structural consistency, expecting a structured report against the template criteria.

## Prompt

> Can you audit the `qa` agent for me? I want to know if it's structurally consistent with the template — whether it's got all the required sections, the right model, no private references, that kind of thing. Just give me the full breakdown.

```markdown
[Pre-flight]
Reading CLAUDE.md... ✓
Reading .claude-plugin/marketplace.json... ✓
Reading plugins/practices/plugin-curator/templates/agent-template.md... ✓

Locating qa agent: plugins/engineering/qa/agents/qa.md... ✓

## Output

### Agent Audit: qa

#### Summary
- Lines: 187 (target: 150–300) ✅
- Quality score: 11/15 criteria met
- Model: sonnet (correct — qa is a specialist)

#### Criteria Status

| Criterion | Status | Notes |
|---|---|---|
| Core statement | ✅ | "You own the quality gate..." — second person, clear ownership |
| Non-negotiable | ⚠️ | Rules present but two are vague: "Maintain quality standards" is not falsifiable |
| Pre-Flight | ✅ | Reads CLAUDE.md at line 18 and .claude/CLAUDE.md at line 22 |
| Domain methodology | ✅ | Steps framed as mandatory throughout |
| Output format | ✅ | Structured report template at line 89 |
| Failure caps | ❌ | No failure caps section found |
| Decision checkpoints | ⚠️ | One checkpoint present but no full checkpoint table |
| Collaboration table | ✅ | Table at line 134, 5 collaborators listed |
| Principles | ✅ | 7 principles, domain-specific |
| What You Don't Do | ✅ | Present at line 162, names owners for excluded activities |
| No private refs | ✅ | No private company names, packages, or URLs found |
| Tool links | ⚠️ | Line 74: "Playwright" mentioned without hyperlink. Line 81: "k6" mentioned without hyperlink |
| Correct model | ✅ | sonnet — qa is a specialist agent |
| Description precision | ✅ | "QA lead — test strategy, quality gates, regression prevention. Use when reviewing test coverage or validating a release" |
| Line count | ✅ | 187 lines (target: 150–300) |

#### Recommended Actions
1. **Add failure caps section** (structural gap) — add: "3 consecutive test failures without root cause → escalate to architect"
2. **Fix tool links** — add [Playwright](https://playwright.dev) and [k6](https://k6.io) at lines 74 and 81
3. **Sharpen non-negotiable rules** — replace "Maintain quality standards" with a specific falsifiable rule
4. **Complete decision checkpoints** — expand the single checkpoint into a full table with trigger, what to ask, and who to ask
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/7.5 criteria met (100%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Agent reads CLAUDE.md and marketplace.json in pre-flight — Pre-Flight Step 1 (labelled MANDATORY) defines both reads explicitly: `Read(file_path="CLAUDE.md")` and `Read(file_path=".claude-plugin/marketplace.json")`. These are positioned before any creating or auditing actions.
- [x] PASS: Agent reads agent template before evaluating — Pre-Flight Step 2 reads `${CLAUDE_PLUGIN_ROOT}/templates/agent-template.md` and `${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md`. The text states "These templates define the MANDATORY structure for all agents and skills." The template read precedes any audit work.
- [x] PASS: Audit output covers all 15 quality criteria — the Audit Output Format's Criteria Status table lists all 15 rows: Core statement, Non-negotiable, Pre-Flight, Domain methodology, Output format, Failure caps, Decision checkpoints, Collaboration table, Principles, What You Don't Do, No private refs, Tool links, Correct model, Description precision, Line count. All 15 are present by name.
- [x] PASS: Each criterion scored as met/partially met/missing — the Audit Output Format uses `✅/⚠️/❌` symbols in the Status column for every row. The Common Issues table defines the patterns that warrant each score. No row can be left blank.
- [x] PASS: Non-passing criteria include specific evidence — the Auditing Existing Agents section Step 3 now states evidence requirements explicitly, with a counter-example directly in the agent definition: "'Missing Pre-Flight' is not a finding. 'No Pre-Flight section found in `agents/devops.md` (expected after line 12)' is a finding." This mandates file path AND line number for non-passing findings. The agent definition now enforces this standard independently of the skill. Previously this was scored 0.5; the updated definition fully meets the criterion.
- [x] PASS: Quality score in X/15 format with line count — the Audit Output Format Summary block shows `Quality score: {X}/{15} criteria met` and `Lines: {count} (target: 150-300)` as required fields in the template.
- [x] PASS: Recommended actions prioritised by impact — the Auditing Existing Agents section Step 4 explicitly states "Prioritise fixes — structural gaps > content gaps > style issues." This ordering rule is present in the agent definition.
- [~] PARTIAL: Boundary check — the agent's "What You Don't Do" section (line 279) now explicitly states: "Audit yourself — skip the plugin-curator agent in 'all' audits. You follow your own meta-structure, not the standard agent template." This is now in the agent definition itself, not only in the skill. The self-exclusion rule is met at both the agent and skill level. PARTIAL ceiling applies per criterion prefix regardless of coverage quality.

## Notes

Two criteria that were previously failing or partial are now fully met. Criterion 5 (evidence specificity) upgraded from 0.5 to PASS: the agent definition at Auditing Existing Agents Step 3 now contains a concrete counter-example mandating file path and line number, matching the standard previously only visible in the audit-agent skill. Criterion 8 (boundary check) is now present in the agent's "What You Don't Do" section — the self-exclusion rule exists at both levels. The PARTIAL ceiling on criterion 8 applies regardless, so the score remains 0.5 for that item, but the definition gap that previously caused the partial is gone.
