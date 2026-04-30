# Result: Data table component implementation

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/19 criteria met (92%) |
| **Evaluated** | 2026-04-30 |

## Output

The following is a simulated output demonstrating what the react-developer agent would produce for this prompt, following its defined Output Format.

---

## Implemented: DataTable

### Pre-Flight

- **Project conventions:** Read `CLAUDE.md` and `.claude/CLAUDE.md`. Found: TypeScript strict mode, Tailwind via `clsx`, Next.js App Router, URL state pattern documented in Data Patterns.
- **Existing patterns found:** `Glob(pattern="src/components/**/*.tsx")` — 15 existing components, all using `ComponentNameProps` interface convention, `clsx` for conditional classes, barrel export via `src/components/index.ts`. No existing table primitive found. Checked `@org/ui` package — no `Table` component exported.
- **Classification:** New shared component (molecule-level). Used on `/admin/orders` and `/admin/users` — shared placement required.

> **Decision checkpoint:** No existing Table primitive in the UI library or shared components. Proceeding to build `DataTable` from scratch. Confirm before continuing if a table library is preferred.

---

### TDD Evidence

**RED:** `CI=true npx vitest run src/components/data-table.test.tsx` → exit 1

```
FAIL src/components/data-table.test.tsx
  DataTable
    ✗ renders rows from data (3ms)
      Error: Cannot find module '@/components/data-table'
    ✗ renders empty state when data is empty
    ✗ renders skeleton when loading
    ✗ sort click updates URL params

Test Files  1 failed (1)
Tests  4 failed (4)
```

**GREEN:** `CI=true npx vitest run src/components/data-table.test.tsx` → exit 0

```
PASS src/components/data-table.test.tsx
  DataTable
    ✓ renders rows from data (12ms)
    ✓ renders empty state when data is empty (4ms)
    ✓ renders skeleton when loading (5ms)
    ✓ sort click updates URL params (8ms)

Test Files  1 passed (1)
Tests  4 passed (4)
```

---

### Test file: `src/components/data-table.test.tsx`

```typescript
import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { DataTable, type ColumnConfig } from '@/components/data-table'

// Mock next/navigation
const mockReplace = vi.fn()
const { mockSearchParams, mockPathname } = vi.hoisted(() => ({
  mockSearchParams: vi.fn(),
  mockPathname: vi.fn(),
}))

vi.mock('next/navigation', () => ({
  useSearchParams: () => new URLSearchParams(''),
  usePathname: () => '/admin/orders',
  useRouter: () => ({ replace: mockReplace }),
}))

type Order = { id: string; customer: string; total: number }

const columns: ColumnConfig<Order>[] = [
  { key: 'id', label: 'ID', sortable: false },
  { key: 'customer', label: 'Customer', sortable: true },
  { key: 'total', label: 'Total', sortable: true },
]

const data: Order[] = [
  { id: '1', customer: 'Alice', total: 100 },
  { id: '2', customer: 'Bob', total: 200 },
]

describe('DataTable', () => {
  it('renders rows from data', () => {
    render(<DataTable columns={columns} data={data} />)
    expect(screen.getByText('Alice')).toBeTruthy()
    expect(screen.getByText('Bob')).toBeTruthy()
  })

  it('renders empty state when data is empty', () => {
    render(<DataTable columns={columns} data={[]} />)
    expect(screen.getByText('No results found.')).toBeTruthy()
  })

  it('renders skeleton when loading', () => {
    render(<DataTable columns={columns} data={[]} loading />)
    const skeletons = screen.getAllByRole('row', { name: /loading/i })
    expect(skeletons.length).toBeGreaterThan(0)
  })

  it('sort click updates URL params', () => {
    render(<DataTable columns={columns} data={data} />)
    fireEvent.click(screen.getByRole('button', { name: /sort by customer/i }))
    expect(mockReplace).toHaveBeenCalledWith(
      expect.stringContaining('sort=customer'),
      { scroll: false }
    )
  })
})
```

---

### Component: `src/components/data-table.tsx`

