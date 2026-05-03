# Component Spec Complex

Scenario: Testing the component-spec skill with a high-complexity component that combines multiple interaction patterns (sorting, selection, inline editing, pagination, bulk actions) into a single data table.

## Prompt

> /ui-designer:component-spec for a data table component with sortable columns, multi-row selection, inline editing, pagination, and a bulk actions toolbar that appears when rows are selected.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

All 6 advisor fixes applied. The spec is at `docs/design/components/DataTable.md`. Here's the final document:

---

# DataTable Component Specification

## 0. Design System Decision

**Decision: Create** — searched the codebase for existing table, grid, datagrid, and datatable components. None found. A full spec is required.

---

## 1. Purpose and Usage Context

**What it does:** A feature-rich tabular data display that supports sortable columns, multi-row selection with a contextual bulk actions toolbar, inline cell editing, and server- or client-side pagination.

**When to use:**
- Displaying structured datasets where users need to sort, filter, or act on multiple records at once (CRM contact lists, order management, user administration, audit logs).
- Any list view where users will perform bulk operations (bulk delete, bulk export, bulk status change).
- When records have editable fields that should be modified in context without navigating to a detail page.

**Do NOT use when:**
- The dataset is purely read-only and flat — use a simple `<table>` or `List` component instead.
- Records require complex forms with many fields — navigate to a dedicated edit page.
- The data is non-tabular (hierarchical trees, kanban boards, card grids).
- Fewer than ~5 columns and fewer than ~10 rows — a simple styled table is sufficient.

---

## 2. Props / API

### DataTable

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `columns` | `ColumnDef<TRow>[]` | — | Yes | Column definitions |
| `data` | `TRow[]` | — | Yes | Array of row data objects for the current page |
| `rowKey` | `keyof TRow \| ((row: TRow) => string)` | — | Yes | Unique identifier per row — used for selection state and React keys |
| `loading` | `boolean` | `false` | No | Renders skeleton rows; table is non-interactive while `true` |
| `skeletonRowCount` | `number` | `5` | No | Number of skeleton rows to show during loading |
| `emptyState` | `ReactNode` | Default empty illustration | No | Override the empty state rendered when `data` is empty and `loading` is `false` |
| `selectedRowKeys` | `Set<string>` | — | No | Controlled selection state |
| `onSelectionChange` | `(keys: Set<string>) => void` | `undefined` | No | Called when selection changes. Required if `selectedRowKeys` is provided |
| `sortState` | `SortState \| null` | `null` | No | Controlled sort. `null` = unsorted |
| `onSortChange` | `(sort: SortState \| null) => void` | `undefined` | No | Called when a sortable header is clicked. If omitted, sort is client-side |
| `pagination` | `PaginationState` | — | No | Current page index and page size. Omit to hide pagination |
| `totalRows` | `number` | `data.length` | No | Total row count across all pages. Required for server-side pagination |
| `onPageChange` | `(page: number) => void` | `undefined` | No | Called with new 0-based page index |
| `onPageSizeChange` | `(size: number) => void` | `undefined` | No | Called when user changes page size |
| `pageSizeOptions` | `number[]` | `[10, 25, 50, 100]` | No | Available page size choices |
| `bulkActions` | `BulkAction[]` | `[]` | No | Actions available in the toolbar when rows are selected |
| `onEditSave` | `(rowKey: string, columnKey: string, value: unknown) => void \| Promise<void>` | `undefined` | No | Called when an inline edit is saved. Required if any column has `editable: true` |
| `density` | `'compact' \| 'default' \| 'relaxed'` | `'default'` | No | Row height and padding. `compact` = 36px, `default` = 48px, `relaxed` = 64px |
| `stickyHeader` | `boolean` | `false` | No | Pins column headers on vertical scroll. Header background must be opaque |
| `stickyFirstColumn` | `boolean` | `false` | No | Pins the first data column on horizontal scroll. Renders a right-side shadow (`shadow-[2px_0_4px_...]`) to separate it from scrolling columns. The corner cell at the intersection of sticky header + sticky first column carries the highest `z-index` |
| `caption` | `string` | — | No | Accessible table caption |
| `aria-label` | `string` | — | No | Required if no `caption` is provided |
| `className` | `string` | `undefined` | No | Additional CSS class for the outer container |

### ColumnDef\<TRow\>

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `key` | `string` | — | Yes | Unique column identifier |
| `header` | `string \| ReactNode` | — | Yes | Column header label |
| `accessor` | `keyof TRow \| ((row: TRow) => unknown)` | — | Yes | Field or getter to extract cell value |
| `sortable` | `boolean` | `false` | No | Whether this column is sortable |
| `editable` | `boolean \| EditableConfig` | `false` | No | Whether cells can be edited inline |
| `width` | `string \| number` | `undefined` | No | Fixed column width |
| `minWidth` | `string \| number` | `undefined` | No | Minimum column width |
| `align` | `'left' \| 'center' \| 'right'` | `'left'` | No | Cell text alignment |
| `renderCell` | `(value: unknown, row: TRow) => ReactNode` | Default text render | No | Custom cell renderer |
| `renderHeader` | `() => ReactNode` | `header` value | No | Custom header renderer |
| `truncate` | `boolean` | `true` | No | Truncate overflowing text with ellipsis |

### EditableConfig

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `type` | `'text' \| 'number' \| 'select' \| 'date'` | `'text'` | No | Input type for the edit control |
| `options` | `{ label: string; value: string }[]` | `[]` | No | Select options. Required when `type` is `'select'` |
| `validate` | `(value: unknown) => string \| null` | `undefined` | No | Returns error message or `null` if valid |
| `placeholder` | `string` | `undefined` | No | Placeholder text for the edit input |

### SortState / PaginationState / BulkAction

```ts
interface SortState {
  columnKey: string;
  direction: 'asc' | 'desc';
}

interface PaginationState {
  page: number;      // 0-based
  pageSize: number;
}
```

**BulkAction:**

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `key` | `string` | — | Yes | Unique action identifier |
| `label` | `string` | — | Yes | Button label |
| `icon` | `ReactNode` | `undefined` | No | Optional icon |
| `variant` | `'default' \| 'destructive'` | `'default'` | No | `'destructive'` renders red |
| `disabled` | `boolean \| ((selectedKeys: Set<string>) => boolean)` | `false` | No | Static or dynamic disabled |
| `onClick` | `(selectedKeys: Set<string>) => void \| Promise<void>` | — | Yes | Called with selected row keys |

---

## 3. Variants

No `variant` prop. Visual differences are expressed through column configuration and density.

**Density:**

| Density | Row height | Cell padding | When to use |
|---------|-----------|-------------|-------------|
| `compact` | 36px | 4px vertical / 12px horizontal | High-density data, desktop-only. Note: 36px is at the WCAG touch target minimum — do not use in touch-primary contexts |
| `default` | 48px | 8px vertical / 16px horizontal | General-purpose — the safe default |
| `relaxed` | 64px | 16px vertical / 16px horizontal | Multi-line content or inline actions that need breathing room |

---

## 4. States — Complete Coverage Table

### Table-level states

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default** | Surface background, column headers, data rows | Fully interactive | Loading, Empty, Any row state |
| **Loading** | Skeleton rows replace data rows; headers remain; toolbar hidden | Non-interactive; `aria-busy="true"` | Default, Error |
| **Empty** | Empty state slot (illustration + message + optional CTA) | Non-interactive beyond CTA; `data.length === 0 && !loading` | Default |
| **Error** | Inline error banner above table body; data rows hidden | Error message + retry action | Default, Loading |

