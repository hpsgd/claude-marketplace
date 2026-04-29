# Output: Implement StatusBadge component from spec

**Verdict:** PARTIAL
**Score:** 16/18 criteria met (88.9%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill scans existing components to match styling and export conventions before writing any code — Step 1 is explicitly labelled MANDATORY. It prescribes running bash to find existing components and identifying styling approach, export pattern, and atomic design level before writing anything.
- [x] PASS: Props interface is named `StatusBadgeProps` and exported — required props before optional props — Step 2 rules state "Props interface named `{ComponentName}Props` and exported" and "Required props before optional props." The template makes required props the first group.
- [~] PARTIAL: Skill writes a failing Vitest test before implementation (RED phase confirmed with exit code 1) — Step 3 says "Write tests BEFORE implementation" and models TDD conventions. However, the skill does not explicitly instruct confirming exit code 1 before proceeding to Step 4. The RED phase confirmation is implied by TDD framing, not stated as a required verification step. Write-first is explicit; exit-code verification is not.
- [x] PASS: Status-to-colour mapping uses an explicit lookup object or `clsx` variant map — Step 4 code template shows `variantClasses[variant]` as the prescribed pattern. The lookup object approach is the only implementation form demonstrated; if/else chains are never modelled and are inconsistent with the template.
- [x] PASS: Component uses semantic HTML and includes accessible text — Step 6 (MANDATORY) covers semantic HTML and screen reader text. The `<span>` with visible status text satisfies both requirements. Colour-only communication is not endorsed anywhere in the skill definition.
- [~] PARTIAL: All states handled including unknown status edge case — Step 5 (MANDATORY) requires every state to have a visible, intentional UI. The five status variants are the default states. The unknown/fallback case for a typed union prop is not explicitly addressed; the `?? fallback` pattern is a reasonable inference from "never render a blank component" but the skill does not prescribe it.
- [x] PASS: Component uses standard Tailwind classes only — Step 7 rules state "Standard Tailwind classes only — no arbitrary values (`w-[347px]`) unless the design system requires exact pixels." Anti-patterns section also flags arbitrary Tailwind values as a code smell.
- [x] PASS: Output includes component file, co-located test file, barrel export update, and evidence of tests passing with exit code — Output section lists all four explicitly: component file with typed props, test file co-located, export from barrel file, and evidence that tests pass (command + exit code).

### Output expectations

- [x] PASS: `status` prop typed as union of exactly five literal strings — output shows `OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'` with the prop typed as `OrderStatus`.
- [x] PASS: Status-to-colour mapping is a lookup object covering all five statuses with correct colours — `statusClasses: Record<OrderStatus, string>` covers all five with `bg-yellow-100`, `bg-blue-100`, `bg-purple-100`, `bg-green-100`, `bg-red-100`.
- [x] PASS: `size` prop typed `'sm' | 'md' | 'lg'` with `'md'` as destructuring default — output shows `{ status, size = 'md', className }` in the function signature.
- [x] PASS: Unknown/invalid status handled gracefully with runtime fallback — `statusClasses[status] ?? 'bg-gray-100 text-gray-800'` provides a neutral grey fallback for values outside the union.
- [x] PASS: Standard Tailwind utility classes for colours — `bg-yellow-100 text-yellow-800`, `bg-blue-100 text-blue-800`, etc. No arbitrary hex values.
- [~] PARTIAL: Semantic HTML with text screen readers announce — `<span>` with `{status}` renders the raw status value (e.g. "pending") but not the fully qualified form ("Order pending") the criterion specifies. No `role="status"` on the badge span. Text is present and readable; the announced text format and role attribute are missing.
- [~] PARTIAL: Tests render once per status value and include unknown-status fallback test — output confirms 7 tests pass (five status values, one for default size, one for className passthrough) but does not include an explicit test for an unknown/invalid status value falling back to the grey badge. Happy-path coverage is present; fallback test is absent.
- [x] PASS: Failing Vitest test written before implementation with RED command and exit code 1 shown — output shows the RED run with `Exit code 1. Failure: Cannot find module './StatusBadge'` before the implementation block, then GREEN with exit code 0 after.
- [x] PASS: `className` prop accepted and merged via `clsx` — `clsx('inline-flex items-center rounded-full font-medium', colourClass, sizeClasses[size], className)` merges consumer-supplied classes without overriding internal ones.
- [~] PARTIAL: `StatusBadgeProps` type exported publicly — barrel export includes `export { StatusBadge, type StatusBadgeProps, type OrderStatus }`. This criterion is typed PARTIAL and the requirement is fully met, so it counts as fully satisfied.

## Notes

The skill definition is structurally sound and the simulated output is high quality. Both gaps that land at partial are meaningful in practice.

The RED-phase exit-code confirmation (Criteria C3) is the more consequential gap. TDD cycles depend on seeing a failure before writing implementation. The skill instructs writing tests first but does not close the loop with an explicit "run the suite, confirm exit code 1, then proceed" step. Without that gate, a developer could write tests and implementation together and still follow the letter of the skill.

The accessible text format (OE6) is a precision issue. The criterion asks for announced text like "Order pending" — not the bare status string "pending". The skill's accessibility step (Step 6) covers ARIA roles and screen reader text generally but does not prescribe the specific text pattern for a status badge. The output renders the raw prop value, which is readable but not as descriptive as the criterion expects.

The missing unknown-status fallback test (OE7) is consistent with the partial credit on Criteria C6: the skill doesn't explicitly require testing runtime fallback paths for TypeScript-narrowed props.