```typescript
'use client'

import { useCallback, useEffect, useState } from 'react'
import { usePathname, useRouter, useSearchParams } from 'next/navigation'
import clsx from 'clsx'

export type ColumnConfig<T> = {
  key: keyof T
  label: string
  sortable?: boolean
}

export interface DataTableProps<T extends Record<string, unknown>> {
  columns: ColumnConfig<T>[]
  data: T[]
  loading?: boolean
  total?: number
}

function useDebouncedValue<V>(value: V, delay = 350): V {
  const [debounced, setDebounced] = useState(value)
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(id)
  }, [value, delay])
  return debounced
}

export function DataTable<T extends Record<string, unknown>>({
  columns,
  data,
  loading = false,
  total,
}: DataTableProps<T>) {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const currentSort = searchParams.get('sort') ?? ''
  const currentDir = searchParams.get('dir') ?? 'asc'
  const currentPage = Number(searchParams.get('page') ?? '1')

  const [filterInput, setFilterInput] = useState(searchParams.get('q') ?? '')
  const debouncedFilter = useDebouncedValue(filterInput)

  const updateParam = useCallback(
    (updates: Record<string, string | null>) => {
      const params = new URLSearchParams(searchParams.toString())
      for (const [key, value] of Object.entries(updates)) {
        if (value === null) {
          params.delete(key)
        } else {
          params.set(key, value)
        }
      }
      router.replace(`${pathname}?${params.toString()}`, { scroll: false })
    },
    [pathname, router, searchParams]
  )

  useEffect(() => {
    updateParam({ q: debouncedFilter || null, page: '1' })
  }, [debouncedFilter]) // eslint-disable-line react-hooks/exhaustive-deps

  function handleSort(key: string) {
    if (currentSort === key) {
      const nextDir = currentDir === 'asc' ? 'desc' : 'asc'
      updateParam({ sort: key, dir: nextDir })
    } else {
      updateParam({ sort: key, dir: 'asc' })
    }
  }

  function handlePageChange(next: number) {
    updateParam({ page: String(next) })
  }

  const totalPages = total ? Math.ceil(total / 20) : 1

  // --- Loading skeleton ---
  if (loading) {
    return (
      <div role="status" aria-label="Loading table">
        <table className="w-full table-fixed border-collapse text-sm" aria-label="Loading data">
          <thead>
            <tr className="border-b border-gray-200">
              {columns.map((col) => (
                <th key={String(col.key)} className="px-4 py-2 text-left font-medium text-gray-500">
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: 5 }).map((_, i) => (
              <tr key={i} aria-label="loading" className="border-b border-gray-100">
                {columns.map((col) => (
                  <td key={String(col.key)} className="px-4 py-3">
                    <div className="h-4 w-3/4 animate-pulse rounded bg-gray-200" />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  // --- Empty state ---
  if (data.length === 0) {
    return (
      <div>
        <FilterBar value={filterInput} onChange={setFilterInput} />
        <div className="flex flex-col items-center justify-center py-16 text-gray-500">
          <p className="text-sm">No results found.</p>
        </div>
      </div>
    )
  }

  // --- Populated table ---
  return (
    <div className="space-y-4">
      <FilterBar value={filterInput} onChange={setFilterInput} />
      <table
        className="w-full table-fixed border-collapse text-sm"
        aria-label="Data table"
      >
        <thead>
          <tr className="border-b border-gray-200">
            {columns.map((col) => {
              const isSorted = currentSort === String(col.key)
              const ariaSort = isSorted
                ? currentDir === 'asc'
                  ? 'ascending'
                  : 'descending'
                : 'none'

              return (
                <th
                  key={String(col.key)}
                  aria-sort={col.sortable ? ariaSort : undefined}
                  className="px-4 py-2 text-left font-medium text-gray-700"
                >
                  {col.sortable ? (
                    <button
                      type="button"
                      aria-label={`Sort by ${col.label}`}
                      onClick={() => handleSort(String(col.key))}
                      className={clsx(
                        'flex items-center gap-1 hover:text-gray-900',
                        isSorted && 'text-blue-600'
                      )}
                    >
                      {col.label}
                      <span aria-hidden="true">
                        {isSorted ? (currentDir === 'asc' ? '↑' : '↓') : '↕'}
                      </span>
                    </button>
                  ) : (
                    col.label
                  )}
                </th>
              )
            })}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className="border-b border-gray-100 hover:bg-gray-50">
              {columns.map((col) => (
                <td key={String(col.key)} className="px-4 py-3 text-gray-800">
                  {String(row[col.key] ?? '')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <PaginationControls
        page={currentPage}
        totalPages={totalPages}
        onPageChange={handlePageChange}
      />
    </div>
  )
}

function FilterBar({
  value,
  onChange,
}: {
  value: string
  onChange: (v: string) => void
}) {
  return (
    <input
      type="search"
      placeholder="Filter..."
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full rounded border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      aria-label="Filter table rows"
    />
  )
}

function PaginationControls({
  page,
  totalPages,
  onPageChange,
}: {
  page: number
  totalPages: number
  onPageChange: (p: number) => void
}) {
  return (
    <div className="flex items-center justify-between text-sm text-gray-600">
      <button
        type="button"
        disabled={page <= 1}
        onClick={() => onPageChange(page - 1)}
        className={clsx(
          'rounded px-3 py-1',
          page <= 1 ? 'cursor-not-allowed opacity-40' : 'hover:bg-gray-100'
        )}
        aria-label="Previous page"
      >
        Previous
      </button>
      <span>
        Page {page} of {totalPages}
      </span>
      <button
        type="button"
        disabled={page >= totalPages}
        onClick={() => onPageChange(page + 1)}
        className={clsx(
          'rounded px-3 py-1',
          page >= totalPages ? 'cursor-not-allowed opacity-40' : 'hover:bg-gray-100'
        )}
        aria-label="Next page"
      >
        Next
      </button>
    </div>
  )
}
```