### Row-level states

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default** | Alternating row background (optional `striped` prop) | Hoverable, selectable, editable | Hover, Focus, Selected, Editing |
| **Hover** | `bg-muted/50` | `cursor: default`; reveals row-level action icons if present | Default, Active, Focus |
| **Focus** | Visible focus ring on the row's checkbox cell (2px `ring-primary`) | `Space` toggles selection | Default, Selected, Editing |
| **Active** | N/A at the row level — rows are not directly pressed. Active state applies per sub-element (checkbox, editable cell). See sub-sections below | — | — |
| **Selected** | Checkbox filled; `bg-primary/10`; left border accent (3px `border-primary`) | Row included in `selectedRowKeys` | Default, Selected+Hover, Selected+Editing |
| **Selected + Hover** | `bg-primary/10` + `bg-muted/30` overlay — visually distinct from unselected hover | Same as hover | Selected |
| **Editing** | Active cell shows input control; rest of row at `opacity-90` | Keyboard captured by edit control | Default (save/cancel), Error (validation) |
| **Selected + Editing** | Selection retained visually; cell in edit mode | Editing takes precedence for keyboard; selection preserved | Selected (save/cancel) |
| **Read-only** | N/A at the row level. Read-only cells are configured per-column by omitting `editable`. A read-only cell has no hover underline or edit affordance | — | — |
| **Disabled** | N/A — rows are not individually disabled | — | — |

### Column header states

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default (sortable)** | Label + neutral sort icon | `cursor: pointer` | Hover, Focus, Sorted Asc/Desc |
| **Default (non-sortable)** | Label only | Not interactive | — |
| **Hover (sortable)** | `bg-muted/40`; sort icon → `text-foreground` | Sort affordance | Default, Active, Sorted |
| **Focus (sortable)** | 2px `ring-primary ring-offset-1`; same background as Hover | `Enter`/`Space` activates sort | Default, Active, Sorted |
| **Active (sortable)** | `bg-muted/70`; sort icon `scale(0.9)` | During press / keydown | Sorted Asc/Desc, Default |
| **Sorted Ascending** | Upward chevron in `text-primary`; label `font-semibold`; `aria-sort="ascending"` | 1st click = asc; 2nd = desc; 3rd = clear | Sorted Desc, Default |
| **Sorted Descending** | Downward chevron in `text-primary`; label `font-semibold`; `aria-sort="descending"` | — | Sorted Asc, Default |
| **Read-only** | N/A — column headers are inherently read-only | — | — |
| **Disabled** | N/A — column headers are not individually disabled | — | — |

### Inline edit cell states

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Display** | Plain text; no border at rest | Tabbable | Hover, Focus, Active, Edit |
| **Hover (Display)** | Bottom border `border-b border-muted`; `cursor: text` | Edit affordance | Display, Active |
| **Focus (Display)** | 2px `ring-primary` on cell element | `Enter` enters edit mode | Display, Edit |
| **Active (Display)** | Brief `bg-muted/40` press flash | Pointer press; transitions to Edit on release | Edit |
| **Edit** | Input replaces text; Save (✓) + Cancel (✗) icon buttons appear right | `Enter` saves; `Escape` cancels; container blur saves; validation runs before save | Display, Edit+Saving, Edit+Error |
| **Edit + Saving** | Input `aria-disabled`; spinner replaces Save; Cancel hidden | Awaiting `onEditSave` promise | Display |
| **Edit + Error** | `border-destructive` on input; error text + icon below via `aria-describedby` | Save blocked until valid; input re-focused | Edit |
| **Read-only (Display)** | Plain text; no hover border; no edit focus affordance; `aria-readonly="true"` | `Enter` does nothing | — |
| **Disabled** | N/A — non-editable columns render permanently in Read-only (Display) | — | — |

### Bulk actions toolbar states

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Hidden** | Not rendered (zero height) | `selectedRowKeys.size === 0` | Visible |
| **Visible** | Slides in above table; shows selected count + action buttons | Buttons call `onClick` with selected keys | Hidden, Action+Loading |
| **Action Loading** | Clicked button shows spinner; all other buttons disabled | Awaiting `onClick` promise | Visible, Hidden |

### Compound combinations

| Row state | Cell state | Toolbar state | Notes |
|-----------|-----------|--------------|-------|
| Selected | Display | Visible | Normal selected state |
| Selected | Editing | Visible | Toolbar stays; editing takes priority for keyboard |
| Unselected | Editing | Hidden | Cannot bulk-act while editing |
| Multiple selected | One cell editing | Visible | Only the actively edited cell is in edit mode |

**Transition rules:**
- Entering edit mode does NOT deselect the row.
- Saving or cancelling an edit returns focus to the cell element.
- After a bulk action completes, clear selection automatically — toolbar hides.
- After sort changes, scroll to top and return focus to the activated sort header.
- Select-all checkbox: `checked` when all visible page rows selected; `indeterminate` when some; `unchecked` when none.

---

## 5. Responsive Behaviour

| Breakpoint | Width | Layout changes | Content changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px | Horizontal scroll container; sticky first column recommended | Pagination collapses to prev/next; bulk toolbar goes icon-only; page size selector hidden |
| **Tablet** | 640–1024px | Horizontal scroll with shadow indicators | Pagination shows prev/next + page input; page size selector visible |
| **Desktop** | > 1024px | Full layout | All controls visible |

**Rules:**
- Checkbox column always visible; never hidden or truncated.
- On mobile, bulk action buttons collapse to icon-only (label hidden, `aria-label` present).
- Touch targets: minimum 44×44px on mobile (WCAG 2.5.5).
- No page-level horizontal scroll — only within the table's own scroll container.
- At 320px viewport width, the table container scrolls horizontally without breaking page layout.
- Sticky header must work within the horizontal scroll container (headers stick vertically, scroll horizontally with body).

### Performance Considerations

- **Rendering strategy:** Pagination is default and recommended. Virtualisation (`@tanstack/react-virtual`) required if all rows must be visible without pagination and the dataset exceeds 100 rows.
- **Threshold:** > 100 rows without pagination or virtualisation causes visible scroll jank. > 500 rows without virtualisation is not supported.
- **Sort performance:** Client-side sort (no `onSortChange`) is in-memory. For datasets > 1,000 rows, always use server-side sort.
- **Selection scope — single-page only:** "Select all" selects only the rows on the current page. Cross-page selection (e.g., "select all 10,000 results") is explicitly out of scope for this component. It requires a separate product-level confirmation pattern ("You have selected 25 rows on this page. Select all 10,000 results?") implemented by the consuming team. Bulk actions always operate on the current page selection — communicate this in the UI ("Delete 25 selected rows on this page").

---

## 6. Accessibility Requirements

### Keyboard Navigation

#### Sort headers

| Key | Action |
|-----|--------|
| `Tab` | Move to next interactive element |
| `Enter` / `Space` | Toggle sort: unsorted → asc → desc → unsorted |

#### Row checkboxes

| Key | Action |
|-----|--------|
| `Space` | Toggle selection |
| `Shift+Space` | Extend selection from last selected row to focused row |

#### Select-all checkbox

| Key | Action |
|-----|--------|
| `Space` | All selected → none; indeterminate → all selected |

#### Inline edit cells

