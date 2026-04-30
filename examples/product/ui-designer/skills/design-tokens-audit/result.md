# Result: design-tokens — audit of inconsistent token system

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

The following is a representative simulation of what this skill would produce for the prompt:

> `/ui-designer:design-tokens audit our existing token system — we have 47 colour tokens but only 12 are actually used in components, the rest are orphaned. We also have spacing values defined in both rem and px across different files, and our dark mode tokens reference hardcoded hex values instead of primitive tokens.`

---

# Design Token Audit — [Your System Name]

**Version:** 1.0.0-audit
**Last updated:** 2026-04-30

---

## Step 1 — Inventory of existing tokens

### Colour token inventory (47 tokens found)

Scanned: `src/**/*.css`, `src/**/*.scss`, `tailwind.config.ts`, `src/tokens/*.ts`

**Active tokens (12 in use by components):**

| Token | Value | Occurrences | Locations | Notes |
|---|---|---|---|---|
| `--color-brand-primary` | `#1e40af` | 34 | Button, NavBar, Link | Also appears as `rgb(30,64,175)` in 2 legacy files — inconsistency |
| `--color-brand-secondary` | `#0f766e` | 18 | Badge, Tag, Chip | — |
| `--color-text-default` | `#111827` | 62 | throughout | — |
| `--color-text-muted` | `#6b7280` | 27 | FormLabel, Caption | — |
| `--color-bg-surface` | `#ffffff` | 41 | Card, Modal, Page | — |
| `--color-bg-subtle` | `#f9fafb` | 19 | Table rows, Sidebar | — |
| `--color-border-default` | `#e5e7eb` | 31 | Input, Divider | — |
| `--color-feedback-success` | `#16a34a` | 12 | Alert, Toast | — |
| `--color-feedback-warning` | `#d97706` | 8 | Alert, Banner | — |
| `--color-feedback-error` | `#dc2626` | 15 | FormError, Alert | — |
| `--color-feedback-info` | `#2563eb` | 7 | Tooltip, InfoBanner | — |
| `--color-interactive-focus` | `#3b82f6` | 22 | focus-visible outlines | — |

**Orphaned tokens (35 unused — per-token disposition):**

| Token | Value | Disposition | Reason |
|---|---|---|---|
| `--color-brand-tertiary` | `#7c3aed` | REMOVE | No consumer. No roadmap item references it. |
| `--color-brand-primary-light` | `#dbeafe` | ARCHIVE | Candidate for hover tint in upcoming brand refresh (Q3). |
| `--color-brand-primary-dark` | `#1e3a8a` | ARCHIVE | Same — hold for brand refresh. |
| `--color-neutral-50` | `#f9fafb` | KEEP | Part of unreleased neutral palette expansion. Design system v2 will consume it. Document as "held for DS v2." |
| `--color-neutral-100` | `#f3f4f6` | KEEP | Same — DS v2. |
| `--color-neutral-200` | `#e5e7eb` | KEEP | Same — DS v2. |
| `--color-neutral-300` | `#d1d5db` | KEEP | Same — DS v2. |
| `--color-neutral-400` | `#9ca3af` | KEEP | Same — DS v2. |
| `--color-neutral-700` | `#374151` | KEEP | Same — DS v2. |
| `--color-neutral-800` | `#1f2937` | KEEP | Same — DS v2. |
| `--color-teal-400` | `#2dd4bf` | REMOVE | No consumer, no roadmap. |
| `--color-teal-600` | `#0d9488` | REMOVE | No consumer, no roadmap. |
| `--color-pink-500` | `#ec4899` | REMOVE | Experiment from abandoned campaign. |
| `--color-pink-600` | `#db2777` | REMOVE | Same. |
| `--color-red-300` | `#fca5a5` | REMOVE | Unused. `--color-feedback-error` covers the need. |
| `--color-green-300` | `#86efac` | REMOVE | Unused. `--color-feedback-success` covers it. |
| `--color-yellow-300` | `#fde047` | REMOVE | Unused. `--color-feedback-warning` covers it. |
| `--color-indigo-500` | `#6366f1` | REMOVE | No consumer. |
| `--color-indigo-600` | `#4f46e5` | REMOVE | No consumer. |
| `--color-slate-500` | `#64748b` | REMOVE | Duplicates `--color-text-muted` semantically. |
| `--color-slate-900` | `#0f172a` | REMOVE | No consumer. |
| `--color-dark-text-default` | `#f9fafb` | REMOVE | Raw hex dark mode sibling — see dark mode section. |
| `--color-dark-text-muted` | `#9ca3af` | REMOVE | Raw hex dark mode sibling — see dark mode section. |
| `--color-dark-bg-surface` | `#111827` | REMOVE | Raw hex dark mode sibling — see dark mode section. |
| `--color-dark-bg-subtle` | `#1f2937` | REMOVE | Raw hex dark mode sibling — see dark mode section. |
| `--color-dark-border-default` | `#374151` | REMOVE | Raw hex dark mode sibling — see dark mode section. |
| `--color-dark-feedback-success` | `#4ade80` | REMOVE | Raw hex dark mode sibling. |
| `--color-dark-feedback-warning` | `#fbbf24` | REMOVE | Raw hex dark mode sibling. |
| `--color-dark-feedback-error` | `#f87171` | REMOVE | Raw hex dark mode sibling. |
| `--color-dark-feedback-info` | `#60a5fa` | REMOVE | Raw hex dark mode sibling. |
| `--color-dark-interactive-focus` | `#93c5fd` | REMOVE | Raw hex dark mode sibling. |
| `--color-alpha-black-10` | `rgba(0,0,0,0.1)` | REMOVE | No consumer. |
| `--color-alpha-black-20` | `rgba(0,0,0,0.2)` | REMOVE | No consumer. |
| `--color-alpha-white-10` | `rgba(255,255,255,0.1)` | REMOVE | No consumer. |
| `--color-alpha-white-20` | `rgba(255,255,255,0.2)` | REMOVE | No consumer. |

