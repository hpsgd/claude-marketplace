# Isc

Scenario: A developer asks for help with a task that has multiple components, explicit exclusions, and implied requirements. The ISC skill must catch all parts including the anti-criteria.

## Prompt

> /isc Update the user profile page to show the new avatar upload feature. The upload should accept JPEG and PNG only, max 5MB, and resize to 200x200 on save. Don't touch the password change section — we're in the middle of a security audit. Also make sure the existing profile tests still pass, and don't add any new npm dependencies.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll decompose this request into Identifiable, Specific, Verifiable Criteria using ISC.

## Reverse Engineer the Request

**Explicit wants:**
- Avatar upload feature on profile page
- Accept JPEG/PNG only, max 5MB
- Resize to 200x200 on save
- Existing tests pass
- No new npm dependencies

**Explicit not-wanted:**
- Don't modify password change section

**Implied wants:**
- File validation (client and server)
- Avatar storage and retrieval
- Avatar display on profile
- Error handling for invalid uploads

**Implied not-wanted:**
- No changes to unrelated profile functionality
- No breaking changes

## Effort Level

**Standard → Extended** (16-24 criteria). Avatar upload has UI, validation, processing, storage, and testing layers.

---

## ISC Checklist

**UI Layer:**
- [ ] **ISC-1**: Avatar upload form element present on profile page — verify: `grep -n "file" [profile-component.tsx]` → file input element exists
- [ ] **ISC-2**: File input accept attribute restricts to JPEG/PNG — verify: `grep "accept=" [profile-component.tsx]` → contains `image/jpeg,image/png`
- [ ] **ISC-3**: File size validation error message present in UI — verify: `grep -i "5mb\|size" [profile-component.tsx]` → error message text exists
- [ ] **ISC-4**: File type validation error message present in UI — verify: `grep -i "jpeg\|png\|format" [profile-component.tsx]` → error message text exists
- [ ] **ISC-5**: Avatar preview/current avatar displays — verify: visual test or component render test passes

**Client-Side Validation:**
- [ ] **ISC-6**: File >5MB rejected before submission — verify: run unit test: upload 6MB file → shows error, button disabled
- [ ] **ISC-7**: Non-image file rejected before submission — verify: run unit test: upload .txt file → shows error, button disabled

**Server-Side Validation:**
- [ ] **ISC-8**: POST with >5MB file returns 400/413 — verify: run integration test → response status 400 or 413
- [ ] **ISC-9**: POST with non-JPEG/PNG file returns 400 — verify: run integration test: POST .gif → 400 error
- [ ] **ISC-10**: Server validates actual file magic bytes, not extension — verify: code review of upload handler → checks magic bytes or uses image library validation

**Image Processing & Storage:**
- [ ] **ISC-11**: Uploaded image resized to exactly 200x200 pixels — verify: read saved image file → check dimensions with `identify` or image library
- [ ] **ISC-12**: Avatar persisted in storage (filesystem or DB) — verify: check storage location → file/record exists
- [ ] **ISC-13**: User profile record updated with avatar path/URL — verify: query user record → avatar field populated

**Display & Integration:**
- [ ] **ISC-14**: Avatar displays on profile page after upload — verify: navigate to profile → avatar renders
- [ ] **ISC-15**: Avatar displays at correct size — verify: inspect element → width/height 200px or style verified
- [ ] **ISC-16**: Password change section unmodified — verify: `git diff` → password section has no changes
- [ ] **ISC-17**: Existing profile fields work (name, email, etc.) — verify: manual test or existing tests → profile crud works
- [ ] **ISC-18**: All existing profile tests pass — verify: `npm test` or `npm test -- profile` → all tests green
- [ ] **ISC-19**: No new npm dependencies added — verify: `git diff package.json` → no new entries in dependencies
- [ ] **ISC-20**: Only profile-related files modified — verify: `git status` → no unrelated files staged/modified

---

