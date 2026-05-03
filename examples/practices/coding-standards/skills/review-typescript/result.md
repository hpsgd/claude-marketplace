# Review Typescript

Scenario: A developer submits a Next.js PR where a Client Component fetches data server-side work should handle, several `any` types appear without justification, and a non-null assertion is used on an optional value.

## Prompt

> Review `app/dashboard/UserList.tsx`. It has `'use client'` at the top, then fetches user data with `const users = await fetch('/api/users').then(r => r.json())` inside the component. The return type of the exported `getUserList` function is missing. There's `const data: any = response.json()` and a `user!.profile.avatar` non-null assertion on line 47. The `tsconfig.json` has `"strict": false`.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The files don't exist in the repo — reviewing based on the description you provided.

Here are the issues, in order of severity:

---

**1. `'use client'` + `await fetch` — architectural mismatch (high)**

A `'use client'` component runs in the browser. `await fetch('/api/users')` inside the component body only works in an async Server Component. In a Client Component you'd get a runtime error or the promise would be unhandled. Fix: either remove `'use client'` and make it a Server Component, or move the fetch into a `useEffect`/SWR/React Query call.

**2. `const data: any = response.json()` — two bugs in one line (high)**

`response.json()` returns a `Promise` — missing `await`, so `data` is a Promise, not the parsed body. The `: any` also defeats type safety. Fix:
```ts
const data: User[] = await response.json();
```

**3. `user!.profile.avatar` non-null assertion (medium)**

The `!` suppresses the nullable check but doesn't make the value safe. If `user` or `user.profile` is actually null at runtime, this throws. Fix: use optional chaining and a fallback:
```ts
user?.profile?.avatar ?? defaultAvatar
```

**4. Missing return type on `getUserList` (medium)**

Without a declared return type the compiler infers it, which is fine while `strict: false` but becomes a contract gap as soon as the signature drifts. Fix:
```ts
async function getUserList(): Promise<User[]>
```

**5. `"strict": false` in `tsconfig.json` (medium)**

This disables `strictNullChecks`, `noImplicitAny`, and others — the root reason issues 2–4 are not already caught at compile time. Enabling `"strict": true` would surface all three as type errors immediately. Worth doing incrementally if the codebase is large, but leaving it off long-term means TypeScript is not doing its job.

---

**Summary of fixes:**
| Issue | Action |
|---|---|
| `'use client'` + async fetch | Convert to Server Component or use `useEffect` |
| Missing `await` + `: any` | `await response.json()` typed as `User[]` |
| Non-null assertion | Optional chaining + fallback |
| Missing return type | Explicit `Promise<User[]>` |
| `strict: false` | Enable `strict: true` |

## Evaluation

