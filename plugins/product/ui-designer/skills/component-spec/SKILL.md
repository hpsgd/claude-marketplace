---
name: component-spec
description: Write a comprehensive component specification — purpose, props API, all states, responsive behaviour, accessibility requirements, and usage examples.
argument-hint: "[component name or description]"
user-invocable: true
allowed-tools: Read, Glob, Grep
---

Write a component specification for $ARGUMENTS.

Before writing, search the codebase for existing implementations of this component or similar components. Reference existing patterns. This spec must be complete enough for an engineer to implement without follow-up questions.

---

## Mandatory Specification Structure

### 1. Purpose and Usage Context

Write exactly two things:
- **What it does**: One sentence describing the component's function
- **When to use it**: Specific scenarios where this component is the right choice, and what to use instead when it is not

Example:
> **What:** A dismissible banner that communicates system-level messages to the user.
> **When to use:** For messages that affect the entire page or application (maintenance windows, billing alerts, feature announcements). Do NOT use for inline form validation (use `FormError`) or transient notifications (use `Toast`).

### 2. Props / API

Document every prop in a table. Every prop must have a type, default value, and description.

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `variant` | `'info' \| 'success' \| 'warning' \| 'error'` | `'info'` | No | Visual style and semantic meaning |
| `children` | `ReactNode` | — | Yes | Content to display |
| `onDismiss` | `() => void` | `undefined` | No | Called when user dismisses. If omitted, banner is not dismissible |
| `icon` | `ReactNode` | Auto from variant | No | Override the default icon for the variant |

**Rules for prop design:**

1. **Use `variant` for visual/semantic differences.** Do not use separate props like `color`, `background`, `severity`. One prop, one decision.
2. **Boolean props must default to `false`.** The default state should be the absence of the modifier: `disabled`, not `enabled`; `loading`, not `loaded`.
3. **Callback props start with `on`.** `onClick`, `onDismiss`, `onChange` — never `handleClick` (that is an internal implementation name).
4. **Avoid string enums for booleans.** If there are only two states, use a boolean. `compact={true}` not `size="compact" | "default"` when there are only two sizes.
5. **Composition over configuration.** Prefer `children` and slot props over complex configuration objects. A component should be composable, not a god-object.
6. **Render-irrelevant props are code smells.** If a prop does not affect rendering, it probably does not belong on this component.

### 3. Variants

For each variant, document:

| Variant | Visual treatment | Semantic meaning | When to use |
|---------|-----------------|------------------|-------------|
| `info` | Blue background, info icon | Neutral information | General announcements, tips |
| `success` | Green background, check icon | Positive confirmation | Completed actions, success states |
| `warning` | Yellow background, alert icon | Caution needed | Approaching limits, deprecation notices |
| `error` | Red background, error icon | Problem requiring action | System errors, failed operations |

Include a note on which variant to use when unsure. There should always be a default.

### 4. States — Complete Coverage Table

Document EVERY state the component can be in. Missing states are the #1 source of implementation bugs. Use this complete list and mark N/A for states that do not apply to this component:

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default** | [Base appearance] | [Normal interaction behaviour] | Hover, Focus |
| **Hover** | [What changes on mouse hover] | [Cursor change, tooltips] | Default, Active |
| **Focus** | [Focus ring style, outline] | [Keyboard focus indicator — MUST be visible] | Default, Active |
| **Active** | [Pressed/clicked appearance] | [Visual feedback during press] | Default |
| **Disabled** | [Reduced opacity, muted colours] | [No interaction, no hover effects, cursor: not-allowed] | — |
| **Loading** | [Skeleton, spinner, or shimmer] | [Non-interactive during load, preserves layout dimensions] | Default, Error |
| **Error** | [Error styling, red border/text] | [Show error message, offer recovery action] | Default |
| **Empty** | [Empty state illustration or message] | [Guide user to populate — CTA if applicable] | Default |
| **Selected** | [Highlight, checkmark, background change] | [Indicates active selection] | Default |
| **Read-only** | [Similar to disabled but full contrast] | [Content is visible and copyable but not editable] | — |

**Rules:**
- Every interactive component MUST define Hover, Focus, Active, and Disabled states. No exceptions.
- Focus state MUST be visually distinct and not rely solely on colour change (for accessibility).
- Loading state MUST preserve the component's layout dimensions to prevent layout shift.
- Disabled state MUST use `aria-disabled` and prevent interaction — do not just change opacity without blocking events.

