---
name: design-review
description: Review a UI implementation against design system conventions, accessibility, consistency, responsiveness, dark mode, and component patterns.
argument-hint: "[file, component, or directory to review]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Review $ARGUMENTS against design system conventions.

This review checks implementation quality across six dimensions. Read all target files before starting. Search for the project's design system primitives and Tailwind config to understand what is available.

---

## Pre-Review: Understand the Design System

Before reviewing, gather context:

1. **Tailwind config**: Read `tailwind.config.js` / `tailwind.config.ts` to understand the theme (colours, spacing, breakpoints, fonts)
2. **Component library**: Search for existing shared components in `components/ui/`, `components/shared/`, or similar directories
3. **Design tokens**: Check for CSS custom properties in global styles (`globals.css`, `variables.css`, etc.)
4. **Conventions**: Look at 2-3 recently merged components to understand established patterns

---

## Dimension 1: Design System Consistency

### Colour Usage
Search for these violations:

```bash
# Hardcoded hex colours (should use theme tokens)
grep -rn '#[0-9a-fA-F]\{3,8\}' --include="*.tsx" --include="*.jsx" --include="*.css"
# Hardcoded rgb/hsl values
grep -rn 'rgb(\|rgba(\|hsl(' --include="*.tsx" --include="*.jsx" --include="*.css"
# Arbitrary Tailwind colour values
grep -rn '\[#' --include="*.tsx" --include="*.jsx"
```

**Rule:** All colours must come from the theme. Hardcoded values break dark mode, theming, and consistency. The only exception is SVG paths that require specific fill values.

### Typography
```bash
# Custom font sizes outside the scale
grep -rn 'fontSize:\|font-size:' --include="*.tsx" --include="*.jsx" --include="*.css" | grep -v 'text-xs\|text-sm\|text-base\|text-lg\|text-xl\|text-2xl\|text-3xl'
# Arbitrary text size values in Tailwind
grep -rn 'text-\[' --include="*.tsx" --include="*.jsx"
```

**Rule:** Use the type scale. Custom font sizes create visual inconsistency and make future scale changes painful.

### Spacing
```bash
# Arbitrary spacing values
grep -rn 'p-\[\|m-\[\|gap-\[\|space-\[' --include="*.tsx" --include="*.jsx"
# Inline style spacing
grep -rn 'padding:\|margin:' --include="*.tsx" --include="*.jsx" | grep -v '.css\|.module'
```

**Rule:** Use the spacing scale (4px increments in Tailwind). Arbitrary values like `py-[72px]` or `mt-[13px]` indicate a spacing system violation. If the design requires non-standard spacing, the design should be questioned, not worked around with arbitrary values.

### Border Radius
```bash
# Arbitrary border radius
grep -rn 'rounded-\[' --include="*.tsx" --include="*.jsx"
```

**Rule:** Use the border radius scale. Consistent rounding is one of the most visible aspects of design system coherence.

---

## Dimension 2: Component Patterns

### Use Existing Components
Search for patterns that reinvent existing primitives:

```bash
# Custom button implementations (should use Button component)
grep -rn '<button' --include="*.tsx" --include="*.jsx" | grep -v 'Button\|button type="submit"'
# Custom link implementations (should use Link from next/link or router)
grep -rn '<a ' --include="*.tsx" --include="*.jsx" | grep -v 'Link\|anchor'
# Custom input implementations
grep -rn '<input' --include="*.tsx" --include="*.jsx" | grep -v 'Input\|Field'
```

**Rule:** Use the design system's component primitives. Custom `<button>` elements bypass shared styling, accessibility features, and loading states.

### Props API Conventions
Check that components follow established conventions:

- `variant` for visual/semantic differences (not `type`, `style`, `kind`)
- `size` for size variations (not `large`, `isSmall`)
- `className` accepted for style overrides (using `clsx` or `cn` for merging)
- `as` or `asChild` for polymorphic rendering (not `component`, `tag`)
- Callback props prefixed with `on` (not `handle`)

