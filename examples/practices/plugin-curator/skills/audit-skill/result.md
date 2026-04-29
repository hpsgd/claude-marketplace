# Output: audit-skill stub detection

**Verdict:** PASS
**Score:** 16/18 criteria met (89%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Step 1 reads the skill template before evaluating — Process opens with `Read(file_path="${CLAUDE_PLUGIN_ROOT}/templates/skill-template.md")` and states "The template defines the MANDATORY structure. The quality criteria at the bottom of the template are the audit checklist." This fires before Step 2 locates any skill.
- [x] PASS: All 12 criteria evaluated and scored — Step 3 lists criteria 1 through 12 with ✅/⚠️/❌ scoring and Anti-Patterns prohibit "Scoring without reading — every criterion requires evidence." The Output Format template has all 12 rows. N/A is explicitly permitted for criteria 8 and 10 when no workflow dependency or external tool is present.
- [x] PASS: 34 lines correctly classified as Stub — Criterion 1's table maps `< 50 | ❌ Stub — needs full rewrite`. Step 4's classification table adds a second trigger: "< 6 criteria passing or < 50 lines → Full rewrite needed." At 34 lines both triggers fire independently.
- [x] PASS: Missing structured output format flagged with evidence — Anti-Patterns states: "'Missing structured output format — skill ends with prose description instead of a markdown template' is a finding." Criterion 7 requires a template with "specific" fields and prohibits "present your findings" as acceptable content.
- [x] PASS: Missing rules section flagged as absent — Criterion 6 requires "Always X / Never Y style rules (not suggestions)" and "Anti-patterns explain what NOT to do and why." A mention of a "preferred tool" is a suggestion, not an imperative rule. The criterion distinguishes these explicitly.
- [x] PASS: Self-containment evaluated — Criterion 3 requires the skill to "define its own methodology" and states "A reader encountering this skill for the first time should understand what to do." A step saying "look for bottlenecks" with no named methodology, tool, or output fails all three checks.
- [x] PASS: Overall state classified as Stub with action "Full rewrite needed" — Step 4's classification table states "Stub: < 6 criteria passing or < 50 lines → Full rewrite needed." Both conditions independently trigger for a 34-line skill. The action label matches the test criterion exactly.
- [~] PARTIAL: Recommended actions include specific guidance — Step 5 specifies the recommended actions field as `{highest priority fix with specific guidance}`. The "with specific guidance" language sets an expectation, but the skill does not define what constitutes specific guidance in the full-rewrite case. The enforcement is nominal rather than structural.

### Output expectations

- [x] PASS: Output classifies performance-profile as STUB — the skill's classification table has a hard line-count trigger at < 50 lines that cannot be escaped by frontmatter quality. A 34-line skill is Stub regardless of criteria scores.
- [x] PASS: Action recommendation is "Full rewrite needed" — Step 4's table maps the Stub state to exactly this action label, not a softer recommendation.
- [x] PASS: All 12 template criteria evaluated — Step 3 defines all 12 with scoring instructions. None are optional; Anti-Patterns prohibit "Scoring without reading."
- [x] PASS: Each criterion scored with specific evidence — the Output Format template mandates an Evidence column: `{quote or issue}`, `{evidence}`, `{step count, structure}` etc. The skill requires evidence per criterion, not just a status symbol.
- [x] PASS: Missing output format finding cites the exact symptom — Anti-Patterns provides the canonical finding language: "Missing structured output format — skill ends with prose description instead of a markdown template." Criterion 7 independently requires a "copy-pasteable" template with specific fields. A skill ending after one vague step has no Output section and no template; the finding language is mandated.
- [x] PASS: Self-containment evaluation flags "look for bottlenecks" / "preferred tool" — Criterion 3 requires the skill to "define its own methodology" and for "a reader encountering this skill for the first time" to "understand what to do." Neither condition is met by "use your preferred tool and look for bottlenecks." An agent invoking this skill has no executable instruction.
- [x] PASS: Missing rules finding distinguishes soft prose from a Rules section — Criterion 6 is explicit: rules must be "Always X / Never Y style rules (not suggestions)." Anti-Patterns reinforces: "Passing stubs — a 9-line skill with correct frontmatter is still ❌ on most criteria." A casual mention of a preferred tool is a suggestion; it does not constitute an anti-patterns section.
- [x] PASS: Line count and target band reported explicitly — the Output Format template includes `Lines: {count} (target: 100–500)` and Criterion 1's table lists every band including `< 50: ❌ Stub`. Both the count and the threshold appear in the required output structure.
- [~] PARTIAL: Rewrite recommendation includes specific guidance on what to include — the recommended actions field uses `{highest priority fix with specific guidance}` as a placeholder, and the Anti-Patterns section prohibits "needs improvement" as a finding. However, the skill does not enumerate what a stub rewrite must contain (multi-step process, named tools, output format template, anti-patterns list) — that substance is left to the evaluating agent's judgment rather than enforced by the skill definition.
- [-] SKIP: Output references the related performance-engineer agent for context — the skill contains no instruction to consult the parent agent's definition during audit or to align rewrite guidance with the parent agent's methodology. There is no mechanism for this in the skill. The criterion is marked PARTIAL in the test, but the skill provides no basis for it at all; scored as SKIP (condition-dependent: only applies if skill instructs cross-referencing the parent agent, which it does not).

## Notes

The dual-trigger Stub classification (< 50 lines OR < 6 criteria passing) is well-designed. A skeleton with good frontmatter cannot game its way to a higher classification via two passing criteria. The Anti-Patterns section is unusually strong — it provides canonical finding language that an evaluator would use verbatim, which is the right approach for a skill where wording precision matters.

The one structural gap is that the recommended actions placeholder does not specify what a stub rewrite must include. The skill tells the evaluator to be specific but does not define what specificity looks like in the full-rewrite case. A future revision could add a rewrite checklist (steps, named tools, output template, rules section) as required elements for any Stub recommendation.

The parent-agent cross-reference criterion in the output expectations has no basis in the skill definition. The skill does not instruct auditors to consult the parent agent's definition, so any output doing so would be the evaluating agent's initiative, not the skill's instruction.
