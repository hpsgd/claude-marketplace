# Output: Design tokens

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 16.5/17 criteria met (97%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: Skill distinguishes between primitive tokens and semantic tokens as separate layers — met: Step 2 defines primitives ("named by what they are, not what they do"); Step 3 defines semantic tokens ("map primitives to purposes"); components required to consume semantic tokens only
- [x] PASS: Skill requires an inventory step — met: Step 1 is dedicated entirely to scanning and cataloguing existing values before any token definition begins, producing a grouped table
- [x] PASS: Skill requires contrast ratio validation against WCAG AA thresholds — met: Step 4 contrast validation table specifies 4.5:1 for normal text and 3:1 for large text/UI; Rules section calls contrast "mandatory, not aspirational"
- [x] PASS: Skill requires token documentation specifying intended use case — met: every token table includes a Usage column; Step 5 template explicitly requires usage guidance
- [x] PASS: Skill covers colour, typography, and spacing at minimum — met: all three defined in Step 2; also radius, shadow, and motion
- [x] PARTIAL: Skill specifies a naming convention — fully met: `[category].[property].[variant].[state]` is explicitly stated and called "non-negotiable" in the Rules section, with consistent examples throughout. Ceiling set by criterion type; criterion is fully satisfied.
- [x] PASS: Skill produces output usable by both designers and developers — met: Step 5 requires Figma Variables/Tokens plugin JSON AND Style Dictionary for CSS custom properties; closing paragraph explicitly prohibits developer-only output
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint — met: all three fields present at lines 1-7

### Output expectations

- [x] PASS: Output inventory step lists existing hardcoded values from Figma + CSS — met: Step 1 scans CSS custom properties, Tailwind config, hardcoded hex values, and theme files; catalogues into a table by colour, spacing, typography with inconsistency flags
- [x] PASS: Output structures tokens in two layers with explanation — met: Step 2 (primitives) and Step 3 (semantic) are distinct steps; semantic tokens reference primitives by name; skill explains why components consume semantic tokens never primitives
- [x] PASS: Output colour tokens include contrast-ratio validation with actual ratios shown — met: Step 4 table has columns for ratio required, actual ratio, and pass/fail for each text/background pair
- [x] PASS: Output covers colour, typography, spacing, and ideally radius, shadow, motion — met: all six categories covered in Step 2
- [x] PASS: Output token names follow a consistent stated convention — met: `[category].[property].[variant].[state]` stated explicitly, applied consistently across all examples
- [x] PASS: Output documentation per token includes intended use case — met: every token table has a Usage column with specific guidance
- [x] PASS: Output is dual-format for Figma and code — met: Step 5 explicitly covers Figma Tokens plugin JSON / Figma Variables AND Style Dictionary for CSS custom properties and SCSS variables
- [x] PASS: Output addresses dark mode / theming — met: semantic token tables include light and dark mode columns in Step 3; dark mode parity check required in Step 4; Rules section states "no mode may be an afterthought"
- [x] PASS: Output migration plan — met: Step 5 documentation template includes a Migration Guide section; Step 4 coverage check tracks replacement of hardcoded values
- [~] PARTIAL: Output addresses tokens for state changes — partially met: hover, active, and focus states are explicitly defined as semantic tokens (`color.interactive.hover`, `color.interactive.active`, `color.border.focus`); disabled state appears in the Step 4 coverage checklist but is not defined as a named semantic token in Step 3 (only `color.text.disabled` is defined; `color.interactive.disabled` is absent from the table)

## Notes

Strong skill definition. The two-layer architecture is enforced as a hard rule rather than a recommendation. Dark mode is a first-class concern throughout. The Step 4 coverage check extends beyond contrast validation to verify all existing hardcoded values are accounted for — a practical migration guard often omitted in token skill definitions.

The token versioning rule (treat value changes as breaking, use semver) is practical and uncommon in skill definitions at this level.

The one genuine gap: `color.interactive.disabled` as a named semantic token is absent from Step 3's colour semantics table, though the coverage checklist in Step 4 asks evaluators to check for it. A designer following the skill could miss defining it while still passing the coverage check by noting "gaps" rather than resolving them.