### Conditional Classes
```bash
# String concatenation for classes (should use clsx/cn)
grep -rn 'className={.*+\|className={.*`' --include="*.tsx" --include="*.jsx" | grep -v 'clsx\|cn('
# Ternary in className without clsx
grep -rn 'className={.*?' --include="*.tsx" --include="*.jsx" | grep -v 'clsx\|cn('
```

**Rule:** Use `clsx` or `cn` for conditional class composition. Template literals and string concatenation produce unreadable class strings and do not handle undefined/false values cleanly.

### Dark Mode
```bash
# dark:hidden / dark:block pattern (should use ThemeImage)
grep -rn 'dark:hidden\|dark:block' --include="*.tsx" --include="*.jsx"
# Checking for images without ThemeImage
grep -rn '<img\|<Image' --include="*.tsx" --include="*.jsx" | grep -v 'ThemeImage'
```

**Rule:** Use `ThemeImage` for images that need dark mode variants. The `dark:hidden` / `dark:block` pattern duplicates DOM elements and increases payload.

---

## Dimension 3: State Coverage

Check that the implementation handles all required states:

### Interactive Elements Must Have:
- **Default**: Base appearance — verified by reading the component
- **Hover**: `hover:` classes present on interactive elements
- **Focus**: `focus:` or `focus-visible:` classes present — MUST be visible
- **Active**: `active:` class for press feedback
- **Disabled**: `disabled:` classes AND `aria-disabled` or `disabled` attribute

```bash
# Interactive elements without hover states
grep -rn 'onClick' --include="*.tsx" --include="*.jsx" -l | xargs grep -L 'hover:'
# Interactive elements without focus states
grep -rn 'onClick' --include="*.tsx" --include="*.jsx" -l | xargs grep -L 'focus:\|focus-visible:'
```

### Data-Dependent Components Must Have:
- **Loading**: Skeleton or spinner while data loads
- **Error**: Error state with recovery action
- **Empty**: Empty state with guidance (not a blank screen)

```bash
# Components using fetch/query without loading state
grep -rn 'useQuery\|useSWR\|fetch(' --include="*.tsx" --include="*.jsx" -l | xargs grep -L 'loading\|isLoading\|skeleton\|Skeleton'
# Components without error handling
grep -rn 'useQuery\|useSWR' --include="*.tsx" --include="*.jsx" -l | xargs grep -L 'error\|isError\|Error'
```

---

## Dimension 4: Accessibility

### Keyboard Support
- All interactive elements reachable via Tab
- Custom interactive elements have `tabIndex={0}` and keyboard handlers
- No positive `tabIndex` values (breaks natural flow)
- Focus trapping on modals/dialogs
- Escape key closes overlays

### Screen Reader Support
- Meaningful `alt` text on images
- `aria-label` on icon-only buttons
- `sr-only` text for visual-only information
- Form inputs have associated labels
- Live regions for dynamic updates

### Contrast
- Text meets 4.5:1 on its background (normal text)
- Large text (18px+ / 14px+ bold) meets 3:1
- Interactive element boundaries meet 3:1
- Focus indicators meet 3:1 against adjacent colours

```bash
# Find potential contrast issues: light grey text on white
grep -rn 'text-gray-300\|text-gray-400\|text-slate-300\|text-slate-400' --include="*.tsx" --include="*.jsx"
# Icon-only buttons without labels
grep -rn '<button\|<Button' --include="*.tsx" --include="*.jsx" | grep 'Icon\|icon' | grep -v 'aria-label\|sr-only\|title'
```

---

## Dimension 5: Responsive Design

### Breakpoint Coverage
Verify the component has responsive styles:

```bash
# Check for responsive breakpoint usage
grep -rn 'sm:\|md:\|lg:\|xl:' --include="*.tsx" --include="*.jsx" [target]
```

**Rule:** Every layout component must have at least mobile and desktop styles. Components that only have desktop styles are incomplete.

### Common Responsive Issues
- Fixed widths (`w-[400px]`) that overflow on mobile — use `max-w-` or responsive widths
- Multi-column layouts without mobile stacking — use `flex-col sm:flex-row`
- Text that is too large on mobile — use responsive text sizes
- Touch targets smaller than 44x44px — check padding on mobile buttons/links
- Horizontal scrolling at any viewport width

```bash
# Fixed widths that may overflow
grep -rn 'w-\[.*px\]\|width:.*px' --include="*.tsx" --include="*.jsx" | grep -v 'max-w\|min-w'
```

---

## Dimension 6: Code Quality

### Component Structure
- Props are typed (TypeScript interface or type)
- Default props are specified
- Component uses `forwardRef` if it wraps a native element
- Component accepts `className` for customisation
- No inline styles (use Tailwind classes or CSS modules)

### Performance
- No unnecessary re-renders (check for object/array literals in JSX)
- Images use `next/image` with proper dimensions
- Large lists use virtualisation
- Heavy components use `React.lazy` or dynamic imports

```bash
# Object literals in JSX (cause re-renders)
grep -rn 'style={{' --include="*.tsx" --include="*.jsx"
# Array literals in JSX props
grep -rn '={\[\]}\|={(\[' --include="*.tsx" --include="*.jsx"
```

---

## Output Format

Present findings in three severity levels:

```markdown
# Design Review: [Target]

**Reviewed:** [files/components reviewed]
**Design system:** [name/location of the design system referenced]

## Blockers (must fix before merge)
Issues that break accessibility, design system compliance, or user experience.

### [Issue title]
- **File:** `[path:line]`
- **Issue:** [What is wrong]
- **Fix:** [Specific change to make]

## Suggestions (should fix, not blocking)
Issues that reduce quality but are not critical.

### [Issue title]
- **File:** `[path:line]`
- **Issue:** [What is wrong]
- **Fix:** [Specific change to make]

## Nits (minor, fix if touching this code)
Style preferences, minor inconsistencies, optimisations.

### [Issue title]
- **File:** `[path:line]`
- **Issue:** [What is wrong]
- **Fix:** [Specific change to make]

## Summary
- Blockers: N
- Suggestions: N
- Nits: N
- **Verdict:** [Approve / Approve with changes / Request changes]
```

**Verdict criteria:**
- **Approve**: No blockers, suggestions are minor
- **Approve with changes**: No blockers, but suggestions should be addressed in a follow-up
- **Request changes**: Has blockers that must be fixed before merge

## Related Skills

- `/ui-designer:component-spec` — review the design against the component spec to catch deviations.
- `/ui-designer:accessibility-audit` — run an accessibility audit alongside the design review for UI changes.
