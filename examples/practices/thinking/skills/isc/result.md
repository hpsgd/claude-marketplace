# Output: isc request decomposition with negatives

**Verdict:** PARTIAL
**Score:** 13.5/18 criteria met (75%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Step 1 extracts all five categories — met: Step 1 of SKILL.md defines exactly five mandatory categories with clear labels and descriptions
- [x] PASS: Explicit not-wanted items appear as separate ISC criteria — met: Step 3's Splitting Test ("Independent failure test") and the example (ISC-3: no references to Chris with a grep command) show anti-criteria become standalone verifiable items
- [x] PASS: Splitting Test applied to compound criteria — met: Step 3 defines four named triggers and says "Apply to EVERY criterion"; Trigger 1 ("And/With test") directly applies to "accept JPEG and PNG"
- [~] PARTIAL: Each criterion stated as verifiable — includes tool and expected observation — partially met: Step 3 defines verifiability and Step 6 requires tool evidence, but the criterion format in Step 5 (`- [ ] ISC-N: [atomic criterion]`) does not mandate embedding the verification command in each line; the example embeds it for one item (ISC-3: grep command) but not for others (ISC-1, ISC-2, ISC-5), leaving the pattern inconsistent
- [x] PASS: Effort level assigned and ISC count meets floor before execution — met: Step 2 defines effort tiers; Step 4 (ISC Count Gate) gates execution on meeting the floor
- [x] PASS: ISC count gate enforced with explicit re-decompose instruction — met: Step 4 states "Below floor = re-decompose. You're grouping things that should be separate." Unambiguous
- [x] PASS: Criteria presented as numbered checklist with checkboxes — met: Step 5 defines the format and instructs marking immediately during execution
- [~] PARTIAL: Domain-specific decomposition applied — partially met: Step 3 provides domain-specific guidance (UI/Visual by element/state, Data/API by rule/error case) but the language is advisory; no gate enforces it was applied, unlike the ISC Count Gate

### Output expectations

- [x] PASS: Explicit-wants list includes avatar upload, JPEG accepted, PNG accepted, max 5MB, resize to 200x200 split per the Splitting Test — met: the Splitting Test's And/With trigger is mandatory and directly produces separate criteria for JPEG and PNG; the skill's structure guarantees this split
- [x] PASS: Explicit-not-wanted items framed as ANTI-criteria verified as false — met: the example shows the pattern (ISC-3: grep returns nothing; ISC-4: no changes to other files); the skill instructs Step 6 verification with tool evidence; an agent following this skill would frame "no password changes" as `git diff` shows nothing
- [~] PARTIAL: Implied-wants includes validation errors visible, upload progress, accessibility — partially met: Step 1's "Implied wants" category instructs extracting "what's necessary but not stated"; progress indication and error states would surface under this. Accessibility is less likely to emerge unless the agent applies it proactively — the skill does not prompt for it specifically
- [~] PARTIAL: Implied-not-wanted (gotchas) includes no regression to existing avatar functionality, no breaking unrelated tests, no client-side image processing libraries — partially met: Step 1's "Gotchas" category and "Implied not-wanted" category together cover regression and test breakage naturally; the no-new-npm-dependencies constraint combined with the resize requirement creates the library gotcha, which Step 1's "Gotchas" category is designed to surface, but the skill does not guarantee an agent reaches this specific conclusion
- [ ] FAIL: Criteria each name a verification method with tool and expected observation embedded in the criterion line — not met: the format template does not require this; Step 5 shows `- [ ] ISC-N: [atomic criterion]` without a verification field; Step 6 handles verification separately; the example only embeds a verification command in one of five criteria
- [x] PASS: Output assigns effort level and ISC count meets the floor — met: Steps 2 and 4 structurally enforce this in any output the skill produces
- [x] PASS: Count gate enforced — met: Step 4 is an explicit re-decompose gate, not advisory
- [~] PARTIAL: Domain-specific decomposition — file upload by validation rule, UI by state, tests by named file — partially met: Step 3's domain-specific guidance covers this but is advisory; an agent may apply it inconsistently; no structural gate ensures it was done
- [x] PASS: Criteria presented as numbered checklist with `[ ]` checkboxes — met: Step 5 format is unambiguous and the example confirms it
- [~] PARTIAL: Resize requirement addressed specifically — aspect ratio, library, non-square inputs — partially met: Step 1's "Gotchas" category and the Logic/Flow domain guidance ("one per branch, per boundary condition") would lead an agent toward these, but the skill does not surface resize edge cases explicitly; an agent could treat "resize to 200x200" as a single criterion and miss aspect ratio handling

## Notes

The skill definition is mechanically sound. The five-category extraction, Splitting Test, and ISC Count Gate are all defined as enforceable steps with clear failure actions. The primary structural gap is the criterion format: the template does not mandate embedding a verification command within each criterion line. Step 6 defers verification to a separate post-execution pass, which means the ISC checklist may not contain tool references inline. The output expectations section specifically requires verification embedded per criterion, and the skill does not structurally guarantee this.

Domain-specific decomposition is the other weak point — it is guidance, not a gate. The skill's advisory framing ("Split differently depending on what you're working on") means an agent that does coarse decomposition will still pass the ISC Count Gate if the raw count is high enough.

The 75% score meets the PARTIAL threshold.
