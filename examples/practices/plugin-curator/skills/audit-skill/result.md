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

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Skill Audit: performance-profile (performance-engineer)

### Summary
- **Lines:** 13 (target: 100–500)
- **Quality score:** 1/12 criteria met
- **State:** **Stub** — needs full rewrite

### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (100–500) | ❌ | 13 lines — far below minimum threshold |
| 2 | Description for auto-invocation | ⚠️ | "Profile an endpoint or service and identify performance bottlenecks." — says what it produces but lacks trigger context (when/why to use it) |
| 3 | Self-contained | ❌ | No methodology or execution context. A user encountering this skill has no idea how to approach profiling or what framework/approach to use |
| 4 | Sequential mandatory steps | ⚠️ | Only one vague step ("Profile using your preferred tool"). Not sequential, not breaking down the process into blocking stages |
| 5 | Verifiable step outputs | ❌ | Step ends with "look for bottlenecks" — no specified output format or verification criteria |
| 6 | Rules with anti-patterns | ❌ | Rules section missing entirely |
| 7 | Structured output format | ❌ | Output Format section missing. Skill ends after Step 1 with no template |
| 8 | Cross-references | ❌ | No references to related skills (e.g., load testing, monitoring setup, instrumentation). Profiling often feeds into or depends on other skills |
| 9 | Generic examples | N/A | No examples present |
| 10 | Tool links | ❌ | Mentions "your preferred tool" but names no tools or provides links to profiling frameworks (k6, Locust, Lighthouse, async-profiler, etc.) |
| 11 | Argument hint | ✅ | `[endpoint or service name]` — clear and properly wrapped |
| 12 | Description precision | ⚠️ | Too generic — doesn't distinguish from other performance work. Lacks specificity about whether this is for load testing, bottleneck analysis, flame graphs, memory profiling, etc. |

### Recommended Actions

1. **Expand to full skill (100–500 lines)** — Define a complete methodology with:
   - Step-by-step profiling process (establish baseline → profile under load → analyze results → document bottlenecks)
   - Specific tool recommendations (k6, Lighthouse, Python profilers, Go pprof, etc.)
   - Rules on what constitutes a bottleneck and when to stop profiling
   - Structured output template (bottleneck list with severity, location, measured impact)

2. **Clarify description and scope** — Specify the context:
   - Is this for web endpoints, background services, CLI tools, microservices?
   - Is it focused on latency, throughput, memory, CPU, or all?
   - When should this skill be used vs. other performance work?

3. **Add executable steps** — Each step should produce verifiable artifacts:
   - Step 1: Establish baseline metrics
   - Step 2: Run profiler under representative load
   - Step 3: Analyze results and identify bottlenecks
   - Step 4: Document findings in structured format

4. **Reference related skills** — If this project has skills for:
   - Load testing, instrumentation, monitoring, benchmarking
   - Link them so users understand the workflow

5. **Provide tool guidance** — Link to profiling tools and explain which to use based on tech stack.

---

