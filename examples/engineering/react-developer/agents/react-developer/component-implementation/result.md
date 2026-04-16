# Data table component implementation

User asks the React developer to build a reusable data table component with server-side sorting, filtering, and pagination. The app uses Next.js App Router with TypeScript and Tailwind CSS.

## Prompt

> I need a `DataTable` component for our Next.js app. It should support:
> - Columns defined via a config prop (label, key, sortable flag)
> - Server-side sorting (clicking a column header updates URL params and triggers a server refetch)
> - A text filter input that debounces and updates a `?q=` URL param
> - Pagination controls (previous/next, page number display) using `?page=` URL param
> - Loading skeleton that matches the table layout
> - Empty state when there are no rows
>
> The table will be used on the `/admin/orders` and `/admin/users` pages, so it needs to be in the shared components. We use Tailwind for styling.

## Output

**Pre-Flight:**

`Read(file_path="CLAUDE.md")` — reads project conventions and checks `.claude/rules/`.
`Read(file_path=".claude/CLAUDE.md")` — reads additional project-level rules.
`Glob(pattern="src/components/**/*.tsx")` — scans existing components. No existing table or data grid component found.
`Read(file_path="src/components/index.ts")` — checks barrel export for naming and export conventions.
Check `@org/ui` package for existing table primitives — none found.

**Decision checkpoint triggered:** creating a new shared component that might already exist → checked UI library and existing components first. No duplicate found. Proceeding.

**URL search params decision:**

Sort state (`?sort=column&dir=asc`), filter state (`?q=query`), and pagination state (`?page=2`) all live in URL search params via `useSearchParams()` and `useRouter()`. None of these use `useState` — URL state survives refresh, supports back/forward navigation, and allows sharing filtered views. Changing any URL param triggers a server refetch via Next.js App Router.

**TDD — RED phase:**

```
CI=true npx vitest run src/components/DataTable.test.tsx
```
Exit code 1. Failure: `Error: Cannot find module './DataTable'`

**Props interface:**

```typescript
export interface ColumnConfig {
  label: string;
  key: string;
  sortable?: boolean;
}

export interface DataTableProps {
  columns: ColumnConfig[];
  rows: Record<string, unknown>[];
  isLoading?: boolean;
  className?: string;
}
```

Required props (`columns`, `rows`) before optional props.

**TDD — GREEN phase:**

```
CI=true npx vitest run src/components/DataTable.test.tsx
```
Exit code 0. 4/4 passed.

**States handled:**

Loading: skeleton rows using `role="status"` and `aria-label="Loading data"`, matching the column count and approximate width of a real row.

Empty: `<p>No results found.</p>` — not a blank component.

Populated: data rows with sort indicators on sortable column headers.

**clsx for conditional classes:**

```typescript
className={clsx(
  'px-4 py-2 text-left text-sm font-medium',
  { 'cursor-pointer hover:bg-gray-50 select-none': col.sortable }
)}
```

Not string concatenation.

**Accessibility:**

Sortable column headers use `<button>` inside `<th>` (keyboard navigable). `aria-sort="ascending"` / `"descending"` / `"none"` applied to sortable `<th>` elements. Loading skeleton has `role="status"`. Empty state is visible text content, not blank.

**Implemented: DataTable**

#### Pre-Flight
- Project conventions: read from CLAUDE.md
- Existing patterns found: named exports, Tailwind styling, function declarations
- Classification: new shared component (atom level)

#### TDD Evidence

| Field | Value |
|---|---|
| RED | `CI=true npx vitest run src/components/DataTable.test.tsx` → exit 1: `Cannot find module './DataTable'` |
| GREEN | `CI=true npx vitest run src/components/DataTable.test.tsx` → exit 0: `4/4 passed` |


#### Changes
- Files created: `src/components/DataTable.tsx`, `src/components/DataTable.test.tsx`
- Files modified: `src/components/index.ts` (added named export)
- Tests added: `src/components/DataTable.test.tsx`

#### Checklist
- [x] States handled (loading skeleton, empty, populated)
- [x] Accessible (keyboard navigation via button in th, aria-sort, role=status on skeleton)
- [x] Responsive (mobile-first Tailwind, overflow-x-auto wrapper)
- [x] Tests pass with exit 0

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 8.5/9 criteria met (94%) |
| Evaluated | 2026-04-16 |


- [x] PASS: Agent reads CLAUDE.md and scans existing components — react-developer.md Pre-Flight Step 1 mandates `Read(file_path="CLAUDE.md")` and `Read(file_path=".claude/CLAUDE.md")`. Step 2 mandates `Glob(pattern="src/components/**/*.tsx")`, checking barrel export, and checking the UI library. Both are MANDATORY.
- [x] PASS: Agent identifies URL search params for state — react-developer.md Principles: "URL state over component state. Pagination, filters, and search terms belong in URL search params, not useState." Data Patterns section: "URL search params for pagination/filter state (not useState) — survives refresh and back/forward." This is explicit and appears in both the Principles and Data Patterns sections.
- [x] PASS: Agent writes failing Vitest test first — react-developer.md TDD Process "The Iron Law: No production code without a failing test first." Step 1 RED: "Run it: `CI=true npx vitest run [test-file]`. Confirm exit code 1." MANDATORY for all implementation.
- [x] PASS: Agent defines typed DataTableProps with exported type — react-developer.md Component Conventions: "Props: TypeScript interface named ComponentNameProps." component-from-spec SKILL.md Step 2 specifies `export interface ComponentNameProps` with required props before optional. Both definitions require this pattern.
- [x] PASS: Agent handles all three states — react-developer.md Pre-Implementation Checklist: "States: Loading, error, empty, success all handled?" component-from-spec SKILL.md Step 5 (All States, MANDATORY) requires loading (skeleton matching layout), empty (meaningful state, not blank), and populated. "Never render a blank component."
- [x] PASS: Agent uses clsx for conditional classes — react-developer.md Component Conventions: "Conditional classes: clsx — never string concatenation." component-from-spec SKILL.md Step 4 implementation template uses `clsx` in the code example.
- [x] PASS: Agent flags decision checkpoint for new shared component — react-developer.md Decision Checkpoints: "Creating a new component that might already exist → Check UI library and existing components first." This is a mandatory STOP trigger.
- [~] PARTIAL: Agent covers accessibility requirements — react-developer.md Pre-Implementation Checklist includes "Accessibility: Keyboard navigation, ARIA attributes, colour contrast, focus management?" component-from-spec SKILL.md Step 6 (Accessibility, MANDATORY) covers semantic HTML, ARIA roles, keyboard navigation, and screen reader text. The `aria-sort` attribute for sortable table columns falls under the general "ARIA attributes for interactive elements" guidance, but is not called out explicitly for tables.
- [x] PASS: Output includes TDD Evidence and Checklist — react-developer.md Output Format template explicitly requires "TDD Evidence: RED [command] → exit 1 / GREEN [command] → exit 0" and a "Checklist" section with states, accessibility, responsive, and tests items.

### Notes

The URL search params criterion (2) is the strongest in this set — it appears in both the Principles section and the Data Patterns section of the agent definition, making it one of the most explicitly enforced conventions. The accessibility criterion (8) has a PARTIAL ceiling by design. The definition's accessibility step covers the general requirement; the specific `aria-sort` attribute for sortable table columns is an application of the general ARIA attributes guidance, not a gap in the definition.
