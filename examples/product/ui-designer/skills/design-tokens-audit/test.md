# Test: design-tokens — audit of inconsistent token system

Scenario: Testing the design-tokens skill with an audit request where the existing token system has orphaned tokens, mixed units, and dark mode tokens that bypass the primitive-semantic hierarchy.

## Prompt

/ui-designer:design-tokens audit our existing token system — we have 47 colour tokens but only 12 are actually used in components, the rest are orphaned. We also have spacing values defined in both rem and px across different files, and our dark mode tokens reference hardcoded hex values instead of primitive tokens.

## Criteria

- [ ] PASS: Inventory step catalogues all 47 existing colour tokens and identifies which 12 are in active use
- [ ] PASS: Orphaned tokens (the 35 unused) are listed with a recommendation to remove or archive
- [ ] PASS: Spacing inconsistency (rem vs px) is flagged with a recommended single unit system
- [ ] PASS: Dark mode tokens are flagged for referencing hardcoded values instead of primitive token aliases
- [ ] PASS: Output is usable by both designers (Figma-compatible format) and developers (CSS custom properties or equivalent)
- [ ] PASS: A migration plan is produced for fixing the inconsistencies, not just a list of problems
- [ ] PARTIAL: Contrast validation is performed on the 12 active colour tokens against WCAG AA thresholds
- [ ] PASS: The distinction between primitive tokens and semantic tokens is maintained in the recommended structure

## Output expectations

- [ ] PASS: Output catalogues all 47 colour tokens — listed with their value (hex / rgb), usage count, and source file — explicitly identifying the 12 in active use vs the 35 orphans
- [ ] PASS: Output's orphan recommendation is concrete — list each of the 35 orphans with a recommended action (REMOVE if truly unused, ARCHIVE if reserved for future use, KEEP if part of an unreleased palette being held) — not a blanket "remove orphans"
- [ ] PASS: Output flags the spacing rem/px inconsistency — names every place where each unit appears, recommends a single canonical unit (rem for accessibility scaling), and provides a conversion table for the migration
- [ ] PASS: Output flags the dark mode tokens that bypass the primitive layer — explicitly naming the offending tokens that hold raw hex values, recommending they be rewritten to reference primitive tokens (`{color-blue-500-dark}`)
- [ ] PASS: Output's migration plan is sequenced — Phase 1 (clean up orphans, no risk), Phase 2 (consolidate spacing units, low risk with find/replace), Phase 3 (refactor dark mode tokens to use primitives, medium risk requires component testing) — with effort estimates per phase
- [ ] PASS: Output is dual-format — the recommended token structure is shown both as Figma library structure (collections / variables) AND as code (CSS custom properties or tokens-spec JSON) — usable by both audiences
- [ ] PASS: Output validates contrast for all 12 active colour tokens against WCAG AA — text-on-background pairs tested at the typical use cases, with the actual ratio shown and any failing pairs flagged
- [ ] PASS: Output preserves the primitive vs semantic separation in the recommended structure — primitive tokens (raw values) form the bottom layer, semantic tokens (`color-action-primary`) reference primitives, never raw values
- [ ] PASS: Output's recommended structure includes governance — how new tokens get added in future (proposed → reviewed → adopted), to prevent the same orphan accumulation from recurring
- [ ] PARTIAL: Output addresses the dark-mode-as-mode pattern — using Figma variable modes / CSS prefers-color-scheme so semantic tokens automatically resolve to the right primitive without separate dark-mode tokens existing as siblings
