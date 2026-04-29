# Output: Component design

| | |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Checks the existing design system first and explicitly identifies which existing components (Input, Button, Avatar, Card) can be reused versus what needs to be created — met. Pre-Flight Step 1 mandates finding the design system, reading style guides, and searching for similar components before proposing anything. Step 2 requires a Reuse / Extend / Create decision for every UI element with justification for any Create call.

- [x] PASS: Documents all 8 required component states for the wizard: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty — met. Section 3 "States (ALL required — no exceptions)" enumerates all 8 states with behaviour and visual treatment columns. Explicit "no exceptions" language.

- [x] PASS: Specifies ARIA roles, labels, and keyboard navigation requirements — not deferred to a future accessibility pass — met. Section 5 Accessibility covers ARIA role, label, live regions, Tab/Enter/Space/Escape keyboard handling, and focus management as mandatory spec sections. The non-negotiable opening ("Accessibility is a constraint, not a feature") and a Decision Checkpoint blocking removal of accessibility requirements both reinforce non-deferral.

- [x] PASS: Addresses the step indicator / progress component as Reuse / Extend / Create with justification — met. Pre-Flight Step 2 requires a Pattern Decision for every UI element. A step indicator is a UI element; the Create justification mandate would produce the required reasoning.

- [x] PASS: Specifies responsive behaviour for both desktop and tablet breakpoints — met. Section 4 Responsive Behaviour includes a table with Mobile (<768px), Tablet (768-1024px), and Desktop (>1024px) breakpoints as mandatory spec output.

- [x] PASS: Documents the error state for each step (e.g. invalid email format in team invite, workspace name taken) — met. Error is one of the 8 mandatory states. Interaction Design's Flow Mapping also requires error paths ("what happens when things go wrong? network error, validation error, timeout, auth expired").

- [~] PARTIAL: Specifies loading states for async operations — partially met. Loading is mandatory in the 8-state table ("Skeleton or spinner, not interactive"). The definition covers loading at the component state level but does not require differentiated loading treatments per async operation within a wizard flow. An OAuth integration connection step (5-15 second roundtrip) versus a form submission (fast) would receive the same generic treatment unless the designer chose to go deeper unprompted.

- [x] PASS: Produces output in a structured component specification format with named sections, not prose — met. The Output Format section provides an explicit named template: Purpose, Pattern Decision, Props, States, Responsive, Accessibility, Usage Examples, Design Notes.

### Output expectations

- [x] PASS: Output addresses each of the 4 wizard steps explicitly — met. The Interaction Design section requires full flow mapping including entry point, happy path, error paths, empty state, and exit points. Per-step breakdown of inputs and interactions would follow from this mandate applied to a 4-step wizard.

- [x] PASS: Design-system reuse decisions are explicit per primitive — met. Pre-Flight Step 2 and the Pattern Decision output section mandate Reuse / Extend / Create per element. Input, Button, Avatar, and Card would each receive an explicit decision with reasoning.

- [x] PASS: Progress / step-indicator decided explicitly as Reuse / Extend / Create with reasoning — met. Same mechanism; every UI element requires a decision, and Create decisions require justification explaining why no existing component works.

- [x] PASS: All 8 component states documented for the wizard shell — met. The mandatory 8-state table includes the exact states needed: Disabled (next button before required fields), Loading (async integration auth), Error (validation failures), Empty (integration step before selection).

- [x] PASS: Accessibility specification covers ARIA roles, labels, and keyboard navigation — met. Section 5 requires ARIA role, label, live regions, Tab order, Enter/Space activation, Escape to close, and focus management on open/close/action.

- [x] PASS: Team-invite step email validation with error states designed — met. Error state is mandatory in the 8-state spec; Interaction Design requires error paths covering validation error. The definition explicitly lists validation error as an error path type.

- [x] PASS: Integration step "or skip" branch designed explicitly — met. Interaction Design requires exit points ("how does the user leave? What state is preserved?") and the flow mapping covers optional branches. The State Transitions diagram also models cancel paths back to idle.

- [x] PASS: Responsive behaviour for desktop AND tablet with layout reflow — met. Section 4 mandates a table with specific layout changes at Tablet (768-1024px) and Desktop (>1024px). Mobile-first rules (`flex-col lg:flex-row`) show layout reflow is an expected output.

- [x] PASS: Can-skip vs cannot-skip per step addressed — met. Interaction Design's exit points ("how does the user leave?") and the Disabled state (where required fields gate progression) together cover required vs optional step design. The "Error prevention over error handling" principle would push explicit gating decisions.

- [~] PARTIAL: Loading state for the integration step OAuth roundtrip specifically — partially met. Loading is a mandatory state. The definition covers spinner/skeleton treatments but does not prescribe specific OAuth roundtrip messaging ("Connecting to GitHub…" with a stall fallback) or time-based UX guidance. A designer following the definition would produce a loading state, but the depth and specificity of the OAuth flow handling is not guaranteed by the definition alone.

## Notes

Strong definition for this scenario. The Pre-Flight mandate, the non-negotiable 8-state table, and the Create-justification requirement directly address the rubric's most specific demands. The partial on loading state granularity is consistent with the previous evaluation — it is a substance gap rather than a structural one. The definition would produce a well-formed spec; the OAuth-specific loading detail depends on the designer's judgment rather than being mandated.

The "can-skip vs cannot-skip" criterion is covered by inference (Disabled state + exit points) rather than a named concept. The definition would produce the right behaviour but does not use that vocabulary explicitly — a minor substance note, not a gap.
