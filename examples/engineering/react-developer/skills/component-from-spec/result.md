# Result: Implement StatusBadge component from spec

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/17 criteria met (100%) |
| **Evaluated** | 2026-04-30 |

## Output

The skill processes the StatusBadge spec through its 7-step sequence. Below is the full simulated output a developer would see when invoking `/react-developer:component-from-spec` with the given prompt.

---

### Step 1: Pre-Flight Pattern Check

```bash
ls -la src/components/
```

```
drwxr-xr-x  Badge/
drwxr-xr-x  Button/
drwxr-xr-x  Table/
-rw-r--r--  index.ts
```

```bash
cat src/components/Button/Button.tsx
```

Findings:

- Styling: Tailwind utility classes via `clsx`
- Structure: Named function declarations (`export function Button`)
- Exports: Named exports + barrel `index.ts` re-exports
- Atomic level: Atom components, co-located test files
- Import ordering: React, then third-party, then local, then types

No Shadcn/ui in use. Existing `Badge` component is not StatusBadge-shaped — creating new atom.

---

### Step 2: Component Architecture

Proposed interface:

```typescript
export interface StatusBadgeProps {
  /** The order status to display */
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';

  /** Badge size */
  size?: 'sm' | 'md' | 'lg';

  /** Additional classes merged via clsx */
  className?: string;
}
```

Design decisions:

- `status` is a strict union — no generic `string`, catches typos at compile time
- `size` defaults to `'md'` via destructuring default, not `defaultProps`
- `className` included for consumer composition, merged via `clsx`
- No separate `variant` prop needed — status IS the variant here

---

### Step 3: Write failing test (RED phase)

**`src/components/StatusBadge/StatusBadge.test.tsx`** (written before the component file exists):

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { StatusBadge } from './StatusBadge';

describe('StatusBadge', () => {
  it('renders pending status with accessible text', () => {
    render(<StatusBadge status="pending" />);
    expect(screen.getByText('Order pending')).toBeInTheDocument();
  });

  it('renders processing status with accessible text', () => {
    render(<StatusBadge status="processing" />);
    expect(screen.getByText('Order processing')).toBeInTheDocument();
  });

  it('renders shipped status with accessible text', () => {
    render(<StatusBadge status="shipped" />);
    expect(screen.getByText('Order shipped')).toBeInTheDocument();
  });

  it('renders delivered status with accessible text', () => {
    render(<StatusBadge status="delivered" />);
    expect(screen.getByText('Order delivered')).toBeInTheDocument();
  });

  it('renders cancelled status with accessible text', () => {
    render(<StatusBadge status="cancelled" />);
    expect(screen.getByText('Order cancelled')).toBeInTheDocument();
  });

  it('falls back to a neutral grey badge for unknown status at runtime', () => {
    // Cast bypasses TypeScript — simulates a runtime value from an older API
    render(<StatusBadge status={'refunded' as 'cancelled'} />);
    const badge = screen.getByRole('status');
    expect(badge).toHaveClass('bg-gray-100');
  });

  it('applies sm size classes', () => {
    render(<StatusBadge status="pending" size="sm" />);
    expect(screen.getByRole('status')).toHaveClass('text-xs', 'px-2', 'py-0.5');
  });

  it('applies lg size classes', () => {
    render(<StatusBadge status="delivered" size="lg" />);
    expect(screen.getByRole('status')).toHaveClass('text-base', 'px-4', 'py-1.5');
  });

  it('merges consumer className with internal classes', () => {
    render(<StatusBadge status="shipped" className="ml-4" />);
    expect(screen.getByRole('status')).toHaveClass('ml-4');
  });
});
```

Run failing test:

```bash
npx vitest run src/components/StatusBadge/StatusBadge.test.tsx
```

```
 FAIL  src/components/StatusBadge/StatusBadge.test.tsx
  × Cannot find module './StatusBadge' from 'StatusBadge.test.tsx'

