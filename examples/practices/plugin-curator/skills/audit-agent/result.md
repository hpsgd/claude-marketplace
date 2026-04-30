# Result: audit-agent single agent full evaluation

**Verdict:** PASS
**Score:** 16/18 criteria met (89%)
**Evaluated:** 2026-04-30

## Output

The following is the simulated output of `/audit-agent devops` — what this skill would produce when run against `plugins/engineering/devops/agents/devops.md`.

---

## Agent Audit: devops

### Summary

- **Lines:** 264 (target: 150–300) ✅
- **Quality score:** 11/15 criteria met (1 N/A)
- **Model:** sonnet (correct)

### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (150–300) | ✅ | 264 lines |
| 2 | Core statement | ✅ | Line 10: "You own the runtime environment — how code gets to production and stays running." Second person, one paragraph |
| 3 | Non-negotiable rules | ✅ | Lines 12–13: "All infrastructure is code. No manual console changes. Every change is reviewable, versionable, and reproducible." Specific and falsifiable |
| 4 | Pre-Flight | ⚠️ | Step 1 (line 18) says "Check for installed rules" but does NOT read `CLAUDE.md` or `.claude/CLAUDE.md` — the mandatory template requirement. Installed-rules check only is partial |
| 5 | Mandatory methodology | ✅ | Step 3 (line 30) classifies work into explicit approach paths; downstream sections (IaC, CI/CD, Containers, etc.) use enforced language ("ENFORCED", "Standards", numbered sequential steps) |
| 6 | Output format | ✅ | Lines 224–244: full template with `## Infrastructure`, Evidence table, Resources Changed, Verification, and Runbook sections |
| 7 | Failure caps | ✅ | Lines 206–208: 3-failure rule for deployments and IaC apply; flaky pipeline rule. Section present at line 204 |
| 8 | Decision checkpoints | ✅ | Lines 210–220: 5 triggers in a table — budget, network topology, database config, secrets, deployment strategy |
| 9 | Collaboration table | ✅ | Lines 248–256: 7 roles listed with how devops works with each |
| 10 | Principles | ⚠️ | Lines 198–202: 5 principles present but count is at the minimum. Each is domain-specific (cattle/pets, shift left, least privilege, automate toil, cost awareness). At 5/10 — borderline depth |
| 11 | What You Don't Do | ✅ | Lines 259–263: 4 exclusions, each naming the owner role |
| 12 | No private refs | ⚠️ | Line 60: "Weasel `ExtendedSchemaObjects`" — Weasel is a .NET library but appears without context or link, reads as internal jargon to an unfamiliar reader. Line 79: "Neon Postgres" mentioned as example without hyperlink. Minor but present |
| 13 | Tool links | ⚠️ | Pulumi linked at line 40 ✅. Testcontainers linked at line 69 ✅. Moon linked at line 85 ✅. Storybook linked at line 86 ✅. NOT linked: "Marten" line 59 (no hyperlink on first mention), "Weasel" line 60 (no hyperlink), "Celery" line 150 (no hyperlink), "GitHub Actions" line 79 (mentioned in prose, not linked) |
| 14 | Correct model | ✅ | Frontmatter: `model: sonnet` — correct for specialist agent |
| 15 | Description precision | ✅ | "DevOps / platform engineer — infrastructure-as-code, CI/CD, deployment, monitoring, incident response. Use for infrastructure work, pipeline configuration, deployment issues, or observability setup." Role ✅, domain summary ✅, trigger conditions ✅ |

### Recommended Actions

**Structural gaps**

1. **Pre-Flight incomplete (Criterion 4):** Step 1 does not read `CLAUDE.md` or `.claude/CLAUDE.md`. Add explicit reads: `Read(file_path="CLAUDE.md")` and `Read(file_path=".claude/CLAUDE.md")` at the start of Step 1, alongside the installed-rules check.

**Content gaps**

2. **Tool links missing (Criterion 13):** Add hyperlinks on first mention for Marten (line 59), Weasel (line 60), Celery (line 150), and GitHub Actions (line 79 — mention it inline with a link or rely on the linked-section context). Suggested: `[Marten](https://martendb.io)`, `[Weasel](https://github.com/JasperFx/weasel)`, `[Celery](https://docs.celeryq.dev)`, `[GitHub Actions](https://docs.github.com/en/actions)`.
3. **Private/internal references (Criterion 12):** "Weasel `ExtendedSchemaObjects`" at line 60 is a .NET library with no introduction — readers unfamiliar with Marten/Weasel will not know what this is. Add a brief inline link or remove it to a domain-specific rule file.

**Style / depth**