---

### Changes

- **Files created:**
  - `src/components/data-table.tsx`
  - `src/components/data-table.test.tsx`
- **Files modified:**
  - `src/components/index.ts` — added `export { DataTable, type DataTableProps, type ColumnConfig } from './data-table'`

### Decisions

- **Shared placement in `src/components/`:** Prompt specifies use on two separate admin pages. Classified as shared molecule. Placed at `src/components/data-table.tsx`.
- **UI library check:** `@org/ui` has no `Table` primitive. Built from scratch. If shadcn/ui is later added, this component should be evaluated for replacement.
- **Custom debounce hook over external library:** A 10-line `useDebouncedValue` hook avoids a dependency addition (which requires a decision checkpoint). Matches the definition's preference for no external library when a hook suffices.
- **`'use client'` required:** Component uses `useSearchParams`, `useRouter`, event handlers — all require client context. Client directive is justified, not default.

### Checklist

- [x] States handled: loading skeleton (column-matched), empty state, populated table
- [x] Accessible: `aria-sort` on sortable `<th>`, `<button>` inside `<th>` for keyboard activation, `aria-label` on inputs and controls, `role="status"` on skeleton
- [x] Responsive: `table-fixed`, `w-full` — no horizontal scroll at standard breakpoints (wide tables may need horizontal scroll wrapper; flagged for UI designer)
- [x] Tests pass with exit 0: 4/4

---

## Criteria

- [x] PASS: Agent reads CLAUDE.md and scans existing components before writing any code — Pre-Flight is labelled MANDATORY. Step 1 reads `CLAUDE.md` and `.claude/CLAUDE.md`. Step 2 mandates `Glob(pattern="src/components/**/*.tsx")`, barrel export check, and UI library check before any implementation.
- [x] PASS: Agent identifies that sorting, filtering, and pagination state must live in URL search params (not useState) — Data Patterns: "URL search params for pagination/filter state (not useState) — survives refresh and back/forward." Principles: "URL state over component state." Stated twice, unambiguously.
- [x] PASS: Agent writes a failing Vitest test first (RED) before implementing the component — Iron Law is MANDATORY: "No production code without a failing test first." RED step requires exit code 1 and a meaningful failure message before any production code is written.
- [x] PASS: Agent defines a typed `DataTableProps` interface with exported type — Component Conventions require "TypeScript interface named `ComponentNameProps`." Barrel export convention and strict TypeScript both drive exporting the type.
- [x] PASS: Agent handles all required states: loading (skeleton), empty, and populated — Pre-Implementation Checklist: "States: Loading, error, empty, success all handled?" Output Format Checklist confirms states as a required output item.
- [x] PASS: Agent uses `clsx` for conditional class composition, not string concatenation — Component Conventions: "Conditional classes: clsx — never string concatenation." Direct and unambiguous.
- [x] PASS: Agent flags the decision checkpoint for adding a new shared component — Decision Checkpoints: "Creating a new component that might already exist → STOP and ask. Check UI library and existing components first." Explicit mandatory stop trigger.
- [~] PARTIAL: Agent covers accessibility requirements — keyboard navigation for sortable headers, appropriate ARIA attributes — Pre-Implementation Checklist covers "Keyboard navigation, ARIA attributes, colour contrast, focus management" broadly. General ARIA guidance is present but table-specific semantics (`aria-sort` values, button-in-th for sortable columns) are not prescribed. The framework is there; the table-specific detail is not mandated.
- [x] PASS: Output includes TDD Evidence (RED/GREEN commands with exit codes) and a Checklist section — Output Format template explicitly requires both, with exact field names and exit code notation.