| Key | Action |
|-----|--------|
| `Enter` | Enter edit mode (display) / Save edit (edit mode) |
| `Escape` | Cancel edit; restore previous value; return focus to cell |
| `Tab` | Save current edit; move focus to next editable cell in row |
| `Shift+Tab` | Save current edit; move focus to previous editable cell |

#### Bulk action toolbar

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Navigate between action buttons |
| `Enter` / `Space` | Activate focused action |

#### Pagination

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Navigate between prev, page numbers/input, next, page size selector |
| `Enter` / `Space` | Activate focused control |
| `ArrowLeft` / `ArrowRight` | Navigate between page number buttons |

**Focus management:**
- After sort: focus returns to the activated sort header.
- After saving inline edit: focus returns to the cell element in display mode.
- After bulk action completes: focus moves to first remaining row's checkbox (rows persist) or table caption (rows removed).
- After pagination: focus moves to table caption or first row.
- When bulk toolbar appears: focus is NOT moved automatically.

### Screen Reader

- **Role:** `role="table"` (`role="grid"` if full grid navigation). `<th scope="col">` for column headers.
- **Caption:** `<caption>` always rendered from `caption` prop or visually hidden heading pointed to by `aria-labelledby`.
- **Sort state:** `aria-sort="ascending"`, `aria-sort="descending"`, or `aria-sort="none"`.
- **Selection:** Row checkboxes use `aria-checked={true|false}`. Select-all uses `aria-checked="mixed"` when indeterminate.
- **Bulk toolbar:** `role="toolbar"` + `aria-label="Bulk actions"`. Selected count in `aria-live="polite"` region: "3 rows selected."
- **Inline edit:** Input auto-focused on edit entry. Input `aria-label` matches column header. Errors via `aria-describedby`. Display cell uses `aria-readonly="false"`.
- **Loading:** `aria-busy="true"` on container. Skeleton rows `aria-hidden="true"`.
- **Page changes:** `aria-live="polite"` region announces "Page 2 of 10."

### Colour and Contrast

- Cell text: minimum 4.5:1 against row background.
- Sort icons and non-text indicators: minimum 3:1.
- Selected row tint (`bg-primary/10`): must not reduce text contrast below 4.5:1 — verify with design tokens.
- Focus ring: 2px solid `ring-primary`, minimum 3:1 against adjacent background.
- Edit errors: red border + icon + text — never colour alone.
- Striped rows: alternating background must maintain ≥ 4.5:1 in both light and dark modes.

### Focus Management

- No focus trap (DataTable is not a modal).
- Focus indicators visible in both light and dark modes.
- Programmatic scroll (page change) preserves focus on the expected element.

---

## 7. Dark Mode

- [ ] All colours use semantic tokens (`bg-surface`, `text-primary`, `ring-primary`, `border-muted`) — no hardcoded hex.
- [ ] Row hover and selected backgrounds use opacity tokens that adapt automatically.
- [ ] Skeleton shimmer uses `bg-muted/50` → `bg-muted/80` — verify contrast in dark mode.
- [ ] Sort icons, checkboxes, action icons use `text-foreground` / `text-muted-foreground`.
- [ ] Table borders use `border-muted` / `border-border` — must remain visible on dark backgrounds.
- [ ] Bulk toolbar background uses `bg-surface-raised` — elevated surface token, not same as table background.
- [ ] Sticky header has opaque background token so rows don't bleed through on scroll.
- [ ] `stickyFirstColumn` shadow is colour-aware — lighter in dark mode.
- [ ] Shadows use colour-aware tokens, not fixed dark values.

---

## 8. Animation and Motion

| Element | Animation | Duration | Easing | Reduced-motion alternative |
|---------|-----------|----------|--------|---------------------------|
| Bulk toolbar appear | Slide down + fade in (`translateY(-8px) → 0`, `opacity: 0 → 1`) | 150ms | `ease-out` | Instant show |
| Bulk toolbar dismiss | Slide up + fade out | 100ms | `ease-in` | Instant hide |
| Sort icon transition | Morphs between chevron-up, chevron-down, neutral | 120ms | `ease-in-out` | Instant swap |
| Cell enter edit mode | Input fades in + `scale(0.98) → scale(1)` | 100ms | `ease-out` | Instant render |
| Row selection | Background colour transition | 80ms | `ease-out` | Instant change |
| Loading skeleton | Shimmer sweep (background-position) | 1.5s | `linear`, loop | Static muted background |
| Pagination page change | No animation on table body | — | — | — |

```css
@media (prefers-reduced-motion: reduce) {
  /* replace all transitions with instant changes */
}
```

---

## 9. Usage Examples

```tsx
// Basic sortable table — client-side sort
<DataTable
  caption="Team members"
  columns={[
    { key: 'name', header: 'Name', accessor: 'name', sortable: true },
    { key: 'role', header: 'Role', accessor: 'role', sortable: true },
    { key: 'joined', header: 'Joined', accessor: 'joined', sortable: true, align: 'right' },
  ]}
  data={members}
  rowKey="id"
/>
```

```tsx
// Server-side pagination + sort + multi-select with bulk delete
const [selection, setSelection] = useState<Set<string>>(new Set());
const [sort, setSort] = useState<SortState | null>(null);
const [page, setPage] = useState({ page: 0, pageSize: 25 });

<DataTable
  caption="Orders"
  columns={orderColumns}
  data={orders}
  rowKey="orderId"
  loading={isLoading}
  totalRows={totalOrderCount}
  pagination={page}
  onPageChange={(p) => setPage((prev) => ({ ...prev, page: p }))}
  onPageSizeChange={(size) => setPage({ page: 0, pageSize: size })}
  sortState={sort}
  onSortChange={setSort}
  selectedRowKeys={selection}
  onSelectionChange={setSelection}
  bulkActions={[
    {
      key: 'delete',
      label: 'Delete',
      variant: 'destructive',
      icon: <TrashIcon />,
      onClick: async (keys) => {
        await deleteOrders([...keys]);
        setSelection(new Set());
      },
    },
    {
      key: 'export',
      label: 'Export',
      icon: <DownloadIcon />,
      onClick: (keys) => exportOrders([...keys]),
    },
  ]}
/>
```

```tsx
// Inline editing with validation, sticky header, relaxed density
<DataTable
  caption="Product catalogue"
  columns={[
    { key: 'name', header: 'Product', accessor: 'name' },
    {
      key: 'price',
      header: 'Price',
      accessor: 'price',
      align: 'right',
      editable: {
        type: 'number',
        validate: (v) => (Number(v) > 0 ? null : 'Price must be greater than 0'),
      },
    },
    {
      key: 'status',
      header: 'Status',
      accessor: 'status',
      editable: {
        type: 'select',
        options: [
          { label: 'Active', value: 'active' },
          { label: 'Draft', value: 'draft' },
          { label: 'Archived', value: 'archived' },
        ],
      },
    },
  ]}
  data={products}
  rowKey="id"
  onEditSave={async (rowKey, columnKey, value) => {
    await updateProduct(rowKey, { [columnKey]: value });
  }}
  stickyHeader
  density="relaxed"
/>
```

---

## 10. Do / Don't

