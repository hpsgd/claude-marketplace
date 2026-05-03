# Audit Skill

Scenario: A contributor asks for an audit of a specific skill that turns out to be a near-stub — correct frontmatter but minimal body content with no structured output format or rules section.

## Prompt

> First, create the stub skill file so it exists on disk:
> 
> ```bash
> mkdir -p plugins/engineering/performance-engineer/skills/performance-profile
> ```
> 
> ```markdown
> ---
> name: performance-profile
> description: Profile an endpoint or service and identify performance bottlenecks.
> argument-hint: "[endpoint or service name]"
> user-invocable: true
> allowed-tools: Read, Bash, Glob, Grep
> ---
> 
> Profile the endpoint or service at $ARGUMENTS.
> 
> ### Step 1: Profile
> 
> Profile the endpoint using your preferred tool and look for bottlenecks.
> ```
> 
> Write the above content to `plugins/engineering/performance-engineer/skills/performance-profile/SKILL.md`.
> 
> After writing the stub file, immediately run the skill — do not stop after the setup step.
> 
> /audit-skill performance-profile (performance-engineer)
> 
> Execution requirements (follow these when running the audit):
> 
> - Use the Read tool on `plugins/practices/plugin-curator/skills/audit-skill/SKILL.md` first — the 12 criteria there are the audit checklist. State which template file you read at the top of the audit (e.g., `Template: plugins/practices/plugin-curator/skills/audit-skill/SKILL.md`).
> - In every Evidence cell, quote the exact phrase from the audited skill that triggered the finding. In the Criterion 3 (Self-contained) row, quote both `look for bottlenecks` and `your preferred tool` directly and explain that another agent invoking the skill cannot proceed without external knowledge.
> - In the Criterion 6 (Rules with anti-patterns) row, explicitly state that the casual prose mention of "preferred tool" is NOT a rules section — distinguish soft prose guidance from a formal Rules section with anti-patterns.
> - In the Criterion 7 (Structured output format) row, cite the exact structural symptom: "skill ends after the single step with no markdown template / no Output Format heading".
> - Reference the parent agent (`performance-engineer`) by name in your Recommended Actions — at least one action must say the rewrite should align with that agent's methodology rather than duplicate it.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Skill Audit: performance-profile (performance-engineer)

**Template:** `/Users/martin/Projects/turtlestack/plugins/practices/plugin-curator/templates/skill-template.md`

### Summary
- **Lines:** 13 (target: 100–500)
- **Quality score:** 1/12 criteria met
- **State:** Stub — needs full rewrite

### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (100–500) | ❌ | 13 lines; stub well under minimum threshold |
| 2 | Description for auto-invocation | ❌ | "Profile an endpoint or service and identify performance bottlenecks" is generic — no specification of tool type, trigger context, or use case |
| 3 | Self-contained | ❌ | Vague prose leaves critical execution details to the reader. "Profile the endpoint using your preferred tool" requires external knowledge of what tools exist. "look for bottlenecks" is undefined — what counts? How are they documented? Reader cannot proceed without external expertise. |
| 4 | Sequential mandatory steps | ❌ | Single step with no mandatory structure. "Profile the endpoint..." reads as suggestion, not blocking procedure. No step progression or decision gates. |
| 5 | Verifiable step outputs | ❌ | Step produces no defined output. No template, format, or structure specified for what "profiling" produces. Impossible to verify completion. |
| 6 | Rules with anti-patterns | ❌ | No Rules section. Casual prose mentions "your preferred tool" — this is soft guidance, not formal imperatives or anti-patterns. Lacks domain-specific rules ("Always measure X under Y conditions", "Never profile without Z baseline"). |
| 7 | Structured output format | ❌ | No Output Format section. Skill ends after single step with no markdown template or Output Format heading. No fields defined, no structure provided for reader to produce output. |
| 8 | Cross-references | ⚠️ | No mention of related skills (performance optimization, load testing, monitoring, profiling tools). Parent agent methodology not referenced. |
| 9 | Generic examples | N/A | No examples present. |
| 10 | Tool links | N/A | "your preferred tool" is undefined; no specific tools named or linked. |
| 11 | Argument hint | ✅ | `[endpoint or service name]` — present, wrapped in brackets, guides user. |
| 12 | Description precision | ⚠️ | Present but too generic. Indistinguishable from other performance-related skills. Lacks specificity: what type of profiling (CPU, memory, latency, I/O)? What systems (web services, databases, batch jobs)? |

### Recommended Actions

1. **Align with `performance-engineer` agent methodology** — The parent agent likely has a defined performance review workflow. This skill should reference that methodology explicitly and implement its profiling phase as a concrete step sequence, not delegate to "your preferred tool."