**State: STUB** — This skill requires a complete rewrite from the methodology up. The current version is a skeleton with correct frontmatter but no executable content.

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
| Verdict | PARTIAL |
| Score | 12.5/16.0 (78%) |
| Evaluated | 2026-05-03 |
| Target duration | 34791 ms |
| Target cost | $0.0807 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 reads the skill template before evaluating — uses template criteria as the audit checklist | FAIL | The captured output shows no explicit step where a skill template is read. The 12-criterion framework used is consistent with a template, but no 'Reading skill template...' or equivalent action is shown. The output jumps directly to the summary table. |
| c2 | All 12 criteria are evaluated and scored — none skipped or assumed | PASS | The table shows exactly 12 rows, all evaluated: criteria 1–12 each receive a status symbol (✅, ⚠️, ❌) and evidence text. Criterion 9 receives 'N/A — No examples present' rather than being silently omitted. |
| c3 | Line count of 13 is correctly classified as a Stub (below 50 lines) — not scored as 'Needs expansion' | PASS | The summary explicitly states 'Lines: 13' and 'State: Stub — needs full rewrite'. The bottom footer also reads 'State: STUB — This skill requires a complete rewrite from the methodology up.' |
| c4 | Missing structured output format is flagged with evidence: "skill ends after the single step with no markdown template" | PASS | Criterion 7 in the table reads: 'Output Format section missing. Skill ends after Step 1 with no template' — directly matching the expected evidence phrase. |
| c5 | Missing rules/anti-patterns section is flagged as absent — a note about "preferred tool" is not a rule | PASS | Criterion 6 states 'Rules section missing entirely.' The 'preferred tool' mention is evaluated separately under criterion 10 (tool links) as a deficiency, not credited as a rules section. |
| c6 | Self-containment is evaluated — "look for bottlenecks" without specifying how fails the self-contained criterion | PARTIAL | Criterion 3 evaluates self-containment: 'No methodology or execution context. A user encountering this skill has no idea how to approach profiling or what framework/approach to use.' The phrase 'look for bottlenecks' is quoted in criterion 5 (verifiable outputs) — 'Step ends with "look for bottlenecks" — no specified output format' — but not in the self-containment row itself. |
| c7 | Overall state is classified as Stub (not Complete or Needs expansion) with the correct action: "Full rewrite needed" | PASS | Summary banner: 'State: Stub — needs full rewrite.' Footer: 'State: STUB — This skill requires a complete rewrite from the methodology up. The current version is a skeleton with correct frontmatter but no executable content.' |
| c8 | Recommended actions include specific guidance on what the rewrite must include — not just "write more content" | PARTIAL | Recommended Action 1 specifies: step-by-step profiling process (baseline → profile under load → analyze → document), specific tool examples (k6, Lighthouse, Python profilers, Go pprof), rules on what constitutes a bottleneck, and a structured output template. Not merely 'write more content.' |
| c9 | Output classifies the performance-profile skill as a STUB (not "Complete" or "Needs expansion") given 13 lines, missing rules section, missing output format, and a single vague step | PASS | Summary header: 'State: Stub — needs full rewrite' with Quality score 1/12. All four cited factors appear in the table: 13 lines (c1), rules missing (c6), output format missing (c7), single vague step (c4 — 'Only one vague step'). |
| c10 | Output's overall action recommendation is "Full rewrite needed" — not "fill in the missing sections" — given how little content is present | PASS | Footer explicitly states: 'This skill requires a complete rewrite from the methodology up.' Recommended Action 1 says 'Expand to full skill (100–500 lines) — Define a complete methodology.' The framing is rewrite, not patch. |
| c11 | Output evaluates all 12 template criteria — even ones that score MISSING, none skipped | PASS | The table contains exactly 12 numbered rows, all with status and evidence text. Even criterion 9 (Generic examples), which would be N/A for a stub, is addressed with 'N/A — No examples present' rather than omitted. |
| c12 | Output scores each criterion as MET / PARTIALLY MET / MISSING with specific evidence — e.g. "no `## Output Format` heading found in the file" not "output format is missing" | PARTIAL | Several criteria cite specific file text (criterion 2 quotes the description, criterion 5 quotes 'look for bottlenecks', criterion 10 quotes 'your preferred tool'). But criterion 6 says only 'Rules section missing entirely' without citing the file structure, and criterion 7 says 'Output Format section missing' which approaches the disallowed phrase 'output format is missing' — saved only by the addition of 'Skill ends after Step 1 with no template.' |
| c13 | Output's missing-output-format finding cites the exact symptom — "skill ends after the single step with no markdown template / no Output section heading" — not just "no output format" | PASS | Criterion 7 reads: 'Output Format section missing. Skill ends after Step 1 with no template.' This matches the required phrasing 'skill ends after the single step with no markdown template.' |
| c14 | Output's self-containment evaluation flags "look for bottlenecks" / "preferred tool" as failing — explaining that another agent invoking this skill cannot proceed without external knowledge of what tools and what bottleneck patterns to look for | PARTIAL | Criterion 3 (self-contained) says 'A user encountering this skill has no idea how to approach profiling or what framework/approach to use.' It refers to a 'user' not an 'agent,' and doesn't cite 'look for bottlenecks' or 'preferred tool' in the self-containment row. 'Preferred tool' appears in criterion 10 and 'look for bottlenecks' appears in criterion 5, not consolidated into the self-containment failure explanation. |
| c15 | Output's missing-rules-section finding distinguishes "soft guidance phrasing in prose" from a Rules section with anti-patterns — the casual mention of preferred tools is NOT a rules section | PARTIAL | Criterion 6 declares 'Rules section missing entirely.' Criterion 10 separately flags 'Mentions "your preferred tool" but names no tools.' The placement of the 'preferred tool' quote under tool links rather than rules implicitly distinguishes them, but the output never explicitly states that the casual tool mention is not a rules section. |
| c16 | Output reports the line count (13) and the target band (50-300 lines for a complete skill) explicitly, classifying 13 as below the stub threshold | PARTIAL | The output reports 'Lines: 13 (target: 100–500)' — the line count is correct and classified as Stub, but the target band stated is 100–500, not 50–300 as the criterion specifies. The threshold numbers differ, making this an incomplete match. |
| c17 | Output's rewrite recommendation includes specific guidance — what the rewritten skill must contain (multi-step process, named tools per stack, output format template with sections, anti-patterns list, rules) — not just "expand it" | PASS | Recommended Action 1 lists: multi-step process (baseline → profile → analyze → document), named tools (k6, Lighthouse, Python profilers, Go pprof), structured output template (bottleneck list with severity, location, measured impact), and 'Rules on what constitutes a bottleneck.' Anti-patterns are implied via the rules mention. Specific, not generic. |
| c18 | Output references the related performance-engineer agent for context — the skill is owned by performance-engineer, so the rewrite should align with the parent agent's methodology and not duplicate it | FAIL | The captured output makes no mention of the performance-engineer parent agent at any point. Recommended Action 4 generically says 'If this project has skills for load testing...' without referencing the owning agent or its methodology. |

### Notes

The output is a competent stub audit that correctly identifies the skill as a Stub requiring a full rewrite, evaluates all 12 criteria with a structured table, and provides actionable rewrite guidance naming specific tools and methodologies. Its main weaknesses are: (1) no visible template-reading step shown before evaluation; (2) self-containment and rules-distinction findings lack the explicit specificity the criteria require (not quoting 'look for bottlenecks' in the self-containment row, not explicitly distinguishing soft prose from a rules section); (3) the target line-count band is reported as 100–500 rather than the expected 50–300; and (4) no reference to the performance-engineer parent agent for alignment context. The score of 78.1% falls just below the 80% PASS threshold.
