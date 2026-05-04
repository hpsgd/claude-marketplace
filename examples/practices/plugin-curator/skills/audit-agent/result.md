# Audit Agent

Scenario: A contributor asks for a full audit of the `devops` agent to check structural consistency before proposing it for the marketplace.

## Prompt

> /audit-agent devops

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Agent Audit: devops

### Summary
- **Lines:** 258 (target: 150–300)
- **Quality score:** 14/15 criteria met (1 partial)
- **Model:** sonnet (correct — specialist agent)

### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (150–300) | ✅ | 258 lines |
| 2 | Core statement | ✅ | Line 10–11: "You own the runtime environment — how code gets to production and stays running..." (second person, clear ownership) |
| 3 | Non-negotiable rules | ✅ | Line 12: "All infrastructure is code. No manual console changes. Every change is reviewable, versionable, and reproducible. Cattle not pets." (specific, falsifiable) |
| 4 | Pre-Flight | ⚠️ | Lines 16–27 present but incomplete: mentions "Check for installed rules" (line 16) but doesn't explicitly state "Read CLAUDE.md and .claude/CLAUDE.md" as Step 1 per template. Step 2 understanding patterns ✅, Step 3 classify work ✅ |
| 5 | Mandatory methodology | ✅ | Core sections use imperatives throughout: "All infrastructure is code," "Pin versions — no `latest`," "Every production deployment must be zero-downtime," "Every alert has a runbook link" (not suggestions) |
| 6 | Output format | ✅ | Lines 222–244: structured template with Evidence table, Resources Changed, Verification, Runbook (machine-parseable) |
| 7 | Failure caps | ✅ | Lines 204–208: "Deployment fails 3 times → STOP," "IaC apply fails 3 times → STOP," "Pipeline flaky → Fix" |
| 8 | Decision checkpoints | ✅ | Lines 210–220: 5 triggers with explanations (creating resources, network topology, database, secrets, deployment strategy) |
| 9 | Collaboration table | ✅ | Lines 246–256: 7 roles (CTO, Architect, Developers, Release Manager, Performance Engineer, Security Engineer, Internal Docs Writer) with collaboration patterns |
| 10 | Principles | ✅ | Lines 196–202: 5 opinionated, domain-specific principles (Cattle not pets, Shift left, Least privilege, Automate the toil, Cost awareness) |
| 11 | What You Don't Do | ✅ | Lines 258–263: 4 excluded activities each naming who owns them (architect, release manager, developers, security engineer + GRC lead) |
| 12 | No private refs | ✅ | Generic examples only: Pulumi, GitHub, Testcontainers, Moon, Marten, Weasel, Celery, Neon Postgres (no internal tools or company names) |
| 13 | Tool links | ✅ | Line 40: [Pulumi](https://www.pulumi.com), Line 69: [Testcontainers](https://testcontainers.com), Line 86: [Moon](https://moonrepo.dev), Line 86: [Storybook](https://storybook.js.org) — all linked |
| 14 | Correct model | ✅ | Line 5: sonnet (specialist, not leadership) |
| 15 | Description precision | ✅ | Line 3: includes role ("DevOps / platform engineer"), domain ("infrastructure-as-code, CI/CD, deployment, monitoring, incident response"), and triggers ("Use for infrastructure work, pipeline configuration, deployment issues, or observability setup") |

### Recommended Actions

1. **Pre-Flight Step 1 — Explicitly read CLAUDE.md first** (Line 16)
   
   Current: "Check for installed rules"
   
   Should be: "Read CLAUDE.md and .claude/CLAUDE.md. Check for installed rules in .claude/rules/ — these are your primary constraints."
   
   This aligns with the template requirement and ensures the agent always starts with project conventions before any work.

---

**Status:** Ready for use. One minor adjustment to Pre-Flight will bring it to 15/15.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-04 |
| Target duration | 34646 ms |
| Target cost | $0.1230 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 reads the agent template file before evaluating the devops agent — uses the template criteria as the audit checklist | PARTIAL | The 15 criteria used (Core statement, Non-negotiable rules, Pre-Flight, Failure caps, Decision checkpoints, etc.) are clearly template-derived, implying the template was consulted. However, the output opens directly with the summary table — there is no explicit statement that the template file was read as Step 1, no file path cited, and no narration of that step. |
| c2 | All 15 criteria are evaluated and scored (met, partially met, or missing) — none left blank | PASS | The table contains exactly 15 numbered rows, each with a status symbol (✅ or ⚠️) and evidence. No row is blank or skipped. |
| c3 | Every non-passing criterion includes specific evidence: what was looked for, what was found or not found, and where (file location or line number) | PASS | The only non-passing criterion (#4, Pre-Flight ⚠️) states: 'Lines 16–27 present but incomplete: mentions Check for installed rules (line 16) but doesn't explicitly state Read CLAUDE.md and .claude/CLAUDE.md as Step 1 per template.' Includes what was looked for, what was found, and specific line references. |
| c4 | Output includes quality score in X/15 format and line count with the 150-300 line target | PASS | Summary block shows 'Lines: 258 (target: 150–300)' and 'Quality score: 14/15 criteria met (1 partial)' — both elements present in the required format. |
| c5 | Model correctness is checked — devops is a specialist agent and should use sonnet, not opus | PASS | Criterion #14 in the table: 'Correct model ✅ \| Line 5: sonnet (specialist, not leadership)' — explicitly verifies model type and explains the specialist rationale. |
| c6 | Tool links criterion checks that external tools mentioned in prose have markdown hyperlinks on first mention | PASS | Criterion #13: 'Tool links ✅ \| Line 40: [Pulumi](https://www.pulumi.com), Line 69: [Testcontainers](https://testcontainers.com), Line 86: [Moon](https://moonrepo.dev), Line 86: [Storybook](https://storybook.js.org) — all linked' — confirms hyperlinks on first mention with line numbers. |
| c7 | Recommended actions are prioritised — structural gaps listed before content gaps before style issues | PASS | Only one recommended action is present: 'Pre-Flight Step 1 — Explicitly read CLAUDE.md first' — a structural gap. With a single action, the ordering is trivially correct and consistent with the priority rule (structural gaps first). |
| c8 | Frontmatter description precision criterion checks that the description includes role, domain summary, and trigger conditions in the required format | PARTIAL | Criterion #15 states: 'Description precision ✅ \| Line 3: includes role (DevOps / platform engineer), domain (infrastructure-as-code, CI/CD, deployment, monitoring, incident response), and trigger conditions (Use for infrastructure work, pipeline configuration, deployment issues, or observability setup)' — all three required elements checked with quotes. |
| c9 | Output evaluates all 15 template criteria for the devops agent — none skipped, none assumed | PASS | The criteria table contains rows #1 through #15, each with a status and evidence field. No criterion is left out or marked as assumed. |
| c10 | Output scores each criterion as MET / PARTIALLY MET / MISSING with a specific evidence reference (file path, line number, or quoted text) for non-MET findings | PASS | All criteria show ✅ (MET) or ⚠️ (PARTIAL). The ⚠️ finding (#4) includes line numbers (16–27) and quoted text ('Check for installed rules'). MET criteria also include line references and quoted text. |
| c11 | Output reports the quality score as `X/15` and the actual line count of the devops agent file, with the 150-300 line target band stated | PASS | 'Lines: 258 (target: 150–300)' and 'Quality score: 14/15 criteria met (1 partial)' both appear in the Summary section at the top of the output. |
| c12 | Output verifies the model is `sonnet` (specialist agent) — flags as MISSING / wrong if it's `opus` or absent from the frontmatter | PASS | Criterion #14: 'Correct model ✅ \| Line 5: sonnet (specialist, not leadership)' — model verified at a specific frontmatter line with the specialist/leadership distinction explained. |
| c13 | Output's tool-links criterion checks the agent body for third-party tool mentions (e.g. Terraform, Docker, GitHub Actions) and confirms each has a markdown hyperlink on first mention | PASS | Criterion #13 lists four tools found in the agent body (Pulumi, Testcontainers, Moon, Storybook) with their URLs and line numbers, concluding 'all linked'. The specific tools differ from the examples in the criterion (which are illustrative), consistent with the devops agent using Pulumi rather than Terraform. |
| c14 | Output's frontmatter description check verifies the description includes the role, domain summary, and trigger conditions — quoting the actual description and flagging missing elements | PASS | Criterion #15 explicitly quotes the description components: role ('DevOps / platform engineer'), domain ('infrastructure-as-code, CI/CD, deployment, monitoring, incident response'), and triggers ('Use for infrastructure work, pipeline configuration, deployment issues, or observability setup') — all three checked, all present. |
| c15 | Output's recommended actions are prioritised — structural gaps (missing Pre-Flight, missing Failure Caps, missing Decision Checkpoints) before content gaps (sparse domain methodology) before style (line-count outside band, banned words) | PASS | One recommended action is listed: Pre-Flight Step 1 (a structural gap). With a single action, ordering is trivially satisfied and consistent with the rule — structural gaps first. |
| c16 | Output checks for private references / company names that shouldn't appear in a marketplace plugin | PASS | Criterion #12: 'No private refs ✅ \| Generic examples only: Pulumi, GitHub, Testcontainers, Moon, Marten, Weasel, Celery, Neon Postgres (no internal tools or company names)' — explicitly checked and cleared. |
| c17 | Output verifies all mandatory sections per template are present — Core, Non-negotiable, Pre-Flight, Output Format, Failure Caps, Decision Checkpoints, Collaboration, Principles, What You Don't Do | PASS | All nine mandatory sections have dedicated criteria rows: Core statement (#2), Non-negotiable rules (#3), Pre-Flight (#4), Output format (#6), Failure caps (#7), Decision checkpoints (#8), Collaboration table (#9), Principles (#10), What You Don't Do (#11) — all verified. |
| c18 | Output identifies any genuine gaps relative to peer specialist agents (e.g. compares devops sections against architect or ai-engineer for parity in depth) | FAIL | No cross-agent comparison appears anywhere in the output. The audit evaluates the devops agent in isolation using the 15 template criteria only. Architect, ai-engineer, or any other peer agent is not mentioned. |

### Notes

The audit output is strong — all 15 template criteria are applied, every non-passing finding includes line-number evidence, the quality score and line count are correctly reported, and the recommended action is well-targeted. The two gaps are: (1) the output doesn't explicitly narrate reading the template file as Step 1 (the criteria are clearly template-derived but the step itself is invisible in the captured response), and (2) there is no cross-agent comparison against peer specialists like architect or ai-engineer, which c18 requires and which would surface depth-parity gaps. The single recommended action being a structural Pre-Flight fix is appropriate, though the small gap list (1 partial out of 15) may reflect the audit skill not finding genuine content or style issues that a stricter peer comparison would surface.
