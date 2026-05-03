# Audit Agent

Scenario: A contributor asks for a full audit of the `devops` agent to check structural consistency before proposing it for the marketplace.

## Prompt

> /audit-agent devops

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Now I have everything I need to produce the audit report.

## Agent Audit: devops

### Summary
- **Lines:** 264 (target: 150–300)
- **Quality score:** 12/15 criteria met (0 N/A)
- **Model:** sonnet (correct)

### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (150–300) | ✅ | 264 lines |
| 2 | Core statement | ✅ | Line 10: "You own the runtime environment — how code gets to production and stays running." Second person, clear ownership |
| 3 | Non-negotiable rules | ✅ | Line 12: "All infrastructure is code. No manual console changes." Specific and falsifiable |
| 4 | Pre-Flight | ⚠️ | Line 17–18: Step 1 reads installed rules only — does not mention reading `CLAUDE.md` or `.claude/CLAUDE.md` as required by template |
| 5 | Mandatory methodology | ✅ | IaC section labelled "(ENFORCED)", incident response labelled "(sequential, blocking)", deployment rules framed as requirements not suggestions |
| 6 | Output format | ✅ | Lines 222–244: structured template with Evidence table, Resources Changed, Verification, and Runbook fields |
| 7 | Failure caps | ✅ | Lines 206–208: 3-failure rule on deployments and IaC applies; flaky pipeline rule present |
| 8 | Decision checkpoints | ✅ | Lines 210–220: 5 triggers with rationale (budget, security impact, data safety, secrets, risk profile) |
| 9 | Collaboration table | ✅ | Lines 248–257: 7 roles (CTO, Architect, Developers, Release Manager, Performance Engineer, Security Engineer, Internal Docs Writer) |
| 10 | Principles | ✅ | Lines 197–202: 5 principles (cattle not pets, shift left, least privilege, automate the toil, cost awareness) — domain-specific and opinionated |
| 11 | What You Don't Do | ✅ | Lines 259–263: 4 boundaries, each names the owning role (architect, release manager, developers, security engineer / GRC lead) |
| 12 | No private refs | ⚠️ | Lines 58–61: Schema Naming section references `Marten` and `Weasel ExtendedSchemaObjects` — open-source but .NET-stack-specific tools that imply a particular project's technology choices, not generic devops guidance |
| 13 | Tool links | ❌ | Line 59: `Marten` mentioned without hyperlink; line 61: `Weasel` mentioned without hyperlink; line 86: `CSharpier` mentioned without hyperlink. (Pulumi, Testcontainers, Moon, Storybook are correctly linked) |
| 14 | Correct model | ✅ | `model: sonnet` — correct for a specialist agent |
| 15 | Description precision | ✅ | Line 3: includes role ("DevOps / platform engineer"), domain ("infrastructure-as-code, CI/CD, deployment, monitoring, incident response"), and triggers ("Use for infrastructure work, pipeline configuration, deployment issues, or observability setup") |

### Recommended Actions

1. **Pre-Flight Step 1 (criterion 4):** Add explicit reads of `CLAUDE.md` and `.claude/CLAUDE.md` before the installed-rules check. Current text skips to rules only, which means the agent may miss project-level conventions entirely.

2. **Tool links (criterion 13):** Add hyperlinks on first mention for three unlinked tools:
   - Line 59: `[Marten](https://martendb.io)`
   - Line 61: `[Weasel](https://github.com/JasperFx/weasel)`
   - Line 86: `[CSharpier](https://csharpier.com)`