Ready to proceed with implementation once you confirm this decomposition captures the full scope.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 12.5/14.0 (89%) |
| Evaluated | 2026-05-04 |
| Target duration | 23248 ms |
| Target cost | $0.0469 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 extracts all five categories — explicit wants, implied wants, explicit not-wanted, implied not-wanted, and gotchas | PARTIAL | The output's 'Reverse Engineer the Request' section contains four of five categories: 'Explicit wants', 'Explicit not-wanted', 'Implied wants', and 'Implied not-wanted'. There is no 'Gotchas' category. Four of five is partial coverage. |
| c2 | Explicit not-wanted items (don't touch password section, no new npm dependencies) appear as separate ISC criteria | PASS | ISC-16 ('Password change section unmodified — verify: `git diff` → password section has no changes') and ISC-19 ('No new npm dependencies added — verify: `git diff package.json` → no new entries in dependencies') are both present as distinct numbered checklist items. |
| c3 | The Splitting Test is applied — compound criteria like "accept JPEG and PNG" become separate verifiable items | FAIL | ISC-2 reads 'File input accept attribute restricts to JPEG/PNG' — both formats are combined in a single criterion. ISC-9 tests a non-image file (.gif) but there are no separate 'JPEG accepted' and 'PNG accepted' ISC items anywhere in the checklist. The prime example cited in the criterion is not split. |
| c4 | Each criterion is stated as verifiable — includes what tool would confirm it and what you'd see | PASS | Every ISC item includes a 'verify:' clause with a tool and expected output. Examples: ISC-1 'verify: `grep -n "file" [profile-component.tsx]` → file input element exists'; ISC-11 'verify: read saved image file → check dimensions with `identify` or image library'; ISC-19 'verify: `git diff package.json` → no new entries in dependencies'. ISC-5 is slightly vague ('visual test or component render test passes') but acceptable. |
| c5 | Effort level is assigned and the ISC count meets the floor for that tier before execution begins | PASS | The output explicitly states 'Standard → Extended (16-24 criteria)' as the effort level. The checklist contains ISC-1 through ISC-20, totalling 20 criteria, which exceeds the stated floor of 16 for the Extended tier. |
| c6 | ISC count gate is enforced — if below floor, skill explicitly states the criterion count is insufficient and decomposes further | PASS | The count gate is implicitly satisfied: the output declares the 'Extended' tier with a floor of 16 and produces 20 criteria, so the gate does not need to trigger. The criterion is vacuously met — there is no shortfall to report. The tier assignment and count are explicitly stated together, fulfilling the gate logic. |
| c7 | Criteria are presented as a numbered checklist with checkboxes, ready to be marked during execution | PASS | All 20 criteria use the `- [ ] **ISC-N**:` format with checkboxes, consistently from ISC-1 through ISC-20, grouped under section headers. |
| c8 | Domain-specific decomposition is applied — UI criteria split by element/state, validation criteria split by rule | PARTIAL | The output is grouped into five domains (UI Layer, Client-Side Validation, Server-Side Validation, Image Processing & Storage, Display & Integration). Within validation, client-side size and type checks are separate from server-side equivalents. However, JPEG and PNG are not split as separate verifiable items, and ISC-5 (avatar preview/display) does not distinguish between upload-time preview and post-save display. Partial domain decomposition is present but not comprehensive. |
| c9 | Output's explicit-wants list includes avatar upload, JPEG and PNG accepted, max 5MB, resize to 200x200 on save — split where the Splitting Test demands ("JPEG accepted" and "PNG accepted" as separate verifiable items, not "both formats accepted") | PARTIAL | The explicit-wants list contains all four items: avatar upload feature, 'Accept JPEG/PNG only, max 5MB', resize to 200x200, and existing tests. However, JPEG and PNG are not split into separate ISC criteria — ISC-2 reads 'File input accept attribute restricts to JPEG/PNG' and no separate ISC items exist for each format. The list is present but the required split is absent. |
| c10 | Output's explicit-not-wanted list includes "do not modify password change section" and "no new npm dependencies" as separate ISC criteria — and these are framed as ANTI-criteria that must be verified false at completion (e.g. `git diff` shows no changes to password section) | PASS | ISC-16: 'Password change section unmodified — verify: `git diff` → password section has no changes'; ISC-19: 'No new npm dependencies added — verify: `git diff package.json` → no new entries in dependencies'. Both are framed as states to confirm absent/unchanged at completion, matching the anti-criteria pattern. |
| c11 | Output's criteria each name a verification method — e.g. "Tool: open profile page in browser → see new upload button" or "Tool: `git diff -- src/profile/password*` → shows no changes" or "Tool: `npm ls --depth=0` → no new package added" | PASS | Every criterion includes a 'verify:' clause specifying a tool and expected observable result: ISC-6 'run unit test: upload 6MB file → shows error, button disabled'; ISC-8 'run integration test → response status 400 or 413'; ISC-19 'verify: `git diff package.json` → no new entries'. The format consistently names how and what to observe. |
| c12 | Output assigns an effort level (likely Small or Medium given file upload + validation + resize + tests) and the resulting ISC criterion count meets the floor for that tier — explicitly stated | PASS | Output states 'Standard → Extended (16-24 criteria)' as effort level. 20 criteria are produced, meeting the stated floor of 16. The tier and count range are explicitly stated before the checklist begins. |
| c13 | Output enforces the count gate — if the initial decomposition is below the floor, the skill states the count is insufficient and decomposes further (e.g. splitting "validation" into per-rule items) | PASS | 20 criteria are produced against a floor of 16 for the Extended tier. The gate condition (below floor) is not triggered. The decomposition includes per-rule splits for validation (ISC-6/7 client-side size/type, ISC-8/9/10 server-side equivalents), demonstrating the gate-avoidance logic through adequate depth. |
| c14 | Output presents criteria as a numbered checklist with `[ ]` checkboxes, ready to be marked during execution | PASS | All 20 ISC items use `- [ ] **ISC-N**:` format with unchecked checkboxes, consistently formatted and ready for in-place marking during execution. |
| c15 | Output addresses the resize requirement specifically — what aspect ratio handling (crop, letterbox, distort), what library performs the resize (server-side vs client-side), what happens to non-square inputs | PARTIAL | ISC-11 ('Uploaded image resized to exactly 200x200 pixels — verify: read saved image file → check dimensions with `identify` or image library') mentions resizing and verification, but does not address aspect ratio handling strategy (crop vs letterbox vs distort), no specific library is named, and no ISC item covers what happens to non-square inputs. Resize is acknowledged but not decomposed. |

### Notes

The output is a strong ISC decomposition that covers most required elements: all five explicit-wants and both explicit-not-wanteds are present with proper anti-criteria framing, every criterion includes a named verification method, effort tier is declared, and the checklist format is correctly applied throughout. The main weaknesses are: (1) the 'gotchas' category is absent from the initial decomposition step; (2) JPEG and PNG are not split into separate ISC items despite this being the canonical example of the Splitting Test in both c3 and c9; (3) the resize requirement lacks specificity about aspect ratio handling and library selection. The output reads as technically thorough but misses the mechanical split that the ISC skill's Splitting Test rule most clearly demands.
