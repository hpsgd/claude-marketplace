# Test: component-spec — complex interactive component

Scenario: Testing the component-spec skill with a high-complexity component that combines multiple interaction patterns (sorting, selection, inline editing, pagination, bulk actions) into a single data table.

## Prompt

/ui-designer:component-spec for a data table component with sortable columns, multi-row selection, inline editing, pagination, and a bulk actions toolbar that appears when rows are selected.

## Criteria

- [ ] PASS: All interaction states are enumerated — empty, loading, loaded, error, and every combination of selection + editing + sorting
- [ ] PASS: Keyboard navigation is specified for all interactive elements (sort headers, checkboxes, inline edit fields, pagination)
- [ ] PASS: The bulk actions toolbar specifies its own states (hidden, visible, count display) and transitions
- [ ] PASS: Inline editing specifies entry/exit behaviour (click to edit, escape to cancel, enter/blur to save, validation errors)
- [ ] PASS: Responsive behaviour is addressed — what happens to columns, pagination, and bulk actions on mobile
- [ ] PARTIAL: Performance considerations are noted for large datasets (virtualisation, pagination vs infinite scroll)
- [ ] PASS: Accessibility requirements include ARIA roles for the table, row selection announcements, and focus management during inline edit
- [ ] PASS: Props API is defined with types, defaults, and required/optional status for each prop

## Output expectations

- [ ] PASS: Output enumerates state combinations — empty, loading, loaded, error are the 4 base data states; each combines with selection state (no selection / partial selection / all selected) and editing state (no edit / row in edit mode) for ~16 distinct visual states; the spec covers these systematically not abstractly
- [ ] PASS: Output's keyboard navigation specification covers — arrow keys for cell traversal, Tab between focusable interactive elements, Space to toggle selection, Enter to enter edit mode, Esc to cancel edit, Enter to commit edit, Cmd/Ctrl+A for select-all
- [ ] PASS: Output's bulk-actions toolbar specifies its lifecycle — appears (slide / fade) when first row selected, count display updates as more rows are selected, slides away when selection is cleared; positioning (sticky bottom or header overlay) is specified
- [ ] PASS: Output's inline-edit interaction is fully specified — click to edit (which click target — cell vs edit button?), Esc cancels (reverts), Enter saves, blur saves with timeout to prevent accidental commits, validation errors appear inline next to the input with revert option
- [ ] PASS: Output's responsive behaviour addresses what happens to columns at narrow widths — column priority (which columns hide first), horizontal scroll vs stacking, what happens to the bulk-actions toolbar on mobile, whether inline editing still works on touch
- [ ] PASS: Output addresses performance for large datasets — virtualisation strategy if datasets exceed pagination capacity, the threshold at which virtualisation kicks in, the trade-off between pagination (simpler, server-friendly) and infinite scroll (faster perceived, harder to bookmark)
- [ ] PASS: Output's ARIA spec covers — `role="grid"` on the table, `role="gridcell"` on cells, `aria-rowselected` for selection state, `aria-busy` during loading, live-region announcements when bulk actions complete or selections change
- [ ] PASS: Output's Props API documents each prop with type (TS), default, required vs optional, description — `data: T[]`, `columns: Column<T>[]`, `loading?: boolean`, `selectedRows?: string[]`, `onSelectionChange?: (rows: string[]) => void`, `onEdit?: (rowId, field, value) => Promise<void>`, etc.
- [ ] PASS: Output addresses sort interaction with selection and editing — what happens to row selection when a sort changes (kept by ID), what happens when a row is being edited and the user triggers a sort (warn / save / cancel)
- [ ] PARTIAL: Output addresses error recovery during inline edit — if the save fails (validation, network, conflict), the cell stays in edit mode with the error message and the user can retry or cancel without losing their input
