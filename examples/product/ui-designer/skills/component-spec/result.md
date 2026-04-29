# Output: Component spec

| | |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/18 criteria met (94.4%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill requires all 8 interaction states: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty — Section 4 lists all 8 in the coverage table, plus Selected and Read-only. The rules beneath mandate Hover, Focus, Active, and Disabled with "No exceptions."

- [x] PASS: Skill requires ARIA roles, labels, and keyboard navigation as mandatory — Section 6 opens with "Every component must meet WCAG 2.1 AA" and contains named sub-sections for keyboard navigation, screen reader (role, label, state announcements, description), colour and contrast, and focus management. None are optional or deferred.

- [x] PASS: Skill requires a design system decision (Reuse / Extend / Create) with justification before specifying the component — Section 0 is labelled "MANDATORY — before writing the spec." It requires an explicit decision statement with justification and specifies that a Reuse decision terminates the spec immediately.

- [x] PASS: Skill requires responsive behaviour specification — Section 5 mandates a breakpoint table covering Mobile (< 640px), Tablet (640–1024px), and Desktop (> 1024px) with layout changes and content changes for each. Touch target minimums and no-horizontal-scroll rules are explicit.

- [x] PASS: Skill requires a properties/variants table documenting all configurable aspects of the component — Section 2 requires a props table with type, default, required, and description columns for every prop. Section 3 requires a variants table with visual treatment, semantic meaning, and when-to-use guidance.

- [x] PASS: Skill requires animation and transition specifications where state changes occur — Section 8 mandates what animates, duration, easing function, `prefers-reduced-motion` handling, and entry/exit animations for appearing components. Maximum duration limits are prescribed (300ms micro-interactions).

- [~] PARTIAL: Skill requires token references for colours, spacing, and typography — Section 7 (Dark Mode) explicitly requires "All colours use semantic tokens, not hardcoded values." Colour tokens are a named mandatory requirement. Spacing and typography tokens are never mentioned anywhere in the skill.

- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — frontmatter at lines 1–7 contains `name: component-spec`, `description: Write a comprehensive component specification…`, and `argument-hint: "[component name or description]"`.

### Output expectations

- [x] PASS: Output's design-system decision is made up front with reasoning — Section 0 is mandatory before any spec content and requires a stated decision plus justification. For a file-upload with drag-and-drop, the skill's example even anticipates this exact case: the sample justification references a `FileInput` component lacking drag-and-drop, pointing to a Create decision.

- [x] PASS: Output documents all 8 interaction states for the file upload — Section 4 mandates the complete coverage table for every state and instructs authors to mark N/A rather than omit. All 8 states would be filled out; drag-over would be captured under Active or as a compound state, and progress would appear under Loading.

- [x] PASS: Output's ARIA / keyboard spec covers role, keyboard activation, and live region announcements — Section 6 mandates `role`, `aria-label`/`aria-labelledby`, `aria-live`/state announcements, and keyboard navigation table including Enter/Space activation and Escape. The skill's template covers every element needed for a file-upload component.

- [x] PASS: Output addresses drag-and-drop AND click-to-browse — Section 1 (Purpose) requires documenting what the component does and when to use it; the prompt explicitly names both interaction modes. Section 4 states table would distinguish drag-over (Active sub-state) from click-to-browse (Focus/Active via keyboard). The skill's compound-state and sub-component guidance supports this.

- [x] PASS: Output specifies invalid-file-type error handling — Section 4 mandates the Error state including "show error message, offer recovery action." Section 2 (Props) requires documenting all props including accepted file types. Together these drive a spec that names the error message content and what types are accepted.

- [x] PASS: Output specifies file-size error handling — Section 4's Error state and Section 2's Props table (which must document a max-size prop) together require this. The Empty state also guides showing constraints upfront.

- [x] PASS: Output's progress indicator is animated with explicit transition — Section 8 mandates animation specifications for every state change, including entry/exit for appearing components, duration, and easing. The Loading state in Section 4 requires "transitions to Default, Error."

- [x] PASS: Output's responsive behaviour describes the component at desktop and mobile — Section 5 mandates all three breakpoints (Mobile < 640px, Tablet, Desktop) with layout and content changes. The 44x44px touch-target rule explicitly targets mobile interaction.

- [x] PASS: Output's properties/variants table documents configurable aspects — Section 2 requires every prop documented with type, default, required, and description. Accepted file types, max size, multiple vs single, optional vs required, and custom error messages would all be documented as props.

- [~] PARTIAL: Output references design tokens by name — Section 7 requires semantic tokens for colour only. The skill does not instruct the author to reference spacing or typography tokens by name. An output following this skill would name colour tokens but likely use hardcoded values or leave spacing/typography tokens unspecified. Partial credit: colour tokens would be present, spacing and typography tokens would not.

## Notes

The skill is structurally strong. Section 0's mandatory gate before any spec content is the most important structural feature — it prevents spec proliferation by requiring a documented search and decision before work begins. The sample justification in that section uses a file-upload example directly, which means this test case is well-aligned with what the skill author intended.

The one consistent gap across both criteria and output sections is the token reference scope. The dark mode checklist names colour tokens but the skill never mentions spacing or typography tokens. For a file-upload component with a drag-over zone, progress bar, and error message typography, those missing token references are not trivial.

The `Related Skills` footer connecting to `/ui-designer:design-review` and `/ui-designer:accessibility-audit` is good practice — it situates the spec step inside a broader verification workflow.
