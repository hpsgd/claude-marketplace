# Output: isc request decomposition with negatives

**Verdict:** PARTIAL
**Score:** 14/15 criteria met (93%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Step 1 extracts all five categories — met: Step 1 of SKILL.md defines exactly five mandatory categories (explicit wants, implied wants, explicit not-wanted, implied not-wanted, gotchas) with clear labels and descriptions
- [x] PASS: Explicit not-wanted items appear as separate ISC criteria — met: Splitting Test ("Independent failure test") and the example (ISC-3: no references to Chris; ISC-4: no changes to other files) show anti-criteria become standalone verifiable items
- [x] PASS: Splitting Test applied to compound criteria — met: Step 3 defines four named triggers and states "Apply to EVERY criterion"; the And/With trigger directly applies to "accept JPEG and PNG" → two separate criteria
- [x] PASS: Each criterion stated as verifiable with tool and expected observation — met: Step 5 format template is `- [ ] ISC-N: [atomic criterion] — verify: [tool] → [expected observation]`; this embeds the verification command in every criterion line by construction
- [x] PASS: Effort level assigned and ISC count meets floor before execution — met: Step 2 defines effort tiers with ISC ranges; Step 4 (ISC Count Gate) gates execution on meeting the floor for the assigned tier
- [x] PASS: ISC count gate enforced with explicit re-decompose instruction — met: Step 4 states "Below floor = re-decompose. You're grouping things that should be separate." Unambiguous; not advisory
- [x] PASS: Criteria presented as numbered checklist with checkboxes — met: Step 5 defines the `- [ ] ISC-N:` format and instructs marking immediately during execution; the example confirms the pattern
- [~] PARTIAL: Domain-specific decomposition applied — partially met: Step 3 provides domain-specific guidance (UI/Visual by element/state, Data/API by validation rule/error case) but the language is advisory ("Split differently depending on what you're working on"); no gate enforces it was applied, unlike the ISC Count Gate

### Output expectations

- [x] PASS: Explicit-wants list splits correctly per Splitting Test — met: the And/With trigger is mandatory and directly produces separate JPEG criterion and PNG criterion; the skill structure guarantees this split for "accept JPEG and PNG"
- [x] PASS: Explicit-not-wanted items framed as anti-criteria with verification method — met: the example shows the pattern (ISC-3: grep returns no matches; ISC-4: git diff shows only README.md); Step 6 requires tool evidence; a correctly-following agent produces `git diff -- src/profile/password*` → no changes and `npm ls --depth=0` → no new packages
- [x] PASS: Criteria each name a verification method embedded in the criterion line — met: Step 5 Output Format section defines `— verify: [tool] → [expected observation]` as a required field in every criterion line, not a post-hoc addition
- [x] PASS: Output assigns effort level and ISC count meets the floor — met: Steps 2 and 4 structurally enforce this; effort must be declared, floor must be met, or the skill instructs re-decomposition
- [x] PASS: Count gate enforced — met: Step 4 is an explicit re-decompose gate; "below floor = re-decompose" is unambiguous
- [x] PASS: Criteria presented as numbered checklist with `[ ]` checkboxes — met: Step 5 format is unambiguous and the example confirms it
- [~] PARTIAL: Resize requirement addressed specifically — aspect ratio handling, library choice, non-square inputs — partially met: Step 1's "Gotchas" category and the Logic/Flow domain guidance ("one per branch, per boundary condition") would lead an agent toward these edge cases, but the skill does not surface resize specifics; an agent could treat "resize to 200x200" as a single criterion and miss aspect ratio handling entirely

## Notes

The skill definition is mechanically sound. The five-category extraction, Splitting Test, ISC Count Gate, and the per-criterion verification format are all defined as enforceable steps with clear failure actions. The Step 5 Output Format template explicitly requires `— verify: [tool] → [expected observation]` on every line, which means the verification method is structurally guaranteed in the output — not deferred to a post-execution Step 6 pass.

The two remaining gaps are both advisory rather than structural. Domain-specific decomposition is guidance without a gate, so a coarse-but-numerically-sufficient decomposition passes. Resize edge cases (aspect ratio, library selection, non-square input handling) are reachable via Gotchas and Logic/Flow guidance but are not surfaced explicitly — an agent may or may not reach them.