4. **Principles at minimum count (Criterion 10):** 5 principles is the floor. Consider adding 2–3 more domain-specific principles (e.g., immutable infrastructure, observability-first, runbook-driven incident response) to bring depth up toward the 8–10 range.

---

## Criteria

- [x] PASS: Step 1 reads the agent template file before evaluating — `Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/agent-template.md")` is the literal first instruction in Step 1; the template's quality criteria are named as the audit checklist
- [x] PASS: All 15 criteria are evaluated and scored — Criterion 1 through Criterion 15 are explicitly enumerated in Step 3 with scoring guidance for each; none left blank
- [x] PASS: Every non-passing criterion includes specific evidence — Step 4 mandates what was looked for, what was found or not found, and where; the Anti-Patterns section reinforces with a concrete counter-example ("Line 91: 'k6' mentioned without hyperlink")
- [x] PASS: Output includes quality score in X/15 format and line count with the 150–300 target — the output format template shows `**Lines:** {count} (target: 150–300)` and `**Quality score:** {X}/15 criteria met ({Y} N/A)` in the Summary block
- [x] PASS: Model correctness is checked for sonnet — Criterion 14 table maps specialists to sonnet; devops is a specialist so sonnet is expected
- [x] PASS: Tool links criterion checks external tools in prose for markdown hyperlinks on first mention — Criterion 13 covers this; Anti-Patterns require citing the specific unlinked tool and line number
- [x] PASS: Recommended actions are prioritised — Step 5 mandates structural gaps first, then content gaps, then style issues
- [~] PARTIAL: Frontmatter description precision criterion checks role, domain summary, and trigger conditions — Criterion 15 specifies all three elements, but the output format evidence column only says `{includes role + domain + triggers?}` rather than requiring the actual description text to be quoted; the check is defined but quoting is implicit, not mandatory

## Output expectations

- [x] PASS: Output evaluates all 15 template criteria for the devops agent — all 15 rows present in the criteria table; none skipped
- [x] PASS: Output scores each criterion with specific evidence reference for non-MET findings — every ⚠️ row in the simulated output cites a line number and quotes the relevant text; ✅ rows also cite line ranges
- [x] PASS: Output reports quality score as X/15 and actual line count with 150–300 target band — Summary block states "264 lines (target: 150–300)" and "11/15 criteria met"
- [x] PASS: Output verifies model is sonnet for specialist agents — Criterion 14 row explicitly states `model: sonnet — correct for specialist agent`
- [x] PASS: Output's tool-links criterion checks agent body for third-party tool mentions and confirms markdown hyperlinks — Criterion 13 row lists Marten (line 59), Weasel (line 60), Celery (line 150), GitHub Actions (line 79) as unlinked; Recommended Actions item 2 provides suggested link targets
- [~] PARTIAL: Output's frontmatter description check verifies description includes role, domain summary, and trigger conditions, quoting the actual description — Criterion 15 row does quote the full description and confirms all three elements present; the skill's output template only says `{includes role + domain + triggers?}` without mandating a quote, so this was done as best practice, not as a required output element
- [x] PASS: Output's recommended actions are prioritised — Recommended Actions section separates structural gaps (Pre-Flight) → content gaps (tool links, private refs) → style/depth (principles count)
- [x] PASS: Output checks for private references / company names — Criterion 12 row flags "Weasel `ExtendedSchemaObjects`" at line 60 and "Neon Postgres" at line 79
- [x] PASS: Output verifies all mandatory sections per template are present — criteria table covers Pre-Flight (4), Output Format (6), Failure Caps (7), Decision Checkpoints (8), Collaboration (9), Principles (10), What You Don't Do (11) individually with line references
- [~] PARTIAL: Output identifies genuine gaps relative to peer specialist agents — the skill has no step for cross-agent comparison; the simulated output does not compare devops against architect or ai-engineer for depth parity because the skill's process does not include that step. The expectation is real and unmet

## Notes

The skill is well-structured with Anti-Patterns doing heavy lifting — naming failure modes with concrete counter-examples meaningfully constrains vague output. The evidence mandate in Step 4 is specific enough to produce consistent results.

Two real gaps surfaced in the simulated output that the existing result.md didn't surface: Pre-Flight on the devops agent is incomplete (reads rules but not CLAUDE.md), and four tools are unlinked. These are genuine findings, not edge cases.

The quoting requirement on Criterion 15 is scored PARTIAL on both sides consistently. In practice a model following this skill would likely quote the description because the output template implies it, but explicit is better than implicit.

The peer comparison criterion is genuinely unmet. The skill has no cross-agent comparison step and the simulated output reflects that. Scored PARTIAL (not SKIP) because the condition applies and the gap is real — it is an aspirational criterion the skill does not address.
