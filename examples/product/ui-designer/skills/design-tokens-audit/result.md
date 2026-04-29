# Output: design-tokens — audit of inconsistent token system

| Field | Value |
|---|---|
| **Verdict** | FAIL |
| **Score** | 12.5/18 criteria met (69%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Inventory step catalogues all 47 existing colour tokens and identifies which 12 are in active use — Step 1 scans CSS custom properties and produces a table with occurrences and locations, enabling the 47 vs 12 split to be identified.
- [x] PASS: Orphaned tokens (the 35 unused) are listed with a recommendation to remove or archive — Step 1's inventory surfaces tokens with zero occurrences; Step 5's migration guide covers disposition for existing codebases.
- [x] PASS: Spacing inconsistency (rem vs px) is flagged with a recommended single unit system — Step 1 shows the exact `16px`/`1rem` inconsistency as a worked example; Step 2 defines a single consistent spacing scale.
- [x] PASS: Dark mode tokens are flagged for referencing hardcoded values instead of primitive token aliases — Step 1 scans for hardcoded hex; Step 3 requires dark mode values to reference primitives; Step 4's parity check flags tokens using raw values instead of aliases.
- [x] PASS: Output is usable by both designers (Figma-compatible format) and developers (CSS custom properties or equivalent) — Step 5 requires both Figma Variables / Figma Tokens JSON and Style Dictionary CSS custom properties. The closing rule adds teeth: "Do not produce a developer-only specification."
- [~] PARTIAL: A migration plan is produced for fixing the inconsistencies, not just a list of problems — Step 5 includes a Migration Guide section, but the skill defines it only as "mapping from old values to new tokens." No phased approach, risk levels, or effort estimates are defined. Partially met.
- [~] PARTIAL: Contrast validation is performed on the 12 active colour tokens against WCAG AA thresholds — Step 4 has a full contrast validation table with correct WCAG AA thresholds. However, the validation operates at semantic pair level, not against each of the 12 named tokens individually. Partially met.
- [x] PASS: The distinction between primitive tokens and semantic tokens is maintained in the recommended structure — the two-layer architecture (Steps 2 and 3) and the "Semantic over primitive" rule enforce this throughout.

### Output expectations

- [x] PASS: Output catalogues all 47 colour tokens with value, usage count, and source file — Step 1's inventory table format includes value, occurrences, and locations, covering all three required fields.
- [ ] FAIL: Output's orphan recommendation is concrete with per-token action (REMOVE / ARCHIVE / KEEP) — the skill produces a usage-count table and a migration guide, but no per-token disposition logic (REMOVE / ARCHIVE / KEEP triage) is defined anywhere. A blanket migration guide is not a per-token recommendation.
- [x] PASS: Output flags spacing rem/px inconsistency naming every location, recommends rem, and provides a conversion table — Step 1 explicitly demonstrates this pattern; Step 2 establishes a single canonical scale; Step 5's migration guide would include conversion mappings. Rem is used throughout the type scale.
- [~] PARTIAL: Output flags dark mode tokens with raw hex values by name and recommends rewriting to reference primitives — Step 4's parity check flags structural violations; Step 1 scans for hardcoded hex. However, the skill doesn't define output that names each offending dark-mode token individually with its raw hex value. The check is structural, not a named audit finding. Partially met.
- [ ] FAIL: Output's migration plan is sequenced with Phase 1/2/3 and effort estimates — the Migration Guide in Step 5 is described as "mapping from old values to new tokens." No phased sequencing, risk levels, or effort estimates are defined.
- [x] PASS: Output is dual-format — Figma library structure AND CSS custom properties / tokens-spec JSON — Step 5 explicitly requires both Figma Variables / Figma Tokens JSON and Style Dictionary CSS custom properties.
- [x] PASS: Output validates contrast for all 12 active colour tokens against WCAG AA — Step 4's contrast validation table covers text-on-background pairs with actual ratios and pass/fail in both light and dark mode.
- [x] PASS: Output preserves primitive vs semantic separation in the recommended structure — Steps 2 and 3 enforce the two-layer architecture; the "Semantic over primitive" rule is non-negotiable.
- [ ] FAIL: Output's recommended structure includes governance — no governance section exists anywhere in the skill. Nothing covers how new tokens get proposed, reviewed, or adopted, which means the orphan accumulation problem the scenario describes has no prevention mechanism.
- [ ] FAIL: Output addresses dark-mode-as-mode pattern using Figma variable modes / CSS prefers-color-scheme — the skill defines light/dark value columns in a table but doesn't address mode resolution (Figma variable modes, CSS `prefers-color-scheme`). The architectural distinction between sibling dark-mode tokens and mode-resolved tokens is absent.

## Notes

The skill is well-structured for token creation and covers the audit scenario's core needs — inventory, inconsistency flagging, primitive-semantic separation, and dual-format output. The gaps cluster in two areas. First, the migration plan is shallow: the skill names a Migration Guide as a required output section but leaves its content undefined beyond "mapping from old values to new tokens." For an audit use case, where the primary deliverable is a remediation path, this is a meaningful omission. Second, governance is entirely absent. The scenario describes a system with orphan accumulation as the presenting problem; a skill that audits without providing a token lifecycle process treats the symptom and ignores the cause. The dark-mode-as-mode gap is forward-looking — current Figma and CSS practice uses mode resolution rather than parallel sibling tokens, and the skill doesn't surface this pattern.
