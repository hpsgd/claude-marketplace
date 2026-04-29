# Output: Data table component implementation

**Verdict:** PASS
**Score:** 17.5/19 criteria met (92%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent reads CLAUDE.md and scans existing components before writing any code — Pre-Flight is labelled MANDATORY. Step 1 reads `CLAUDE.md` and `.claude/CLAUDE.md`. Step 2 mandates `Glob(pattern="src/components/**/*.tsx")`, barrel export check, and UI library check. All required before writing code.
- [x] PASS: Agent identifies that sorting, filtering, and pagination state must live in URL search params (not useState) — met in two explicit locations: Data Patterns ("URL search params for pagination/filter state (not useState) — survives refresh and back/forward") and Principles ("URL state over component state. Pagination, filters, and search terms belong in URL search params, not useState").
- [x] PASS: Agent writes a failing Vitest test first (RED) before implementing the component — TDD Iron Law is MANDATORY: "No production code without a failing test first." RED step requires exit code 1 and a meaningful failure message.
- [x] PASS: Agent defines a typed `DataTableProps` interface with exported type — Component Conventions require "TypeScript interface named `ComponentNameProps`"; barrel export via `src/components/index.ts` makes exporting the interface the required convention.
- [x] PASS: Agent handles all required states: loading (skeleton), empty, and populated — Pre-Implementation Checklist: "States: Loading, error, empty, success all handled?" Output Format Checklist confirms this is a required output section.
- [x] PASS: Agent uses `clsx` for conditional class composition, not string concatenation — Component Conventions: "Conditional classes: clsx — never string concatenation." Direct and unambiguous.
- [x] PASS: Agent flags the decision checkpoint for adding a new shared component — Decision Checkpoints: "Creating a new component that might already exist → STOP and ask. Check UI library and existing components first." Explicit mandatory stop trigger.
- [~] PARTIAL: Agent covers accessibility requirements — keyboard navigation for sortable headers, appropriate ARIA attributes — Pre-Implementation Checklist covers "Keyboard navigation, ARIA attributes, colour contrast, focus management" broadly. General ARIA guidance is present but table-specific semantics (`aria-sort` values, button-in-th for sortable columns) are not prescribed. Framework is there; table-specific detail is not.
- [x] PASS: Output includes TDD Evidence (RED/GREEN commands with exit codes) and a Checklist section — Output Format template explicitly requires both, with exact field names and exit code notation.

### Output expectations

- [x] PASS: Output places `DataTable` in the shared components folder — Pre-Flight Step 2 classifies components by atomic level and shared vs. app-specific; the prompt states the table is used on two separate pages, so the agent classifies it as shared.
- [x] PASS: Output's `DataTableProps` is a typed and exported interface with generic `<T>` type parameter — TypeScript strict mode and Component Conventions drive typed interfaces; generic `<T>` for row data follows from strict mode and `noUncheckedIndexedAccess`.
- [x] PASS: Output stores sort, filter, and page state in URL search params using `useSearchParams` / `usePathname` from `next/navigation` — Data Patterns section mandates this; Next.js App Router section covers the navigation imports.
- [x] PASS: Output's text filter uses a debounce before updating `?q=` param — Data Patterns explicitly mentions "`DebouncedSearch` for text filters (URL param → server refetch)."
- [x] PASS: Output's column header click handler toggles sort direction and updates URL params — "No client-side filtering, sorting, or pagination — server does the work" combined with URL state principle drives correct implementation.
- [x] PASS: Output renders three distinct UI states — loading skeleton, empty state, populated table — Pre-Implementation Checklist and Output Format Checklist both mandate this.
- [x] PASS: Output uses `clsx` for conditional classNames — explicitly mandated in Component Conventions.
- [x] PASS: Output writes the failing Vitest test first with RED/GREEN evidence and exit codes — Iron Law is non-negotiable; Output Format mandates commands with exit codes.
- [~] PARTIAL: Output addresses accessibility — `aria-sort` on sortable headers, keyboard-activatable — Pre-Implementation Checklist covers ARIA and keyboard navigation generally. `aria-sort` attribute with ascending/descending/none values and button-inside-th are derivable but not explicitly prescribed by the definition. A well-aligned agent would likely get there; the definition doesn't guarantee the exact pattern.
- [~] PARTIAL: Output checks the project's existing UI library for an existing Table primitive — Decision Checkpoints and Pre-Flight Step 2 both require checking the UI library. However, the definition doesn't require this to surface explicitly as a named decision in the output's Decisions section — it may happen silently during Pre-Flight.

## Notes

The definition is strong. URL state is the most forcefully stated convention in the file, appearing in both Principles and Data Patterns with identical intent. TDD is unusually explicit for an agent definition — the Iron Law with exit codes and failure caps gives high confidence the RED phase actually fires before any production code.

The main ceiling is accessibility specificity. The definition covers ARIA and keyboard navigation as checklist items but doesn't prescribe table-specific patterns. An agent following this definition would likely produce correct `aria-sort` usage, but the definition doesn't guarantee it.

The `DataTableProps` generic criterion warrants a note: the definition requires `ComponentNameProps` naming and strict TypeScript, but doesn't explicitly require a generic `<T>` parameter on the table. The agent would produce it as a natural consequence of strict typing, but it's not mandated.