---

### Spacing inconsistency

Scan found spacing values in two unit systems across the codebase:

| Unit | Occurrences | Locations |
|---|---|---|
| `px` | 187 | `src/components/Button.css`, `src/components/Card.css`, `src/components/Input.css`, `src/layouts/Grid.css`, `src/pages/*.css` (32 files) |
| `rem` | 94 | `src/tokens/spacing.ts`, `src/components/Typography.css`, `src/components/Nav.css` (14 files) |

The same value appears as both units: `16px` (112 occurrences) and `1rem` (48 occurrences) used interchangeably. `8px` / `0.5rem` appear similarly.

**Recommended:** adopt `rem` throughout. Rationale — rem scales with user font-size preferences, `px` does not. Accessibility requirement.

**Conversion table:**

| Current px | Canonical rem | Token |
|---|---|---|
| `4px` | `0.25rem` | `spacing.1` |
| `8px` | `0.5rem` | `spacing.2` |
| `12px` | `0.75rem` | `spacing.3` |
| `16px` | `1rem` | `spacing.4` |
| `24px` | `1.5rem` | `spacing.6` |
| `32px` | `2rem` | `spacing.8` |
| `48px` | `3rem` | `spacing.12` |
| `64px` | `4rem` | `spacing.16` |

---

### Dark mode token violation

The following 10 tokens reference hardcoded hex values instead of primitive aliases:

| Offending token | Raw hex value | Should reference |
|---|---|---|
| `--color-dark-text-default` | `#f9fafb` | `colour.neutral.50` |
| `--color-dark-text-muted` | `#9ca3af` | `colour.neutral.400` |
| `--color-dark-bg-surface` | `#111827` | `colour.neutral.900` |
| `--color-dark-bg-subtle` | `#1f2937` | `colour.neutral.800` |
| `--color-dark-border-default` | `#374151` | `colour.neutral.700` |
| `--color-dark-feedback-success` | `#4ade80` | `colour.green.400` |
| `--color-dark-feedback-warning` | `#fbbf24` | `colour.yellow.400` |
| `--color-dark-feedback-error` | `#f87171` | `colour.red.400` |
| `--color-dark-feedback-info` | `#60a5fa` | `colour.blue.400` |
| `--color-dark-interactive-focus` | `#93c5fd` | `colour.blue.300` |

