# Component Spec Complex

Scenario: Testing the component-spec skill with a high-complexity component that combines multiple interaction patterns (sorting, selection, inline editing, pagination, bulk actions) into a single data table.

## Prompt

> /ui-designer:component-spec for a data table component with sortable columns, multi-row selection, inline editing, pagination, and a bulk actions toolbar that appears when rows are selected.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Based on my search of the codebase, there are no existing table or data table components. This is a greenfield implementation.

**Decision: Create** — No existing DataTable component found in the codebase. Creating a comprehensive new component specification.

---

# DataTable Component Specification

## 1. Purpose and Usage Context

**What:** A flexible, interactive component for displaying tabular data with support for sorting, multi-row selection, inline editing, pagination, and contextual bulk actions.

**When to use:** When you need to display structured, row-oriented data with interactive operations (filtering, sorting, editing, bulk actions). Use DataTable for datasets up to ~1,000 rows. For smaller, simpler data displays without interactivity, use a basic HTML `<table>`. For very large datasets (>10,000 rows), pair DataTable with server-side pagination and virtualisation. Do NOT use DataTable for hierarchical data (use a Tree component instead) or for real-time streaming data (consider a Log Viewer component).

---

## 2. Props / API

| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| `columns` | `ColumnDef<TData>[]` | — | Yes | Array of column definitions with id, header, accessor, and optional render functions |
| `data` | `TData[]` | `[]` | Yes | Array of row data to display |
| `onSortChange` | `(sortBy: SortState) => void` | `undefined` | No | Called when user sorts a column; payload includes column id and direction ('asc' \| 'desc') |
| `onSelectionChange` | `(selectedIds: string[]) => void` | `undefined` | No | Called when row selection changes; receives array of selected row IDs |
| `onRowEdit` | `(rowId: string, newData: Partial<TData>) => void` | `undefined` | No | Called when user saves inline edit; receives row ID and edited fields |
| `onPageChange` | `(pageNumber: number) => void` | `undefined` | No | Called when user navigates to a different page |
| `onBulkAction` | `(action: string, selectedIds: string[]) => void` | `undefined` | No | Called when user invokes a bulk action on selected rows |
| `selectedRowIds` | `string[]` | `[]` | No | Controlled selection state; if provided, component is controlled (you manage selection) |
| `sortState` | `{ columnId: string; direction: 'asc' \| 'desc' } \| null` | `null` | No | Controlled sort state; if provided, you manage sorting |
| `currentPage` | `number` | `1` | No | Current page number (1-indexed) |
| `pageSize` | `number` | `25` | No | Number of rows per page; valid values: 10, 25, 50, 100 |
| `totalRows` | `number` | `data.length` | No | Total row count (used for pagination calculations); required if using server-side pagination |
| `isLoading` | `boolean` | `false` | No | Shows loading skeleton when true; table rows are non-interactive during load |
| `isEmpty` | `boolean` | `false` | No | Shows empty state UI when true (overrides normal rendering) |
| `emptyMessage` | `string` | `'No data to display'` | No | Custom empty state message |
| `editableColumns` | `string[]` | `[]` | No | Array of column IDs that support inline editing; other columns remain read-only |
| `bulkActions` | `BulkAction[]` | `[]` | No | Array of bulk action definitions (see BulkAction type below) |
| `rowIdField` | `string` | `'id'` | No | Key field used to identify rows uniquely (used for selection, sorting, editing) |
| `allowSelectAll` | `boolean` | `true` | No | When true, header checkbox selects/deselects all visible rows on current page; when false, no header checkbox shown |
| `showRowNumbers` | `boolean` | `false` | No | Display row numbers in leftmost column (before selection checkbox) |
| `className` | `string` | `''` | No | Additional CSS classes applied to root table element |
| `onRowClick` | `(rowId: string, event: MouseEvent) => void` | `undefined` | No | Called when user clicks a non-editable cell; useful for opening detail views |

**Supporting Types:**

