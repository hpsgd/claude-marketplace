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
