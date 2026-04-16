# Audit skill stub detection

A contributor asks for an audit of a specific skill that turns out to be a near-stub — correct frontmatter but minimal body content with no structured output format or rules section.

## Prompt

> /audit-skill performance-profile (performance-engineer)
>
> (The skill has valid frontmatter with a good description and argument-hint, an opening paragraph, and a single vague step saying "Profile the endpoint using your preferred tool and look for bottlenecks." No rules section, no output format template, no anti-patterns. 34 lines total.)

```markdown
[Step 1: Reading template]
Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md") ✓

[Step 2: Finding skill]
find plugins -path '*/performance-engineer/skills/performance-profile/SKILL.md' ✓ (34 lines)

## Output

### Skill Audit: performance-profile (performance-engineer)

#### Summary
- **Lines:** 34 (target: 100–500)
- **Quality score:** 3/12 criteria met
- **State:** Stub — Full rewrite needed

#### Criteria

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Line count (100–500) | ❌ | 34 lines — below the 50-line stub threshold |
| 2 | Description for auto-invocation | ✅ | Description includes what it produces and when to invoke |
| 3 | Self-contained | ❌ | "Profile the endpoint using your preferred tool and look for bottlenecks" — specifies no methodology |
| 4 | Sequential mandatory steps | ❌ | Only 1 step; not sequential; uses "look for" rather than imperative instruction |
| 5 | Verifiable step outputs | ❌ | No verifiable output defined for the single step |
| 6 | Rules with anti-patterns | ❌ | No rules section. "Preferred tool" is a choice, not a rule |
| 7 | Structured output format | ❌ | Skill ends after the single step with no markdown template |
| 8 | Cross-references | N/A | Skill has no workflow dependencies that require cross-references |
| 9 | Generic examples | ✅ | No private references found in the 34 lines |
| 10 | Tool links | N/A | No specific external tools mentioned |
| 11 | Argument hint | ✅ | argument-hint present and wrapped in brackets |
| 12 | Description precision | ❌ | Description field is adequate but skill body does not support the implied capability |

#### Recommended Actions
1. **Full rewrite required** (State: Stub) — rewrite must include sequential steps, a named profiling tool, a structured output template, and a rules section
2. **Add rules section** — at minimum: "Always establish a baseline before profiling. Never profile production without load-shedding controls"
3. **Add output format template** — structured table: endpoint, test scenario, baseline metrics, peak metrics, bottleneck type, fix recommendation
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/7.5 criteria met (100%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Step 1 reads the skill template before evaluating — the skill's Process section begins with Step 1: `Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md")`. The accompanying text states "The template defines the MANDATORY structure. The quality criteria at the bottom of the template are the audit checklist." This is the first step, before any skill is located.
- [x] PASS: All 12 criteria evaluated and scored — Step 3 defines all 12 criteria with ✅/⚠️/❌ scoring instructions. The Anti-Patterns section states "Scoring without reading — every criterion requires evidence from the actual file content." The Output Format shows a 12-row criteria table. Criterion 10 uses N/A when no tools are mentioned, which is an explicitly permitted scoring state per the Anti-Patterns note about edge cases.
- [x] PASS: 34 lines correctly classified as Stub — Criterion 1's line count table shows `< 50: ❌ Stub — needs full rewrite`. Step 4's classification table confirms "Stub: < 6 criteria passing or < 50 lines → Full rewrite needed." At 34 lines both conditions fire independently; the Stub classification is unambiguous.
- [x] PASS: Missing structured output format flagged with specific evidence — the Anti-Patterns section gives the exact finding pattern: "'Missing structured output format — skill ends with prose description instead of a markdown template' is a finding." Criterion 7 requires "a template showing the exact output structure" with "fields are specific (not 'present your findings')." A skill that ends after a single step has no template at all.
- [x] PASS: Missing rules section flagged as absent — Criterion 6 defines the requirement: "Must have a rules or anti-patterns section with specific imperatives... 'Always X' / 'Never Y' style rules." A "preferred tool" mention is explicitly a choice, not a rule. The definition distinguishes between imperatives and suggestions.
- [x] PASS: Self-containment evaluated — Criterion 3 requires the skill to "define its own methodology" and states "A reader encountering this skill for the first time should understand what to do." "Look for bottlenecks" without naming a tool, defining a method, or specifying output fails this: no methodology, no tool, no output.
- [x] PASS: State classified as Stub with action "Full rewrite needed" — Step 4's classification table states "Stub: < 6 criteria passing or < 50 lines → Full rewrite needed." Both triggers are met independently at 34 lines. The required action label matches the criterion exactly.
- [~] PARTIAL: Recommended actions include specific guidance — Step 5 specifies the Recommended Actions field as `{highest priority fix with specific guidance}`. The "with specific guidance" language implies specificity is required. The skill does not define what constitutes specific guidance vs vague guidance in the full-rewrite case — it sets the expectation but leaves the substance to judgment. PARTIAL ceiling applies per criterion prefix.

## Notes

The Stub classification has two independent triggers (< 50 lines OR < 6 criteria passing). This means a skeleton skill with correct frontmatter and a few passing criteria cannot escape the Stub classification by having good metadata. The design correctly separates structural completeness (line count) from criterion scoring. The Anti-Patterns note on edge cases ("thinking skills and plugin-curator skills have different structures") is the right escape valve — it allows N/A scoring without breaking the classification logic.

No changes since previous evaluation. Verdict unchanged at PASS (100%).