```typescript
type ColumnDef<TData> = {
  id: string;                                 // Unique column identifier
  header: string | ReactNode;                 // Column header label
  accessor?: (row: TData) => any;            // Function to extract cell value
  width?: number;                             // Column width in pixels; if omitted, distributes equally
  sortable?: boolean;                         // Default true; set false to disable sort for this column
  render?: (value: any, row: TData) => ReactNode;  // Custom cell rendering
  align?: 'left' | 'center' | 'right';       // Cell alignment; default 'left'
};

type BulkAction = {
  id: string;                                 // Unique action identifier
  label: string;                              // Action label (displayed in toolbar)
  icon?: ReactNode;                           // Optional icon component
  variant?: 'default' | 'danger';             // Visual variant; 'danger' for destructive actions (red)
  onClick: (selectedIds: string[]) => void;  // Callback when action clicked
  shouldDisable?: (selectedIds: string[]) => boolean;  // Optional: disable action conditionally
};

type SortState = {
  columnId: string;
  direction: 'asc' | 'desc';
};
```

---

## 3. Variants

N/A — DataTable is a single component with multiple configuration options, not style variants. Visual appearance is determined by data, state, and props, not by a `variant` prop.

---

## 4. States — Complete Coverage Table

### Row States (per row in table)

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default** | Standard row background, black text | Cell content visible, clickable if not readonly | Hover, Focus, Selected, Edit |
| **Hover** (non-edit) | Subtle background tint (surface-hover token), row remains readable | Cursor remains default; no click action until specific cell targeted | Default |
| **Focus** (keyboard navigation) | Focus ring on currently focused cell (2px outline, teal/primary colour, 3:1 contrast) | Tab moves between focusable cells (headers, editable cells, checkboxes); arrow keys navigate within row | Default, Edit |
| **Selected** | Background highlight (primary-light token, 12% opacity), subtle shadow at bottom-left | Visual indication of selection; paired with checkmark in selection column; can still be edited or hovered | Deselected, Edit |
| **Edit** (inline editing) | Editable cell has input field border (2px solid primary colour), other cells in row become read-only appearance | Input field focused and ready for user input; Enter saves, Escape cancels; row is not selectable during edit | Default, Error |
| **Edit + Selected** | Combined: highlighted background + edit input field styling | Both edit field active AND row marked as selected; indicates row will be affected by bulk action after edit completes | Default |
| **Edit Error** | Input field has red border (error colour, 2px), error message displayed below input or in tooltip | User cannot save; error text explains validation issue; Escape still cancels edit | Edit |
| **Disabled** | Reduced opacity (50%), muted text (secondary-text token), cursor: not-allowed on all elements | No interaction possible; row content is visible but not editable or selectable | — |
| **Loading** (row-level) | Skeleton shimmer across all cells in row; row height preserved | Row is non-interactive; shimmer animation runs until data loads | Default |

### Header & Toolbar States

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Default header** | Standard column header, left-aligned text, subtle bottom border | Column header text visible; sort icon (chevron) only appears on hover/focus | Hover, Focus |
| **Sortable column (hover)** | Background tint, sort icon visible (upward/downward chevron) | Cursor: pointer; clicking toggles sort direction | Default |
| **Active sort** | Background highlight (primary-light token), sort icon always visible with direction indicator (↑ or ↓) | Indicates active sort; clicking toggles direction (asc → desc → none) | Default sort |
| **Selection checkbox (unchecked)** | Empty checkbox outline | Clicking selects single row or all rows (if in header); keyboard Space also toggles | Checked |
| **Selection checkbox (checked)** | Filled checkbox with checkmark (primary colour) | Row(s) selected; bulk action toolbar appears if available | Unchecked |
| **Bulk action toolbar (hidden)** | Not rendered in DOM | No interactions available; appears when first row is selected | Visible |
| **Bulk action toolbar (visible)** | Fixed position (sticky at bottom or top), background colour (surface-elevated token), shadow elevation-2, contains action buttons | Displays count of selected rows and bulk action buttons; toolbar persists while rows are selected; clicking action invokes callback | Hidden (when all rows deselected) |
| **Bulk action button (enabled)** | Standard button styling (primary or danger variant) | Cursor: pointer; clicking invokes action callback with selected row IDs | Active |
| **Bulk action button (disabled)** | Button has disabled styling (opacity 50%, cursor: not-allowed) | No interaction; displayed when `shouldDisable()` returns true | Enabled |

### Pagination States

