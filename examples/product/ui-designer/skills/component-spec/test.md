# Test: Component spec

Scenario: Testing whether the component-spec skill definition requires all 8 interaction states, accessibility requirements, and responsive behaviour as mandatory sections.

## Prompt


/ui-designer:component-spec for a file upload component that supports drag-and-drop and click-to-browse, with progress indicator and error handling for invalid file types.

## Criteria


- [ ] PASS: Skill requires all 8 interaction states: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty
- [ ] PASS: Skill requires ARIA roles, labels, and keyboard navigation as mandatory — not optional or deferred
- [ ] PASS: Skill requires a design system decision (Reuse / Extend / Create) with justification before specifying the component
- [ ] PASS: Skill requires responsive behaviour specification — the component must be described at multiple breakpoints
- [ ] PASS: Skill requires a properties/variants table documenting all configurable aspects of the component
- [ ] PASS: Skill requires animation and transition specifications where state changes occur (e.g. drag-over highlight, upload progress)
- [ ] PARTIAL: Skill requires token references for colours, spacing, and typography — partial credit if tokens are mentioned but not required to be referenced by name
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields
