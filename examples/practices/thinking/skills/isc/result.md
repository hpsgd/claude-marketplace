# Isc

Scenario: A developer asks for help with a task that has multiple components, explicit exclusions, and implied requirements. The ISC skill must catch all parts including the anti-criteria.

## Prompt

> /isc Update the user profile page to show the new avatar upload feature. The upload should accept JPEG and PNG only, max 5MB, and resize to 200x200 on save. Don't touch the password change section — we're in the middle of a security audit. Also make sure the existing profile tests still pass, and don't add any new npm dependencies.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## ISC Decomposition

**Effort level:** Extended (multi-file feature with validation, server-side processing, and test constraints) → target 16–32 criteria.

---

### Step 1: Reverse-engineered requirements

**Explicit wants:** Avatar upload on profile page; JPEG/PNG only; max 5MB; resize to 200×200 on save; existing tests pass; no new npm dependencies.

**Implied wants:** Client-side validation before upload; server-side re-validation (defence-in-depth); error messages for both failure modes; avatar displayed after upload; upload control visually integrated with profile layout.

**Explicit not-wanted:** No changes to password change section; no new npm dependencies.

**Implied not-wanted:** No refactoring of unrelated profile code; no regressions in other profile features.

**Gotchas:** Resize dimension (crop vs. fit not specified — pick one and note it); client-only validation is insufficient without server-side mirror; "no new npm deps" constrains which image-resize approach is usable; "don't touch password section" must be precise — file-level, not just line-level.

---

### ISC Checklist

**UI / Profile Page**

- [ ] ISC-1: Avatar upload `<input type="file">` (or equivalent) rendered on the profile page — verify: `grep -r "type=\"file\"" <profile-component>` → match found inside profile avatar section
- [ ] ISC-2: Upload input `accept` attribute restricts to JPEG and PNG — verify: read profile component → `accept` contains `image/jpeg` and `image/png` (and nothing else)
- [ ] ISC-3: Current avatar (or placeholder fallback) displayed via `<img>` on profile page — verify: read profile component → `<img>` element present referencing avatar state
- [ ] ISC-4: Avatar upload control visually placed in avatar/profile-photo section, not inside or adjacent to password section — verify: read component structure → upload input is outside password change block

**Client-side validation**

- [ ] ISC-5: Client rejects files whose MIME type is not `image/jpeg` or `image/png` — verify: read validation function → type check against `['image/jpeg', 'image/png']` before any upload call
- [ ] ISC-6: Client rejects files larger than 5 242 880 bytes (5 × 1024 × 1024) — verify: read validation function → `file.size > 5 * 1024 * 1024` guard present
- [ ] ISC-7: Invalid file type surfaces a visible error message in the UI — verify: read component → conditional error render present for type-rejection case
- [ ] ISC-8: File-too-large surfaces a visible error message in the UI — verify: read component → conditional error render present for size-rejection case

**Server-side validation**

- [ ] ISC-9: Server handler validates MIME type is `image/jpeg` or `image/png` and returns an error response for anything else — verify: read handler → MIME check with non-2xx response path
- [ ] ISC-10: Server handler enforces 5MB max and returns an error response for oversized uploads — verify: read handler → size limit enforced, non-2xx response path

**Image processing**

- [ ] ISC-11: Saved avatar file is exactly 200 pixels wide — verify: read resize call → width argument is `200`
- [ ] ISC-12: Saved avatar file is exactly 200 pixels tall — verify: read resize call → height argument is `200`
- [ ] ISC-13: Resize uses an already-present dependency (no new package introduced) — verify: `git diff package.json` → zero additions in `dependencies` or `devDependencies`
- [ ] ISC-14: Lock file (`package-lock.json` / `yarn.lock` / `pnpm-lock.yaml`) has no new package entries — verify: `git diff <lock-file>` → no new package blocks

**Password section isolation**

- [ ] ISC-15: Password change component/file is not modified — verify: `git diff --name-only` → no password-related filenames listed
- [ ] ISC-16: Password change section renders intact (no accidental JSX restructuring) — verify: read profile page → password section markup unchanged compared to base commit

**Test hygiene**

- [ ] ISC-17: All pre-existing profile test assertions pass — verify: run profile test suite → zero failures, zero skipped tests that were previously passing
- [ ] ISC-18: No existing test assertion is deleted or weakened — verify: `git diff <test-files>` → no `-` lines removing `expect`/`assert` calls
- [ ] ISC-19: New avatar tests (if added) do not conflict with existing test setup/teardown — verify: run full test suite → no test isolation errors or ordering failures

**Scope containment**

- [ ] ISC-20: Only profile page, avatar handler, and directly related files are modified — verify: `git diff --name-only` → no files outside profile/avatar scope

---

