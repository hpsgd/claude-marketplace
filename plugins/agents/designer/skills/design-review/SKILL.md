---
name: design-review
description: Review a UI implementation against design system conventions, accessibility, and consistency.
argument-hint: "[file, component, or directory to review]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
---

Review $ARGUMENTS against design system conventions.

## Checks

### Design system consistency
- Components use existing design system primitives (not custom implementations)
- Tailwind classes use standard values (not arbitrary values like `py-[72px]`)
- Colour usage matches the theme (not hardcoded hex values)
- Typography follows the scale (not custom font sizes)
- Spacing follows the scale (not one-off margins/padding)

### Component patterns
- Variants use `variant` prop (not `background`, `style`, etc.)
- Props-based API (configurable, not hardcoded values)
- `ThemeImage` used for dark mode images (not `dark:hidden` patterns)
- `clsx` for conditional classes
- `Link` from `next/link` for all links (not native `<a>`)

### Accessibility
- Interactive elements have keyboard support
- Images have alt text
- Colour contrast meets WCAG AA
- Focus management on modals/dialogs
- ARIA attributes present and correct

### Responsive
- Layout works at mobile, tablet, desktop breakpoints
- No horizontal scrolling at any breakpoint
- Touch targets are at least 44x44px on mobile

## Output

Present findings grouped by severity: blockers, suggestions, nits. Include file and line for each.
