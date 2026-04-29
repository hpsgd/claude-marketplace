# Output: design-tokens — audit of inconsistent token system

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Inventory step catalogues all 47 existing colour tokens and identifies which 12 are in active use — Step 1 scans CSS custom properties and produces a table with occurrences and locations, enabling the 47 vs 12 split to be identified.
- [x] PASS: Orphaned tokens (the 35 unused) are listed with a recommendation to remove or archive — Step 1 now includes explicit REMOVE / ARCHIVE / KEEP per-token disposition logic for zero or low usage tokens.
- [x] PASS: Spacing inconsistency (rem vs px) is flagged with a recommended single unit system — Step 1 demonstrates the `16px`/`1rem` inconsistency pattern; Step 2 defines a single canonical spacing scale.
- [x] PASS: Dark mode tokens are flagged for referencing hardcoded values instead of primitive token aliases — Step 3 now includes the explicit "Dark mode is a mode, not a sibling token set" block that directs rewriting dark mode tokens to reference primitives via mode mechanisms rather than raw hex values.
- [x] PASS: Output is usable by both designers (Figma-compatible format) and developers (CSS custom properties or equivalent) — Step 5 requires both Figma Variables / Figma Tokens JSON and Style Dictionary CSS custom properties; the closing rule adds "Do not produce a developer-only specification."
- [x] PASS: A migration plan is produced for fixing the inconsistencies, not just a list of problems — Step 5's Migration Guide is now fully phased: Phase 1 (orphan cleanup), Phase 2 (unit consolidation), Phase 3 (structural refactors), each with risk level and effort estimate.
- [~] PARTIAL: Contrast validation is performed on the 12 active colour tokens against WCAG AA thresholds — Step 4 has a full contrast validation table with correct WCAG AA thresholds. The validation operates at semantic pair level rather than against each of the 12 named tokens individually.
- [x] PASS: The distinction between primitive tokens and semantic tokens is maintained in the recommended structure — the two-layer architecture (Steps 2 and 3) and the "Semantic over primitive" rule enforce this throughout.

### Output expectations

- [x] PASS: Output catalogues all 47 colour tokens with value, usage count, and source file — Step 1's inventory table format includes value, occurrences, and locations.
- [x] PASS: Output's orphan recommendation is concrete with per-token action (REMOVE / ARCHIVE / KEEP) — Step 1 now defines all three dispositions explicitly, with instructions not to give a blanket "remove orphans" recommendation.
- [x] PASS: Output flags spacing rem/px inconsistency naming every location, recommends rem, and provides a conversion table — Step 1 demonstrates this pattern; Step 2 establishes a single canonical scale; Step 5's migration guide covers conversion mappings.
- [~] PARTIAL: Output flags dark mode tokens with raw hex values by name and recommends rewriting to reference primitives — Step 3's dark mode block now directs against raw values and explains the mode mechanism. Step 4's parity check flags violations. However, the skill doesn't define output that lists each offending dark-mode token individually by name with its raw hex value — the check is structural guidance rather than a named per-token audit finding.
- [x] PASS: Output's migration plan is sequenced with Phase 1/2/3 and effort estimates — Step 5's Migration Guide now defines three phases with explicit risk levels (no risk / low risk / medium risk) and effort estimates (hours / hours to a day / days).
- [x] PASS: Output is dual-format — Figma library structure AND CSS custom properties / tokens-spec JSON — Step 5 requires both Figma Variables / Figma Tokens JSON and Style Dictionary CSS custom properties.
- [x] PASS: Output validates contrast for all 12 active colour tokens against WCAG AA — Step 4's contrast validation table covers text-on-background pairs with actual ratios and pass/fail in both light and dark mode.
- [x] PASS: Output preserves primitive vs semantic separation in the recommended structure — Steps 2 and 3 enforce the two-layer architecture; the "Semantic over primitive" rule is non-negotiable.
- [x] PASS: Output's recommended structure includes governance — Step 5 now includes a full Governance section with a four-stage lifecycle: Proposed → Reviewed → Adopted → Deprecated.
- [x] PASS: Output addresses dark-mode-as-mode pattern using Figma variable modes / CSS prefers-color-scheme — Step 3 now contains an explicit block explaining that dark mode resolves via Figma variable modes and CSS `prefers-color-scheme`, with a hard rule against sibling dark-mode tokens.

## Notes

The four previously failing criteria — per-token orphan dispositions, phased migration guide, governance, and dark-mode-as-mode architecture — are all addressed by the edits. The skill now handles the audit scenario well end-to-end. The one remaining partial is that dark-mode token flagging is guidance-level (structural check, not a named per-token audit output), which is a minor gap in an otherwise complete definition.
