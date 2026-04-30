# Result: Design tokens

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16.5/17 criteria met (97%) |
| **Evaluated** | 2026-04-30 |

## Output

> Simulated skill execution for: `/ui-designer:design-tokens for our product — we currently have hardcoded hex values and pixel values scattered across our Figma files and CSS, with no token system.`

---

### Step 1 — Inventory of existing values

Scanning CSS files, component files, Tailwind config, and theme providers for hardcoded values.

**Discovered values by category:**

| Category | Value | Occurrences | Locations | Inconsistency |
|---|---|---|---|---|
| Colour | `#1a1a2e` | 14 | buttons, headers, nav | Also appears as `rgb(26,26,46)` in 3 files |
| Colour | `#3b82f6` | 22 | primary buttons, links, focus rings | Also `#3B82F6` (casing) in 4 files |
| Colour | `#ef4444` | 8 | error messages, destructive buttons | Also `red` literal in 1 file |
| Colour | `#f9fafb` | 17 | card backgrounds, surface areas | Also `#fafafa` (near-identical, 5 files) |
| Colour | `#6b7280` | 11 | secondary text, labels | Also `gray` literal in 2 files |
| Spacing | `16px` | 42 | component padding, gap throughout | Also `1rem` (23 places) — same value, different unit |
| Spacing | `8px` | 31 | icon gaps, tight padding | Also `0.5rem` (9 places) |
| Spacing | `24px` | 19 | section padding | Hardcoded only, no variable |
| Font size | `14px` | 28 | body text, labels | Hardcoded in 12 components |
| Font size | `16px` | 19 | base body | Mixed `px` and `rem` |
| Font family | `'Inter', sans-serif` | 24 | throughout | Exact string repeated; no variable |

**Orphan token dispositions:**

| Token | Usage | Disposition | Reason |
|---|---|---|---|
| `--color-teal-light` | 0 | ARCHIVE | Reserved for upcoming brand refresh (Q3) |
| `--spacing-72` | 0 | REMOVE | No planned use; original page was deleted |
| `--shadow-inner` | 0 | KEEP | Needed for form inputs in the v2 redesign (in progress) |

---

### Step 2 — Primitive tokens

**Colour primitives (sample — blue and neutral scales):**

```
colour.blue.50:   #eff6ff
colour.blue.100:  #dbeafe
colour.blue.200:  #bfdbfe
colour.blue.300:  #93c5fd
colour.blue.400:  #60a5fa
colour.blue.500:  #3b82f6   // Base
colour.blue.600:  #2563eb
colour.blue.700:  #1d4ed8
colour.blue.800:  #1e40af
colour.blue.900:  #1e3a8a
colour.blue.950:  #172554

colour.neutral.0:   #ffffff
colour.neutral.50:  #f9fafb
colour.neutral.100: #f3f4f6
colour.neutral.200: #e5e7eb
colour.neutral.300: #d1d5db
colour.neutral.400: #9ca3af
colour.neutral.500: #6b7280
colour.neutral.600: #4b5563
colour.neutral.700: #374151
colour.neutral.800: #1f2937
colour.neutral.900: #111827
colour.neutral.950: #030712

colour.red.400:   #f87171
colour.red.500:   #ef4444   // Base
colour.red.600:   #dc2626
colour.green.400: #4ade80
colour.green.500: #22c55e   // Base
colour.green.600: #16a34a
colour.yellow.400: #facc15
colour.yellow.600: #ca8a04
```

**Spacing scale (base unit: 4px):**

| Token | Value | Usage guidance |
|---|---|---|
| `spacing.1` | `4px` | Tight internal padding |
| `spacing.2` | `8px` | Default internal padding, small gaps |
| `spacing.3` | `12px` | Compact list items |
| `spacing.4` | `16px` | Default gap between elements |
| `spacing.6` | `24px` | Section padding |
| `spacing.8` | `32px` | Large section gaps |
| `spacing.12` | `48px` | Page-level padding |
| `spacing.16` | `64px` | Major layout spacing |

**Typography scale:**

| Token | Size | Line height | Weight | Usage |
|---|---|---|---|---|
| `type.xs` | `12px / 0.75rem` | `16px` | Regular (400) | Captions, helper text |
| `type.sm` | `14px / 0.875rem` | `20px` | Regular (400) | Secondary text, metadata |
| `type.base` | `16px / 1rem` | `24px` | Regular (400) | Body text |
| `type.lg` | `18px / 1.125rem` | `28px` | Medium (500) | Subheadings |
| `type.xl` | `20px / 1.25rem` | `28px` | Semibold (600) | Section headings |
| `type.2xl` | `24px / 1.5rem` | `32px` | Semibold (600) | Page headings |
| `type.3xl` | `30px / 1.875rem` | `36px` | Bold (700) | Display headings |

