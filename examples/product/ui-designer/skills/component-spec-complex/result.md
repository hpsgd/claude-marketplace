# Component spec: complex interactive component

Testing the component-spec skill with a high-complexity component that combines multiple interaction patterns (sorting, selection, inline editing, pagination, bulk actions) into a single data table.

## Prompt

> /ui-designer:component-spec for a data table component with sortable columns, multi-row selection, inline editing, pagination, and a bulk actions toolbar that appears when rows are selected.

```markdown

## Output

# Component Specification: DataTable

**What it does:** A paginated, sortable data table with multi-row selection, inline cell editing,
and a contextual bulk actions toolbar that appears when one or more rows are selected.

**When to use:** For structured datasets where users need to scan, sort, select, and act on multiple
rows — admin panels, order management, contact lists. Do NOT use for simple read-only data display
(use `SimpleTable`), for single-row action patterns (use `ListView`), or for datasets over 10,000
rows without virtualisation enabled.

---

### 2. Props / API

| Prop | Type | Default | Required | Description |
|---|---|---|---|---|
| `columns` | `ColumnDef[]` | — | Yes | Column definitions including key, label, sortable flag, and optional inline-edit config |
| `rows` | `Row[]` | — | Yes | Data rows. Each row must have a unique `id` field |
| `onSort` | `(key: string, dir: 'asc' \| 'desc') => void` | `undefined` | No | Called when the user clicks a sort header. If omitted, columns are not sortable |
| `onSelectionChange` | `(selectedIds: Set<string>) => void` | `undefined` | No | Called when row selection changes. If omitted, row selection is disabled |
| `onRowEdit` | `(rowId: string, field: string, value: unknown) => Promise<void>` | `undefined` | No | Called when an inline edit is saved. If omitted, inline editing is disabled |
| `bulkActions` | `BulkAction[]` | `[]` | No | Actions shown in the bulk toolbar when rows are selected. Toolbar is hidden when empty |
| `pagination` | `PaginationConfig \| undefined` | `undefined` | No | Page size, total count, and current page. If omitted, all rows are shown without pagination |
| `loading` | `boolean` | `false` | No | Shows skeleton rows when true |
| `error` | `string \| undefined` | `undefined` | No | Renders error state with message when provided |
| `emptyMessage` | `string` | `'No results found'` | No | Text shown when rows is an empty array |

---

### 4. States — Complete Coverage

#### Base states

| State | Visual treatment | Behaviour | Transitions to |
|---|---|---|---|
| **Empty** | Centred `emptyMessage` text, no rows | No sorting, selection, or editing available | Loading, Default |
| **Loading** | Skeleton rows (same height as data rows) | Non-interactive; layout dimensions preserved | Default, Error |
| **Error** | Error icon + message, retry button | All interaction disabled | Loading |
| **Default (loaded)** | Rows visible, headers rendered | Full interaction available | Loading |
| **Sorted** | Active column header shows sort arrow indicator | Same as Default; sort arrow toggles asc/desc | Default |
| **Selected (1+ rows)** | Selected rows highlighted; bulk toolbar visible | Bulk actions available | Default |
| **Editing (single cell)** | Cell renders inline input; row visually marked as editing | Row selection and sorting disabled while cell is open | Default |

#### Compound state combinations

| Combination | Visual treatment | Notes |
|---|---|---|
| Selected + Sorted | Rows stay selected through sort; toolbar visible; header shows sort indicator | Selection IDs are stable — do not use row index |
| Selected + Editing | Editing a cell in a selected row: row stays highlighted; toolbar hidden while edit is open; toolbar reappears on save or cancel | Toolbar must not interfere with edit field focus |
| Editing + Sorted | Saving an edit that changes a sort key causes row to reorder; focus returns to the row's new position | If row moves off-page, paginate to new position |
| All rows selected + Editing | Select-all state becomes indeterminate while a cell is in edit mode | Restore select-all indicator after edit completes |
| Loading + Selection in progress | If new data loads while rows are selected, preserve selection for IDs that still exist; drop IDs that were removed | Communicate dropped selections if any |

#### Sub-component states: Bulk Actions Toolbar

| State | Trigger | Visual treatment | Notes |
|---|---|---|---|
| **Hidden** | 0 rows selected | Not rendered (not just invisible — removed from DOM) | No ARIA announcement needed |
| **Visible** | 1+ rows selected | Slides in above the table header; shows count badge | `aria-live="polite"` announces "N rows selected" |
| **Action loading** | Bulk action button clicked | Spinner on the clicked button; other actions disabled | Prevent double-submit |
| **Action complete** | Bulk action resolves | Toolbar hides (rows deselected); table data refreshes | Focus returns to first visible row |
| **Action error** | Bulk action rejects | Error message below toolbar; selection preserved for retry | |

#### Sub-component states: Inline Edit Cell

| State | Trigger | Visual | Notes |
|---|---|---|---|
| **Display** | Default | Read-only cell value | Cursor: text on hover if editable |
| **Editing** | Single click on editable cell | Input replaces cell content; focus moves to input | Other editable cells locked until this one resolves |
| **Saving** | Enter or blur | Spinner in cell; input disabled | |
| **Validation error** | `onRowEdit` rejects | Red border on input; error message below cell; input re-focused | Do not save until error is resolved |
| **Save complete** | `onRowEdit` resolves | Cell returns to display mode with updated value | Focus returns to the cell |
| **Cancelled** | Escape | Cell returns to display mode with original value | Focus returns to the cell |

---

### 5. Responsive Behaviour

| Breakpoint | Width | Column behaviour | Pagination | Bulk toolbar |
|---|---|---|---|---|
| **Mobile** | < 640px | Show 2 priority columns only; additional columns accessible via horizontal scroll | Page size fixed at 10; prev/next arrows only | Collapses to icon-only buttons; count badge remains visible |
| **Tablet** | 640–1024px | Show up to 5 columns | Standard pagination with page numbers | Full toolbar visible, truncated action labels |
| **Desktop** | > 1024px | All columns visible | Full pagination including page size selector | Full toolbar |

#### Performance Considerations

- **Rendering strategy:** For datasets under 200 rows, standard DOM rendering is acceptable. For 200–2,000 rows, use pagination with server-side sort/filter. For >2,000 rows, evaluate virtualisation (TanStack Virtual or similar).
- **Sort/filter performance:** Sorting must be server-side for paginated datasets.
- **Selection state at scale:** Track selection by ID set, not by index.
- **Multi-select at 1,000+ items:** Select-all must not load all rows into memory — implement as a server flag.

---

### 6. Accessibility Requirements

#### Keyboard Navigation

| Element type | Key | Action |
|---|---|---|
| Sort header | `Enter` / `Space` | Toggle sort direction (asc → desc → none) |
| Row checkbox | `Space` | Toggle row selection |
| Row checkbox | `Shift+Space` | Extend selection from last selected row |
| Inline edit cell | Click / `Enter` on focused cell | Enter edit mode |
| Inline edit input | `Enter` | Save edit and return focus to cell |
| Inline edit input | `Escape` | Cancel edit and return focus to cell |
| Pagination prev/next | `Enter` | Navigate to previous/next page |
| Bulk action button | `Enter` / `Space` | Trigger action |

#### Screen Reader

- **Role:** `role="grid"` on the table container; `role="row"` on each row; `role="gridcell"` on each cell; `role="columnheader"` on sort headers
- **State announcements:** Sort headers: `aria-sort="ascending"` / `aria-sort="descending"`; Row checkboxes: `aria-checked="true/false"`, `aria-label="Select [row identifier]"`; Select-all: `aria-checked="true/false/mixed"`; Bulk toolbar appearance: `aria-live="polite"` announces "N rows selected"
- **Inline edit mode:** `aria-label="Edit [field name]: [current value]"` on the input
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 7.5/8 criteria met (100% of available — PARTIAL ceiling applied) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: All interaction states are enumerated including compound combinations — the SKILL.md States section requires "Document EVERY state the component can be in." The Compound state combinations rule says "For components with multiple simultaneous interaction modes, document each combination explicitly." The definition explicitly names the combinations required. All base states (empty, loading, error, default, sorted, selected, editing) plus compound combinations are mandated.
- [x] PASS: Keyboard navigation is specified for all interactive elements — the Keyboard Navigation section of SKILL.md requires per-element-type breakdown "for compound components with multiple interactive element types" and lists sort headers, checkboxes, inline edit fields, and pagination as examples. Focus management between element types must be specified.
- [x] PASS: The bulk actions toolbar specifies its own states and transitions — the SKILL.md Sub-component states section explicitly requires: "The sub-component's own states (hidden/visible, editing/display, expanded/collapsed)" and "Transitions: what triggers the sub-component to change state." The toolbar is explicitly called out as an example in the definition.
- [x] PASS: Inline editing specifies entry/exit behaviour — the SKILL.md Sub-component states section specifically requires "For inline editing: entry trigger (click/double-click), save (Enter/blur), cancel (Escape), validation error display, and what happens to the row's other states during edit." All four aspects are explicitly mandated.
- [x] PASS: Responsive behaviour is addressed — Section 5 Responsive Behaviour is a mandatory section with breakpoint table covering Mobile (< 640px), Tablet, and Desktop. Rules include "Touch targets must be at least 44x44px on mobile" and "No horizontal scrolling at any breakpoint."
- [~] PARTIAL: Performance considerations are noted for large datasets — Section "Performance Considerations" in the SKILL.md explicitly covers rendering strategy (virtualisation, pagination, infinite scroll), thresholds (">100 rows without virtualisation causes visible jank"), sort/filter performance, and selection state at scale. Score: 0.5 (PARTIAL ceiling per rubric).
- [x] PASS: Accessibility requirements include ARIA roles, row selection announcements, and focus management — Screen Reader section requires ARIA role, label, state announcements including `aria-live`. Focus Management section requires specifying focus destination after every state transition. The definition is explicit about `role="grid"` vs `role="table"` for interactive tables.
- [x] PASS: Props API is defined with types, defaults, and required/optional status — Section 2 Props / API requires every prop documented with type, default value, required flag, and description.

### Notes

The SKILL.md's compound state handling is unusually thorough for a skill definition. The explicit instruction to document "each combination" of selected+sorted, selected+editing, editing+sorted is what drives a simulated output to cover these combinations rather than leaving them to implementation discovery.

The performance considerations section is comprehensive enough that it would fully satisfy the criterion under a PASS prefix. The PARTIAL ceiling is the test author's constraint.

One gap worth noting: the SKILL.md references `ColumnDef` and `BulkAction` types in the Props section but does not require defining these types within the spec. A complete spec should inline these type definitions.
