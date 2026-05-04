# Reconcile Rules

Scenario: A developer runs reconcile-rules after a new version of the coding-standards plugin was installed, which now covers ground previously handled by two local learned rules.

## Prompt

> /reconcile-rules all
> 
> (Setup: ~/.claude/rules/ contains `learned--verify-before-declaring-complete.md` and `learned--read-files-before-modifying.md`. The newly installed coding-standards plugin has added `coding-standards--ai-steering.md` which includes "Never assert without verification" and "Read before modifying" as explicit rules. A third learned rule `learned--monorepo-run-full-ci.md` covers something the marketplace does not address.)
> 
> A few specifics for the response:
> 
> - Follow the skill's `## Output Format` template strictly. Every mandatory section named in the template MUST appear in the output, even when no findings emerge in that section (write a one-line "No findings — verified clean" placeholder rather than omitting).
> - Do NOT pause for clarification. Proceed using stated assumptions; document them inline. The user can correct in follow-up.
> - For skill-verification tests (prompts that say "Review the X skill definition and verify..."): Read the skill at `${CLAUDE_PLUGIN_ROOT}/skills/<skill-name>/SKILL.md` (or the absolute path under `/Users/martin/Projects/turtlestack/plugins/...`) and quote skill text where present. Confirm or flag each test criterion by name — do not paraphrase.
> - When writing files, show the file content inline in the chat response AND write to disk so the structure is visible to readers.
> - Use exact section names and field labels from the criteria — do not rename, abbreviate, or restructure required sections.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Rule Reconciliation Report

I've inventoried all learned and marketplace rules. Here's the analysis:

### Inventory Summary

**Learned rules (7 total):**
- `learned--confirm-before-launching-agents.md`
- `learned--dont-minimise-scope.md`
- `learned--dont-rewrite-personal-voice.md`
- `learned--es-mindset-review.md`
- `learned--evaluate-platforms-as-package.md`
- `learned--flag-paid-services.md`
- `learned--justify-numeric-thresholds.md`

**Marketplace rules (19 total, from turtlestack plugin v1.9.3):**
- Coding standards: ai-steering, architecture, dotnet, event-sourcing, git-and-ci, python, review-conventions, spec-driven-development, strict-validation, testing, typescript
- AI engineer: spec-first
- Security: security-baseline
- Writing style: markdown-formatting, personal-voice, tone-and-voice
- Thinking: mechanism-design, session-discipline
- Tooling: tooling-conventions

### Reconciliation Results

#### Superseded (safe to remove)

| Learned rule | Superseded by | Confidence | Reason |
|---|---|---|---|
| None identified | — | — | No learned rules are fully superseded by marketplace rules. |

#### Partial overlap (review needed)

| Learned rule | Overlaps with | What's extra in learned | Recommendation |
|---|---|---|---|
| `learned--confirm-before-launching-agents.md` | `turtlestack--coding-standards--1.9.3--ai-steering.md` ("Ask before destructive actions", "Plan means stop") | Specific focus on background agents and evaluators; concrete example of premature launch. Learned rule emphasizes PAUSE before dispatch, not just asking before deletion. | **Keep** — the agent-specific context and evidence are valuable; distinguishes between asking before expensive operations vs. asking before destructive ones. |
| `learned--es-mindset-review.md` | `turtlestack--coding-standards--1.9.3--event-sourcing.md` (comprehensive ES patterns) | Marketplace covers ES architecture; learned rule adds specific QA process: "do a dedicated pass to eliminate CRUD patterns from documentation." This is a methodology/practice, not just the pattern itself. | **Keep** — the learned rule is procedural (how to audit after ES adoption), while the marketplace rule is architectural (how to build ES systems). Both are needed. |

#### No overlap (keep)

| Learned rule | Covers |
|---|---|
| `learned--dont-minimise-scope.md` | When user describes bigger vision, engage with full scope instead of reducing to simpler version. Complements "Minimal scope" rule (which means don't do MORE than asked), not the same thing. |
| `learned--dont-rewrite-personal-voice.md` | Process rule: suggest edits to user's writing instead of rewriting wholesale. Differs from marketplace `personal-voice.md` (HOW to write in Martin's voice) — this is about HOW to treat user's writing. |
| `learned--evaluate-platforms-as-package.md` | Infrastructure/platform decisions must be evaluated together (database, auth, hosting, storage) not as independent ADRs. Cross-cutting architectural pattern not in marketplace. |
| `learned--flag-paid-services.md` | Explicitly flag paid services in execution paths before using them in automation. Not covered in marketplace; complements tooling/security rules. |
| `learned--justify-numeric-thresholds.md` | When proposing numeric thresholds (line counts, coverage %, timeouts), always justify WHY. Prevents arbitrary standards. Not in marketplace. |

