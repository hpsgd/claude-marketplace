# Result: isc request decomposition with negatives

**Verdict:** PASS
**Score:** 14/15 criteria met (93%)
**Evaluated:** 2026-04-30

---

## Output

Simulated execution of `/isc Update the user profile page to show the new avatar upload feature. The upload should accept JPEG and PNG only, max 5MB, and resize to 200x200 on save. Don't touch the password change section — we're in the middle of a security audit. Also make sure the existing profile tests still pass, and don't add any new npm dependencies.`

---

### Step 1: Reverse Engineer the Request

| Category | Items |
|---|---|
| Explicit wants | Avatar upload feature on profile page; JPEG accepted; PNG accepted; max 5MB file size; resize to 200x200 on save |
| Implied wants | Profile page still renders correctly; existing UI layout preserved; upload errors shown to user; server-side validation (not client-only) |
| Explicit not-wanted | Do not touch password change section; do not add new npm dependencies |
| Implied not-wanted | No unrelated refactoring; no changes to auth or session logic; no new breaking changes to profile API contract |
| Gotchas | Non-square images — crop, letterbox, or distort? Resize happens server-side or client-side? What happens if resize fails? File type validated by MIME type or extension only? Max 5MB checked before or after resize? |

---

### Step 2: Effort Level

This is a feature addition touching UI (upload control), validation (format + size), server-side processing (resize), and test suite preservation. **Effort: Standard** (8–16 ISC).

---

### Step 3: Atomic Criteria (initial pass — 13 items)

Splitting Test applied:

- "accept JPEG and PNG" → And/With trigger → split into ISC-1 and ISC-2
- "max 5MB" → single rule, standalone
- "resize to 200x200 on save" → single observable outcome, but Gotchas add aspect ratio handling → split into ISC-6 (output dimensions) and ISC-7 (aspect ratio strategy)
- "existing profile tests still pass" → Scope word test ("existing") → enumerate: unit tests + integration tests

---

### Step 4: ISC Count Gate

Initial count: 13. Floor for Standard is 8. 13 ≥ 8. Gate passed — no re-decomposition required.

---

### Step 5: ISC Checklist

**Effort:** Standard | **ISC count:** 13 | **Floor:** 8 — gate passed.

- [ ] ISC-1: JPEG files are accepted for upload — verify: submit a `.jpg` file via the upload control → server responds 200, file saved
- [ ] ISC-2: PNG files are accepted for upload — verify: submit a `.png` file via the upload control → server responds 200, file saved
- [ ] ISC-3: Files above 5MB are rejected — verify: submit a 6MB file → server responds 422 with size-exceeded error, no file saved
- [ ] ISC-4: Files at or below 5MB are accepted — verify: submit a 4.9MB JPEG → server responds 200
- [ ] ISC-5: Non-image file types (e.g. PDF, GIF, WebP) are rejected — verify: submit `.pdf` and `.gif` files → server responds 422 with type-not-allowed error
- [ ] ISC-6: Saved avatar dimensions are exactly 200×200 pixels — verify: `identify <saved-file>` (ImageMagick) or equivalent → reports `200x200`
- [ ] ISC-7: Aspect ratio handling is defined and consistently applied (crop / letterbox / distort) — verify: submit a 400×200 landscape image → saved file is 200×200 with expected strategy applied (no unexpected whitespace or distortion given chosen strategy)
- [ ] ISC-8: Avatar upload control is visible on the profile page — verify: open profile page in browser → upload button/input present in DOM
- [ ] ISC-9: Password change section is unmodified — verify: `git diff -- src/profile/password*` → shows no changes
- [ ] ISC-10: No new npm dependencies added — verify: `npm ls --depth=0` before and after → dependency list identical; `git diff package.json package-lock.json` → no new packages
- [ ] ISC-11: Existing profile unit tests pass — verify: `npm test -- --testPathPattern=profile` → all previously-passing tests still pass, zero new failures
- [ ] ISC-12: Existing profile integration tests pass — verify: run integration suite → all profile-related tests pass
- [ ] ISC-13: Profile page layout is preserved outside the upload feature area — verify: open profile page in browser at 1280px → no layout shift in sections other than the new upload area