3. **Schema Naming section (criterion 12):** The Schema Naming subsection (lines 57–61) is .NET/Marten-specific and reads as project-level convention rather than generic devops guidance. Either move it to a project rule file (e.g., `devops--database-schema.md`) and reference it by name, or generalise it to "dedicate a schema per service; use whatever migration tooling your stack provides."

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.5/17.0 (97%) |
| Evaluated | 2026-05-01 |
| Target duration | 90924 ms |
| Target cost | $0.1600 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 reads the agent template file before evaluating the devops agent — uses the template criteria as the audit checklist | PASS | Opening line 'Now I have everything I need to produce the audit report' implies prior file reading; the 15-criteria table structure (Pre-Flight, Failure Caps, Decision Checkpoints, Collaboration, etc.) matches a defined template format, confirming template was consulted. |
| c2 | All 15 criteria are evaluated and scored (met, partially met, or missing) — none left blank | PASS | The table lists exactly 15 numbered rows, each with a ✅, ⚠️, or ❌ status. No row is blank or marked N/A. |
| c3 | Every non-passing criterion includes specific evidence: what was looked for, what was found or not found, and where (file location or line number) | PASS | Criterion 4 (⚠️): 'Line 17–18: Step 1 reads installed rules only — does not mention reading CLAUDE.md'; criterion 12 (⚠️): 'Lines 58–61: Schema Naming section references Marten and Weasel ExtendedSchemaObjects'; criterion 13 (❌): 'Line 59: Marten mentioned without hyperlink; line 61: Weasel mentioned without hyperlink; line 86: CSharpier mentioned without hyperlink.' All non-passing entries cite specific lines. |
| c4 | Output includes quality score in X/15 format and line count with the 150-300 line target | PASS | Summary section states 'Quality score: 12/15 criteria met (0 N/A)' and 'Lines: 264 (target: 150–300)'. |
| c5 | Model correctness is checked — devops is a specialist agent and should use sonnet, not opus | PASS | Criterion 14 row: 'Correct model ✅ \| `model: sonnet` — correct for a specialist agent'. Explicitly verified sonnet and gave the justification. |
| c6 | Tool links criterion checks that external tools mentioned in prose have markdown hyperlinks on first mention | PASS | Criterion 13 Evidence column names tools missing links (Marten, Weasel, CSharpier) and also confirms correctly linked tools: 'Pulumi, Testcontainers, Moon, Storybook are correctly linked'. |
| c7 | Recommended actions are prioritised — structural gaps listed before content gaps before style issues | PASS | Recommended Actions: #1 Pre-Flight Step 1 (structural gap), #2 Tool links (content gap — missing hyperlinks), #3 Schema Naming section (content/style — over-specific project convention). Structural first, then content, then style. |
| c8 | Frontmatter description precision criterion checks that the description includes role, domain summary, and trigger conditions in the required format | PARTIAL | Criterion 15 Evidence: 'Line 3: includes role ("DevOps / platform engineer"), domain ("infrastructure-as-code, CI/CD, deployment, monitoring, incident response"), and triggers ("Use for infrastructure work, pipeline configuration, deployment issues, or observability setup")'. All three elements checked and quoted. Ceiling capped at PARTIAL. |
| c9 | Output evaluates all 15 template criteria for the devops agent — none skipped, none assumed | PASS | Table rows 1–15 are all present with explicit status values (✅/⚠️/❌). No criterion is left unevaluated. |
| c10 | Output scores each criterion as MET / PARTIALLY MET / MISSING with a specific evidence reference (file path, line number, or quoted text) for non-MET findings | PASS | Each table row has an Evidence column. Non-passing entries (criteria 4, 12, 13) all cite line numbers (Lines 17–18, Lines 58–61, Lines 59/61/86). Passing entries cite line ranges confirming presence. |
| c11 | Output reports the quality score as `X/15` and the actual line count of the devops agent file, with the 150-300 line target band stated | PASS | 'Quality score: 12/15 criteria met (0 N/A)' and 'Lines: 264 (target: 150–300)' both appear in the Summary section. |
| c12 | Output verifies the model is `sonnet` (specialist agent) — flags as MISSING / wrong if it's `opus` or absent from the frontmatter | PASS | Criterion 14: '✅ \| `model: sonnet` — correct for a specialist agent'. Confirmed present and correct model value. |
| c13 | Output's tool-links criterion checks the agent body for third-party tool mentions (e.g. Terraform, Docker, GitHub Actions) and confirms each has a markdown hyperlink on first mention | PASS | Criterion 13 Evidence: lists Marten (line 59), Weasel (line 61), CSharpier (line 86) as missing links, and confirms 'Pulumi, Testcontainers, Moon, Storybook are correctly linked'. Both missing and present tool links are checked. |
| c14 | Output's frontmatter description check verifies the description includes the role, domain summary, and trigger conditions — quoting the actual description and flagging missing elements | PASS | Criterion 15 Evidence quotes the actual content: role 'DevOps / platform engineer', domain 'infrastructure-as-code, CI/CD, deployment, monitoring, incident response', triggers 'Use for infrastructure work, pipeline configuration, deployment issues, or observability setup'. No elements are flagged as missing, which is consistent with a ✅ rating. |
| c15 | Output's recommended actions are prioritised — structural gaps (missing Pre-Flight, missing Failure Caps, missing Decision Checkpoints) before content gaps (sparse domain methodology) before style (line-count outside band, banned words) | PASS | Recommended Actions: #1 Pre-Flight Step 1 (structural gap), #2 Tool links (content gap), #3 Schema Naming section (generalization/style). Pre-Flight is the only structural failing criterion and it is first. Failure Caps and Decision Checkpoints both passed so correctly absent from recommendations. |
| c16 | Output checks for private references / company names that shouldn't appear in a marketplace plugin | PASS | Criterion 12 (No private refs ⚠️): 'Lines 58–61: Schema Naming section references `Marten` and `Weasel ExtendedSchemaObjects` — open-source but .NET-stack-specific tools that imply a particular project's technology choices, not generic devops guidance'. Criterion and Recommended Action #3 both address this. |
| c17 | Output verifies all mandatory sections per template are present — Core, Non-negotiable, Pre-Flight, Output Format, Failure Caps, Decision Checkpoints, Collaboration, Principles, What You Don't Do | PASS | All nine mandatory sections are verified: Core statement (c2 ✅), Non-negotiable rules (c3 ✅), Pre-Flight (c4 ⚠️), Output format (c6 ✅), Failure caps (c7 ✅), Decision checkpoints (c8 ✅), Collaboration table (c9 ✅), Principles (c10 ✅), What You Don't Do (c11 ✅). Each maps to a numbered criterion row. |
| c18 | Output identifies any genuine gaps relative to peer specialist agents (e.g. compares devops sections against architect or ai-engineer for parity in depth) | FAIL | The audit report contains no mention of peer agents (architect, ai-engineer, or any other specialist). No cross-agent comparison appears anywhere in the output — not in the criteria table, not in the recommended actions, and not in any summary text. |

### Notes

The audit output is thorough and well-structured, passing 16 of 18 criteria. It correctly evaluates all 15 template criteria with line-level evidence for non-passing items, prioritises recommended actions from structural to content to style, verifies model correctness, and flags both missing tool hyperlinks and private/project-specific references. The one genuine gap is c18: no cross-agent peer comparison is present anywhere in the output. The PARTIAL ceiling on c18 means this contributes 0 to the total but only 0.5 to the max, limiting the score impact. The output is otherwise very complete for a template-driven audit.