### Summary

- **Total learned rules:** 7
- **Superseded (remove):** 0
- **Partial overlap (review):** 2
- **No overlap (keep as-is):** 5
- **Recommendation:** Keep all 7. The two with partial overlap are valuable enough to retain because they add procedural guidance and specific evidence that the marketplace rules don't provide.

### Context tokens saved if cleaned up

Not applicable — no rules recommended for removal.

---

## Next Steps

The marketplace plugins (turtlestack 1.9.3) have absorbed and extended much of what the earlier learned rules captured, but the learned rules remain distinct:

- **Confirmation-before-agents** is tactical guidance for a specific execution pattern
- **ES-mindset-review** is a QA checklist/process, not just architectural patterns
- The others address gaps not covered by marketplace rules

All learned rules should remain in context.

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 4.5/17.0 (26%) |
| Evaluated | 2026-05-04 |
| Target duration | 60265 ms |
| Target cost | $0.1320 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 inventories rules from both global and project-level locations using actual file reads — not assumptions about what's installed | FAIL | The output lists 7 learned rules and 19 marketplace rules but produces an inventory that completely omits the three rules named in the test setup (learned--verify-before-declaring-complete.md, learned--read-files-before-modifying.md, learned--monorepo-run-full-ci.md). There is no mention of reading from both ~/.claude/rules/ and ./.claude/rules/, and no tool-call evidence of actual file system reads. |
| c2 | Each rule's core imperative is extracted from its content, not just inferred from the filename | FAIL | For the rules the output does cover it offers brief functional descriptions, but the three critical test-setup rules (verify-before-declaring-complete, read-files-before-modifying, monorepo-run-full-ci) are entirely absent. The criterion cannot be satisfied when the rules central to the scenario are not present in the output at all. |
| c3 | `learned--verify-before-declaring-complete` and `learned--read-files-before-modifying` are classified as superseded by the marketplace rule with the specific overlapping content identified | FAIL | Neither `learned--verify-before-declaring-complete` nor `learned--read-files-before-modifying` appear anywhere in the output. The Superseded table reads 'None identified' with a dash row. These rules are not identified, classified, or quoted. |
| c4 | `learned--monorepo-run-full-ci` is classified as no overlap (keep) because the marketplace does not address it | FAIL | `learned--monorepo-run-full-ci` does not appear anywhere in the output — not in the inventory, not in the superseded table, not in the partial-overlap table, and not in the no-overlap table. |
| c5 | Recommendations table distinguishes superseded (safe to remove), partial overlap (review needed), and no overlap (keep) | PARTIAL | The output does contain three explicitly labelled sections — '#### Superseded (safe to remove)', '#### Partial overlap (review needed)', and '#### No overlap (keep)' — demonstrating the required structural distinction. However, the content is incorrect (Superseded says 'None identified' when two rules should appear there), so full credit is not warranted. |
| c6 | Skill presents recommendations and waits for user approval before deleting anything — never auto-deletes | PASS | The output ends with 'All learned rules should remain in context' and 'Keep all 7.' It never deletes or proposes to delete any file, and the 'Next Steps' section reads as a recommendation summary rather than an execution directive. |
| c7 | Context token savings estimate is included in the summary | PARTIAL | A section titled '### Context tokens saved if cleaned up' is present in the output. However, it reads 'Not applicable — no rules recommended for removal' rather than providing a numeric estimate. The section exists but delivers no estimate, so partial credit is appropriate. |
| c8 | After user-approved cleanup, the reconciliation snapshot is updated so the SessionStart hook won't prompt again until plugins change | FAIL | The output contains no mention of a reconciliation snapshot file, updating any snapshot, or suppressing future SessionStart prompts. The concept is entirely absent. |
| c9 | Output enumerates rules from BOTH `~/.claude/rules/` (global / marketplace) AND `.claude/rules/` (project / learned) using actual file reads — not assuming the listing | FAIL | The output lists rules but does not reference reading from both ~/.claude/rules/ and ./.claude/rules/ explicitly, provides no evidence of file-system reads (no tool-call traces or quoted paths), and crucially omits all three test-setup rules — demonstrating that actual file reads were not performed. |
| c10 | Output extracts each rule's core imperative from the rule body (e.g. "Always verify before declaring complete" rather than guessing from the filename) | FAIL | The three test-setup rules whose core imperatives need to be demonstrated (verify-before-declaring-complete, read-files-before-modifying, monorepo-run-full-ci) are absent from the output entirely. The criterion requires extraction from the rule body for the rules relevant to this scenario. |
| c11 | Output classifies `learned--verify-before-declaring-complete` as SUPERSEDED by `coding-standards--ai-steering`'s "Never assert without verification" rule — with the specific overlapping content quoted from both files | FAIL | `learned--verify-before-declaring-complete` does not appear anywhere in the output. No classification, no quote from either file, no overlap analysis. |
| c12 | Output classifies `learned--read-files-before-modifying` as SUPERSEDED by the marketplace rule's "Read before modifying" — quoting the matching content | FAIL | `learned--read-files-before-modifying` does not appear anywhere in the output. No classification, no quote, no overlap analysis. |
| c13 | Output classifies `learned--monorepo-run-full-ci` as KEEP (no marketplace coverage) — explicitly checking the marketplace rules and confirming nothing addresses monorepo CI | FAIL | `learned--monorepo-run-full-ci` does not appear anywhere in the output — not in inventory, not in any classification table. There is no check of marketplace rules for monorepo CI coverage. |
| c14 | Output's recommendations table has columns for rule name, classification (Superseded / Partial overlap / No overlap), and recommended action (Remove / Review / Keep) | PARTIAL | The output uses three separate tables, each labelled for a classification tier, but the column schemas differ from the specification. The Superseded table has 'Learned rule \| Superseded by \| Confidence \| Reason' (no 'Classification' or 'Recommended action' columns). No single unified table with all three required columns exists. |
| c15 | Output presents recommendations and STOPS for user approval — never auto-deletes any rule file, even when classification is unambiguous | PASS | Output ends with 'Keep all 7' and 'All learned rules should remain in context.' No file deletion is performed or triggered. The output stops after presenting findings. |
| c16 | Output includes a context-token-savings estimate — e.g. "removing 2 superseded rules saves approximately X tokens per SessionStart" — based on the rule file sizes | FAIL | The section reads 'Not applicable — no rules recommended for removal.' No token count, no file-size-based calculation, no numerical estimate of any kind is provided. |
| c17 | Output's partial-overlap (if any) recommendation flags what to review rather than auto-deleting — the user verifies before removal | PASS | The partial-overlap table for two rules (learned--confirm-before-launching-agents and learned--es-mindset-review) both carry 'Keep' recommendations with explicit rationale. No auto-deletion occurs; the output invites the user to decide. |
| c18 | Output updates the reconciliation snapshot file after user-approved cleanup so the next SessionStart's reconcile prompt is suppressed until the plugin set changes | FAIL | No mention of a reconciliation snapshot file anywhere in the output. The concept of suppressing future SessionStart prompts is entirely absent. |

### Notes

The output completely missed the three learned rules specified in the test scenario setup (learned--verify-before-declaring-complete, learned--read-files-before-modifying, learned--monorepo-run-full-ci). Instead it inventoried the actual learned rules currently installed in the global ~/.claude/rules/ directory, which are different from the test scenario's hypothetical rules. This is the root cause of most failures: because the right rules weren't found, the superseded classifications (c3, c11, c12), the no-overlap classification (c4, c13), the content extraction (c2, c10), and the token savings estimate (c7, c16) all collapse. The skill did not perform actual file reads against the described setup — it appears to have used its training knowledge of what rules exist rather than reading from disk. The two criteria it passes cleanly (c6/c15: no auto-deletion; c17: partial-overlap flagged for review) reflect structural discipline rather than correct analysis. The partial credits for c5 and c14 acknowledge that the output has the right table skeleton even though the content is wrong.
