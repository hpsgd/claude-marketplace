---
name: design-tokens
description: "Create or audit a design token set — colour, spacing, typography, and other foundational design values. Produces a structured token specification with semantic naming and usage guidance. Use when establishing a design system or auditing token consistency."
argument-hint: "[design system name, or 'audit' to review existing tokens]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Create or audit a design token set for $ARGUMENTS.

Design tokens are the single source of truth for visual design decisions. They replace hardcoded values with named, structured, and themeable primitives. Every colour, spacing value, font size, shadow, and motion value in the system must flow through tokens.

## Step 1 — Inventory existing tokens

Before defining anything new, understand what exists:

1. **Scan for CSS custom properties.** Search for `--` prefixed variables in CSS/SCSS files.
2. **Scan for Tailwind config.** Check `tailwind.config.js/ts` for custom theme extensions.
3. **Scan for hardcoded values.** Search for hex colours (`#[0-9a-fA-F]{3,8}`), pixel values, and raw font sizes in component files.
4. **Scan for theme files.** Look for existing token files, theme providers, or design system config.
5. **Catalogue inconsistencies.** List every unique value found. Flag duplicates (e.g., `#333`, `#333333`, `rgb(51,51,51)` all being the same colour used in different places).

**Output of this step:** A table of discovered values grouped by category (colour, spacing, typography, etc.) with usage counts and inconsistency flags.

| Category | Value | Occurrences | Locations | Inconsistency |
|---|---|---|---|---|
| Colour | `#1a1a2e` | 14 | buttons, headers, nav | Also appears as `rgb(26,26,46)` in 3 files |
| Spacing | `16px` | 42 | throughout | Also `1rem` (23 places) — same value, different unit |
| Font size | `14px` | 28 | body text | Hardcoded in 12 components instead of using token |

## Step 2 — Define primitive tokens

Primitives are the raw values. They are named by what they are, not what they do.

### Colour palette

Define a complete colour scale for each hue. Every step must meet contrast requirements when paired with its intended background.

```
colour.blue.50:   #eff6ff    // Lightest tint
colour.blue.100:  #dbeafe
colour.blue.200:  #bfdbfe
colour.blue.300:  #93c5fd
colour.blue.400:  #60a5fa
colour.blue.500:  #3b82f6    // Base
colour.blue.600:  #2563eb
colour.blue.700:  #1d4ed8
colour.blue.800:  #1e40af
colour.blue.900:  #1e3a8a    // Darkest shade
colour.blue.950:  #172554
```

Repeat for each hue in the system (neutral, red, green, yellow, etc.). Include:
- **Neutrals** — at least 11 steps from white to black
- **Brand colours** — primary, secondary
- **Feedback colours** — success (green), warning (yellow/amber), error (red), info (blue)

### Spacing scale

Use a consistent mathematical scale. Document the base unit and progression:

| Token | Value | Usage guidance |
|---|---|---|
| `spacing.1` | `4px` | Tight internal padding |
| `spacing.2` | `8px` | Default internal padding, small gaps |
| `spacing.4` | `16px` | Default gap between elements |
| `spacing.6` | `24px` | Section padding |
| `spacing.8` | `32px` | Large section gaps |
| `spacing.16` | `64px` | Major layout spacing |

### Typography scale

| Token | Size | Line height | Weight | Usage |
|---|---|---|---|---|
| `type.xs` | `12px` / `0.75rem` | `16px` | Regular | Captions, labels |
| `type.sm` | `14px` / `0.875rem` | `20px` | Regular | Secondary text, metadata |
| `type.base` | `16px` / `1rem` | `24px` | Regular | Body text |
| `type.lg` | `18px` / `1.125rem` | `28px` | Medium | Subheadings |
| `type.xl` | `20px` / `1.25rem` | `28px` | Semibold | Section headings |
| `type.2xl` | `24px` / `1.5rem` | `32px` | Semibold | Page headings |
| `type.3xl` | `30px` / `1.875rem` | `36px` | Bold | Display headings |

### Other primitives

Define scales for:
- **Border radius** — `radius.none`, `radius.sm`, `radius.md`, `radius.lg`, `radius.full`
- **Shadow** — `shadow.sm`, `shadow.md`, `shadow.lg`, `shadow.xl`
- **Motion** — `duration.fast` (100ms), `duration.normal` (200ms), `duration.slow` (300ms) and easing functions

## Step 3 — Define semantic tokens

Semantic tokens map primitives to purposes. Components consume semantic tokens, never primitives.

### Colour semantics