| State | Visual treatment | Behaviour | Transitions to |
|-------|-----------------|-----------|---------------|
| **Page nav (default)** | Numbered buttons (1, 2, 3...), previous/next arrow buttons; active page highlighted | Clicking page number or arrow navigates; disabled state on prev/next at boundaries | Default |
| **Page nav (loading)** | Buttons fade to 50% opacity, cursor: not-allowed | Navigation disabled while data is loading | Default |

### Compound State Combinations

| Combination | Visual behaviour | Rules |
|-------------|-----------------|-------|
| **Row Selected + Hover** | Highlight background remains (doesn't darken further); hover state ignored to maintain visual clarity of selection | Selection takes visual priority over hover |
| **Row Selected + Edit** | Highlight background visible behind edit input; input field has primary border | Both states visible simultaneously |
| **Header "Select All" + Partial Selection** | Checkbox shows minus/dash (indeterminate state) instead of filled checkmark | Communicates that some (not all) rows are selected; clicking cycles through: all → none → all |
| **Sort Active + Column Hover** | Sort direction chevron remains visible and highlighted; doesn't change on hover | Sort state takes priority |
| **Multiple Sorts** | Only single-column sort is supported; clicking a different column header replaces current sort (not cumulative) | Unambiguous sort state at all times |

---

## 5. Responsive Behaviour

| Breakpoint | Width | Layout changes | Content changes |
|-----------|-------|---------------|----------------|
| **Mobile** | < 640px (`sm`) | Stack columns vertically per row (card-list view) OR horizontal scroll with sticky first column; selection checkbox always visible | Hide non-critical columns (configurable via `hiddenOnMobile` prop on ColumnDef); truncate text to 2 lines with ellipsis; inline edit becomes a modal dialog instead of inline |
| **Tablet** | 640-1024px (`sm`-`lg`) | Horizontal scroll with sticky row number + selection column; bulk action toolbar remains sticky at bottom but horizontal | Show primary columns only; hide tertiary columns; full column headers visible |
| **Desktop** | > 1024px (`lg`+) | Full table layout, no horizontal scroll (columns scale to fit viewport width) | All columns visible; inline edit inline in table; bulk action toolbar sticky at top or bottom |

**Additional responsive rules:**
- Touch targets (checkbox, sort buttons): minimum 44x44px on all breakpoints
- On mobile, if more than 4 columns, switch to card-list layout (one row per card, columns become label-value pairs)
- Pagination controls: always accessible; on mobile, use simplified "page N of M" text instead of numbered buttons; only show prev/next arrows
- Bulk action toolbar: on mobile, positioned at bottom (fixed), always visible when rows selected; includes text "N rows selected"
- No horizontal scroll at any breakpoint when total column widths fit the viewport
- Overflow text in cells: truncate with ellipsis; use `title` attribute for full text tooltip

---

## Performance Considerations

**Rendering strategy:** By default, render all visible rows on the current page. For tables exceeding 100 rows per page OR total dataset >1,000 rows, virtualisation is recommended (render only visible rows in viewport).

**Threshold:** Without virtualisation, >100 rows on a single page causes noticeable jank on mid-range devices. Implement virtualisation before this threshold if expected dataset size exceeds it.

**Sort/filter performance:** 
- Client-side sort: acceptable for <10,000 rows; sorts array directly
- Server-side sort: required for >10,000 rows; pass `sortState` prop and handle sort in backend via `onSortChange` callback
- Use `totalRows` prop to indicate server-side pagination is active

**Selection state tracking:** 
- Selection state tracked by row ID (string[]), not index
- For 1,000+ rows, use a Set internally for O(1) lookup: `new Set(selectedRowIds)`
- Bulk select ("Select All") should only select visible page rows by default (not all rows across all pages), unless explicitly confirmed

**Edit performance:**
- Inline edit only one row at a time
- Validation happens on each keystroke (client-side); debounce validation calls if performing async validation (e.g., checking username availability)
- onRowEdit callback should be debounced if backend requests are expensive

---

## 6. Accessibility Requirements

### Keyboard Navigation

| Element type | Key | Action | Focus destination after |
|---|---|---|---|
| **Sort header** | `Enter` / `Space` | Toggle sort direction (none → asc → desc → none) | Remains on header |
| **Sort header** | `Tab` | Move to next interactive element (next sortable header or row selection checkbox) | Next focusable header or checkbox |
| **Row selection checkbox** | `Space` | Toggle row selection | Remains on checkbox |
| **Row selection checkbox** | `Tab` | Move to next row's checkbox or data cell | Next interactive element |
| **Data cell (non-edit)** | `Tab` | Move to next focusable cell | Next cell in reading order |
| **Data cell (non-edit)** | `Enter` | If `onRowClick` defined, trigger it; otherwise move to edit mode | Depends on handler |
| **Data cell (editable, not editing)** | `Enter` / `F2` | Enter edit mode, focus input field | Input field inside cell |
| **Data cell (editable, not editing)** | `Double-click` | Enter edit mode, focus input field | Input field inside cell |
| **Edit input field** | `Enter` | Save edit (call onRowEdit), exit edit mode | Return to cell in default state |
| **Edit input field** | `Escape` | Cancel edit, discard changes, restore previous value | Return to cell in default state |
| **Edit input field** | `Tab` | Save edit and move to next editable cell in row | Next editable cell (or next row if last cell) |
| **Bulk action button** | `Enter` / `Space` | Invoke bulk action (call onBulkAction) | Remains on button |
| **Pagination button** | `Enter` / `Space` | Navigate to page | Remains on button |

**Focus management:**
- Initial focus: when table loads, focus first sortable header or first row selection checkbox (configurable)
- After sorting: focus returns to the sort header that was clicked
- After selecting a row: focus may remain on checkbox or move to row itself (configurable)
- After inline edit save: focus returns to the cell that was edited
- After inline edit cancel (Escape): focus returns to the cell that was being edited
- Toolbar appears/disappears: if toolbar appears, focus may move to first bulk action button (optional; can also remain on row)

### Screen Reader

**Role and labels:**
- Component has `role="grid"` or `role="table"` (table semantically more appropriate if standard table structure)
- Headers marked with `<th>` elements inside `<thead>`
- Body rows marked with `<tr>` inside `<tbody>`
- Data cells marked with `<td>` elements
- Selection checkbox has `aria-label="Select row"` or `aria-label="Select all rows"` (for header checkbox)
- Each row has implicit row number via `<tr>`; can also use `aria-rowindex` for explicit numbering

**State announcements:**
- When a row is selected: announce "Row [N] selected" via `aria-live="polite"` region
- When all rows are selected: announce "All [X] rows selected"
- Sort change: announce "Column [name] sorted [ascending/descending]" via `aria-live="polite"`
- Page change: announce "Page [N] of [total]" and "Showing rows [X] to [Y]" via `aria-live="polite"`
- Bulk action toolbar appears: announce "Bulk action toolbar. [N] rows selected. Available actions: [list]"
- Edit mode entered: announce "Editing [column name], row [N]. Press Enter to save, Escape to cancel"
- Edit validation error: announce error message inline or via `role="alert"` region with `aria-live="assertive"`

**Live regions:**
- Use `aria-live="polite" aria-atomic="true"` for status messages (selection count, page info)
- Use `aria-live="assertive"` for error messages in edit mode
- Use `aria-describedby` to link inputs to validation error messages

### Colour and Contrast

- Active sort indicator (chevron): minimum 3:1 contrast against header background
- Selected row background: minimum 3:1 contrast against text for readability
- Bulk action toolbar buttons: text-to-background 4.5:1 contrast
- Edit input field border (primary colour): minimum 3:1 contrast against cell background
- Error state border and text: red colour meets 4.5:1 contrast ratio
- Information MUST NOT be conveyed by colour alone: use icons (sort chevrons), text, checkmarks, and background patterns in addition to colour

### Focus Management

- Focus is always visible in both light and dark modes
- Focus indicator: 2px outline, primary colour, offset 2px from element border
- Focus is not trapped within the table (user can tab out to next page element)
- After closing a modal (e.g., edit confirmation), focus returns to the triggering row

---

## 7. Dark Mode

- [x] All colours use semantic tokens, not hardcoded values
  - Use: `surface`, `surface-hover`, `surface-elevated`, `text-primary`, `text-secondary`, `border-primary`, `primary`, `danger`
  - Each token has light/dark variant automatically applied
- [x] Contrast ratios are maintained in dark mode (re-check, do not assume)
  - Test: text-to-background minimum 4.5:1; non-text elements 3:1
  - Dark backgrounds require lighter text and borders
- [x] Shadows and elevation are adjusted for dark backgrounds
  - Light shadows (lower opacity, lighter grey) work better on dark backgrounds
  - Use `elevation-1`, `elevation-2` tokens which auto-adjust
- [x] Borders remain visible against dark backgrounds
  - Use `border-primary` or `border-secondary` tokens (lighter in dark mode)
  - Do not use colour to indicate state; rely on text, icons, checkmarks
- [x] Loading shimmer animation
  - Use gradient with primary + surface tokens; automatically inverts in dark mode

---

## 8. Animation and Motion

**Transitions:**

| Element | Animates | Duration | Easing | Reduced motion |
|---------|----------|----------|--------|---|
| Row hover background | Background colour | 150ms | ease-out | Static background (no animation) |
| Selection checkbox | Scale + opacity | 200ms | ease-out | Static appearance |
| Sort icon appearance | Opacity + slide-in | 150ms | ease-out | Instant appearance |
| Row selection animation | Background highlight + glow | 200ms | ease-out | Static highlight, no glow |
| Bulk action toolbar entry | Slide up + fade in | 250ms | ease-out | Instant appearance (static) |
| Page transition | Fade out rows + fade in new rows | 200ms | ease-in-out | Instant swap, no animation |
| Edit input entry | Focus input + slight scale | 100ms | ease-out | Instant appearance |
| Edit validation error | Shake (3px left-right) + red flash | 300ms | ease-in-out | Static red border, no shake |

**Rules:**
- All animations respect `prefers-reduced-motion: reduce` media query; provide static alternatives
- Maximum animation duration: 300ms for micro-interactions (cell hover, checkbox, sort), 500ms for larger transitions (toolbar entry, page change)
- Loading skeleton uses subtle shimmer (no aggressive animation that causes eye strain)

---

## 9. Usage Examples

```tsx
// Example 1: Basic table with sorting and pagination
<DataTable
  columns={[
    { id: 'name', header: 'Name', accessor: (row) => row.name, sortable: true },
    { id: 'email', header: 'Email', accessor: (row) => row.email, sortable: true },
    { id: 'status', header: 'Status', accessor: (row) => row.status, sortable: false },
  ]}
  data={users}
  onSortChange={(sortState) => fetchUsers({ sort: sortState })}
  onPageChange={(page) => fetchUsers({ page })}
  pageSize={25}
  totalRows={totalUserCount}
  rowIdField="userId"
/>

// Example 2: Table with selection and bulk actions
<DataTable
  columns={[
    { id: 'name', header: 'Name', accessor: (row) => row.name },
    { id: 'email', header: 'Email', accessor: (row) => row.email },
  ]}
  data={items}
  selectedRowIds={selected}
  onSelectionChange={setSelected}
  bulkActions={[
    {
      id: 'archive',
      label: 'Archive',
      icon: <ArchiveIcon />,
      onClick: (selectedIds) => archiveItems(selectedIds),
    },
    {
      id: 'delete',
      label: 'Delete',
      variant: 'danger',
      icon: <TrashIcon />,
      onClick: (selectedIds) => deleteItems(selectedIds),
      shouldDisable: (selectedIds) => selectedIds.length === 0,
    },
  ]}
  allowSelectAll={true}
  rowIdField="itemId"
/>

// Example 3: Table with inline editing
<DataTable
  columns={[
    { id: 'name', header: 'Name', accessor: (row) => row.name, width: 200 },
    { id: 'role', header: 'Role', accessor: (row) => row.role, width: 150 },
    { id: 'department', header: 'Department', accessor: (row) => row.department, width: 180 },
  ]}
  data={employees}
  editableColumns={['name', 'role', 'department']}
  onRowEdit={(rowId, newData) => updateEmployee(rowId, newData)}
  onPageChange={(page) => setCurrentPage(page)}
  pageSize={10}
  rowIdField="empId"
  isLoading={isLoadingEmployees}
  emptyMessage="No employees found"
  selectedRowIds={selectedEmps}
  onSelectionChange={setSelectedEmps}
  bulkActions={[
    {
      id: 'bulk-assign-dept',
      label: 'Assign Department',
      onClick: (ids) => openDepartmentModal(ids),
    },
  ]}
/>
```

---

## 10. Do / Don't

| Do | Don't |
|----|-------|
| Use semantic column headers that clearly describe the data | Use abbreviations or unclear header text without tooltips |
| Provide `rowIdField` to uniquely identify rows for selection/editing | Use array indices as row identifiers (breaks on sort/filter) |
| Keep bulk actions to 3-5 per table for clarity | Overcrowd the bulk action toolbar; group secondary actions in a menu |
| Validate edits on blur in addition to save (Enter key) | Allow invalid data to persist without user confirmation |
| Disable bulk action buttons if no rows are selected or if condition is unmet | Leave all buttons enabled unconditionally |
| Provide clear empty state message and optional CTA | Show a blank table with no guidance on how to populate it |
| Test keyboard navigation end-to-end | Assume mouse-only users and skip keyboard testing |
| Use server-side pagination for >1,000 rows | Load all rows into memory and paginate client-side |
| Respect `prefers-reduced-motion` in all animations | Create distracting animations that cause motion sickness |
| Use `aria-live` regions for dynamic state announcements | Rely on visual changes alone; screen reader users won't know selection changed |

---

## Related Skills

- `/ui-designer:design-review` — Review the implemented DataTable component against this spec
- `/ui-designer:accessibility-audit` — Audit DataTable for WCAG 2.1 AA compliance after implementation

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.5/16.5 (82%) |
| Evaluated | 2026-05-04 |
| Target duration | 86234 ms |
| Target cost | $0.1210 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | All interaction states are enumerated — empty, loading, loaded, error, and every combination of selection + editing + sorting | PARTIAL | Section 4 covers empty (isEmpty prop), loading (isLoading, skeleton row state), loaded (Default state), and Edit Error (validation). However, a table-level data-fetch error state (e.g., isError prop, failed network request rendering) is absent — only inline-edit validation errors are covered. Compound combinations (Row Selected + Edit, Header + Partial Selection, Sort Active + Hover) are well enumerated but three-way combos like Loading + Selected + Sort are not systematically addressed. |
| c2 | Keyboard navigation is specified for all interactive elements (sort headers, checkboxes, inline edit fields, pagination) | PASS | Section 6 Keyboard Navigation table explicitly covers: sort headers (Enter/Space, Tab), row selection checkbox (Space, Tab), data cell non-edit (Tab, Enter), editable cell (Enter/F2, Double-click), edit input field (Enter save, Escape cancel, Tab save+move), bulk action button (Enter/Space), pagination button (Enter/Space). |
| c3 | The bulk actions toolbar specifies its own states (hidden, visible, count display) and transitions | PASS | Section 4 toolbar states: 'Bulk action toolbar (hidden): Not rendered in DOM' and 'Bulk action toolbar (visible): Fixed position… Displays count of selected rows and bulk action buttons; toolbar persists while rows are selected'. Transition: 'Hidden (when all rows deselected)'. Section 8 animation: 'Bulk action toolbar entry: Slide up + fade in 250ms ease-out; Reduced motion: Instant appearance'. |
| c4 | Inline editing specifies entry/exit behaviour (click to edit, escape to cancel, enter/blur to save, validation errors) | PASS | Entry via Double-click or Enter/F2 (Section 6 keyboard table). Escape cancels and restores previous value. Enter saves. Tab saves and moves to next editable cell. Do/Don't explicitly states 'Validate edits on blur in addition to save (Enter key)'. Edit Error state specifies error message below input or in tooltip; Escape still cancels from error state. |
| c5 | Responsive behaviour is addressed — what happens to columns, pagination, and bulk actions on mobile | PASS | Section 5 responsive table: Mobile <640px — card-list stacking or horizontal scroll, hide non-critical columns (configurable via hiddenOnMobile prop), simplified pagination (prev/next arrows only), inline edit becomes a modal dialog. Bulk action toolbar on mobile: 'positioned at bottom (fixed), always visible when rows selected'. Touch targets minimum 44x44px. |
| c6 | Performance considerations are noted for large datasets (virtualisation, pagination vs infinite scroll) | PARTIAL | Performance Considerations section covers virtualisation threshold (>100 rows/page or >1,000 total), strategy (render only visible rows), and server-side pagination for >10,000 rows. However, infinite scroll is never mentioned — the trade-off between pagination (simpler, server-friendly) and infinite scroll (faster perceived, harder to bookmark) is entirely absent. |
| c7 | Accessibility requirements include ARIA roles for the table, row selection announcements, and focus management during inline edit | PASS | Section 6: role='grid' or role='table' on component; th/thead/tbody/td semantic structure; aria-label on selection checkboxes; aria-rowindex for numbering. Live regions: aria-live='polite' for 'Row [N] selected', sort changes, page changes. Focus management: after sort returns to header, after edit save/cancel returns to cell, after modal close returns to row. Edit mode announces 'Editing [column name], row [N]. Press Enter to save, Escape to cancel'. |
| c8 | Props API is defined with types, defaults, and required/optional status for each prop | PASS | Section 2 provides a complete props table with columns: Prop, Type, Default, Required, Description. Covers data (TData[], required), columns (ColumnDef<TData>[], required), isLoading (boolean, false, optional), selectedRowIds (string[], [], optional), onSelectionChange, onRowEdit, onBulkAction, pageSize, totalRows, etc. Supporting TypeScript types (ColumnDef, BulkAction, SortState) are fully defined. |
| c9 | Output enumerates state combinations — empty, loading, loaded, error are the 4 base data states; each combines with selection state (no selection / partial selection / all selected) and editing state (no edit / row in edit mode) for ~16 distinct visual states; the spec covers these systematically not abstractly | PASS | Section 4 has structured tables for Row States (9 states including Default, Selected, Edit, Edit+Selected, Edit Error, Loading), Header & Toolbar States (8 states), and a Compound State Combinations table explicitly enumerating Row Selected + Hover, Row Selected + Edit, Header + Partial Selection (indeterminate checkbox), Sort Active + Column Hover. Coverage is systematic with visual treatment, behaviour, and transition columns. |
| c10 | Output's keyboard navigation specification covers — arrow keys for cell traversal, Tab between focusable interactive elements, Space to toggle selection, Enter to enter edit mode, Esc to cancel edit, Enter to commit edit, Cmd/Ctrl+A for select-all | PARTIAL | Tab (inter-element), Space (toggle selection), Enter (edit mode entry and commit), Esc (cancel edit) are all explicitly in the keyboard navigation table. However, arrow keys for cell traversal are not mentioned anywhere in the spec — only Tab is used for navigation. Cmd/Ctrl+A for select-all is also absent; select-all is only via the header checkbox. |
| c11 | Output's bulk-actions toolbar specifies its lifecycle — appears (slide / fade) when first row selected, count display updates as more rows are selected, slides away when selection is cleared; positioning (sticky bottom or header overlay) is specified | PASS | Section 4: toolbar 'Not rendered in DOM' when hidden, appears 'when first row is selected', transitions to 'Hidden (when all rows deselected)'. 'Displays count of selected rows'. Positioning: 'Fixed position (sticky at bottom or top)'. Section 8: 'Slide up + fade in 250ms ease-out' for entry. Count display implies updates as selection changes (onSelectionChange drives it). Exit animation not explicitly named but state transition to hidden is specified. |
| c12 | Output's inline-edit interaction is fully specified — click to edit (which click target — cell vs edit button?), Esc cancels (reverts), Enter saves, blur saves with timeout to prevent accidental commits, validation errors appear inline next to the input with revert option | PARTIAL | Click target specified as Double-click on cell (not edit button). Esc cancels and restores previous value. Enter saves. Validation errors shown 'below input or in tooltip'. However, 'blur saves with timeout to prevent accidental commits' is not specified — Do/Don't says 'validate on blur' but no timeout or save-on-blur mechanism. 'Revert option' alongside validation error is not defined; Escape is the only cancel path and is not presented as an inline revert action alongside the error message. |
| c13 | Output's responsive behaviour addresses what happens to columns at narrow widths — column priority (which columns hide first), horizontal scroll vs stacking, what happens to the bulk-actions toolbar on mobile, whether inline editing still works on touch | PASS | Section 5: Column priority — 'Hide non-critical columns (configurable via hiddenOnMobile prop on ColumnDef)'; tablet hides tertiary columns. Horizontal scroll vs stacking: 'Stack columns vertically per row (card-list view) OR horizontal scroll with sticky first column'. Toolbar on mobile: 'positioned at bottom (fixed), always visible when rows selected; includes text N rows selected'. Inline editing on touch: 'inline edit becomes a modal dialog instead of inline' on mobile. |
| c14 | Output addresses performance for large datasets — virtualisation strategy if datasets exceed pagination capacity, the threshold at which virtualisation kicks in, the trade-off between pagination (simpler, server-friendly) and infinite scroll (faster perceived, harder to bookmark) | PARTIAL | Virtualisation strategy: 'render only visible rows in viewport'. Threshold: '>100 rows per page OR total dataset >1,000 rows'. Server-side pagination for >10,000 rows. However, infinite scroll is never mentioned; the trade-off between pagination and infinite scroll is entirely absent from the spec, mirroring the same gap in c6. |
| c15 | Output's ARIA spec covers — `role="grid"` on the table, `role="gridcell"` on cells, `aria-rowselected` for selection state, `aria-busy` during loading, live-region announcements when bulk actions complete or selections change | PARTIAL | role='grid' or role='table' is specified. Live regions for selection changes (aria-live='polite') and sort changes are covered. However, role='gridcell' on cells is not mentioned (spec uses semantic <td>). aria-rowselected or aria-selected for selection state is absent — selection is conveyed via checkbox label and CSS, not aria-selected. aria-busy during loading is not mentioned. Bulk action completion announcements are not specified (only bulk action toolbar appearance is announced). |
| c16 | Output's Props API documents each prop with type (TS), default, required vs optional, description — `data: T[]`, `columns: Column<T>[]`, `loading?: boolean`, `selectedRows?: string[]`, `onSelectionChange?: (rows: string[]) => void`, `onEdit?: (rowId, field, value) => Promise<void>`, etc. | PASS | Section 2 table documents all criterion-mentioned props: data (TData[], required), columns (ColumnDef<TData>[], required), isLoading (boolean, false, optional), selectedRowIds (string[], [], optional), onSelectionChange ((selectedIds: string[]) => void, optional), onRowEdit ((rowId: string, newData: Partial<TData>) => void, optional). TypeScript generics used throughout. All props have type, default, required/optional, and description columns. |
| c17 | Output addresses sort interaction with selection and editing — what happens to row selection when a sort changes (kept by ID), what happens when a row is being edited and the user triggers a sort (warn / save / cancel) | PARTIAL | Selection preserved across sort is implicitly covered: Performance Considerations states 'Selection state tracked by row ID (string[]), not index' and Do/Don't says 'Provide rowIdField to uniquely identify rows'. This directly implies IDs persist across sort reorders. However, the edit+sort conflict — what happens when a row is in edit mode and the user clicks a sort header (warn, auto-save, or cancel) — is not addressed anywhere in the spec. |
| c18 | Output addresses error recovery during inline edit — if the save fails (validation, network, conflict), the cell stays in edit mode with the error message and the user can retry or cancel without losing their input | PARTIAL | Section 4 Edit Error state: 'User cannot save; error text explains validation issue; Escape still cancels edit' — confirms cell stays in edit mode on validation error and user can cancel. However, network failures and conflict errors (e.g., optimistic concurrency 409) are not addressed. The onRowEdit callback's error handling path (what happens if the Promise rejects) is not specified. Only client-side validation errors are in scope. |

### Notes

The spec is genuinely comprehensive and production-quality, covering the vast majority of criteria in careful detail. It excels at the props API, toolbar lifecycle, responsive breakpoints, and animation tables. The main recurring gaps are: (1) no table-level data-fetch error state (isError prop / error rendering) — only inline-edit validation errors are covered; (2) arrow key cell traversal and Cmd/Ctrl+A select-all are absent from the keyboard spec; (3) the pagination-vs-infinite-scroll trade-off discussion is entirely missing; (4) several specific ARIA attributes (role='gridcell', aria-rowselected, aria-busy) are not called out; and (5) the edit+sort conflict scenario (what happens when a user triggers sort while a row is in edit mode) is unaddressed. Despite these gaps, the spec's breadth and structure place it well above the PASS threshold.