| Field | Value |
|---|---|
| Verdict | FAIL |
| Score | 5.5/17.0 (32%) |
| Evaluated | 2026-05-01 |
| Target duration | 19448 ms |
| Target cost | $0.0560 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill executes all six mandatory passes — does not skip any pass including Next.js patterns (Pass 4) | FAIL | The output contains no mention of passes, pass numbers, or pass labels whatsoever. It lists five numbered issues by severity, with no reference to a multi-pass review structure. |
| c2 | Data fetching inside a Client Component is flagged as a Pass 4 finding — data fetching belongs in Server Components | PARTIAL | Issue 1 flags the `'use client'` + `await fetch` combination and states data fetching belongs in a Server Component. However, it is never labeled 'Pass 4' — only labeled '(high)' severity. |
| c3 | `const data: any` is flagged as a Pass 1 type safety finding with the specific line as evidence | PARTIAL | Issue 2 quotes `const data: any = response.json()` and identifies the `: any` as defeating type safety. However, there is no 'Pass 1' label and no line number cited as evidence. |
| c4 | Missing return type on exported `getUserList` function is flagged as a Pass 1 finding | PARTIAL | Issue 4 flags the missing return type and provides a fix. No 'Pass 1' label is present. |
| c5 | Non-null assertion (`user!.profile.avatar`) is flagged as a Pass 1 finding with the suggestion to use optional chaining or an early return | PARTIAL | Issue 3 flags `user!.profile.avatar` and suggests `user?.profile?.avatar ?? defaultAvatar` (optional chaining + fallback). No 'Pass 1' label. |
| c6 | `"strict": false` in tsconfig is flagged as a critical Pass 1 finding | FAIL | Issue 5 is labeled '(medium)' severity — not 'critical'. There is also no 'Pass 1' label. The criterion explicitly requires 'critical' designation. |
| c7 | Each finding includes severity, pass label, file path with line reference, and a concrete code fix | FAIL | Findings include severity and code fix blocks, but none include a pass label or a file path with line reference (e.g. 'app/dashboard/UserList.tsx:47'). Two of four required structural elements are absent from every finding. |
| c8 | Anti-patterns table at the end of the skill's output references the relevant anti-pattern for each finding type (as vs as any, etc.) | FAIL | The output ends with a 'Summary of fixes' table (Issue \| Action columns). This is not an anti-patterns table and does not reference anti-pattern names or codes. |
| c9 | Output flags the `'use client'` + data fetching combination in `app/dashboard/UserList.tsx` as a Pass 4 finding — with the fix being to convert to a Server Component (remove `'use client'`, move `await fetch` into the async server component body) or split into a server-fetched parent + client-rendered child | PARTIAL | Issue 1 states 'either remove `'use client'` and make it a Server Component' — matching the first fix option. The second option given is 'useEffect/SWR/React Query', not 'server-fetched parent + client-rendered child'. No Pass 4 label. File path not cited. |
| c10 | Output flags `const data: any = response.json()` as a Pass 1 type-safety finding — with the fix using `unknown` and a Zod parse, or a typed response interface | PARTIAL | Issue 2 flags the line and provides `const data: User[] = await response.json()` as a fix — a typed interface approach. Does not use `unknown` + Zod. No Pass 1 label. |
| c11 | Output flags the missing return type on exported `getUserList` with a concrete suggested signature (e.g. `export async function getUserList(): Promise<User[]>`) | PASS | Issue 4 provides the fix: `async function getUserList(): Promise<User[]>` — matching the required signature form (the 'export' keyword is absent but the criterion uses 'e.g.' indicating it is illustrative). |
| c12 | Output flags `user!.profile.avatar` as a Pass 1 non-null-assertion finding — with the fix using optional chaining (`user?.profile?.avatar`) and an explicit fallback or early return | PARTIAL | Issue 3 gives fix `user?.profile?.avatar ?? defaultAvatar` — optional chaining plus explicit fallback. No Pass 1 label. |
| c13 | Output flags `"strict": false` in `tsconfig.json` as a CRITICAL Pass 1 finding — explaining that without strict mode, the other type-safety findings can't be caught at compile time, and naming the specific strict flags required | PARTIAL | Issue 5 names specific flags ('This disables `strictNullChecks`, `noImplicitAny`, and others') and explains it is 'the root reason issues 2–4 are not already caught at compile time'. However severity is labeled 'medium', not CRITICAL, and no Pass 1 label is present. |
| c14 | Output's findings each include severity, pass label, file path with line reference, and a concrete code fix block — not just descriptions | FAIL | Same gap as c7: pass labels and file-path-with-line-reference are absent from every finding. Only severity and code fixes are present. |
| c15 | Output runs all six mandatory passes including Next.js patterns (Pass 4) and reports per-pass finding counts even where zero | FAIL | No pass structure exists in the output. No per-pass finding counts are reported. The output is a flat numbered list. |
| c16 | Output's overall verdict is REQUEST_CHANGES — strict-off plus an `any` plus a non-null assertion plus client-component data fetching is too many type-safety violations for APPROVE | FAIL | The output has no explicit overall verdict. There is no 'REQUEST_CHANGES', 'APPROVE', or equivalent verdict statement anywhere. |
| c17 | Output's fetch-on-client critique includes the practical impact — extra round-trip latency, CSR-only data load (poor LCP), no server-side error handling, and exposes the API endpoint to clients | FAIL | Issue 1 only states the code 'only works in an async Server Component' and would cause 'a runtime error or the promise would be unhandled'. None of the four required practical impacts (latency, LCP, server-side error handling, API endpoint exposure) are mentioned. |
| c18 | Output's anti-pattern references include the specific terms from the rules (`as any`, non-null assertion, client-side data fetching, strict-mode-disabled) | PARTIAL | The output uses 'non-null assertion' in issue 3's header, discusses `: any` explicitly, and discusses strict mode. It does not use the exact terms 'as any', 'client-side data fetching', or 'strict-mode-disabled' from the rules, and there is no structured anti-patterns reference section. |

### Notes

The captured output is a competent general-purpose code review that correctly identifies all five real issues and provides reasonable fixes for each. However, it completely fails to execute the structured skill format: there are no pass labels, no six-pass framework, no overall REQUEST_CHANGES verdict, no file-path-with-line-reference citations, no anti-patterns table, and no per-pass finding counts. The severity of 'strict: false' is downgraded to 'medium' when the skill requires 'critical'. The fetch-on-client critique lacks all four required practical impacts (latency, LCP, server-side error handling, API endpoint exposure). The output reads as if a capable reviewer answered the question ad-hoc rather than executing the coding-standards:review-typescript skill with its mandatory structure.
