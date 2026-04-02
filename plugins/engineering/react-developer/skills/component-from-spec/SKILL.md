---
name: component-from-spec
description: Implement a React component from a design specification or component-spec output.
argument-hint: "[component spec, description, or reference to spec file]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.tsx"
  - "**/*.jsx"
---

Implement a React component from the specification at $ARGUMENTS.

## Process (sequential — do not skip steps)

### Step 1: Pre-Flight Pattern Check (MANDATORY)

Before writing any code, examine existing components to match project conventions:

1. **Scan for patterns:**
   ```bash
   # Find existing components to match conventions
   ls -la src/components/ 2>/dev/null || ls -la app/components/ 2>/dev/null
   ```

2. **Identify and match:**
   - **Styling approach:** Tailwind classes? CSS modules? Styled-components? Shadcn/ui?
   - **Component structure:** Function declarations or arrow functions?
   - **Export pattern:** Named exports? Default exports? Barrel files (`index.ts`)?
   - **Atomic design level:** Atoms, molecules, organisms? Feature-based?
   - **State management:** useState, useReducer, Zustand, Jotai?
   - **Import ordering:** React first? Third-party? Local? Types?

3. **Read the spec completely:** Props, variants, states, responsive behaviour, accessibility requirements, interactions, animations

**Rules:**
- Never introduce a new styling approach — match the existing project
- Never deviate from the existing component structure without justification
- If the project uses Shadcn/ui, compose from existing primitives before creating new ones

### Step 2: Component Architecture

Before writing JSX, design the component API:

**Props interface (TypeScript MANDATORY):**
```typescript
export interface ComponentNameProps {
  /** Required props first, grouped by purpose */
  title: string;
  items: Item[];

  /** Variant prop for visual modes */
  variant?: 'default' | 'compact' | 'expanded';

  /** State props */
  isLoading?: boolean;
  isDisabled?: boolean;

  /** Event handlers — use standard naming */
  onSelect?: (item: Item) => void;
  onDismiss?: () => void;

  /** Composition props */
  className?: string;
  children?: React.ReactNode;
}
```

**Rules:**
- Props interface named `{ComponentName}Props` and exported
- Required props before optional props
- Variant prop for visual modes — `variant`, not `type` or `mode`
- Boolean props use `is`/`has`/`can` prefix: `isLoading`, `hasError`, `canEdit`
- Event handlers use `on` prefix: `onSelect`, `onChange`, `onDismiss`
- Always accept `className` for composition (merged via `clsx`)
- Default values declared in the function signature, not in defaultProps

### Step 3: TDD for Components

Write tests BEFORE implementation. Test behaviour, not implementation details.

**Test file: `component-name.test.ts` (co-located)**

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentName } from './component-name';

describe('ComponentName', () => {
  it('renders the title', () => {
    render(<ComponentName title="Hello" items={[]} />);
    expect(screen.getByText('Hello')).toBeInTheDocument();
  });

  it('calls onSelect when an item is clicked', async () => {
    const onSelect = vi.fn();
    const items = [{ id: '1', label: 'Item 1' }];
    render(<ComponentName title="Test" items={items} onSelect={onSelect} />);

    await userEvent.click(screen.getByText('Item 1'));
    expect(onSelect).toHaveBeenCalledWith(items[0]);
  });

  it('renders loading skeleton when isLoading is true', () => {
    render(<ComponentName title="Test" items={[]} isLoading />);
    expect(screen.getByRole('status')).toBeInTheDocument();
  });

  it('renders empty state when items is empty and not loading', () => {
    render(<ComponentName title="Test" items={[]} />);
    expect(screen.getByText(/no items/i)).toBeInTheDocument();
  });
});
```

**Rules:**
- Query by role, label, or text — never by test-id unless no semantic option exists
- Use `userEvent` (not `fireEvent`) for user interactions
- Test all states: default, loading, error, empty, disabled
- Test keyboard interactions for interactive components
- No snapshot tests for logic — only for catching unintended visual changes

### Step 4: Implementation

**Component structure:**

```typescript
import { clsx } from 'clsx';

export interface ComponentNameProps {
  // ... (from Step 2)
}