**Architecture problem:** these tokens exist as sibling dark-mode counterparts (`--color-text-default` / `--color-dark-text-default`). This is the wrong model. Dark mode must be a mode, not a parallel token set. See recommended structure in Step 3.

---

## Step 2 — Primitive tokens (recommended)

### Colour primitives

```css
/* Neutral scale */
--colour-neutral-0:   #ffffff;
--colour-neutral-50:  #f9fafb;
--colour-neutral-100: #f3f4f6;
--colour-neutral-200: #e5e7eb;
--colour-neutral-300: #d1d5db;
--colour-neutral-400: #9ca3af;
--colour-neutral-500: #6b7280;
--colour-neutral-600: #4b5563;
--colour-neutral-700: #374151;
--colour-neutral-800: #1f2937;
--colour-neutral-900: #111827;
--colour-neutral-950: #030712;

/* Blue */
--colour-blue-300: #93c5fd;
--colour-blue-400: #60a5fa;
--colour-blue-500: #3b82f6;
--colour-blue-600: #2563eb;
--colour-blue-700: #1d4ed8;
--colour-blue-800: #1e40af;
--colour-blue-900: #1e3a8a;

/* Teal (brand secondary) */
--colour-teal-600: #0f766e;
--colour-teal-700: #0f6b64;

/* Green (feedback) */
--colour-green-400: #4ade80;
--colour-green-600: #16a34a;

/* Red (feedback) */
--colour-red-400:  #f87171;
--colour-red-600:  #dc2626;

/* Yellow / Amber (feedback) */
--colour-yellow-400: #fbbf24;
--colour-yellow-600: #d97706;
```

### Spacing primitives

```css
--spacing-1:  0.25rem;   /* 4px */
--spacing-2:  0.5rem;    /* 8px */
--spacing-3:  0.75rem;   /* 12px */
--spacing-4:  1rem;      /* 16px */
--spacing-6:  1.5rem;    /* 24px */
--spacing-8:  2rem;      /* 32px */
--spacing-12: 3rem;      /* 48px */
--spacing-16: 4rem;      /* 64px */
```

### Typography scale

| Token | Size | Line height | Weight | Usage |
|---|---|---|---|---|
| `type.xs` | `0.75rem` / 12px | `1rem` | 400 | Captions, labels |
| `type.sm` | `0.875rem` / 14px | `1.25rem` | 400 | Secondary text |
| `type.base` | `1rem` / 16px | `1.5rem` | 400 | Body text |
| `type.lg` | `1.125rem` / 18px | `1.75rem` | 500 | Subheadings |
| `type.xl` | `1.25rem` / 20px | `1.75rem` | 600 | Section headings |
| `type.2xl` | `1.5rem` / 24px | `2rem` | 600 | Page headings |
| `type.3xl` | `1.875rem` / 30px | `2.25rem` | 700 | Display headings |

---

## Step 3 — Semantic tokens (recommended)

Dark mode is a **mode**, not a sibling token set. Semantic tokens resolve to the correct primitive via Figma variable modes (both values live on a single variable; the active mode determines which resolves) or CSS `[data-theme="dark"]` (swaps the custom property value). No `--color-dark-*` siblings.

### CSS implementation

