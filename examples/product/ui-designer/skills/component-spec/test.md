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

## Output expectations

- [ ] PASS: Output's design-system decision (Reuse / Extend / Create) is made up front with reasoning — likely Create because file-upload with drag-and-drop has no existing primitive, or Extend if there's a base Input/Box to build from
- [ ] PASS: Output documents all 8 interaction states for the file upload — Default (drop zone visible), Hover (hover over the zone), Focus (keyboard focus on the click-to-browse), Active (currently dragging file over), Disabled (uploads not currently allowed), Loading (upload in progress with progress bar), Error (invalid file type / size), Empty (no files added yet)
- [ ] PASS: Output's ARIA / keyboard spec covers — `role="region"` with `aria-label="File upload"`, the drop zone is keyboard-activatable (Enter/Space triggers file picker), live region announces "Uploading X.pdf..." and completion / error
- [ ] PASS: Output addresses drag-and-drop AND click-to-browse — drag accepts files dropped over the zone, click-to-browse opens the OS file picker; both lead to the same upload flow
- [ ] PASS: Output specifies invalid-file-type error handling — visible error message stating which file types ARE accepted (e.g. "Only .pdf and .docx files are supported. The file you tried to upload is .xlsx"), file rejection without form interruption
- [ ] PASS: Output specifies file-size error handling — max size threshold visible in the empty state, error if exceeded with the specific file size shown
- [ ] PASS: Output's progress indicator is animated with explicit transition — appears on upload start, updates with progress %, transitions to success or error state
- [ ] PASS: Output's responsive behaviour describes the component at desktop (full-width drop zone) AND mobile (smaller drop zone, single-column, tap-to-browse takes priority over drag since drag is awkward on touch)
- [ ] PASS: Output's properties / variants table documents configurable aspects — accepted file types, max size, multiple-files vs single-file, optional vs required, custom error messages
- [ ] PARTIAL: Output references design tokens by name — `color-border-default`, `spacing-md`, `radius-lg` — for every visual property, not just hex codes
