# Implement StatusBadge component from spec

Developer invokes the component-from-spec skill with a spec for a StatusBadge component that renders a coloured badge for order statuses: pending (yellow), processing (blue), shipped (purple), delivered (green), cancelled (red).

## Prompt

> Implement from this spec: A `StatusBadge` component that displays an order status as a coloured pill badge. Variants map to statuses: pending=yellow, processing=blue, shipped=purple, delivered=green, cancelled=red. Accepts a `status` prop (typed union), an optional `size` prop (sm | md | lg, default md), and an optional `className`. Should be accessible (screen readers should read the status text). Used in order list tables and order detail pages.

## Output

**Step 1 — Pre-flight pattern check:**

```bash
ls -la src/components/
```

Scans for existing badge or pill components — none found. Reads `src/components/index.ts` — named exports, function declarations, Tailwind classes, no CSS modules. Atomic design level: atom.

**Step 2 — Props interface:**

```typescript
export type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';

export interface StatusBadgeProps {
  status: OrderStatus;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}
```

Required prop (`status`) before optional props (`size`, `className`).

**Step 3 — TDD (RED):**

```
CI=true npx vitest run src/components/StatusBadge.test.tsx
```

Exit code 1. Failure: `Error: Cannot find module './StatusBadge'`

**Step 4 — Implementation with lookup object:**

```typescript
import { clsx } from 'clsx';

const statusClasses: Record<OrderStatus, string> = {
  pending: 'bg-yellow-100 text-yellow-800',
  processing: 'bg-blue-100 text-blue-800',
  shipped: 'bg-purple-100 text-purple-800',
  delivered: 'bg-green-100 text-green-800',
  cancelled: 'bg-red-100 text-red-800',
};

const sizeClasses = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-1 text-sm',
  lg: 'px-3 py-1.5 text-base',
};

export function StatusBadge({ status, size = 'md', className }: StatusBadgeProps) {
  const colourClass = statusClasses[status] ?? 'bg-gray-100 text-gray-800';
  return (
    <span
      className={clsx(
        'inline-flex items-center rounded-full font-medium',
        colourClass,
        sizeClasses[size],
        className
      )}
    >
      {status}
    </span>
  );
}
```

Not an if/else chain. TypeScript exhaustiveness via `Record<OrderStatus, string>`.

**Step 5 — All states:**

All 5 status values render with the correct colour class. Unknown status (runtime edge case — TypeScript union prevents it at compile time, but the `?? 'bg-gray-100 text-gray-800'` fallback handles runtime surprises).

**Step 6 — Accessibility:**

Status text is rendered as visible content in the `<span>`, so screen readers read it directly. Colour coding is supplementary, not the only indicator. No `aria-hidden` on the text. A `<span>` with inline text is correct semantic HTML for a badge.

**Step 7 — Tailwind:**

`bg-yellow-100`, `text-yellow-800`, `bg-blue-100`, `px-2.5`, `py-1`, `rounded-full` — all standard Tailwind scale values. No arbitrary values.

**TDD (GREEN):**

```
CI=true npx vitest run src/components/StatusBadge.test.tsx
```

Exit code 0. 7/7 passed (one test per status value, one for default size, one for className passthrough).

**Output:**

- `src/components/StatusBadge.tsx` — component with typed props, lookup table, accessibility
- `src/components/StatusBadge.test.tsx` — co-located, behaviour-based tests
- `src/components/index.ts` — updated with `export { StatusBadge, type StatusBadgeProps, type OrderStatus }`
- Test evidence: exit code 0, 7/7 passed

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8/8 criteria met (100%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Skill scans existing components before writing code — component-from-spec SKILL.md Step 1 (Pre-Flight Pattern Check, MANDATORY): "Before writing any code, examine existing components to match project conventions." Lists specific checks: styling approach, component structure, export pattern, atomic design level.
- [x] PASS: Props interface named StatusBadgeProps, exported, required before optional — component-from-spec SKILL.md Step 2: "Props interface named `{ComponentName}Props` and exported." Rules: "Required props before optional props." The template shows this structure explicitly.
- [x] PASS: Skill writes failing test before implementation — component-from-spec SKILL.md Step 3 (TDD for Components): "Write tests BEFORE implementation." Rules include confirming exit code 1 in the RED phase before writing any production code.
- [x] PASS: Status-to-colour mapping uses lookup object — component-from-spec SKILL.md Step 4 implementation template uses `variantClasses[variant]` lookup pattern explicitly in the code template. The implementation pattern in the definition is a lookup object, not an if/else chain.
- [x] PASS: Semantic HTML with accessible text — component-from-spec SKILL.md Step 6 (Accessibility, MANDATORY): "Semantic HTML: Use `<button>`, `<nav>`, `<main>`, `<article>`, not `<div onClick>`." For a badge, making the status text visible (not `aria-hidden`) ensures screen readers can read it without additional ARIA markup.
- [x] PASS: All 5 status values plus unknown status edge case — component-from-spec SKILL.md Step 5 (All States, MANDATORY): "Never render a blank component. Every state has a visible, intentional UI." All five status values are the default states; the unknown status fallback handles the edge case required by "every state."
- [x] PASS: Standard Tailwind classes only — component-from-spec SKILL.md Step 7 Rules: "Standard Tailwind classes only — no arbitrary values (`w-[347px]`) unless the design system requires exact pixels." Anti-Patterns: "Arbitrary Tailwind values — `text-[13.5px]` is a code smell."
- [x] PASS: Output includes component file, test file, barrel export, and test evidence — component-from-spec SKILL.md Output section: "Deliver: 1. Component file with typed props, all states, accessibility. 2. Test file co-located, testing behaviour not implementation. 3. Export from the appropriate barrel file. 4. Any extracted sub-components. 5. Evidence that tests pass (command + exit code)." All four required artefacts are explicitly listed.

### Notes

Every criterion traces to a specific step or rule in component-from-spec SKILL.md. The lookup object criterion (4) is supported by the Step 4 implementation template rather than a prohibition of if/else chains — the template is the prescribed approach. The accessibility criterion (5) is met through visible text content; a `<span>` badge that shows the status word is inherently accessible without additional ARIA. No gaps identified in this definition for this scenario.
