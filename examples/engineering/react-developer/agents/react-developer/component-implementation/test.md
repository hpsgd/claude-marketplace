# Test: Data table component implementation

Scenario: User asks the React developer to build a reusable data table component with server-side sorting, filtering, and pagination. The app uses Next.js App Router with TypeScript and Tailwind CSS.

## Prompt

I need a `DataTable` component for our Next.js app. It should support:
- Columns defined via a config prop (label, key, sortable flag)
- Server-side sorting (clicking a column header updates URL params and triggers a server refetch)
- A text filter input that debounces and updates a `?q=` URL param
- Pagination controls (previous/next, page number display) using `?page=` URL param
- Loading skeleton that matches the table layout
- Empty state when there are no rows

The table will be used on the `/admin/orders` and `/admin/users` pages, so it needs to be in the shared components. We use Tailwind for styling.

## Criteria

- [ ] PASS: Agent reads CLAUDE.md and scans existing components before writing any code
- [ ] PASS: Agent identifies that sorting, filtering, and pagination state must live in URL search params (not useState)
- [ ] PASS: Agent writes a failing Vitest test first (RED) before implementing the component
- [ ] PASS: Agent defines a typed `DataTableProps` interface with exported type
- [ ] PASS: Agent handles all required states: loading (skeleton), empty, and populated
- [ ] PASS: Agent uses `clsx` for conditional class composition, not string concatenation
- [ ] PASS: Agent flags the decision checkpoint for adding a new shared component (checks UI library for existing primitives)
- [ ] PARTIAL: Agent covers accessibility requirements — keyboard navigation for sortable headers, appropriate ARIA attributes
- [ ] PASS: Output includes TDD Evidence (RED/GREEN commands with exit codes) and a Checklist section
