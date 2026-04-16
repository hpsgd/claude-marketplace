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