| Semantic token | Light mode value | Dark mode value | Usage |
|---|---|---|---|
| `color.text.primary` | `colour.neutral.900` | `colour.neutral.50` | Main body text |
| `color.text.secondary` | `colour.neutral.600` | `colour.neutral.400` | Supporting text, labels |
| `color.text.disabled` | `colour.neutral.400` | `colour.neutral.600` | Disabled elements |
| `color.text.inverse` | `colour.neutral.50` | `colour.neutral.900` | Text on coloured backgrounds |
| `color.bg.surface` | `colour.neutral.0` | `colour.neutral.900` | Default background |
| `color.bg.surface-raised` | `colour.neutral.50` | `colour.neutral.800` | Cards, raised elements |
| `color.bg.surface-overlay` | `colour.neutral.0` | `colour.neutral.800` | Modals, popovers |
| `color.border.default` | `colour.neutral.200` | `colour.neutral.700` | Default borders |
| `color.border.focus` | `colour.blue.500` | `colour.blue.400` | Focus rings |
| `color.feedback.success` | `colour.green.600` | `colour.green.400` | Success states |
| `color.feedback.warning` | `colour.yellow.600` | `colour.yellow.400` | Warning states |
| `color.feedback.error` | `colour.red.600` | `colour.red.400` | Error states |
| `color.feedback.info` | `colour.blue.600` | `colour.blue.400` | Informational states |
| `color.interactive.default` | `colour.blue.600` | `colour.blue.400` | Buttons, links |
| `color.interactive.hover` | `colour.blue.700` | `colour.blue.300` | Hover state |
| `color.interactive.active` | `colour.blue.800` | `colour.blue.200` | Pressed state |

### Spacing semantics

| Semantic token | Value | Usage |
|---|---|---|
| `space.inline.sm` | `spacing.1` | Tight inline spacing (icon to label) |
| `space.inline.md` | `spacing.2` | Default inline spacing |
| `space.stack.sm` | `spacing.2` | Tight vertical spacing |
| `space.stack.md` | `spacing.4` | Default vertical spacing |
| `space.inset.sm` | `spacing.2` | Small component padding |
| `space.inset.md` | `spacing.4` | Default component padding |
| `space.inset.lg` | `spacing.6` | Large component padding |

## Step 4 — Validate coverage

Run these checks against the token set:

### Contrast validation

| Pair | Ratio required | Actual ratio | Pass/Fail |
|---|---|---|---|
| `text.primary` on `bg.surface` | 4.5:1 (AA normal text) | [calculated] | [result] |
| `text.secondary` on `bg.surface` | 4.5:1 (AA normal text) | [calculated] | [result] |
| `text.primary` on `bg.surface-raised` | 4.5:1 (AA normal text) | [calculated] | [result] |
| `interactive.default` on `bg.surface` | 3:1 (AA large text / UI) | [calculated] | [result] |
| `feedback.error` on `bg.surface` | 4.5:1 (AA normal text) | [calculated] | [result] |

**Rule:** Every text colour and its intended background must meet WCAG 2.1 AA. Check both light and dark mode.

### Dark mode parity

Every semantic token must have both a light and dark mode value. Flag any token that maps to the same primitive in both modes — it is likely a bug.

### Coverage check

| Check | Status |
|---|---|
| All hardcoded colours in codebase have a token equivalent | [Pass / N issues] |
| All spacing values in codebase align to the spacing scale | [Pass / N issues] |
| All font sizes in codebase align to the type scale | [Pass / N issues] |
| All interactive states have distinct tokens (default, hover, active, focus, disabled) | [Pass / Gaps] |
| All feedback states are covered (success, warning, error, info) | [Pass / Gaps] |

## Step 5 — Document the token set

Compile the final token specification:

```markdown
# Design Tokens: [System Name]

**Version:** [semver]
**Last updated:** [date]

## Token Architecture
- **Primitives:** Raw values (colour scales, spacing scale, type scale)
- **Semantic:** Purpose-mapped tokens that reference primitives
- **Component:** Component-specific tokens that reference semantic tokens (optional)

## Naming Convention
`[category].[property].[variant].[state]`
- Example: `color.text.primary`, `color.bg.surface`, `color.interactive.hover`

## Primitives
[Full primitive definitions from Step 2]

## Semantic Tokens
[Full semantic mapping from Step 3]

## Validation Results
[Contrast checks, coverage audit from Step 4]

## Migration Guide
[For existing codebases: mapping from old values to new tokens]

## Design Tool Export
- **Figma:** Token JSON compatible with the Figma Tokens plugin (or Figma Variables for native support)
- **Style Dictionary:** Configuration for generating CSS custom properties, SCSS variables, and platform-specific formats
```

The output must be usable by both designers (Figma Variables or Figma Tokens plugin JSON) and developers (CSS custom properties via Style Dictionary). Do not produce a developer-only specification — if the token set can't be imported into the design tool, designers will diverge from it.

## Rules

- **Semantic over primitive.** Components must never reference primitive tokens directly. `color.text.primary` not `colour.neutral.900`. Primitives are for the token definition layer; semantic tokens are for the component layer.
- **Contrast ratios are mandatory, not aspirational.** Every text/background pair must meet WCAG 2.1 AA (4.5:1 normal text, 3:1 large text and UI elements). Check both light and dark mode.
- **Dark mode parity.** Every semantic token must resolve in both light and dark mode. No mode may be an afterthought.
- **Naming conventions are non-negotiable.** Follow the `[category].[property].[variant].[state]` pattern consistently. Do not mix naming styles within a token set.
- **One value, one token.** If two tokens resolve to the same primitive, they must have distinct semantic purposes. If they don't, merge them.
- **Tokens are versioned.** Changing a token value is a breaking change for consumers. Treat the token set as a public API with semver.

## Related Skills

- `/ui-designer:component-spec` — components consume design tokens. Define tokens first, then reference them in component specs.
- `/ui-designer:accessibility-audit` — audits contrast ratios and colour usage, which depend on correct token implementation.
