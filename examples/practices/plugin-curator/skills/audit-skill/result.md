# Result: audit-skill stub detection

**Verdict:** PASS
**Score:** 16.5/18.5 criteria met (89%)
**Evaluated:** 2026-04-30

---

## Output

Simulated execution of `/audit-skill performance-profile (performance-engineer)` against the scenario described in test.md: a skill with valid frontmatter, one vague step, no rules section, no output format, 34 lines total.

---

## Skill Audit: performance-profile (performance-engineer)

### Summary

| Property | Value |
|---|---|
| **Lines** | 34 (target: 100–500) |
| **Quality score** | 2.5/12 criteria met |
| **State** | Stub |
| **Action** | Full rewrite needed |

---

### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (100–500) | ❌ | 34 lines — below 50-line stub threshold. Both independent triggers for Stub fire: < 50 lines and < 6 criteria passing |
| 2 | Description for auto-invocation | ✅ | Frontmatter description names the task and implies a trigger condition (performance investigation). Specific enough for Claude to auto-invoke |
| 3 | Self-contained | ❌ | "Profile the endpoint using your preferred tool and look for bottlenecks" requires external knowledge of (a) which tools apply to which stacks and (b) what bottleneck patterns to look for. An agent invoking this skill cold cannot proceed without that knowledge |
| 4 | Sequential mandatory steps | ❌ | Single step present. No numbered progression, no blocking structure. One vague instruction is not a process |
| 5 | Verifiable step outputs | ❌ | The single step produces no defined artefact. "Look for bottlenecks" does not specify what a completed step looks like or how it can be verified |
| 6 | Rules with anti-patterns | ❌ | No `## Rules` or `## Anti-Patterns` section present. The phrase "preferred tool" is soft guidance in prose — it is not an imperative rule, does not use "Always X / Never Y" structure, and does not describe what not to do or why |
| 7 | Structured output format | ❌ | Skill ends after the single vague step with no `## Output Format` heading, no markdown template, and no field definitions. There is nothing copy-pasteable as a starting point |
| 8 | Cross-references | ❌ | No references to related skills (e.g., load-test-plan, capacity-plan) despite clear workflow dependencies within the performance-engineer plugin |
| 9 | Generic examples | ✅ | No private company names, internal packages, or proprietary tool references |
| 10 | Tool links | ❌ | "Preferred tool" names no specific tools — no links possible. The absence of any named tool is itself a structural gap |
| 11 | Argument hint | ✅ | Frontmatter `argument-hint` present and bracketed |
| 12 | Description precision | ⚠️ | Description identifies the task type but does not distinguish this skill from a general performance debugging request. Does not name the artefact produced |

**Score: 3 ✅ + 1 ⚠️ (0.5) = 3.5/12 — Stub (< 6 criteria passing, < 50 lines)**

---

### Recommended Actions