**20 criteria — meets Extended floor (16).** Ready to execute against the codebase once you confirm.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 13.0/14.0 (93%) |
| Evaluated | 2026-05-01 |
| Target duration | 45020 ms |
| Target cost | $0.0798 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Step 1 extracts all five categories — explicit wants, implied wants, explicit not-wanted, implied not-wanted, and gotchas | PASS | Step 1 contains clearly labelled sections: 'Explicit wants:', 'Implied wants:', 'Explicit not-wanted:', 'Implied not-wanted:', and 'Gotchas:' — all five categories present. |
| c2 | Explicit not-wanted items (don't touch password section, no new npm dependencies) appear as separate ISC criteria | PASS | ISC-15 covers 'Password change component/file is not modified'; ISC-16 covers password section rendering; ISC-13 covers 'Resize uses an already-present dependency (no new package introduced)'; ISC-14 covers lock file having no new entries — both not-wanted items appear as separate criteria. |
| c3 | The Splitting Test is applied — compound criteria like "accept JPEG and PNG" become separate verifiable items | PARTIAL | Splitting is applied in several places (ISC-11/ISC-12 split resize into width and height; ISC-5/ISC-6 split type vs. size validation; ISC-7/ISC-8 split error messages by failure mode; ISC-9/ISC-10 split server-side by rule). However, 'JPEG and PNG accepted' is NOT split — ISC-2 checks both together ('accept contains image/jpeg and image/png') and ISC-5 also handles both in one criterion. |
| c4 | Each criterion is stated as verifiable — includes what tool would confirm it and what you'd see | PASS | Every ISC item includes a 'verify:' clause specifying both a tool/command and the expected observation. Examples: ISC-1 'verify: grep -r "type=\"file\"" <profile-component> → match found inside profile avatar section'; ISC-15 'verify: git diff --name-only → no password-related filenames listed'. |
| c5 | Effort level is assigned and the ISC count meets the floor for that tier before execution begins | PASS | Output states 'Effort level: Extended (multi-file feature with validation, server-side processing, and test constraints) → target 16–32 criteria' and confirms '20 criteria — meets Extended floor (16). Ready to execute against the codebase once you confirm.' |
| c6 | ISC count gate is enforced — if below floor, skill explicitly states the criterion count is insufficient and decomposes further | PASS | Output explicitly checks and confirms '20 criteria — meets Extended floor (16)' — demonstrating the gate was applied. The floor is named, the count is compared to it, and execution is deferred pending confirmation. |
| c7 | Criteria are presented as a numbered checklist with checkboxes, ready to be marked during execution | PASS | All 20 items use the format '- [ ] ISC-N: ...' — numbered identifiers and empty checkboxes present throughout the ISC Checklist section. |
| c8 | Domain-specific decomposition is applied — UI criteria split by element/state, validation criteria split by rule | PARTIAL | UI criteria split by element (ISC-1 input, ISC-2 accept attribute, ISC-3 avatar display, ISC-4 placement). Validation split by layer (client ISC-5/6, server ISC-9/10) and by rule (type vs. size). Error messages split per rule (ISC-7 type error, ISC-8 size error). Good domain decomposition throughout. |
| c9 | Output's explicit-wants list includes avatar upload, JPEG and PNG accepted, max 5MB, resize to 200x200 on save — split where the Splitting Test demands ("JPEG accepted" and "PNG accepted" as separate verifiable items, not "both formats accepted") | PARTIAL | Explicit-wants list in Step 1 includes all four items: 'Avatar upload on profile page; JPEG/PNG only; max 5MB; resize to 200×200 on save.' However, JPEG and PNG are NOT split into separate ISC criteria — ISC-2 checks both together ('accept contains image/jpeg and image/png') and ISC-5 checks both in one criterion, failing the specific split requirement. |
| c10 | Output's explicit-not-wanted list includes "do not modify password change section" and "no new npm dependencies" as separate ISC criteria — and these are framed as ANTI-criteria that must be verified false at completion (e.g. `git diff` shows no changes to password section) | PASS | ISC-15 uses 'verify: git diff --name-only → no password-related filenames listed'; ISC-14 uses 'verify: git diff <lock-file> → no new package blocks'; ISC-13 uses 'verify: git diff package.json → zero additions' — all framed as verifying absence of change (anti-criteria). |
| c11 | Output's criteria each name a verification method — e.g. "Tool: open profile page in browser → see new upload button" or "Tool: `git diff -- src/profile/password*` → shows no changes" or "Tool: `npm ls --depth=0` → no new package added" | PASS | Every criterion contains a 'verify:' clause with a specific tool or action and expected observable result. Examples include grep commands, git diff commands, 'read component', 'run profile test suite', 'run full test suite'. |
| c12 | Output assigns an effort level (likely Small or Medium given file upload + validation + resize + tests) and the resulting ISC criterion count meets the floor for that tier — explicitly stated | PASS | Effort level 'Extended' is assigned with explicit floor of 16; 20 criteria are produced and the output states '20 criteria — meets Extended floor (16).' The tier and count are both explicitly named. |
| c13 | Output enforces the count gate — if the initial decomposition is below the floor, the skill states the count is insufficient and decomposes further (e.g. splitting "validation" into per-rule items) | PASS | Output shows awareness of the gate: 'target 16–32 criteria' stated upfront, final count confirmed as '20 criteria — meets Extended floor (16).' The gate was enforced and passed. |
| c14 | Output presents criteria as a numbered checklist with `[ ]` checkboxes, ready to be marked during execution | PASS | All criteria use '- [ ] ISC-N:' format with empty checkboxes and sequential numeric identifiers ISC-1 through ISC-20. |
| c15 | Output addresses the resize requirement specifically — what aspect ratio handling (crop, letterbox, distort), what library performs the resize (server-side vs client-side), what happens to non-square inputs | PARTIAL | Gotchas section notes 'Resize dimension (crop vs. fit not specified — pick one and note it)' — flagging the ambiguity. ISC-13 notes resize must use an existing dependency. However, no specific approach is chosen, no library is named, and the handling of non-square inputs is not resolved in the criteria. |

### Notes

The output is a high-quality ISC decomposition that covers all five Step 1 categories, produces 20 well-structured verifiable criteria with explicit tooling, enforces the effort tier gate, and correctly frames anti-criteria using git diff verification. The primary gap is the failure to split 'JPEG and PNG accepted' into separate verifiable ISC items — the skill identifies both in the explicit-wants prose but collapses them in ISC-2 and ISC-5. The resize section notes the crop-vs-fit ambiguity but does not resolve it or name a library. These are minor gaps in an otherwise thorough decomposition.