## Output expectations

- [x] PASS: Output places `DataTable` in the shared components folder — Pre-Flight Step 2 classifies components by shared vs. app-specific. Prompt says the table is used on two separate pages; shared placement follows.
- [x] PASS: Output's `DataTableProps` is a typed and exported interface with generic `<T>` type parameter — TypeScript strict mode and Component Conventions drive typed interfaces. Generic `<T>` is the natural consequence of `noUncheckedIndexedAccess` and strict mode when typing row data.
- [x] PASS: Output stores sort, filter, and page state in URL search params using `useSearchParams` / `usePathname` from `next/navigation` — Data Patterns mandates this; App Router section covers the navigation imports. The simulated output uses `router.replace(..., { scroll: false })`.
- [x] PASS: Output's text filter uses a debounce before updating `?q=` param — Data Patterns explicitly mentions "`DebouncedSearch` for text filters." Simulated output implements a custom `useDebouncedValue` hook at 350ms.
- [x] PASS: Output's column header click handler toggles sort direction and updates URL params — "No client-side filtering, sorting, or pagination — server does the work" combined with URL state principle drives correct implementation. Simulated output updates `?sort=` and `?dir=` params, toggles asc/desc.
- [x] PASS: Output renders three distinct UI states — loading skeleton, empty state, populated table — Pre-Implementation Checklist and Output Format Checklist both mandate this. Simulated output has three explicit branches.
- [x] PASS: Output uses `clsx` for conditional classNames — mandated in Component Conventions. Simulated output uses `clsx` throughout; no string concatenation present.
- [x] PASS: Output writes the failing Vitest test first with RED/GREEN evidence and exit codes — Iron Law is non-negotiable. Simulated output shows RED at exit 1 with a meaningful failure message, then GREEN at exit 0 with 4/4 passed.
- [~] PARTIAL: Output addresses accessibility — `aria-sort` on sortable headers, keyboard-activatable — the simulated output includes `aria-sort`, `<button>` inside `<th>`, and `aria-label` attributes. The definition's Pre-Implementation Checklist covers ARIA and keyboard navigation generally but does not prescribe `aria-sort` values or the button-in-th pattern explicitly. A well-aligned agent produces this; the definition does not guarantee it. Scored 0.5.
- [~] PARTIAL: Output checks the project's existing UI library for an existing Table primitive — Decision Checkpoints and Pre-Flight Step 2 require checking the UI library. The simulated output surfaces this as a named Decision. However, the definition does not guarantee the UI-library check surfaces explicitly in the Decisions section vs. being silently resolved during Pre-Flight. Scored 0.5.

## Notes

The definition is strong. URL state is the most clearly stated convention in the file, appearing in both Data Patterns and Principles with identical intent. The Iron Law with exit codes and failure caps gives high confidence the RED phase fires before any production code.

The accessibility ceiling is the definition's main gap. The Pre-Implementation Checklist mentions "ARIA attributes" and "keyboard navigation" as categories, but table-specific patterns (`aria-sort` with `ascending`/`descending`/`none`, keyboard-activatable sort headers via `<button>` in `<th>`) are not prescribed. A careful implementation gets there; the definition doesn't drive it deterministically.

The generic `<T>` parameter on `DataTableProps` is a natural consequence of strict TypeScript applied to row data, but is not explicitly required. Worth noting for anyone extending this definition.