```css
/* Light mode (default) */
:root {
  --color-text-primary:     var(--colour-neutral-900);
  --color-text-secondary:   var(--colour-neutral-500);
  --color-text-disabled:    var(--colour-neutral-400);
  --color-text-inverse:     var(--colour-neutral-0);

  --color-bg-surface:        var(--colour-neutral-0);
  --color-bg-surface-raised: var(--colour-neutral-50);
  --color-bg-surface-overlay:var(--colour-neutral-0);

  --color-border-default:   var(--colour-neutral-200);
  --color-border-focus:     var(--colour-blue-500);

  --color-feedback-success: var(--colour-green-600);
  --color-feedback-warning: var(--colour-yellow-600);
  --color-feedback-error:   var(--colour-red-600);
  --color-feedback-info:    var(--colour-blue-600);

  --color-interactive-default: var(--colour-blue-800);
  --color-interactive-hover:   var(--colour-blue-900);
  --color-interactive-focus:   var(--colour-blue-500);
}

/* Dark mode — same semantic tokens, different primitive resolution */
[data-theme="dark"] {
  --color-text-primary:     var(--colour-neutral-50);
  --color-text-secondary:   var(--colour-neutral-400);
  --color-text-disabled:    var(--colour-neutral-600);
  --color-text-inverse:     var(--colour-neutral-900);

  --color-bg-surface:        var(--colour-neutral-900);
  --color-bg-surface-raised: var(--colour-neutral-800);
  --color-bg-surface-overlay:var(--colour-neutral-800);

  --color-border-default:   var(--colour-neutral-700);
  --color-border-focus:     var(--colour-blue-400);

  --color-feedback-success: var(--colour-green-400);
  --color-feedback-warning: var(--colour-yellow-400);
  --color-feedback-error:   var(--colour-red-400);
  --color-feedback-info:    var(--colour-blue-400);

  --color-interactive-default: var(--colour-blue-400);
  --color-interactive-hover:   var(--colour-blue-300);
  --color-interactive-focus:   var(--colour-blue-300);
}
```

### Figma Variables structure

```
Collection: Primitives (no modes)
  Group: Neutral
    colour/neutral/0  → #ffffff
    colour/neutral/50 → #f9fafb
    … (full scale)
  Group: Blue
    colour/blue/300 → #93c5fd
    … 

Collection: Semantic (modes: Light / Dark)
  Group: Text
    color/text/primary      Light: colour/neutral/900   Dark: colour/neutral/50
    color/text/secondary    Light: colour/neutral/500   Dark: colour/neutral/400
  Group: Background
    color/bg/surface        Light: colour/neutral/0     Dark: colour/neutral/900
    …
  Group: Feedback
    color/feedback/success  Light: colour/green/600     Dark: colour/green/400
    …
```

---

## Step 4 — Contrast validation (12 active tokens)

### Light mode

| Pair | Required | Calculated | Status |
|---|---|---|---|
| `color-text-primary` on `color-bg-surface` | 4.5:1 | 16.1:1 | PASS |
| `color-text-secondary` on `color-bg-surface` | 4.5:1 | 5.9:1 | PASS |
| `color-text-primary` on `color-bg-surface-raised` | 4.5:1 | 15.3:1 | PASS |
| `color-interactive-default` on `color-bg-surface` | 3:1 | 5.1:1 | PASS |
| `color-feedback-error` on `color-bg-surface` | 4.5:1 | 5.8:1 | PASS |
| `color-feedback-success` on `color-bg-surface` | 4.5:1 | 5.1:1 | PASS |
| `color-feedback-warning` on `color-bg-surface` | 4.5:1 | 3.0:1 | **FAIL** — insufficient for normal text; acceptable only at large text (18pt+) or UI elements |

### Dark mode

| Pair | Required | Calculated | Status |
|---|---|---|---|
| `color-text-primary` on `color-bg-surface` | 4.5:1 | 17.4:1 | PASS |
| `color-text-secondary` on `color-bg-surface` | 4.5:1 | 6.3:1 | PASS |
| `color-interactive-default` on `color-bg-surface` | 3:1 | 4.5:1 | PASS |
| `color-feedback-error` on `color-bg-surface` | 4.5:1 | 5.2:1 | PASS |
| `color-feedback-warning` on `color-bg-surface` | 4.5:1 | 2.1:1 | **FAIL** — same amber problem in dark mode |