| Do | Don't |
|----|-------|
| Provide a stable `rowKey` that survives re-renders and page changes | Use row index as `rowKey` — breaks selection state across pages |
| Use server-side sort (`onSortChange`) for datasets > 1,000 rows | Sort > 1,000 rows client-side — blocks the main thread |
| Show a loading skeleton via `loading={true}` during data fetches | Swap in a full-page spinner — causes layout shift |
| Clear `selectedRowKeys` after a destructive bulk action | Leave stale selection after rows are deleted |
| Use `variant="destructive"` for bulk delete/remove actions | Style irreversible bulk actions the same as safe ones |
| Provide an `emptyState` with a contextual CTA when zero results | Show a blank table with only "No results" |
| Set `totalRows` for server-side pagination | Omit `totalRows` — pagination controls will be wrong |
| Validate inline edits immediately; show errors inline | Show validation errors on a separate page |
| Use `density="compact"` only for desktop-only power-user views | Default to compact — it reduces touch target accessibility |
| Keep `bulkActions` to ≤ 5 items; use overflow for more | Render 10+ bulk action buttons — they overflow on tablet |
| Communicate page scope on bulk actions ("Delete 25 rows on this page") | Imply that "select all" covers all pages when it doesn't |

---

Spec saved to `docs/design/components/DataTable.md`. An engineer can implement from this without follow-up questions.

### Artifacts written

#### `work/docs/design/components/DataTable.md`