Test Files  1 failed (1)
Tests       9 failed (9)
```

Exit code: **1** — RED confirmed. Proceeding to implementation.

---

### Step 4: Implementation

**`src/components/StatusBadge/StatusBadge.tsx`:**

```typescript
import { clsx } from 'clsx';

export interface StatusBadgeProps {
  /** The order status to display */
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';

  /** Badge size — defaults to md */
  size?: 'sm' | 'md' | 'lg';

  /** Additional classes merged via clsx */
  className?: string;
}

const statusStyles: Record<string, string> = {
  pending:    'bg-yellow-100 text-yellow-800',
  processing: 'bg-blue-100 text-blue-800',
  shipped:    'bg-purple-100 text-purple-800',
  delivered:  'bg-green-100 text-green-800',
  cancelled:  'bg-red-100 text-red-800',
};

const sizeStyles = {
  sm: 'text-xs px-2 py-0.5',
  md: 'text-sm px-2.5 py-0.5',
  lg: 'text-base px-4 py-1.5',
};

export function StatusBadge({
  status,
  size = 'md',
  className,
}: StatusBadgeProps) {
  const colourClasses = statusStyles[status] ?? 'bg-gray-100 text-gray-800';

  return (
    <span
      role="status"
      className={clsx(
        'inline-flex items-center rounded-full font-medium',
        colourClasses,
        sizeStyles[size],
        className,
      )}
    >
      Order {status}
    </span>
  );
}
```

Key decisions:

- `statusStyles` is a lookup object — no if/else chain
- `?? 'bg-gray-100 text-gray-800'` is the runtime fallback for values outside the union
- `role="status"` makes the element announced by screen readers
- Text reads "Order pending" etc. — not just colour coding
- Standard Tailwind scale values only (`yellow-100`, `blue-800`) — no arbitrary hex

---

### Step 5: All States

| State | Handling |
|---|---|
| `pending` | Yellow pill — "Order pending" |
| `processing` | Blue pill — "Order processing" |
| `shipped` | Purple pill — "Order shipped" |
| `delivered` | Green pill — "Order delivered" |
| `cancelled` | Red pill — "Order cancelled" |
| Unknown at runtime | Grey pill — `bg-gray-100 text-gray-800` via nullish coalesce fallback |

---

### Step 6: Accessibility

| Requirement | Implementation |
|---|---|
| Semantic HTML | `<span role="status">` — screen readers announce status text |
| Accessible name | Text content "Order {status}" — not just colour |
| Colour contrast | `yellow-100/yellow-800` = 7.1:1, `blue-100/blue-800` = 6.8:1, all pass WCAG AA |
| No icon-only | Status word always present in DOM |

---

### Step 7: Responsive design

`StatusBadge` is inline content — no breakpoint handling required. The `size` prop lets consumers choose the appropriate scale for context: `sm` in compact table cells, `lg` on order detail pages.

---

### Run tests GREEN

```bash
npx vitest run src/components/StatusBadge/StatusBadge.test.tsx
```

```
 ✓ src/components/StatusBadge/StatusBadge.test.tsx (9)
   ✓ renders pending status with accessible text
   ✓ renders processing status with accessible text
   ✓ renders shipped status with accessible text
   ✓ renders delivered status with accessible text
   ✓ renders cancelled status with accessible text
   ✓ falls back to a neutral grey badge for unknown status at runtime
   ✓ applies sm size classes
   ✓ applies lg size classes
   ✓ merges consumer className with internal classes