1. **Full rewrite — do not patch.** With 34 lines, a single vague step, no output format, no rules section, and no cross-references, targeted fixes would still leave a skeleton. The rewrite must include:
   - A numbered multi-step process (at minimum: instrument → baseline → load → analyse → report)
   - Named tools per stack — e.g., [k6](https://k6.io) for HTTP load, [py-spy](https://github.com/benfred/py-spy) for Python CPU profiling, [dotnet-trace](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/dotnet-trace) for .NET
   - A `## Output Format` section with a markdown template: bottleneck summary table, p50/p95/p99 latency fields, identified hot paths, recommended fixes
   - A `## Rules` section with anti-patterns: e.g., "Never profile against production without a read-only replica," "Never report a single percentile — always report p50, p95, and p99," "Never classify a finding as a bottleneck without a reproduction threshold"
   - Cross-references to `load-test-plan` (provides inputs) and `capacity-plan` (consumes output)

2. **Align with the performance-engineer agent.** The rewrite should reference what the parent agent delegates vs. what the skill handles independently, to avoid duplication and ensure self-containment when invoked without agent context.

3. **Replace "preferred tool" with conditional tool selection.** Specify which tool applies under which conditions (language, runtime, infrastructure type) so any agent can execute the skill without external knowledge.

---

## Evaluation

### Criteria (definition quality)

- [x] PASS: Step 1 reads the skill template before evaluating — Process opens with `Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md")` and states "The template defines the MANDATORY structure. The quality criteria at the bottom of the template are the audit checklist." This fires before Step 2 locates any skill — met
- [x] PASS: All 12 criteria evaluated and scored — Step 3 defines criteria 1–12 with ✅/⚠️/❌ scoring and the Anti-Patterns section prohibits "Scoring without reading." The Output Format template has all 12 rows. N/A is explicitly permitted for criteria 8 and 10 when no dependency or tool exists — met
- [x] PASS: 34 lines correctly classified as Stub — Criterion 1's table maps `< 50` to ❌ Stub. Step 4's classification table adds a second trigger: `< 6 criteria passing or < 50 lines → Full rewrite needed`. Both fire independently for a 34-line skill — met
- [x] PASS: Missing structured output format flagged with evidence — Anti-Patterns states the canonical finding: "Missing structured output format — skill ends with prose description instead of a markdown template is a finding." Criterion 7 requires a copy-pasteable template with specific fields — met
- [x] PASS: Missing rules section flagged as absent — Criterion 6 requires "Always X / Never Y style rules (not suggestions)." The "preferred tool" mention is a suggestion. The criterion distinguishes these explicitly — met
- [x] PASS: Self-containment evaluated — Criterion 3 requires the skill to "define its own methodology" and states "A reader encountering this skill for the first time should understand what to do." A step saying "look for bottlenecks" with no named methodology or output fails both checks — met
- [x] PASS: Overall state classified as Stub with action "Full rewrite needed" — Step 4's table states "Stub: < 6 criteria passing or < 50 lines → Full rewrite needed." The action label matches the test criterion exactly — met
- [~] PARTIAL: Recommended actions include specific guidance — the output format uses `{highest priority fix with specific guidance}` as a placeholder. The Anti-Patterns section prohibits vague findings. However, the skill does not enumerate what a stub rewrite must contain (multi-step process, named tools, output template, anti-patterns list). The constraint is implied but not enforced structurally — partially met

### Output expectations (simulated output quality)

- [x] PASS: Output classifies performance-profile as STUB — 3.5/12 score, below 6, and 34 lines below 50. Both Stub triggers fire — met
- [x] PASS: Overall action is "Full rewrite needed" — stated in summary table and recommendation #1 — met
- [x] PASS: All 12 template criteria evaluated — each row populated, none skipped — met
- [x] PASS: Each criterion scored with specific evidence — e.g., "34 lines — below 50-line stub threshold", "no `## Output Format` heading found", "'preferred tool' is soft guidance in prose — not an imperative rule" — met
- [x] PASS: Missing output format cites exact symptom — "Skill ends after the single vague step with no `## Output Format` heading, no markdown template" — met
- [x] PASS: Self-containment evaluation flags "preferred tool" / "look for bottlenecks" — Criterion 3 row explains that an agent invoking the skill cold cannot proceed without external knowledge of tools and bottleneck patterns — met
- [x] PASS: Missing rules finding distinguishes soft prose from a Rules section — Criterion 6 row states "'preferred tool' is soft guidance in prose — it is not an imperative rule, does not use 'Always X / Never Y' structure, and does not describe what not to do or why" — met
- [x] PASS: Line count (34) and target band (100–500) reported explicitly, 34 classified as below stub threshold — met in summary table and Criterion 1 row — met
- [x] PASS: Rewrite recommendation includes specific guidance — recommendation #1 lists multi-step process, named tools per stack, output format template with specific sections, anti-patterns list, and cross-references — met
- [~] PARTIAL: Output references performance-engineer agent for context — recommendation #2 references the parent agent and advises aligning the rewrite with what the agent delegates vs. the skill handles independently. Addresses the intent but does not go deep on methodology alignment — partially met

## Notes

The dual-trigger Stub classification (< 50 lines OR < 6 criteria passing) is well-designed. A skeleton with good frontmatter cannot game its way to a higher classification. The Anti-Patterns section is strong — it provides canonical finding language verbatim, which is the right approach for a skill where wording precision matters.

The one structural gap: the recommended actions placeholder does not specify what a stub rewrite must contain. The skill tells the evaluator to be specific but does not define what specificity looks like in the full-rewrite case. A future revision could add a rewrite checklist (numbered steps, named tools, output template, rules section) as required elements for any Stub recommendation.

Note on line-count thresholds: the skill definition uses 100–500 as the target band and < 50 as the stub cutoff. The test scenario's expected output mentions "50-300 lines for a complete skill" — this does not match the skill's actual thresholds. The simulated output uses the skill's own numbers, which is correct.
