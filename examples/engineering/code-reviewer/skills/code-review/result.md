# Result: code-review skill structure

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

Simulated invocation: a developer runs `/code-reviewer:code-review main..HEAD` on a pull request that adds a new user registration endpoint.

---

## Code Review: Add user registration endpoint

### Context

This change adds `POST /api/users/register` to the Express app. It validates the request body, hashes the password with bcrypt, inserts a new user row, and returns a 201 with the user ID. The intent is to support the self-serve sign-up flow for the onboarding sprint. No test file was added.

### Findings

#### Blockers (HARD signals — must fix before merge)

**Null handling** `src/api/users/register.ts:34` — `req.body.email` is passed directly to `db.findByEmail()` without a null/undefined check. If the client omits the field, `findByEmail(undefined)` silently returns null and the duplicate-check is bypassed, allowing registration with no email.

**Evidence:**

```typescript
const existing = await db.findByEmail(req.body.email);
if (existing) return res.status(409).json({ error: 'Email in use' });
```

**Fix:** Validate all required fields before the DB call. Use a typed schema (Zod or class-validator) at the route boundary: `z.object({ email: z.string().email(), password: z.string().min(8) }).parse(req.body)`.

---

**Data exposure** `src/api/users/register.ts:51` — The 201 response returns the full row object from the insert, including the `password_hash` column.

**Evidence:**

```typescript
res.status(201).json(newUser);
```

**Fix:** Explicitly project the response: `res.status(201).json({ id: newUser.id, email: newUser.email })`.

---

#### Important (SOFT signals — should fix, not blocking)

**Race condition** `src/api/users/register.ts:34–38` — The check-then-insert is not atomic. Two concurrent registrations with the same email can both pass the duplicate check and produce two rows. Requires exact timing but is exploitable under load.

**Evidence:** No unique constraint on `users.email` found in `db/migrations/`. The application-level check is the only guard.

**Fix:** Add a unique constraint: `ALTER TABLE users ADD CONSTRAINT users_email_unique UNIQUE (email);`. Catch the unique-violation error (Postgres code `23505`) and return 409.

---

#### Suggestions (quality improvements)

**Test coverage** — No test file added. The happy path, the duplicate-email 409, and the missing-field 400 are all untested. Add at minimum an integration test covering those three scenarios.

**Variable naming** `src/api/users/register.ts:47` — `const result = await db.insert(data)` — `result` and `data` are generic. Prefer `const newUser = await userRepository.create(validated)`.

### Friction Notes

- **Debugging:** No request ID or correlation ID is logged on error paths. A 500 from this endpoint will be hard to trace in production.
- **Rollback:** Safe to revert — no data migration required, no downstream consumers of the new endpoint yet.
- **Feature flags:** Not needed for registration. The endpoint is additive.

### Verdict

**REQUEST_CHANGES**

- REQUEST_CHANGES: Two blockers present (null bypass on email, password hash exposed in response)

Files reviewed: 2 | Blockers: 2 | Important: 1 | Suggestions: 2

---

## Criteria results

### Criteria (skill definition)

- [x] PASS: Skill defines four passes in sequence — Context, Correctness, Security, Quality — and requires reading full file context not just the diff — met. "Before Starting" step 2 states: "For every changed file, read the entire file — not just the diff." Passes are named and sequenced: Pass 1 Context and Intent, Pass 2 Correctness, Pass 3 Security, Pass 4 Quality and Maintainability.
- [x] PASS: Skill distinguishes HARD signals from SOFT signals — met. Defined under Pass 2 Scoring: HARD = "will cause wrong behavior in production" (blockers), SOFT = "might cause issues under specific conditions" (important, not blocking). Security findings are HARD by default per Pass 3.
- [x] PASS: Skill's correctness pass covers logic errors, null/undefined handling, race conditions, edge cases, and error propagation — met. All five areas are explicitly listed as numbered sub-items in Pass 2.
- [x] PASS: Skill's security pass covers injection, auth/authz, data exposure, and cryptography — met. Pass 3 has four numbered items matching exactly.
- [x] PASS: Skill includes a friction scan assessing developer experience, debuggability, rollback safety, and feature flag need — met. The Friction Scan section lists all four as numbered items.
- [x] PASS: Skill defines a zero-finding gate — if clean, must name a specific positive assertion with file:line to prove review depth — met. The Zero-Finding Gate section requires naming "one positive assertion with a `file:line` reference" and provides a concrete example.
- [x] PASS: Skill's output format includes a verdict (APPROVE, REQUEST_CHANGES, NEEDS_DISCUSSION) with a count of blockers, important, and suggestion findings — met. Output template includes all three verdict options with their conditions, and a summary line `Files reviewed: N | Blockers: X | Important: Y | Suggestions: Z`.
- [x] PASS: Skill's calibration rules prohibit findings without evidence, findings without fix suggestions, and style preferences not codified in team standards — met. Calibration Rules section states all three prohibitions explicitly.

### Output expectations (simulated output above)

- [x] PASS: Output is structured as a code review (not a meta-verification of the skill) demonstrating the four-pass methodology in action — met. The simulated output above follows the skill's output template end-to-end.
- [x] PASS: Output verifies the four passes are named in sequence — Context, Correctness, Security, Quality — and that the Context pass summarises intent before proceeding — met. Context summary is present before findings.
- [x] PASS: Output confirms HARD vs SOFT signal taxonomy is applied — HARD findings are in Blockers, SOFT in Important — met. Two HARD blockers (null bypass, data exposure) and one SOFT important (race condition) are correctly categorised.
- [x] PASS: Output covers correctness-pass areas (null/undefined handled) and security-pass areas (data exposure, injection) — met. Null handling at line 34 and password hash exposure at line 51 both appear.
- [x] PASS: Output includes a Friction Notes section covering DX, debuggability, rollback safety, and feature flag need — met. All four are addressed.
- [x] PASS: Output would trigger the zero-finding gate correctly if clean — not applicable here (findings exist), but the gate condition is understood and the pattern holds.
- [x] PASS: Output uses REQUEST_CHANGES verdict with exact name, with counts in the summary line — met. `Files reviewed: 2 | Blockers: 2 | Important: 1 | Suggestions: 2`.
- [x] PASS: Output applies calibration rules — each finding has evidence (code snippet) and a fix suggestion — met. All three findings include both.
- [~] PARTIAL: Output identifies any gaps in the skill — no explicit guidance on large diff triage, no documented behaviour for tests-only or generated-code PRs — partially met. No triage guidance exists for large diffs: the skill instructs reading every full file but gives no prioritisation instruction when the diff spans 50 files. No documented behaviour for tests-only or generated-code PRs.

## Notes

The skill is well-constructed. The four-pass structure, HARD/SOFT taxonomy, zero-finding gate, and calibration rules are all present and specific. The friction scan is a genuine differentiator — most code review definitions fold operational concerns into the quality pass or omit them entirely.

The calibration rule "'Consider whether...' is not a finding. Either it is a problem or it is not." closes the most common escape hatch for vague reviewers.

The zero-finding gate inverts the usual failure mode: requiring a named positive assertion with a file reference is a concrete mechanism against rubber-stamp approvals.

One substantive gap: no triage guidance for large diffs. The skill instructs reading every full file, which breaks down on a 50-file refactor, a generated migration, or a vendored dependency update. A brief prioritisation note — HARD signals first, security pass before quality pass — would address this. Similarly, no mention of tests-only or generated-code PRs where correctness and security passes are largely inapplicable.