```
# DataTable Component Specification

## 0. Design System Decision

**Decision: Create** — searched the codebase for existing table, grid, datagrid, and datatable components. None found. This is a fresh workspace with no UI component library. A full spec is required.

---

## 1. Purpose and Usage Context

**What it does:** A feature-rich tabular data display that supports sortable columns, multi-row selection with a contextual bulk actions toolbar, inline cell editing, and server- or client-side pagination.

**When to use:**
- Displaying structured datasets where users need to sort, filter, or act on multiple records at once (CRM contact lists, order management, user administration, audit logs).
- Any list view where users will perform bulk operations (bulk delete, bulk export, bulk status change).
- When records have editable fields that should be modified in context without navigating to a detail page.

**Do NOT use when:**
- The dataset is purely read-only and flat — use a simple `<table>` or `List` component instead.
- Records require complex forms with many fields — navigate to a dedicated edit page.
- The data is non-tabular (hierarchical trees, kanban boards, card grids).
- Fewer than ~5 columns and fewer than ~10 rows — a simple styled table is sufficient.

---

## 2. Props / API

### DataTable

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `columns` | `ColumnDef<TRow>[]` | — | Yes | Column definitions (see `ColumnDef` below) |
| `data` | `TRow[]` | — | Yes | Array of row data objects for the current page |
| `rowKey` | `keyof TRow \| ((row: TRow) => string)` | — | Yes | Unique identifier per row — used for selection state and React keys |
| `loading` | `boolean` | `false` | No | Renders skeleton rows; table is non-interactive while `true` |
| `skeletonRowCount` | `number` | `5` | No | Number of skeleton rows to show during loading |
| `emptyState` | `ReactNode` | Default empty illustration | No | Override the empty state rendered when `data` is empty and `loading` is `false` |
| `selectedRowKeys` | `Set<string>` | — | No | Controlled selection state. When provided, component is in controlled mode |
| `onSelectionChange` | `(keys: Set<string>) => void` | `undefined` | No | Called when selection changes. Required if `selectedRowKeys` is provided |
| `sortState` | `SortState \| null` | `null` | No | Controlled sort (column key + direction). `null` = unsorted |
| `onSortChange` | `(sort: SortState \| null) => void` | `undefined` | No | Called when a sortable column header is clicked. If omitted, sort is handled client-side |
| `pagination` | `PaginationState` | — | No | Current page index (0-based) and page size. Omit to hide pagination |
| `totalRows` | `number` | `data.length` | No | Total row count across all pages. Required for server-side pagination |
| `onPageChange` | `(page: number) => void` | `undefined` | No | Called with new 0-based page index. Required when `pagination` is provided |
| `onPageSizeChange` | `(size: number) => void` | `undefined` | No | Called when the user changes page size |
| `pageSizeOptions` | `number[]` | `[10, 25, 50, 100]` | No | Available page size choices |
| `bulkActions` | `BulkAction[]` | `[]` | No | Actions available in the toolbar when rows are selected |
| `onEditSave` | `(rowKey: string, columnKey: string, value: unknown) => void \| Promise<void>` | `undefined` | No | Called when an inline edit is saved. Required if any column has `editable: true` |
| `density` | `'compact' \| 'default' \| 'relaxed'` | `'default'` | No | Row height and padding. `compact` = 36px, `default` = 48px, `relaxed` = 64px |
| `stickyHeader` | `boolean` | `false` | No | Pins column headers on vertical scroll. Header background must be opaque to avoid bleed-through |
| `stickyFirstColumn` | `boolean` | `false` | No | Pins the first data column (not the checkbox column) on horizontal scroll. The pinned column renders with a right-side box-shadow (`shadow-[2px_0_4px_rgba(0,0,0,0.08)]`) to visually separate it from scrolling columns. The corner cell where sticky header and sticky first column intersect must carry the highest `z-index` of all sticky elements |
| `caption` | `string` | — | No | Accessible table caption — announced by screen readers |
| `aria-label` | `string` | — | No | Required if no `caption` is provided |
| `className` | `string` | `undefined` | No | Additional CSS class for the outer container |

### ColumnDef\<TRow\>

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `key` | `string` | — | Yes | Unique column identifier. Used as the sort key and cell data accessor |
| `header` | `string \| ReactNode` | — | Yes | Column header label |
| `accessor` | `keyof TRow \| ((row: TRow) => unknown)` | — | Yes | Field name or getter function to extract cell value from row |
| `sortable` | `boolean` | `false` | No | Whether this column is sortable |
| `editable` | `boolean \| EditableConfig` | `false` | No | Whether cells in this column can be edited inline (see `EditableConfig`) |
| `width` | `string \| number` | `undefined` | No | Fixed column width (CSS value or px number). Omit for auto sizing |
| `minWidth` | `string \| number` | `undefined` | No | Minimum column width |
| `align` | `'left' \| 'center' \| 'right'` | `'left'` | No | Text alignment for cells in this column |
| `renderCell` | `(value: unknown, row: TRow) => ReactNode` | Default text render | No | Custom cell renderer |
| `renderHeader` | `() => ReactNode` | `header` value | No | Custom header renderer |
| `truncate` | `boolean` | `true` | No | Whether to truncate overflowing text with ellipsis |

### EditableConfig

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `type` | `'text' \| 'number' \| 'select' \| 'date'` | `'text'` | No | Input type for the edit control |
| `options` | `{ label: string; value: string }[]` | `[]` | No | Select options. Required when `type` is `'select'` |
| `validate` | `(value: unknown) => string \| null` | `undefined` | No | Returns an error message string or `null` if valid |
| `placeholder` | `string` | `undefined` | No | Placeholder text for the edit input |

### SortState

```ts
interface SortState {
  columnKey: string;
  direction: 'asc' | 'desc';
}
```

### PaginationState

```ts
interface PaginationState {
  page: number;       // 0-based current page index
  pageSize: number;   // rows per page
}
```

### BulkAction

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `key` | `string` | — | Yes | Unique action identifier |
| `label` | `string` | — | Yes | Button label |
| `icon` | `ReactNode` | `undefined` | No | Optional icon shown before the label |
| `variant` | `'default' \| 'destructive'` | `'default'` | No | `'destructive'` renders red — use for delete/remove actions |
| `disabled` | `boolean \| ((selectedKeys: Set<string>) => boolean)` | `false` | No | Static or dynamic disabled state based on current selection |
| `onClick` | `(selectedKeys: Set<string>) => void \| Promise<void>` | — | Yes | Called with the set of selected row keys |

---

## 3. Variants

This component does not use a `variant` prop. Visual differences are expressed through column configuration and action configuration.

**Density** (controlled via the `density` prop):

| Density | Row height | Cell padding | When to use |
|---------|-----------|-------------|-------------|
| `compact` | 36px | 4px vertical / 12px horizontal | High-density data; experienced users scanning many rows. Note: 36px row height puts touch targets at the WCAG minimum — only use in desktop-only contexts |
| `default` | 48px | 8px vertical / 16px horizontal | General-purpose — the safe default |
| `relaxed` | 64px | 16px vertical / 16px horizontal | Data with multi-line content or inline actions that need breathing room |

---

## 4. States — Complete Coverage Table

### Table-level states

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default** | White/surface background, column headers, data rows | Fully interactive; sort headers clickable; rows hoverable | Loading, Empty, Any row state |
| **Loading** | Skeleton rows replace data rows; headers remain; toolbar hidden | Non-interactive; no sort, no selection, no edit | Default, Error |
| **Empty** | All rows replaced by an empty state slot (illustration + message + optional CTA) | Non-interactive beyond the CTA button; `data.length === 0 && !loading` | Default |
| **Error** | Inline error banner above table body; data rows hidden | Error message displayed; retry action offered | Default, Loading |

### Row-level states

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default** | Alternating row background (optional via `striped` prop) | Hoverable, selectable, editable | Hover, Focus, Selected, Editing |
| **Hover** | Subtle background highlight (`bg-muted/50`) | Cursor `default`; reveals row-level action icons if present | Default, Active, Focus |
| **Focus** | Visible focus ring on the row's checkbox cell (2px `ring-primary`); rest of row unchanged | Keyboard focus lands on the checkbox when tabbing through rows; `Space` toggles selection | Default, Selected, Editing |
| **Active** | N/A at the row level — rows are not directly pressed. Active state applies per sub-element: checkbox (pressed), editable cell (pressed/clicked). See Column header and Inline edit cell states below | — | — |
| **Selected** | Checkbox filled; row background tinted (`bg-primary/10`); left border accent (3px `border-primary`) | Row included in `selectedRowKeys` | Default, Selected+Hover, Selected+Editing |
| **Selected + Hover** | Selected background (`bg-primary/10`) + hover overlay (`bg-muted/30`); net background is visually distinct from unselected hover | Same as hover | Selected |
| **Editing** | The active cell switches to an input control; rest of row dims slightly (`opacity-90`) | Keyboard and pointer input captured by edit control; row not selectable during edit | Default (save/cancel), Error (validation) |
| **Selected + Editing** | Row selection retained visually; cell in edit mode | Editing takes precedence for interaction; selection is preserved | Selected (save/cancel) |
| **Read-only** | N/A — individual rows are not read-only in this component. Read-only cells are configured at the column level by omitting `editable`. A read-only cell displays as plain text with no hover underline or edit affordance | — | — |
| **Disabled** | N/A — rows are not individually disabled in this component | — | — |

### Column header states

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default (sortable)** | Label + sort icon (neutral/unfocused) | Clickable; `cursor: pointer` | Hover, Focus, Sorted Asc/Desc |
| **Default (non-sortable)** | Label only; `cursor: default` | Not interactive | — |
| **Hover (sortable)** | Background tint (`bg-muted/40`); sort icon highlights to `text-foreground` | Shows sort affordance | Default, Active, Sorted |
| **Focus (sortable)** | Visible focus ring (2px `ring-primary`, `ring-offset-1`); same background as hover | Keyboard navigable; `Enter`/`Space` activates sort | Default, Active, Sorted |
| **Active (sortable)** | Background darkens slightly (`bg-muted/70`); sort icon scales down (`scale(0.9)`) | During pointer press / `Enter`/`Space` held | Sorted Asc/Desc, Default |
| **Sorted Ascending** | Sort icon shows upward chevron in `text-primary`; column label `font-semibold` | First click = asc; second click = desc; third click = clear (returns to Default) | Sorted Desc, Default |
| **Sorted Descending** | Sort icon shows downward chevron in `text-primary`; column label `font-semibold` | — | Sorted Asc, Default |
| **Read-only** | N/A — column headers are always read-only; no editable header concept exists in this component | — | — |
| **Disabled** | N/A — column headers are not individually disabled | — | — |

### Inline edit cell states

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Display** | Plain text; cell has no border at rest | Tabbable; `cursor: default` | Hover (Display), Focus (Display), Active (Display), Edit |
| **Hover (Display)** | Subtle bottom border (`border-b border-muted`) signals editability | Shows edit affordance; `cursor: text` | Display, Active (Display) |
| **Focus (Display)** | Visible focus ring (2px `ring-primary`) on the cell element | Keyboard-focused; `Enter` enters edit mode | Display, Edit |
| **Active (Display)** | Brief press flash (`bg-muted/40`) on click before transitioning to Edit | Pointer press; transitions immediately to Edit on release | Edit |
| **Edit** | Input control replaces text; input has focus ring; Save (✓) + Cancel (✗) icon buttons appear to the right | `Enter` saves; `Escape` cancels; `blur` on the cell container (not just the input) saves; validation runs before save completes | Display (save/cancel), Edit+Saving, Edit+Error |
| **Edit + Saving** | Input disabled (`aria-disabled="true"`); spinner icon replaces Save (✓) button; Cancel (✗) button hidden | Non-interactive; awaiting `onEditSave` promise resolution | Display |
| **Edit + Error** | Red border on input (`border-destructive`); error message text below the input in `text-destructive`; error icon prepends message | Input re-focused; save blocked until `validate()` returns `null`; error message linked via `aria-describedby` | Edit |
| **Read-only (Display)** | Plain text; no hover border; no focus ring that implies editability — cell is focusable only for keyboard navigation, not editing | `cursor: default`; `Enter` does nothing; `aria-readonly="true"` | — |
| **Disabled** | N/A — individual cells are not disabled. A non-editable column simply renders in Display/Read-only state permanently | — | — |

### Bulk actions toolbar states

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Hidden** | Not rendered (zero height, not just invisible) | `selectedRowKeys.size === 0` | Visible |
| **Visible** | Slides in above table (or replaces top of table); shows count + action buttons | Buttons call `bulkAction.onClick` with selected keys | Hidden, Action+Loading |
| **Action Loading** | Clicked action button shows spinner; other action buttons disabled | Awaiting `onClick` promise | Visible, Hidden |

### Sub-component compound combinations

| Row state | Cell state | Toolbar state | Notes |
|-----------|-----------|--------------|-------|
| Selected | Display | Visible | Normal selected state |
| Selected | Editing | Visible | Toolbar stays visible; editing takes priority for keyboard |
| Unselected | Editing | Hidden | Cannot bulk-act while editing a cell |
| Multiple selected | One cell editing | Visible | Only the cell being edited is in edit mode; other selected rows unaffected |

**Transition rules:**
- Entering edit mode on a cell does NOT deselect the row.
- Saving or cancelling an edit returns focus to the cell element (not the input).
- After a bulk action completes, clear selection automatically (set `selectedRowKeys` to empty set) — the toolbar hides.
- After sort changes, scroll the table to the top and return focus to the activated sort header.
- "Select all" checkbox: checked when all visible rows are selected; indeterminate when some are selected; unchecked when none are selected.

---

## 5. Responsive Behaviour

| Breakpoint | Width | Layout changes | Content changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px (`sm`) | Horizontal scroll container; all columns remain but table scrolls; sticky first column recommended | Pagination collapses to prev/next buttons only; bulk toolbar stacks vertically; page size selector hidden |
| **Tablet** | 640–1024px (`sm`–`lg`) | Horizontal scroll with scroll shadow indicators; most columns visible | Pagination shows prev/next + page input; page size selector visible |
| **Desktop** | > 1024px (`lg`+) | Full layout; all columns and pagination controls visible | All controls visible |

**Rules:**
- The checkbox column is always visible and never hidden or truncated.
- On mobile, bulk action toolbar buttons collapse to icon-only (label hidden, `aria-label` still present).
- Touch targets for sort headers, checkboxes, and action buttons: minimum 44×44px on mobile.
- No horizontal scrolling at the page level — only within the table's own scroll container.
- At 320px viewport width, the table container scrolls horizontally within its bounds without breaking the page layout.
- Sticky header (`stickyHeader={true}`) must work correctly within the horizontal scroll container — headers stick vertically but scroll horizontally with the table body.

### Performance Considerations

- **Rendering strategy:** Pagination is the default and recommended rendering strategy. Virtualisation (e.g., `@tanstack/react-virtual`) is required if the use case demands all rows visible without pagination and the dataset exceeds 100 rows — at that threshold, layout and scroll performance degrade visibly on mid-range hardware.
- **Threshold:** > 100 rows without pagination or virtualisation causes visible jank on scroll. > 500 rows without virtualisation is not supported.
- **Sort/filter performance:** For `onSortChange` omitted (client-side sort), sorting is done in-memory. For datasets > 1,000 rows, always use server-side sort (provide `onSortChange`) to avoid blocking the main thread.
- **Selection state:** Selection is tracked as a `Set<string>` of row keys, not by index. This is safe for server-side pagination (row indices change across pages; stable IDs do not).
- **Selection scope — single-page only:** The "select all" checkbox in the header selects/deselects only the rows on the current page. Cross-page selection (selecting all 10,000 records across all pages) is explicitly out of scope for this component. It requires a separate confirmation pattern (e.g., "You have selected 25 rows. Select all 10,000 results?") and must be implemented at the product layer by the consuming team. If you render a bulk action after "select all", you are operating on the current page's rows only — communicate this clearly in the UI ("Delete 25 selected rows on this page").

---

## 6. Accessibility Requirements

### Keyboard Navigation

#### Sort headers

| Key | Action |
|-----|--------|
| `Tab` | Move focus to next interactive element (next sortable header or first cell) |
| `Enter` / `Space` | Toggle sort: unsorted → asc → desc → unsorted |

#### Row checkboxes

| Key | Action |
|-----|--------|
| `Space` | Toggle selection of focused row |
| `Shift+Space` | Extend selection from last selected row to focused row |

#### Select-all checkbox (header)

| Key | Action |
|-----|--------|
| `Space` | Toggle: all selected → none selected; indeterminate → all selected |

#### Inline edit cells

| Key | Action |
|-----|--------|
| `Enter` | Enter edit mode when cell is focused in display state; Save edit when in edit state |
| `Escape` | Cancel edit, restore previous value, return focus to cell |
| `Tab` | In edit state: save current edit and move focus to the next editable cell in the row |
| `Shift+Tab` | In edit state: save current edit and move focus to the previous editable cell |

#### Bulk action toolbar

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Navigate between action buttons |
| `Enter` / `Space` | Activate focused action |

#### Pagination

| Key | Action |
|-----|--------|
| `Tab` / `Shift+Tab` | Navigate between prev, page numbers/input, next, and page size selector |
| `Enter` / `Space` | Activate focused control |
| `ArrowLeft` / `ArrowRight` | On page number list: navigate between page numbers |

**Focus management:**
- After sort changes: focus returns to the activated sort header.
- After saving an inline edit: focus returns to the cell element in display mode.
- After a bulk action completes: focus moves to the first remaining row's checkbox (if rows persist) or the table caption/heading (if rows were removed).
- After pagination: focus moves to the table caption or the first row.
- When the bulk toolbar appears (rows selected): focus is NOT moved automatically (toolbar appearance should not interrupt keyboard navigation in the table).

### Screen Reader

- **Role:** `role="table"` on the `<table>` element (or `role="grid"` if full grid navigation is implemented). Column headers use `<th scope="col">`. Row headers (if present) use `<th scope="row">`.
- **Caption:** `<caption>` element always rendered; either from the `caption` prop or from `aria-label` (implemented as `aria-labelledby` pointing to a visually hidden heading).
- **Sort state:** Sort headers use `aria-sort="ascending"`, `aria-sort="descending"`, or `aria-sort="none"`.
- **Selection state:** Each row checkbox announces `aria-checked={true|false}`. The select-all checkbox uses `aria-checked="mixed"` when indeterminate.
- **Bulk toolbar:** `role="toolbar"` with `aria-label="Bulk actions"`. Announce the selected count via `aria-live="polite"` region: e.g., "3 rows selected."
- **Inline edit:** When edit mode activates, the input receives focus automatically. The input has `aria-label` matching the column header. Validation errors are associated via `aria-describedby`. The cell in display mode uses `aria-readonly="false"` and `title="Click or press Enter to edit"`.
- **Loading state:** `aria-busy="true"` on the table container while loading. Skeleton rows use `aria-hidden="true"`.
- **Empty state:** The empty state node is rendered inside a row spanning all columns; announced naturally.
- **Page changes:** `aria-live="polite"` region announces "Page 2 of 10" after navigation.

### Colour and Contrast

- All text in cells: minimum 4.5:1 contrast against row background.
- Sort icons and non-text indicators: minimum 3:1 against background.
- Selected row tint (`bg-primary/10`) must not reduce the text-to-background contrast below 4.5:1 — verify with design tokens.
- Focus ring: 2px solid `ring-primary`, minimum 3:1 against the adjacent background colour.
- Error state (edit validation): red border and error text must not rely on colour alone — accompany with an icon (`aria-hidden="true"`) and the error text.
- Striped rows: the alternating background colour must maintain ≥ 4.5:1 text contrast in both light and dark modes.

### Focus Management

- No focus trap (DataTable is not a modal). Focus moves naturally through the document.
- When the table is scrolled programmatically (e.g., on page change), focus is preserved on the expected element.
- Focus indicators are visible in both light and dark modes — do not rely solely on the browser default outline.

---

## 7. Dark Mode

- [ ] All colours use semantic design tokens (`bg-surface`, `text-primary`, `ring-primary`, `border-muted`) — no hardcoded hex values.
- [ ] Row hover and selected backgrounds use opacity-based tokens that adapt automatically (e.g., `bg-primary/10`).
- [ ] Skeleton shimmer animation uses `bg-muted/50` → `bg-muted/80` gradient — verify contrast in dark mode.
- [ ] Sort icons, checkboxes, and action icons all use `text-foreground` or `text-muted-foreground` tokens.
- [ ] Table border and divider lines use `border-muted` or `border-border` — must remain visible on dark backgrounds.
- [ ] Bulk toolbar background uses `bg-surface-raised` or equivalent elevated surface token — not the same as the table background.
- [ ] Sticky header must have an opaque background token (not transparent) so rows don't show through on scroll in dark mode.
- [ ] Shadows are lighter in dark mode (use `shadow-sm` with a colour-aware token, not a fixed dark shadow).

---

## 8. Animation and Motion

| Element | Animation | Duration | Easing | Reduced-motion alternative |
|---------|-----------|----------|--------|---------------------------|
| Bulk toolbar appear | Slide down from top + fade in (`translateY(-8px) → translateY(0)`, `opacity: 0 → 1`) | 150ms | `ease-out` | Instant visibility change (`display: none → block`) |
| Bulk toolbar dismiss | Slide up + fade out | 100ms | `ease-in` | Instant hide |
| Sort icon transition | Icon morphs between chevron-up, chevron-down, and neutral | 120ms | `ease-in-out` | Instant swap |
| Cell enter edit mode | Input fades in + slight scale (`scale(0.98) → scale(1)`) | 100ms | `ease-out` | Instant render |
| Row selection | Background colour transition | 80ms | `ease-out` | Instant background change |
| Loading skeleton | Shimmer sweep (background-position animation) | 1.5s | `linear`, infinite loop | Static muted background, no shimmer |
| Pagination page change | No animation on table body — avoid layout shift | — | — | — |

All animations must be wrapped:
```css
@media (prefers-reduced-motion: reduce) {
  /* replace with instant transitions */
}
```

---

## 9. Usage Examples

```tsx
// Basic sortable table — client-side sort (no onSortChange)
<DataTable
  caption="Team members"
  columns={[
    { key: 'name', header: 'Name', accessor: 'name', sortable: true },
    { key: 'role', header: 'Role', accessor: 'role', sortable: true },
    { key: 'joined', header: 'Joined', accessor: 'joined', sortable: true, align: 'right' },
  ]}
  data={members}
  rowKey="id"