### 5. Responsive Behaviour

Define behaviour at each breakpoint. Use the project's breakpoint system (Tailwind defaults shown):

| Breakpoint | Width | Layout changes | Content changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px (`sm`) | [Stack vertically, full-width] | [Truncate text, hide secondary actions behind menu] |
| **Tablet** | 640-1024px (`sm`-`lg`) | [Adjust grid columns, reduce padding] | [Show primary + secondary actions] |
| **Desktop** | > 1024px (`lg`+) | [Full layout, standard padding] | [Show all content and actions] |

**Rules:**
- Touch targets must be at least 44x44px on mobile (WCAG 2.5.5)
- No horizontal scrolling at any breakpoint
- Text must remain readable without horizontal scrolling when viewport is 320px wide
- Component must not break at intermediate widths between breakpoints

### 6. Accessibility Requirements

Every component must meet WCAG 2.1 AA. Specify each requirement explicitly:

#### Keyboard Navigation
| Key | Action |
|-----|--------|
| `Tab` | [Where focus moves to] |
| `Shift+Tab` | [Reverse focus movement] |
| `Enter` / `Space` | [Primary activation — what happens] |
| `Escape` | [Dismiss/close behaviour — what closes, where focus returns] |
| `Arrow keys` | [Navigation within the component, if applicable] |

#### Screen Reader
- **Role**: What ARIA role does this component use? (`role="alert"`, `role="dialog"`, `role="button"`, etc.)
- **Label**: How is the component announced? (`aria-label`, `aria-labelledby`, or visible text)
- **State announcements**: What is announced when state changes? (`aria-live`, `aria-expanded`, `aria-selected`)
- **Description**: Additional context via `aria-describedby` if the label alone is insufficient

#### Colour and Contrast
- Text-to-background contrast: minimum 4.5:1 for normal text, 3:1 for large text (18px+ or 14px+ bold)
- Non-text elements (icons, borders, focus indicators): minimum 3:1 against adjacent colours
- Information MUST NOT be conveyed by colour alone — use icons, text, or patterns in addition to colour

#### Focus Management
- Where does focus go when the component appears? (For modals, popovers, drawers)
- Where does focus return when the component closes?
- Is focus trapped within the component? (Required for modals and dialogs)
- Is the focus indicator visible in both light and dark modes?

### 7. Dark Mode

- [ ] All colours use semantic tokens, not hardcoded values
- [ ] Contrast ratios are maintained in dark mode (re-check, do not assume)
- [ ] Images use `ThemeImage` component or have dark-mode variants
- [ ] Shadows and elevation are adjusted for dark backgrounds (lighter shadows, not darker)
- [ ] Borders remain visible against dark backgrounds

### 8. Animation and Motion

- Specify transitions: what animates, duration, easing function
- All animations must respect `prefers-reduced-motion: reduce` — provide static alternatives
- Entry/exit animations for components that appear/disappear (modals, tooltips, drawers)
- Maximum animation duration: 300ms for micro-interactions, 500ms for page transitions

### 9. Usage Examples

Provide 3 examples showing different configurations:

```tsx
// Basic usage
<Component variant="info">
  Your trial expires in 3 days.
</Component>

// With dismiss callback
<Component variant="warning" onDismiss={() => setDismissed(true)}>
  This API version is deprecated. <Link href="/migrate">Migrate now</Link>
</Component>

// Error state with action
<Component variant="error">
  Payment failed. <Button variant="link" onClick={retry}>Try again</Button>
</Component>
```

### 10. Do / Don't

End with explicit guidance:

| Do | Don't |
|----|-------|
| Use `variant` to communicate severity | Use custom colours outside the variant system |
| Keep content concise (1-2 sentences) | Put long-form content or multiple paragraphs inside |
| Provide a dismiss action for non-critical messages | Make error banners dismissible if the error needs resolution |
| Use one banner at a time per page section | Stack multiple banners — consolidate into one |

---

## Output Format

Present the spec as a single structured document using the sections above. If a section is not applicable to this component, include it with "N/A — [reason]" rather than omitting it. Missing sections cause implementation gaps.

## Related Skills

- `/ui-designer:design-review` — review the implemented component against this spec.
- `/ui-designer:accessibility-audit` — audit the component for WCAG compliance after implementation.