2. **Define verifiable outputs** — Add structured output format section with specific fields: bottleneck type (CPU/memory/I/O/latency), location (function/query/endpoint), current vs. baseline metrics, and recommended action tier (critical/high/medium).

3. **Specify profiling tools with links** — Replace "your preferred tool" with concrete alternatives (e.g., [k6](https://k6.io/) for load testing, [Lighthouse](https://developers.google.com/web/tools/lighthouse) for web performance, [pprof](https://github.com/google/pprof) for Go, [cProfile](https://docs.python.org/3/library/profile.html) for Python). Include selection criteria.

4. **Add Rules section** — Anti-patterns like "Never profile without a baseline for comparison", "Always run 3+ iterations to account for variance", "Don't profile on production without read-only access."

5. **Expand to minimum 100 lines** — Add 3–4 sequential steps: (1) Select tool based on system type, (2) Establish baseline/control environment, (3) Profile under defined load/conditions, (4) Document findings in output format.

6. **Tighten description** — e.g., "Profile a web service or API endpoint under load using industry tools (k6, Lighthouse, wrk). Identify CPU, memory, latency, and throughput bottlenecks. Use when optimizing response times or investigating performance regressions."

### Artifacts written

#### `work/plugins/engineering/performance-engineer/skills/performance-profile/SKILL.md`

```
---
name: performance-profile
description: Profile an endpoint or service and identify performance bottlenecks.
argument-hint: "[endpoint or service name]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Profile the endpoint or service at $ARGUMENTS.

### Step 1: Profile

Profile the endpoint using your preferred tool and look for bottlenecks.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/18.0 (94%) |
| Evaluated | 2026-05-03 |
| Target duration | 41458 ms |
| Target cost | $0.0800 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 reads the skill template before evaluating — uses template criteria as the audit checklist | PASS | Output states 'Template: /Users/martin/Projects/turtlestack/plugins/practices/plugin-curator/templates/skill-template.md' at the top, and the audit evaluates exactly 12 numbered criteria consistent with reading a checklist template first. The file path differs from the instructed audit-skill/SKILL.md but the audit is grounded in a named template with 12 criteria. |
| c2 | All 12 criteria are evaluated and scored — none skipped or assumed | PASS | The output table contains rows for all 12 numbered criteria. Criteria 9 and 10 are marked 'N/A' with explanatory text ('No examples present' and 'your preferred tool is undefined; no specific tools named or linked') — these constitute evaluations, not skips. |
| c3 | Line count of 13 is correctly classified as a Stub (below 50 lines) — not scored as 'Needs expansion' | PASS | Summary section reads '**Lines:** 13 (target: 100–500)' and '**State:** Stub — needs full rewrite'. The classification is explicitly Stub, not 'Needs expansion'. |
| c4 | Missing structured output format is flagged with evidence: "skill ends after the single step with no markdown template" | PASS | Criterion 7 row states: 'Skill ends after single step with no markdown template or Output Format heading. No fields defined, no structure provided for reader to produce output.' The required phrase 'skill ends after the single step with no markdown template' appears verbatim (capitalisation aside). |
| c5 | Missing rules/anti-patterns section is flagged as absent — a note about "preferred tool" is not a rule | PASS | Criterion 6 row: 'No Rules section. Casual prose mentions "your preferred tool" — this is soft guidance, not formal imperatives or anti-patterns.' Explicitly flags absence of a rules section and explicitly distinguishes the prose mention from a rule. |
| c6 | Self-containment is evaluated — "look for bottlenecks" without specifying how fails the self-contained criterion | PASS | Criterion 3 row quotes the exact phrase: '"look for bottlenecks" is undefined — what counts? How are they documented? Reader cannot proceed without external expertise.' Both required phrases ('look for bottlenecks' and 'your preferred tool') are directly cited. |
| c7 | Overall state is classified as Stub (not Complete or Needs expansion) with the correct action: "Full rewrite needed" | PASS | Summary: '**State:** Stub — needs full rewrite'. Recommended Action 5 also says 'Expand to minimum 100 lines — Add 3–4 sequential steps' as part of a full rewrite prescription. |
| c8 | Recommended actions include specific guidance on what the rewrite must include — not just "write more content" | PARTIAL | Recommended Actions enumerate concrete items: verifiable output fields (bottleneck type CPU/memory/I/O/latency, location, metrics), named profiling tools (k6, Lighthouse, pprof, cProfile) with links, specific anti-patterns ('Never profile without a baseline', 'Always run 3+ iterations'), and 3–4 defined sequential steps. Specific and actionable, not generic. |
| c9 | Output classifies the performance-profile skill as a STUB (not "Complete" or "Needs expansion") given 13 lines, missing rules section, missing output format, and a single vague step | PASS | '**State:** Stub — needs full rewrite' in the Summary section. Quality score is '1/12 criteria met', reinforcing the Stub classification. |
| c10 | Output's overall action recommendation is "Full rewrite needed" — not "fill in the missing sections" — given how little content is present | PASS | Summary states '**State:** Stub — needs full rewrite'. Recommended Action 1 opens with 'Align with performance-engineer agent methodology' as the primary rewrite directive rather than incremental patching. |
| c11 | Output evaluates all 12 template criteria — even ones that score MISSING, none skipped | PASS | The criteria table has rows numbered 1 through 12, each with a status symbol and evidence text. No row is absent. Criteria 9 and 10 use 'N/A' but include explanatory text, indicating evaluation rather than omission. |
| c12 | Output scores each criterion as MET / PARTIALLY MET / MISSING with specific evidence — e.g. "no `## Output Format` heading found in the file" not "output format is missing" | PASS | Each row includes a specific evidence quote: criterion 1 quotes '13 lines; stub well under minimum threshold'; criterion 7 says 'Skill ends after single step with no markdown template or Output Format heading. No fields defined'; criterion 3 quotes the actual prose from the skill file. Evidence is drawn from the file contents, not generic statements. |
| c13 | Output's missing-output-format finding cites the exact symptom — "skill ends after the single step with no markdown template / no Output section heading" — not just "no output format" | PASS | Criterion 7 row: 'Skill ends after single step with no markdown template or Output Format heading.' This matches the required symptom phrasing precisely. |
| c14 | Output's self-containment evaluation flags "look for bottlenecks" / "preferred tool" as failing — explaining that another agent invoking this skill cannot proceed without external knowledge of what tools and what bottleneck patterns to look for | PASS | Criterion 3: '"Profile the endpoint using your preferred tool" requires external knowledge of what tools exist. "look for bottlenecks" is undefined — what counts? How are they documented? Reader cannot proceed without external expertise.' Both phrases quoted; external-knowledge explanation provided. |
| c15 | Output's missing-rules-section finding distinguishes "soft guidance phrasing in prose" from a Rules section with anti-patterns — the casual mention of preferred tools is NOT a rules section | PASS | Criterion 6: 'Casual prose mentions "your preferred tool" — this is soft guidance, not formal imperatives or anti-patterns.' Explicitly names the distinction between prose phrasing and a formal Rules section with anti-patterns. |
| c16 | Output reports the line count (13) and the target band (100-500 lines for a complete skill) explicitly, classifying 13 as below the stub threshold | PASS | Summary: '**Lines:** 13 (target: 100–500)'. Criterion 1 row: '13 lines; stub well under minimum threshold'. Both line count and target band are explicitly stated in the output. |
| c17 | Output's rewrite recommendation includes specific guidance — what the rewritten skill must contain (multi-step process, named tools per stack, output format template with sections, anti-patterns list, rules) — not just "expand it" | PASS | Recommended Actions specify: 3–4 sequential steps (select tool, establish baseline, profile under load, document findings); named tools k6, Lighthouse, pprof, cProfile with links; output fields (bottleneck type, location, current vs baseline metrics, action tier); anti-patterns ('Never profile without a baseline', 'Always run 3+ iterations', 'Don't profile on production without read-only access'). |
| c18 | Output references the related performance-engineer agent for context — the skill is owned by performance-engineer, so the rewrite should align with the parent agent's methodology and not duplicate it | PARTIAL | Recommended Action 1: 'Align with `performance-engineer` agent methodology — The parent agent likely has a defined performance review workflow. This skill should reference that methodology explicitly and implement its profiling phase as a concrete step sequence.' Names the parent agent and calls for alignment. Does not explicitly state 'do not duplicate' the parent agent's methodology. |

### Notes

The audit output is strong and hits nearly every criterion. All 12 template criteria are evaluated with specific evidence drawn from the skill file's actual text. The required exact phrases ('skill ends after the single step with no markdown template or Output Format heading', 'look for bottlenecks', 'your preferred tool') all appear verbatim in the relevant criterion rows. The Stub classification and full-rewrite recommendation are clearly stated. The only minor gaps: the template file cited is `templates/skill-template.md` rather than the `audit-skill/SKILL.md` prescribed in the execution requirements (though this does not affect criterion scoring meaningfully), and c18 references the performance-engineer agent for alignment without explicitly saying 'do not duplicate its methodology' — both capped-PARTIAL criteria receive their maximum 0.5 score. The overall output is well-structured and evidence-driven.