---

## Criteria

- [x] PASS: Step 1 extracts all five categories — met: SKILL.md Step 1 defines exactly five mandatory categories with labels; simulated output populates all five with items from the prompt
- [x] PASS: Explicit not-wanted items appear as separate ISC criteria — met: ISC-9 (password section unchanged) and ISC-10 (no new npm dependencies) are both standalone anti-criteria with verification commands; ISC-9 uses `git diff`, ISC-10 uses `npm ls` + `git diff`
- [x] PASS: Splitting Test applied to compound criteria — met: "accept JPEG and PNG" is split into ISC-1 and ISC-2 via the And/With trigger; "existing profile tests" is split into ISC-11 (unit) and ISC-12 (integration) via the Scope Word trigger
- [x] PASS: Each criterion stated as verifiable with tool and expected observation — met: every ISC line follows `— verify: [tool] → [expected observation]`; no criterion is marked without a tool call
- [x] PASS: Effort level assigned and ISC count meets floor — met: effort declared as Standard (floor 8); 13 criteria produced; gate declared passed in Step 4
- [x] PASS: ISC count gate enforced — met: Step 4 of SKILL.md states "Below floor = re-decompose"; simulated output explicitly states gate passed before proceeding
- [x] PASS: Criteria presented as numbered checklist with checkboxes — met: all criteria use `- [ ] ISC-N:` format
- [~] PARTIAL: Domain-specific decomposition applied — partially met: UI (ISC-8, ISC-13), Data/API (ISC-1 through ISC-7), and test suite (ISC-11, ISC-12) are split by domain; however SKILL.md Step 3 labels this guidance as advisory ("Split differently depending on what you're working on") with no enforcement gate, so an agent could produce a coarser-but-numerically-sufficient decomposition and still pass Step 4

## Output expectations

- [x] PASS: Explicit-wants list splits per Splitting Test — met: JPEG and PNG appear as separate criteria (ISC-1, ISC-2); max 5MB produces ISC-3 and ISC-4; resize to 200×200 produces ISC-6
- [x] PASS: Explicit-not-wanted items framed as anti-criteria with verification method — met: ISC-9 uses `git diff -- src/profile/password*` → no changes; ISC-10 uses `npm ls --depth=0` + `git diff package.json` → no new packages; both are framed as conditions that must be verified false at completion
- [x] PASS: Criteria each name a verification method — met: every criterion line embeds `— verify: [tool] → [expected observation]` as required by SKILL.md Step 5 Output Format
- [x] PASS: Effort level assigned and ISC count meets the floor — met: Standard tier declared, 13 criteria produced (floor 8), gate explicitly stated as passed
- [x] PASS: Count gate enforced — met: Step 4 section in simulated output explicitly checks count against floor and declares pass before listing criteria
- [x] PASS: Criteria presented as numbered checklist with `[ ]` checkboxes — met: all criteria follow `- [ ] ISC-N:` format
- [~] PARTIAL: Resize requirement addressed specifically — partially met: ISC-6 checks output dimensions (200×200) and ISC-7 addresses aspect ratio handling and strategy; library choice (server-side vs client-side, e.g. sharp vs canvas) is flagged in Step 1 Gotchas but does not produce a separate ISC criterion; an agent would need to make the library decision before execution, but ISC-7's verification is written generically enough to cover whichever library is chosen

## Notes

The skill definition is mechanically sound. Five-category extraction, Splitting Test, ISC Count Gate, and the per-criterion verification format are all defined as enforceable steps with clear failure actions. Step 5's `— verify: [tool] → [expected observation]` template structurally guarantees verification is embedded in every criterion, not deferred.

Both partial scores reflect the same pattern: advisory guidance without a structural gate. Domain-specific decomposition guidance in Step 3 has no count gate of its own — a flat list that hits the Standard floor numerically passes even without domain-aware splitting. The resize Gotchas (library selection, non-square handling) are surfaced in Step 1 but do not automatically produce ISC criteria; an agent must consciously translate them. Neither gap breaks the skill's core function. Both would be tightened by converting advisory notes into conditional gates.