export function ComponentName({
  title,
  items,
  variant = 'default',
  isLoading = false,
  isDisabled = false,
  onSelect,
  className,
}: ComponentNameProps) {
  // 1. Hooks first (useState, useEffect, custom hooks)
  // 2. Derived state (computed from props/state, no useMemo unless measured)
  // 3. Event handlers
  // 4. Early returns for special states

  if (isLoading) {
    return <ComponentNameSkeleton />;
  }

  if (items.length === 0) {
    return <ComponentNameEmpty />;
  }

  // 5. Main render
  return (
    <div className={clsx('base-classes', variantClasses[variant], className)}>
      {/* ... */}
    </div>
  );
}
```

**Rules:**
- Function declarations (`function ComponentName`), not arrow functions, for top-level components
- Hooks at the top, before any conditionals or early returns (React rules of hooks)
- Derived state computed inline — no `useMemo` unless profiling shows a performance problem
- `useCallback` only when passing to memoised children or in dependency arrays
- Early returns for loading, error, empty states — before the main render
- `clsx` for conditional class composition — never string interpolation

### Step 5: All States (MANDATORY — every state must be handled)

| State | Must handle | Implementation |
|---|---|---|
| **Default** | Always | Normal rendering with data |
| **Loading** | If data is async | Skeleton or spinner with `role="status"` and `aria-label` |
| **Error** | If data can fail | Error message with retry action |
| **Empty** | If collection can be empty | Meaningful empty state, not just blank space |
| **Disabled** | If interactive | Reduced opacity, no hover effects, `aria-disabled="true"` |
| **Hover/Focus** | If interactive | Visual feedback via CSS `:hover`/`:focus-visible` |
| **Active/Selected** | If selectable | `aria-selected="true"`, visual indicator |
| **Overflow** | If content varies | Text truncation, scrollable containers, responsive layout |

**Rules:**
- Never render a blank component. Every state has a visible, intentional UI
- Loading skeletons match the layout of the loaded state (not a generic spinner)
- Error states include a way to recover (retry button, link to support)
- Empty states explain what the user can do to populate the component

### Step 6: Accessibility (MANDATORY)

| Requirement | Implementation | Test |
|---|---|---|
| Semantic HTML | Use `<button>`, `<nav>`, `<main>`, `<article>`, not `<div onClick>` | Query by role in tests |
| ARIA roles | `role="status"` for loading, `role="alert"` for errors, `role="list"` for lists | Verify with `getByRole` |
| Keyboard navigation | Tab order, Enter/Space for activation, Escape for dismissal, Arrow keys for lists | Test with `userEvent.keyboard` |
| Focus management | Focus trap in modals, focus restoration on close, visible focus ring | Test focus element after interaction |
| Screen reader text | `aria-label` for icon buttons, `aria-live` for dynamic content | Verify ARIA attributes |
| Colour contrast | Minimum 4.5:1 for text, 3:1 for large text | Manual check against design |
| Motion | `prefers-reduced-motion` media query for animations | CSS media query |

**Rules:**
- If it's clickable, it's a `<button>`, not a `<div>` or `<span>`
- If it navigates, it's an `<a>`, not a `<button>`
- Every image has `alt` text (empty string `alt=""` for decorative images)
- Every form input has a visible label (or `aria-label` if visually hidden)
- Focus ring visible on keyboard navigation (`focus-visible`, not `focus`)

### Step 7: Responsive Design

| Breakpoint | Approach |
|---|---|
| Mobile-first | Default styles are mobile. Add complexity with `sm:`, `md:`, `lg:` |
| Touch targets | Minimum 44x44px for interactive elements on mobile |
| Layout shifts | No content jumps on load — reserve space with skeletons |
| Text overflow | Truncate with ellipsis or expand/collapse, never horizontal scroll |
| Images | `next/image` with `sizes` attribute, responsive source sets |

**Tailwind breakpoint usage:**
```tsx
<div className="flex flex-col gap-2 md:flex-row md:gap-4 lg:gap-6">
  <div className="w-full md:w-1/3 lg:w-1/4">Sidebar</div>
  <div className="w-full md:w-2/3 lg:w-3/4">Content</div>
</div>
```

**Rules:**
- Standard Tailwind classes only — no arbitrary values (`w-[347px]`) unless the design system requires exact pixels
- Mobile layout first, desktop enhancements via breakpoints
- Test at 320px, 768px, 1024px, 1440px minimum

## Anti-Patterns (NEVER do these)

- **Div soup** — using `<div>` for everything. Use semantic HTML elements
- **Prop drilling** — passing props through 3+ levels. Use context, composition, or state management
- **useEffect for derived state** — compute from props/state inline. `useEffect` is for side effects, not data transformation
- **Index as key** — use a stable unique identifier. Index keys cause bugs with reordering and deletion
- **Inline styles** — use Tailwind classes or CSS modules. Inline styles break the design system
- **Arbitrary Tailwind values** — `text-[13.5px]` is a code smell. Use standard scale values
- **Missing error boundaries** — wrap components that fetch data or use third-party libraries
- **God components** — if a component is >200 lines, extract sub-components

## Output

Deliver:
1. Component file (`component-name.tsx`) with typed props, all states, accessibility
2. Test file (`component-name.test.ts`) co-located, testing behaviour not implementation
3. Export from the appropriate barrel file (`index.ts`)
4. Any extracted sub-components (skeleton, empty state)
5. Evidence that tests pass (command + exit code)

## Related Skills

- `/ui-designer:component-spec` — this skill consumes the component spec as input. Write the spec first, then build the component from it.
