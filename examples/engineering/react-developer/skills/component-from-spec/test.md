# Test: Implement StatusBadge component from spec

Scenario: Developer invokes the component-from-spec skill with a spec for a StatusBadge component that renders a coloured badge for order statuses: pending (yellow), processing (blue), shipped (purple), delivered (green), cancelled (red).

## Prompt

Implement from this spec: A `StatusBadge` component that displays an order status as a coloured pill badge. Variants map to statuses: pending=yellow, processing=blue, shipped=purple, delivered=green, cancelled=red. Accepts a `status` prop (typed union), an optional `size` prop (sm | md | lg, default md), and an optional `className`. Should be accessible (screen readers should read the status text). Used in order list tables and order detail pages.

## Criteria

- [ ] PASS: Skill scans existing components to match styling and export conventions before writing any code
- [ ] PASS: Props interface is named `StatusBadgeProps` and exported — required props before optional props
- [ ] PASS: Skill writes a failing Vitest test before implementation (RED phase confirmed with exit code 1)
- [ ] PASS: Status-to-colour mapping uses an explicit lookup object or `clsx` variant map — not a chain of if/else
- [ ] PASS: Component uses semantic HTML appropriate for its role and includes accessible text (not just colour coding)
- [ ] PASS: All states are handled — the component renders correctly for all 5 status values plus any edge cases (unknown status)
- [ ] PASS: Component uses standard Tailwind classes — no arbitrary values like `bg-[#f5a623]`
- [ ] PASS: Output includes component file, co-located test file, barrel export update, and evidence of tests passing with exit code

## Output expectations

- [ ] PASS: Output's `status` prop is typed as a union of exactly the five literal strings — `'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'` — not a generic string
- [ ] PASS: Output's status-to-colour mapping is a lookup object or `clsx`/`cva` variant map covering all five statuses (pending=yellow, processing=blue, shipped=purple, delivered=green, cancelled=red), not an if/else chain
- [ ] PASS: Output's `size` prop is typed `'sm' | 'md' | 'lg'` with `'md'` as the default value (via destructuring default), not just documented as the default
- [ ] PASS: Output handles unknown/invalid status values gracefully — either via TypeScript-narrowed exhaustive union (compile-time) plus a runtime fallback (neutral grey badge) — not an uncaught error
- [ ] PASS: Output uses standard Tailwind utility classes for colours (e.g. `bg-yellow-100 text-yellow-800`), not arbitrary hex values like `bg-[#f5a623]`
- [ ] PASS: Output uses semantic HTML — a `<span>` with `role="status"` or text content that screen readers announce ("Order pending"), not just a coloured div with no accessible name
- [ ] PASS: Output's tests render the component once per status value and assert the visible text and the applied class — at minimum 5 tests for happy paths plus an unknown-status fallback test
- [ ] PASS: Output writes the failing Vitest test before implementation — RED command and exit code 1 shown — then implementation, then GREEN with exit code 0
- [ ] PASS: Output supports the optional `className` prop and merges it with internal classes via `clsx`/`cn` so consumers can extend without overriding
- [ ] PARTIAL: Output exports the `StatusBadgeProps` type publicly so order-list-table and order-detail consumers can compose with it (`Pick<StatusBadgeProps, 'status'>` etc.)