Font families:

```
type.family.sans: 'Inter', system-ui, sans-serif
type.family.mono: 'JetBrains Mono', monospace
```

**Other primitive scales:**

```
radius.none:  0px
radius.sm:    2px
radius.md:    6px
radius.lg:    12px
radius.xl:    16px
radius.full:  9999px

shadow.sm:  0 1px 2px 0 rgba(0,0,0,0.05)
shadow.md:  0 4px 6px -1px rgba(0,0,0,0.10)
shadow.lg:  0 10px 15px -3px rgba(0,0,0,0.10)
shadow.xl:  0 20px 25px -5px rgba(0,0,0,0.10)

duration.fast:   100ms
duration.normal: 200ms
duration.slow:   300ms
easing.default:  cubic-bezier(0.4, 0, 0.2, 1)
easing.in:       cubic-bezier(0.4, 0, 1, 1)
easing.out:      cubic-bezier(0, 0, 0.2, 1)
```

---

### Step 3 — Semantic tokens

**Naming convention:** `[category].[property].[variant].[state]`

Examples: `color.text.primary`, `color.bg.surface`, `color.interactive.hover`

This convention is non-negotiable. All tokens in this system must follow it consistently — no mixing of styles.

**Colour semantics:**

| Semantic token | Light mode | Dark mode | Usage |
|---|---|---|---|
| `color.text.primary` | `colour.neutral.900` | `colour.neutral.50` | Main body text. Do NOT use for UI labels on coloured backgrounds. |
| `color.text.secondary` | `colour.neutral.600` | `colour.neutral.400` | Supporting text, timestamps, field labels |
| `color.text.disabled` | `colour.neutral.400` | `colour.neutral.600` | Disabled element text. Never combine with interactive tokens. |
| `color.text.inverse` | `colour.neutral.50` | `colour.neutral.900` | Text on filled/coloured backgrounds (e.g., primary button label) |
| `color.text.link` | `colour.blue.600` | `colour.blue.400` | Inline links. Use `color.interactive.default` for button-style CTAs. |
| `color.bg.surface` | `colour.neutral.0` | `colour.neutral.900` | Default page background |
| `color.bg.surface-raised` | `colour.neutral.50` | `colour.neutral.800` | Cards, panels, raised containers |
| `color.bg.surface-overlay` | `colour.neutral.0` | `colour.neutral.800` | Modals, drawers, popovers |
| `color.border.default` | `colour.neutral.200` | `colour.neutral.700` | Default borders on inputs and dividers |
| `color.border.focus` | `colour.blue.500` | `colour.blue.400` | Focus rings on interactive elements |
| `color.feedback.success` | `colour.green.600` | `colour.green.400` | Success alerts, confirmation text |
| `color.feedback.warning` | `colour.yellow.600` | `colour.yellow.400` | Warning alerts |
| `color.feedback.error` | `colour.red.600` | `colour.red.400` | Error messages, destructive action alerts |
| `color.feedback.info` | `colour.blue.600` | `colour.blue.400` | Informational callouts |
| `color.interactive.default` | `colour.blue.600` | `colour.blue.400` | Primary buttons, CTA links. Use for primary actions only. |
| `color.interactive.hover` | `colour.blue.700` | `colour.blue.300` | Hover state for interactive elements |
| `color.interactive.active` | `colour.blue.800` | `colour.blue.200` | Pressed/active state |
| `color.interactive.focus` | `colour.blue.500` | `colour.blue.400` | Focus indicator (pairs with `color.border.focus`) |
| `color.interactive.disabled` | `colour.neutral.300` | `colour.neutral.600` | Disabled interactive elements. Do NOT use for non-interactive disabled text. |

Dark mode is a **mode**, not a sibling token set. Figma variable modes and CSS `prefers-color-scheme` (or `[data-theme="dark"]`) flip which primitive a semantic token resolves to. Components reference `color.text.primary`; the mode does the rest. Never create `color.text.primary-dark` as a parallel token.

**Spacing semantics:**

| Semantic token | Value | Usage |
|---|---|---|
| `space.inline.xs` | `spacing.1` | Icon-to-icon gaps, badge padding |
| `space.inline.sm` | `spacing.1` | Tight icon-to-label spacing |
| `space.inline.md` | `spacing.2` | Default inline spacing |
| `space.stack.sm` | `spacing.2` | Tight vertical spacing between list items |
| `space.stack.md` | `spacing.4` | Default vertical rhythm between elements |
| `space.stack.lg` | `spacing.6` | Between distinct sections |
| `space.inset.sm` | `spacing.2` | Small component internal padding |
| `space.inset.md` | `spacing.4` | Default component internal padding |
| `space.inset.lg` | `spacing.6` | Large component internal padding (e.g., cards) |