/>
```

```tsx
// Server-side pagination + sort + multi-select with bulk delete
const [selection, setSelection] = useState<Set<string>>(new Set());
const [sort, setSort] = useState<SortState | null>(null);
const [page, setPage] = useState({ page: 0, pageSize: 25 });

<DataTable
  caption="Orders"
  columns={orderColumns}
  data={orders}
  rowKey="orderId"
  loading={isLoading}
  totalRows={totalOrderCount}
  pagination={page}
  onPageChange={(p) => setPage((prev) => ({ ...prev, page: p }))}
  onPageSizeChange={(size) => setPage({ page: 0, pageSize: size })}
  sortState={sort}
  onSortChange={setSort}
  selectedRowKeys={selection}
  onSelectionChange={setSelection}
  bulkActions={[
    {
      key: 'delete',
      label: 'Delete',
      variant: 'destructive',
      icon: <TrashIcon />,
      onClick: async (keys) => {
        await deleteOrders([...keys]);
        setSelection(new Set());
      },
    },
    {
      key: 'export',
      label: 'Export',
      icon: <DownloadIcon />,
      onClick: (keys) => exportOrders([...keys]),
    },
  ]}
/>
```

```tsx
// Inline editing with validation
<DataTable
  caption="Product catalogue"
  columns={[
    { key: 'name', header: 'Product', accessor: 'name' },
    {
      key: 'price',
      header: 'Price',
      accessor: 'price',
      align: 'right',
      editable: {
        type: 'number',
        validate: (v) => (Number(v) > 0 ? null : 'Price must be greater than 0'),
      },
    },
    {
      key: 'status',
      header: 'Status',
      accessor: 'status',
      editable: {
        type: 'select',
        options: [
          { label: 'Active', value: 'active' },
          { label: 'Draft', value: 'draft' },
          { label: 'Archived', value: 'archived' },
        ],
      },
    },
  ]}
  data={products}
  rowKey="id"
  onEditSave={async (rowKey, columnKey, value) => {
    await updateProduct(rowKey, { [columnKey]: value });
  }}
  stickyHeader
  density="default"