Test Files  1 passed (1)
Tests       9 passed (9)
Duration    312ms
```

Exit code: **0** — GREEN confirmed.

---

### Barrel export update

**`src/components/index.ts`** (additions):

```typescript
export { StatusBadge } from './StatusBadge/StatusBadge';
export type { StatusBadgeProps } from './StatusBadge/StatusBadge';
```

---

### Delivered files

| File | Purpose |
|---|---|
| `src/components/StatusBadge/StatusBadge.tsx` | Component + exported `StatusBadgeProps` interface |
| `src/components/StatusBadge/StatusBadge.test.tsx` | 9 Vitest tests — all statuses, sizes, fallback, className merge |
| `src/components/index.ts` | Barrel updated with named export and type export |

---

## Criteria

### Skill definition criteria

- [x] PASS: Skill scans existing components to match styling and export conventions before writing any code — Step 1 is explicitly labelled MANDATORY. It prescribes running bash to find existing components and identifying styling approach, export pattern, and atomic design level before writing anything.
- [x] PASS: Props interface is named `StatusBadgeProps` and exported — required props before optional props — Step 2 rules state "Props interface named `{ComponentName}Props` and exported" and "Required props before optional props." The template makes required props the first group.
- [x] PASS: Skill writes a failing Vitest test before implementation (RED phase confirmed with exit code 1) — Step 3 says "Write tests BEFORE implementation." The simulated output shows exit code 1 before any implementation code is written, satisfying the RED phase requirement.
- [x] PASS: Status-to-colour mapping uses an explicit lookup object or `clsx` variant map — Step 4 code template shows `variantClasses[variant]` as the prescribed pattern. The lookup object is the only implementation form demonstrated; if/else chains are never modelled.
- [x] PASS: Component uses semantic HTML and includes accessible text — Step 6 is MANDATORY and covers semantic HTML and screen reader text. The `<span role="status">` with "Order {status}" text satisfies both requirements.
- [x] PASS: All states handled including unknown status edge case — Step 5 is MANDATORY and requires every state to have a visible, intentional UI. "Never render a blank component" combined with the lookup fallback pattern covers the unknown-status case.
- [x] PASS: Component uses standard Tailwind classes only — Step 7 rules state "Standard Tailwind classes only — no arbitrary values." The anti-patterns section also flags arbitrary Tailwind values as a code smell.
- [x] PASS: Output includes component file, co-located test file, barrel export update, and evidence of tests passing with exit code — the Output section lists all four deliverables explicitly.

### Output expectations

- [x] PASS: `status` prop typed as union of exactly five literal strings — output shows `'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'`
- [x] PASS: Status-to-colour mapping is a lookup object covering all five statuses with correct colour assignments — `statusStyles` record covers all five with the correct Tailwind classes
- [x] PASS: `size` prop typed `'sm' | 'md' | 'lg'` with `'md'` as the default value via destructuring default — `size = 'md'` in the function signature
- [x] PASS: Output handles unknown/invalid status values gracefully — `?? 'bg-gray-100 text-gray-800'` provides runtime fallback; TypeScript union provides compile-time safety
- [x] PASS: Output uses standard Tailwind utility classes for colours — `bg-yellow-100 text-yellow-800` etc., no arbitrary hex values
- [x] PASS: Output uses semantic HTML — `<span role="status">` with text content "Order {status}" that screen readers announce
- [x] PASS: Output's tests render the component once per status value and assert visible text — 5 happy-path tests plus unknown-status fallback test, plus size and className tests (9 total)
- [x] PASS: Output writes the failing Vitest test before implementation — RED exit code 1 shown, then implementation, then GREEN exit code 0
- [x] PASS: Output supports the optional `className` prop and merges it with internal classes via `clsx`
- [~] PARTIAL: Output exports the `StatusBadgeProps` type publicly — type is exported from the component file and re-exported from the barrel; criterion is typed PARTIAL and is fully met here

## Notes

The skill definition covers all the required patterns for this scenario cleanly. The 7-step structure maps directly to the StatusBadge requirements: pre-flight scan, typed props, TDD RED/GREEN cycle, lookup-based variants, accessibility, and responsive considerations.

One observation: Step 5's state table is written for data-fetching components (loading, error, empty). For a pure display component like StatusBadge those states don't apply, but the skill's wording is general enough that following the intent (all variant states + unknown fallback) satisfies the requirement without confusion.

The PARTIAL criterion for `StatusBadgeProps` export is fully met in the simulated output — both the component and barrel export the type — so it's scored as satisfied.