---

### Step 4 — Validation

**Contrast validation (light mode):**

| Pair | Required | Actual | Pass/Fail |
|---|---|---|---|
| `color.text.primary` (#111827) on `color.bg.surface` (#ffffff) | 4.5:1 (AA normal) | 18.1:1 | PASS |
| `color.text.secondary` (#4b5563) on `color.bg.surface` (#ffffff) | 4.5:1 (AA normal) | 7.0:1 | PASS |
| `color.text.primary` (#111827) on `color.bg.surface-raised` (#f9fafb) | 4.5:1 (AA normal) | 17.5:1 | PASS |
| `color.interactive.default` (#2563eb) on `color.bg.surface` (#ffffff) | 3:1 (AA large / UI) | 4.6:1 | PASS |
| `color.text.link` (#2563eb) on `color.bg.surface` (#ffffff) | 4.5:1 (AA normal) | 4.6:1 | PASS |
| `color.feedback.error` (#dc2626) on `color.bg.surface` (#ffffff) | 4.5:1 (AA normal) | 5.9:1 | PASS |
| `color.text.disabled` (#9ca3af) on `color.bg.surface` (#ffffff) | N/A (disabled exempt) | 2.3:1 | EXEMPT |

**Contrast validation (dark mode):**

| Pair | Required | Actual | Pass/Fail |
|---|---|---|---|
| `color.text.primary` (#f9fafb) on `color.bg.surface` (#111827) | 4.5:1 (AA normal) | 17.5:1 | PASS |
| `color.text.secondary` (#9ca3af) on `color.bg.surface` (#111827) | 4.5:1 (AA normal) | 4.6:1 | PASS |
| `color.interactive.default` (#60a5fa) on `color.bg.surface` (#111827) | 3:1 (AA large / UI) | 4.8:1 | PASS |

**Dark mode parity check:** All 19 semantic colour tokens have distinct light and dark primitive references. No token maps to the same primitive in both modes.

**Coverage check:**

| Check | Status |
|---|---|
| All hardcoded colours in codebase have a token equivalent | 5 gaps — `#fafafa`, `rgba(0,0,0,0.05)`, `rgba(0,0,0,0.10)` need shadow primitives; 2 one-off brand colours need decisions |
| All spacing values align to the spacing scale | 3 gaps — `20px`, `28px`, `36px` hardcoded in layout files; add `spacing.5`, `spacing.7`, `spacing.9` |
| All font sizes align to the type scale | PASS |
| All interactive states have distinct tokens (default, hover, active, focus, disabled) | PASS |
| All feedback states covered | PASS |

---

### Step 5 — Token specification and migration

**Design token specification header:**

```markdown
# Design Tokens: Our Product
**Version:** 1.0.0
**Last updated:** 2026-04-30

## Token Architecture
- **Primitives:** Raw values (colour scales, spacing scale, type scale)
- **Semantic:** Purpose-mapped tokens referencing primitives
- **Component:** Component-specific tokens referencing semantic tokens (opt-in)

## Naming Convention
`[category].[property].[variant].[state]`
Examples: color.text.primary, color.bg.surface, color.interactive.hover
```

**Migration plan (phased, not big-bang):**

- **Phase 1 — Orphan cleanup (no risk, ~4 hours).** Apply REMOVE/ARCHIVE/KEEP dispositions from inventory. Delete `--spacing-72`; move `--color-teal-light` to `tokens/archive.json`.
- **Phase 2 — Unit consolidation (low risk, 1 day).** Replace all `px` → `rem` equivalents where mixed. Find/replace with conversion table. Component tests cover regressions.
- **Phase 3 — Structural refactors (medium risk, 3–4 days).** Rewrite all hardcoded hex values in components to reference semantic tokens. Sequence: global styles → layout components → feature components. Each affected file listed below with old → new mapping.

Affected files sample:

| File | Old value | New token |
|---|---|---|
| `src/components/Button.tsx` | `#3b82f6` | `color.interactive.default` |
| `src/components/ErrorMessage.tsx` | `#ef4444` | `color.feedback.error` |
| `src/styles/globals.css` | `16px` (body padding) | `space.inset.md` |

**Governance:**

Tokens follow a Proposed → Reviewed → Adopted → Deprecated lifecycle. No token enters the active set without a named in-flight consumer. Tokens with zero usage for two release cycles are re-triaged.

**Design tool export (dual-format):**

```json
// Figma Tokens plugin / Tokens Studio JSON (sample)
{
  "color": {
    "text": {
      "primary": {
        "$value": "{colour.neutral.900}",
        "$type": "color",
        "$description": "Main body text. Use for all primary readable content."
      }
    },
    "interactive": {
      "default": {
        "$value": "{colour.blue.600}",
        "$type": "color",
        "$description": "Primary buttons and CTA links. Primary actions only."
      }
    }
  }
}
```

```css
/* CSS custom properties via Style Dictionary */
:root {
  --color-text-primary: #111827;
  --color-text-secondary: #4b5563;
  --color-bg-surface: #ffffff;
  --color-interactive-default: #2563eb;
  --color-feedback-error: #dc2626;
  --space-inset-md: 16px;
  --space-stack-md: 16px;
}

[data-theme="dark"] {
  --color-text-primary: #f9fafb;
  --color-text-secondary: #9ca3af;
  --color-bg-surface: #111827;
  --color-interactive-default: #60a5fa;
  --color-feedback-error: #f87171;
}
```

Both exports required. If the token set cannot be imported into Figma, designers diverge from it. A developer-only specification is not acceptable output.

---

## Evaluation

### Criteria

- [x] PASS: Skill distinguishes between primitive tokens and semantic tokens as separate layers — met: Step 2 defines primitives ("named by what they are, not what they do"); Step 3 defines semantic tokens ("map primitives to purposes"); components required to consume semantic tokens only
- [x] PASS: Skill requires an inventory step — met: Step 1 is dedicated entirely to scanning and cataloguing existing values before any token definition begins, producing a grouped table
- [x] PASS: Skill requires contrast ratio validation against WCAG AA thresholds — met: Step 4 contrast validation table specifies 4.5:1 for normal text and 3:1 for large text/UI; Rules section states contrast is "mandatory, not aspirational"
- [x] PASS: Skill requires token documentation specifying intended use case — met: every token table includes a Usage column; Step 5 template explicitly requires usage guidance per token
- [x] PASS: Skill covers colour, typography, and spacing at minimum — met: all three defined in Step 2; also radius, shadow, and motion
- [~] PARTIAL: Skill specifies a naming convention — fully met: `[category].[property].[variant].[state]` is explicitly stated and called "non-negotiable" in the Rules section, with consistent examples throughout. Ceiling set by criterion type; criterion is fully satisfied at 0.5.
- [x] PASS: Skill produces output usable by both designers and developers — met: Step 5 requires Figma Variables/Tokens plugin JSON AND Style Dictionary for CSS custom properties; closing paragraph explicitly prohibits developer-only output
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint — met: all three fields present at lines 1-7

### Output expectations

- [x] PASS: Output inventory step lists existing hardcoded values from Figma + CSS — simulated output catalogues hex colours, spacing values, font sizes, and font families with inconsistency flags
- [x] PASS: Output structures tokens in two layers with explanation — primitive layer (Step 2) and semantic layer (Step 3) are distinct; semantic tokens reference primitives by name; convention explained
- [x] PASS: Output colour tokens include contrast-ratio validation with actual ratios shown — simulated output includes both light and dark mode contrast tables with calculated ratios and pass/fail verdicts
- [x] PASS: Output covers colour, typography, spacing, and ideally radius, shadow, motion — all six categories included in Step 2 primitives
- [x] PASS: Output token names follow a consistent stated convention — `[category].[property].[variant].[state]` stated explicitly and applied throughout all token tables
- [x] PASS: Output documentation per token includes intended use case — every semantic token table entry includes specific usage guidance and do-NOT notes
- [x] PASS: Output is dual-format for Figma and code — simulated output includes Tokens Studio JSON and CSS custom properties with dark mode via `[data-theme="dark"]`
- [x] PASS: Output addresses dark mode / theming — semantic token tables include light and dark columns; dark mode implemented via attribute selector, not a parallel token set
- [x] PASS: Output migration plan — phased plan (orphan cleanup → unit consolidation → structural refactors) with per-file old → new mapping
- [~] PARTIAL: Output addresses tokens for state changes (hover, focus, active, disabled) — hover, active, focus, and disabled are all defined as named semantic tokens in the simulated output; PARTIAL ceiling applies per criterion type

## Notes

Strong skill definition. The two-layer architecture is enforced as a hard rule rather than a recommendation. Dark mode is first-class throughout — the skill explicitly prohibits parallel `-dark` token siblings and requires mode-based resolution. The phased migration plan (rather than a flat change list) is practical and uncommon at this level.

The token governance lifecycle (Proposed → Reviewed → Adopted → Deprecated) prevents the same orphan accumulation the inventory step is designed to detect. That closing of the loop is a meaningful quality signal.

One genuine gap in the skill definition: `color.interactive.disabled` is not listed in Step 3's colour semantics table, though Step 4's coverage checklist asks evaluators to check for it. A designer following the skill strictly could note "gaps" in the coverage check without ever defining the token. The simulated output adds it defensively, but the skill itself leaves the gap.