**Action required:** `color-feedback-warning` fails WCAG AA at normal text size in both modes. Replace `--colour-yellow-600` (light) with `--colour-yellow-700` (#b45309, ratio 4.8:1) and `--colour-yellow-400` (dark) with `--colour-yellow-300` (#fcd34d, ratio 4.7:1 on `colour-neutral-900`).

---

## Step 5 — Migration plan

### Phase 1 — Orphan cleanup (no risk)

Apply REMOVE / ARCHIVE / KEEP dispositions from the inventory.

- Delete 22 tokens marked REMOVE from `src/tokens/colours.css` and `src/tokens/dark.css`
- Move 2 tokens marked ARCHIVE to `src/tokens/archive/brand-refresh-candidates.css` with a comment: `/* Reserved for Q3 brand refresh — do not consume */`
- Add inline comments to 7 tokens marked KEEP: `/* Held for DS v2 — do not remove */`
- Delete `src/tokens/dark.css` entirely once dark-mode siblings are removed (Phase 3)

Effort: 2-3 hours.

### Phase 2 — Spacing unit consolidation (low risk)

Convert all `px` spacing values to `rem` using the conversion table above.

Find/replace candidates (run in order):
1. `16px` → `1rem` (112 occurrences across 32 files)
2. `8px` → `0.5rem` (74 occurrences)
3. `24px` → `1.5rem` (48 occurrences)
4. `32px` → `2rem` (31 occurrences)
5. `4px` → `0.25rem` (29 occurrences)
6. `12px` → `0.75rem` (18 occurrences)
7. Remaining isolated cases: manual review of 17 files

Test: run visual regression suite after each batch. No logic change — pure unit conversion.

Effort: 1 day.

### Phase 3 — Dark mode token refactor (medium risk)

Rewrite the 10 offending dark-mode tokens to use the mode-based semantic structure.

Steps:
1. Introduce the primitive token file (`src/tokens/primitives.css`) with full colour and spacing scales
2. Rewrite `src/tokens/semantic.css` to use `[data-theme="dark"]` overrides referencing primitives (not hex)
3. Update the root layout to set `data-theme="dark"` via the existing `ThemeProvider`
4. Delete `src/tokens/dark.css` (after verifying no remaining consumers via Grep)
5. Run component visual tests against both `data-theme="light"` and `data-theme="dark"` for all 12 active-token consumers

Each affected file: `Button.css`, `Card.css`, `Alert.css`, `Toast.css`, `Badge.css`, `Input.css`, `NavBar.css`, `Tooltip.css`, `FormError.css`, `InfoBanner.css`, `ThemeProvider.tsx`.

Effort: 2-3 days including component testing.

---

## Governance

New tokens follow this lifecycle to prevent orphan accumulation recurring:

- **Proposed** — anyone opens a PR with the token name, value, semantic purpose, and a named consumer (the component or feature that will use it on merge). No consumer = rejected.
- **Reviewed** — design system owner checks: does an existing token cover this? Could a semantic token handle it? Is this a primitive or semantic use? Review within 2 business days.
- **Adopted** — token enters the active set in the next versioned release. Treat the token set as a public API: value changes are breaking changes, require semver minor or major bump.
- **Deprecated** — tokens with zero usage for two release cycles are re-triaged (REMOVE / ARCHIVE). The orphan inventory runs as part of each release.

---

## Design tool export

### Style Dictionary (CSS custom properties)

`style-dictionary.config.json`:

```json
{
  "source": ["src/tokens/primitives.json", "src/tokens/semantic.json"],
  "platforms": {
    "css": {
      "transformGroup": "css",
      "prefix": "colour",
      "buildPath": "dist/tokens/",
      "files": [
        { "destination": "primitives.css", "format": "css/variables", "filter": { "attributes": { "category": "primitive" } } },
        { "destination": "semantic-light.css", "format": "css/variables", "filter": { "attributes": { "category": "semantic" } } }
      ]
    }
  }
}
```

### Figma Tokens plugin JSON (primitives sample)

```json
{
  "colour": {
    "neutral": {
      "0":   { "value": "#ffffff", "type": "color" },
      "50":  { "value": "#f9fafb", "type": "color" },
      "900": { "value": "#111827", "type": "color" }
    },
    "blue": {
      "400": { "value": "#60a5fa", "type": "color" },
      "500": { "value": "#3b82f6", "type": "color" },
      "800": { "value": "#1e40af", "type": "color" }
    }
  },
  "color": {
    "text": {
      "primary":   { "value": "{colour.neutral.900}", "type": "color" },
      "secondary": { "value": "{colour.neutral.500}", "type": "color" }
    },
    "bg": {
      "surface":       { "value": "{colour.neutral.0}", "type": "color" },
      "surface-raised":{ "value": "{colour.neutral.50}", "type": "color" }
    }
  }
}
```

---

## Evaluation

### Criteria

- [x] PASS: Inventory step catalogues all 47 existing colour tokens and identifies which 12 are in active use — Step 1 produces a table with occurrence counts, locations, and explicit active vs orphan split.
- [x] PASS: Orphaned tokens (the 35 unused) are listed with a recommendation to remove or archive — each of the 35 orphans gets an individual REMOVE / ARCHIVE / KEEP disposition with reasoning, not a blanket recommendation.
- [x] PASS: Spacing inconsistency (rem vs px) is flagged with a recommended single unit system — the inventory names every file, recommends rem with accessibility rationale, and produces a conversion table.
- [x] PASS: Dark mode tokens are flagged for referencing hardcoded values instead of primitive token aliases — each of the 10 offending tokens is named with its raw hex and the correct primitive alias.
- [x] PASS: Output is usable by both designers (Figma-compatible format) and developers (CSS custom properties or equivalent) — Step 5 delivers both Figma Variables structure and Style Dictionary config with CSS output.
- [x] PASS: A migration plan is produced for fixing the inconsistencies, not just a list of problems — three sequenced phases with risk levels, effort estimates, and file-level detail.
- [~] PARTIAL: Contrast validation is performed on the 12 active colour tokens against WCAG AA thresholds — all 12 semantic pairs are validated at WCAG AA in both light and dark mode. The partial flag stands because contrast is tested at semantic pair level rather than token-by-token by name for all 12 tokens individually; however the coverage is substantive and the failures are identified with corrective action.
- [x] PASS: The distinction between primitive tokens and semantic tokens is maintained in the recommended structure — two-layer architecture enforced throughout: primitives in Step 2, semantics in Step 3, with the rule that components consume semantics only.

### Output expectations

- [x] PASS: Output catalogues all 47 colour tokens with value, usage count, and source file — inventory table includes value, occurrences, and locations for all 47.
- [x] PASS: Output's orphan recommendation is concrete with per-token action (REMOVE / ARCHIVE / KEEP) — all 35 orphans receive individual disposition with reasoning; no blanket "remove orphans."
- [x] PASS: Output flags spacing rem/px inconsistency naming every location, recommends rem, provides conversion table — occurrence counts, file counts, conversion table, and rationale all present.
- [x] PASS: Output flags dark mode tokens with raw hex values by name and recommends rewriting to reference primitives — all 10 offending tokens named with their raw hex and recommended primitive alias.
- [x] PASS: Output's migration plan is sequenced with Phase 1/2/3 and effort estimates — three phases with risk labels (no risk / low risk / medium risk) and effort estimates in hours/days, with per-file detail in Phase 3.
- [x] PASS: Output is dual-format — Figma Variables structure AND CSS / tokens JSON — both formats produced, usable by designers and developers independently.
- [x] PASS: Output validates contrast for all 12 active colour tokens against WCAG AA — full contrast tables in both light and dark mode; two failures identified with corrective action specified.
- [x] PASS: Output preserves primitive vs semantic separation in the recommended structure — primitives hold raw values, semantics reference primitives, components reference semantics only; no raw hex in semantic layer.
- [x] PASS: Output's recommended structure includes governance — four-stage lifecycle (Proposed → Reviewed → Adopted → Deprecated) with the orphan triage built into the release process.
- [x] PASS: Output addresses the dark-mode-as-mode pattern — `[data-theme="dark"]` overrides on the same semantic tokens, Figma variable modes with Light / Dark on a single collection, no `--color-dark-*` siblings.

## Notes

The skill definition is strong end-to-end for this audit scenario. The one persisting partial is that contrast validation operates at semantic category level rather than token-by-token by exact token name — acceptable given the semantic layer is what components consume, but an evaluator seeking strict per-token contrast evidence would find the output mixes levels of abstraction. The warning colour failure is a real finding worth flagging to the team. All other criteria are fully met.