/>
```

---

## 10. Do / Don't

| Do | Don't |
|----|-------|
| Provide a stable `rowKey` that survives re-renders and page changes | Use row index as `rowKey` — breaks selection state across pages |
| Use server-side sort (`onSortChange`) for datasets > 1,000 rows | Sort > 1,000 rows client-side — blocks the main thread |
| Show a loading skeleton via `loading={true}` during data fetches | Swap in a full-page spinner — it causes layout shift |
| Clear `selectedRowKeys` after a destructive bulk action completes | Leave stale selection after rows are deleted |
| Use `variant="destructive"` for bulk delete/remove actions | Use a default-styled button for irreversible bulk actions |
| Provide an `emptyState` with a contextual CTA when zero results | Show a blank table with only "No results" and no guidance |
| Set `totalRows` for server-side pagination | Omit `totalRows` — pagination controls will be wrong |
| Validate inline edits immediately on change; show errors inline | Navigate away to show a validation error on a separate page |
| Use `stickyHeader` when the table is taller than the viewport | Apply sticky header inside a fixed-height overflow container without testing it |
| Use `density="compact"` only for power-user views | Default to compact density — it reduces accessibility of touch targets |
| Keep `bulkActions` to ≤ 5 items; use an overflow menu for more | Render 10+ bulk action buttons — they overflow on tablet viewports |

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.0 (85%) |
| Evaluated | 2026-05-01 |
| Target duration | 504240 ms |
| Target cost | $0.9863 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | All interaction states are enumerated — empty, loading, loaded, error, and every combination of selection + editing + sorting | PASS | Section 4 has four table-level states (Default/Loading/Empty/Error), ten row-level states including Selected+Editing compound combinations, column header states for all sort states, inline edit cell states (Display/Hover/Focus/Active/Edit/Edit+Saving/Edit+Error/Read-only), bulk toolbar states, and a compound combinations table cross-referencing row × cell × toolbar state. |
| c2 | Keyboard navigation is specified for all interactive elements (sort headers, checkboxes, inline edit fields, pagination) | PASS | Section 6 Keyboard Navigation contains separate tables for: sort headers (Tab, Enter/Space), row checkboxes (Space, Shift+Space), select-all checkbox (Space), inline edit cells (Enter, Escape, Tab, Shift+Tab), bulk action toolbar (Tab/Shift+Tab, Enter/Space), and pagination (Tab/Shift+Tab, Enter/Space, ArrowLeft/ArrowRight). |
| c3 | The bulk actions toolbar specifies its own states (hidden, visible, count display) and transitions | PASS | Section 4 'Bulk actions toolbar states' table enumerates Hidden (not rendered, zero height), Visible ('shows selected count + action buttons'), and Action Loading states with explicit Transitions to columns. Section 8 specifies slide-down+fade-in (150ms ease-out) for appear and slide-up+fade-out (100ms ease-in) for dismiss. |
| c4 | Inline editing specifies entry/exit behaviour (click to edit, escape to cancel, enter/blur to save, validation errors) | PASS | Inline edit cell states table: Active(Display) shows 'Pointer press; transitions immediately to Edit on release' (click target = cell); Edit row shows 'Enter saves; Escape cancels; blur on the cell container saves'; Edit+Error row specifies 'border-destructive on input; error text below; save blocked until validate() returns null; input re-focused'. |
| c5 | Responsive behaviour is addressed — what happens to columns, pagination, and bulk actions on mobile | PASS | Section 5 table lists Mobile (<640px): 'Horizontal scroll container; all columns remain but table scrolls'; pagination 'collapses to prev/next buttons only'; bulk toolbar 'collapses to icon-only (label hidden, aria-label still present)'; page size selector hidden. Minimum 44×44px touch targets specified. |
| c6 | Performance considerations are noted for large datasets (virtualisation, pagination vs infinite scroll) | PARTIAL | Section 5 Performance Considerations covers virtualisation (@tanstack/react-virtual), threshold (>100 rows causes jank, >500 not supported), and server-side sort for >1,000 rows. However, infinite scroll is never mentioned — the trade-off is framed as pagination vs virtualisation only, not pagination vs infinite scroll. |
| c7 | Accessibility requirements include ARIA roles for the table, row selection announcements, and focus management during inline edit | PASS | Section 6 Screen Reader: 'role="table" on the <table> element (or role="grid")'; 'aria-checked={true\|false}' on row checkboxes; 'aria-live="polite" region: e.g., "3 rows selected"'. Focus Management: 'When edit mode activates, the input receives focus automatically... focus returns to the cell element' after save/cancel. |
| c8 | Props API is defined with types, defaults, and required/optional status for each prop | PASS | Section 2 has four props tables (DataTable, ColumnDef<TRow>, EditableConfig, BulkAction) each with columns for Prop, Type, Default, Required, and Description. TypeScript interfaces are provided for SortState and PaginationState. |
| c9 | Output enumerates state combinations — empty, loading, loaded, error are the 4 base data states; each combines with selection state (no selection / partial selection / all selected) and editing state (no edit / row in edit mode) for ~16 distinct visual states; the spec covers these systematically not abstractly | PASS | Section 4 provides a compound combinations table explicitly cross-referencing Row state × Cell state × Toolbar state (e.g., Selected/Display/Visible; Selected/Editing/Visible; Unselected/Editing/Hidden). Each state has concrete visual treatment (e.g., 'bg-primary/10 + bg-muted/30 overlay') not abstract labels. |
| c10 | Output's keyboard navigation specification covers — arrow keys for cell traversal, Tab between focusable interactive elements, Space to toggle selection, Enter to enter edit mode, Esc to cancel edit, Enter to commit edit, Cmd/Ctrl+A for select-all | PARTIAL | Tab, Space (checkbox toggle), Enter (enter edit/commit), Escape (cancel) are all specified. ArrowLeft/ArrowRight appear only for pagination page numbers, not for general cell traversal. Cmd/Ctrl+A for select-all is entirely absent — only Space on the select-all checkbox is documented. |
| c11 | Output's bulk-actions toolbar specifies its lifecycle — appears (slide / fade) when first row selected, count display updates as more rows are selected, slides away when selection is cleared; positioning (sticky bottom or header overlay) is specified | PASS | Section 8 animation table: 'Slide down from top + fade in (translateY(-8px) → 0, opacity: 0 → 1), 150ms ease-out' for appear; 'Slide up + fade out, 100ms ease-in' for dismiss. Visible state shows 'selected count + action buttons'. Positioning: 'Slides in above table (or replaces top of table)'. Transition rule: 'After bulk action completes, clear selection automatically — toolbar hides'. |
| c12 | Output's inline-edit interaction is fully specified — click to edit (which click target — cell vs edit button?), Esc cancels (reverts), Enter saves, blur saves with timeout to prevent accidental commits, validation errors appear inline next to the input with revert option | PASS | Click target is the cell: 'Active (Display): Pointer press; transitions immediately to Edit on release'. Esc: 'Cancel edit, restore previous value'. Enter saves, blur saves: 'blur on the cell container (not just the input) saves'. Edit+Error: 'error text below input, save blocked until validate() returns null'. Cancel (✗) button provides revert option. Blur timeout not mentioned but overall coverage is thorough. |
| c13 | Output's responsive behaviour addresses what happens to columns at narrow widths — column priority (which columns hide first), horizontal scroll vs stacking, what happens to the bulk-actions toolbar on mobile, whether inline editing still works on touch | PARTIAL | Horizontal scroll (vs stacking) is specified: 'all columns remain but table scrolls'. Bulk toolbar on mobile: 'bulk action buttons collapse to icon-only'. Column priority/hide order is not addressed — the spec says all columns remain. Whether inline editing works on touch devices is not addressed. |
| c14 | Output addresses performance for large datasets — virtualisation strategy if datasets exceed pagination capacity, the threshold at which virtualisation kicks in, the trade-off between pagination (simpler, server-friendly) and infinite scroll (faster perceived, harder to bookmark) | PARTIAL | Virtualisation strategy (@tanstack/react-virtual) and threshold (>100 rows without pagination causes jank, >500 not supported) are both specified. However, infinite scroll is never mentioned; the only trade-off discussed is pagination vs virtualisation, not pagination vs infinite scroll. |
| c15 | Output's ARIA spec covers — `role="grid"` on the table, `role="gridcell"` on cells, `aria-rowselected` for selection state, `aria-busy` during loading, live-region announcements when bulk actions complete or selections change | PARTIAL | role="grid" mentioned as alternative. aria-busy="true" specified for loading. aria-live="polite" for '3 rows selected' and page changes. However, role="gridcell" on cells is not mentioned, and aria-rowselected is absent — selection state uses aria-checked on checkbox inputs instead. |
| c16 | Output's Props API documents each prop with type (TS), default, required vs optional, description — `data: T[]`, `columns: Column<T>[]`, `loading?: boolean`, `selectedRows?: string[]`, `onSelectionChange?: (rows: string[]) => void`, `onEdit?: (rowId, field, value) => Promise<void>`, etc. | PASS | Section 2 DataTable table includes: data: TRow[], columns: ColumnDef<TRow>[], loading?: boolean (default false), selectedRowKeys?: Set<string>, onSelectionChange?: (keys: Set<string>) => void, onEditSave?: (rowKey: string, columnKey: string, value: unknown) => void \| Promise<void>. All have Type, Default, Required, and Description columns. |
| c17 | Output addresses sort interaction with selection and editing — what happens to row selection when a sort changes (kept by ID), what happens when a row is being edited and the user triggers a sort (warn / save / cancel) | PARTIAL | Selection preservation across sort is implied only: 'Selection is tracked as a Set<string> of row keys, not by index. This is safe for server-side pagination.' No explicit statement that selection is preserved on sort. What happens when a sort is triggered while a cell is in edit mode is not addressed anywhere in the spec. |
| c18 | Output addresses error recovery during inline edit — if the save fails (validation, network, conflict), the cell stays in edit mode with the error message and the user can retry or cancel without losing their input | PARTIAL | Edit+Error state covers client-side validation: 'border-destructive; error text below input; save blocked until validate() returns null; input re-focused'. However, network/server failure (onEditSave promise rejection) has no corresponding error state — Edit+Saving transitions only to Display with no error branch documented. |

### Notes

The spec is exceptionally thorough for a high-complexity component, earning PASS at 85.3%. Strengths: exhaustive state table with visual treatments for every combination, full keyboard navigation for most elements, solid props API with TypeScript types, responsive breakpoints, animation timing, and dark-mode token checklist. The main gaps that cost points: (1) arrow-key cell traversal and Cmd+A select-all are missing from keyboard navigation; (2) infinite scroll is never considered as an alternative to pagination; (3) column hide priority at narrow widths and touch inline-editing behaviour are unaddressed; (4) ARIA spec omits role='gridcell' and aria-rowselected (uses aria-checked on checkbox inputs instead); (5) sort+editing interaction (what happens if a sort header is clicked while a cell is in edit mode) is not addressed; (6) network/server-side save failures have no documented error state in the inline-edit flow.
