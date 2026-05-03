# Test: design-tokens — audit of inconsistent token system

Scenario: Testing the design-tokens skill with an audit request where the existing token system has orphaned tokens, mixed units, and dark mode tokens that bypass the primitive-semantic hierarchy.

## Prompt

First, create the token files to audit:

```bash
mkdir -p src/tokens src/components
```

Write to `src/tokens/colors.css`:

```css
/* Primitive colour tokens — 47 defined */
:root {
  /* Blues */
  --color-blue-50: #eff6ff;
  --color-blue-100: #dbeafe;
  --color-blue-200: #bfdbfe;
  --color-blue-300: #93c5fd;
  --color-blue-400: #60a5fa;
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-blue-700: #1d4ed8;
  --color-blue-800: #1e40af;
  --color-blue-900: #1e3a8a;

  /* Grays */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;

  /* Reds */
  --color-red-50: #fef2f2;
  --color-red-100: #fee2e2;
  --color-red-400: #f87171;
  --color-red-500: #ef4444;
  --color-red-600: #dc2626;
  --color-red-700: #b91c1c;

  /* Greens */
  --color-green-50: #f0fdf4;
  --color-green-100: #dcfce7;
  --color-green-500: #22c55e;
  --color-green-600: #16a34a;
  --color-green-700: #15803d;

  /* Yellows */
  --color-yellow-50: #fefce8;
  --color-yellow-100: #fef9c3;
  --color-yellow-500: #eab308;
  --color-yellow-600: #ca8a04;
  --color-yellow-700: #a16207;

  /* Semantic tokens */
  --color-action-primary: var(--color-blue-500);
  --color-action-primary-hover: var(--color-blue-600);
  --color-action-danger: var(--color-red-500);
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-500);
  --color-border-default: var(--color-gray-200);
  --color-surface-default: #ffffff;
  --color-surface-subtle: var(--color-gray-50);

  /* Dark mode semantic tokens — BUG: reference hardcoded hex instead of primitives */
  --color-dm-action-primary: #60a5fa;
  --color-dm-text-primary: #f9fafb;
  --color-dm-surface-default: #1f2937;
  --color-dm-border-default: #374151;
}
```

Write to `src/tokens/spacing.css`:

```css
/* Spacing tokens — mixed rem and px (inconsistent) */
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 1rem;    /* BUG: px/rem mix — should be 16px */
  --space-5: 1.25rem; /* BUG: px/rem mix */
  --space-6: 1.5rem;  /* BUG: px/rem mix */
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 3rem;   /* BUG: px/rem mix */
  --space-16: 64px;
}
```

Write to `src/components/button.css`:

```css
/* Only uses 8 of the 47 colour tokens */
.btn { padding: var(--space-2) var(--space-4); border-radius: 6px; font-size: 14px; }
.btn-primary { background: var(--color-action-primary); color: white; }
.btn-primary:hover { background: var(--color-action-primary-hover); }
.btn-danger { background: var(--color-action-danger); color: white; }
```

Write to `src/components/form.css`:

```css
/* Uses 4 tokens */
input { border: 1px solid var(--color-border-default); color: var(--color-text-primary); }
label { color: var(--color-text-secondary); font-size: 14px; }
```

Then run:

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
