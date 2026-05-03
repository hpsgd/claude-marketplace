# Review Typescript

Scenario: A developer submits a Next.js PR where a Client Component fetches data server-side work should handle, several `any` types appear without justification, and a non-null assertion is used on an optional value.

## Prompt

> Review `app/dashboard/UserList.tsx`. It has `'use client'` at the top, then fetches user data with `const users = await fetch('/api/users').then(r => r.json())` inside the component. The return type of the exported `getUserList` function is missing. There's `const data: any = response.json()` and a `user!.profile.avatar` non-null assertion on line 47. The `tsconfig.json` has `"strict": false`.
> 
> A few specifics for the response (output structured per the review-typescript template):
> 
> - **Run all 6 passes** in order: **Pass 1 (Type safety)**, **Pass 2 (React/component patterns)**, **Pass 3 (Imports & boundaries)**, **Pass 4 (Next.js App Router patterns)**, **Pass 5 (Performance)**, **Pass 6 (Tests)**. Even passes with zero findings get `Pass N: 0 findings`.
> - **Per-pass summary table at top**: rows for all 6 passes with finding counts.
> - **Each finding uses structured format**: `**Severity:** CRITICAL/HIGH/MEDIUM/LOW | **Pass:** N | **File:** path:line | **Evidence:** \`code snippet\` | **Anti-pattern:** [named term from rules] | **Fix:** [concrete fix code]`. File:line REQUIRED on every finding.
> - **Findings**:
>   - **Pass 4, HIGH** — `app/dashboard/UserList.tsx` — `'use client'` + `await fetch` data fetching in Client Component. Fix options: (a) convert to Server Component (drop `'use client'`, move fetch to async server body) OR (b) split into server-fetched parent + client-rendered child. Practical impact: extra round-trip latency, CSR-only data load (poor LCP), no server-side error handling, exposes API endpoint to clients.
>   - **Pass 1, HIGH** — `const data: any = response.json()` line ~14. Anti-pattern: `as any` / `: any`. Fix: `const data: unknown = await response.json(); const users = userArraySchema.parse(data);` (Zod) OR typed interface.
>   - **Pass 1, HIGH** — exported `getUserList` missing return type annotation. Anti-pattern: missing public-API type. Fix: add explicit `Promise<User[]>` return type.
>   - **Pass 1, HIGH** — `user!.profile.avatar` line 47. Anti-pattern: non-null assertion. Fix: `user?.profile?.avatar ?? defaultAvatar` (optional chaining + fallback) OR early return if `user` undefined.
>   - **Pass 1, CRITICAL** — `"strict": false` in `tsconfig.json`. Anti-pattern: strict-mode-disabled. WHY: without strict mode, the other type-safety findings (any, missing return types, non-null assertions) cannot be caught at compile time. Required flags: `strict: true` (which enables `strictNullChecks`, `noImplicitAny`, `noImplicitThis`, `alwaysStrict`, `strictBindCallApply`, `strictFunctionTypes`, `strictPropertyInitialization`).
> - **Overall verdict**: **REQUEST_CHANGES** (strict-off + `any` + non-null assertion + client-component data fetching is too many type-safety violations for APPROVE).
> - **Anti-patterns reference table at end** with named anti-patterns from rules: `as any`, `non-null assertion`, `client-side data fetching`, `strict-mode-disabled`, `missing return type on public API`.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The repository doesn't contain this file yet. I'll construct the review based on your description, following the review-typescript template structure exactly as specified.

---

# Code Review: `app/dashboard/UserList.tsx`

## Per-Pass Summary

| Pass | Name | Findings |
|---|---|---|
| 1 | Type Safety | 4 |
| 2 | React/Component Patterns | 0 |
| 3 | Imports & Boundaries | 0 |
| 4 | Next.js App Router | 1 |
| 5 | Performance | 1 |
| 6 | Tests | 0 |
| **Total** | | **6** |

---

## Pass 1: Type Safety — 4 findings

**Severity:** CRITICAL | **Pass:** 1 | **File:** `tsconfig.json` | **Evidence:** `"strict": false` | **Anti-pattern:** `strict-mode-disabled` | **Fix:**
```json
{
  "compilerOptions": {
    "strict": true
  }
}
```
Without strict mode, TypeScript cannot enforce the downstream type-safety rules. All other violations in this file become undetectable at compile time.

---

**Severity:** HIGH | **Pass:** 1 | **File:** `app/dashboard/UserList.tsx:~14` | **Evidence:** `const data: any = response.json()` | **Anti-pattern:** `as any` (implicit `any` typing) | **Fix:**
```typescript
import { z } from 'zod';

const userSchema = z.object({
  id: z.string(),
  name: z.string(),
  profile: z.object({
    avatar: z.string().optional(),
  }),
});

const userArraySchema = z.array(userSchema);
type User = z.infer<typeof userArraySchema>;

const users = userArraySchema.parse(
  await fetch('/api/users').then(r => r.json())
);
```
Parsing at the boundary ensures data is safe before use and gives proper types for the rest of the component.

---

**Severity:** HIGH | **Pass:** 1 | **File:** `app/dashboard/UserList.tsx` (function export) | **Evidence:** Missing return type on exported `getUserList` | **Anti-pattern:** `missing return type on public API` | **Fix:**
```typescript
export async function getUserList(): Promise<User[]> {
  // ...
}
```
Public APIs must declare return types explicitly. This prevents accidental changes to the contract and forces you to think about what the function actually returns.

---

**Severity:** HIGH | **Pass:** 1 | **File:** `app/dashboard/UserList.tsx:47` | **Evidence:** `user!.profile.avatar` | **Anti-pattern:** `non-null assertion` | **Fix:**
```typescript
// Option A: Optional chaining + fallback
const avatarUrl = user?.profile?.avatar ?? '/default-avatar.png';

// Option B: Guard clause
if (!user?.profile?.avatar) {
  return <div>User profile incomplete</div>;
}
const avatarUrl = user.profile.avatar;
```
Non-null assertions hide assumptions. Use optional chaining to traverse safely, or guard explicitly if the value is required.

---

## Pass 2: React/Component Patterns — 0 findings

---

## Pass 3: Imports & Boundaries — 0 findings

---

## Pass 4: Next.js App Router — 1 finding

**Severity:** HIGH | **Pass:** 4 | **File:** `app/dashboard/UserList.tsx:1-12` | **Evidence:** `'use client'` directive + `await fetch()` for data fetching inside component | **Anti-pattern:** `client-side data fetching` | **Fix:**

**Option A — Convert to Server Component (recommended):**
```typescript
// Remove 'use client' from top
// Move fetch to the component body (already async)

export default async function UserList() {
  const users = await fetch('http://localhost:3000/api/users', {
    cache: 'no-store', // or appropriate revalidation
  }).then(r => r.json());
  
  return (
    <div>
      {users.map(user => (
        <UserListItem key={user.id} user={user} />
      ))}
    </div>
  );
}

// Extracted into separate file for client-specific logic
'use client';
function UserListItem({ user }: { user: User }) {
  return <div>{user.name}</div>;
}
```

**Option B — Split into server parent + client child:**
```typescript
// app/dashboard/page.tsx (Server Component)
export default async function UserListPage() {
  const users = await getUserList();
  return <UserListClient users={users} />;
}

// app/dashboard/UserListClient.tsx (Client Component)
'use client';
function UserListClient({ users }: { users: User[] }) {
  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

**Practical impact:** Client Components with `await fetch()` cause extra round-trip latency, poor LCP (all data loads client-side), no server-side error handling, and expose internal API endpoints to browser clients.

---

## Pass 5: Performance — 1 finding

**Severity:** MEDIUM | **Pass:** 5 | **File:** `app/dashboard/UserList.tsx:~8` | **Evidence:** `const users = await fetch('/api/users').then(r => r.json())` without cache strategy | **Anti-pattern:** `cache-unspecified request` | **Fix:**
```typescript
const users = await fetch('/api/users', {
  next: { revalidate: 60 }, // ISR: revalidate every 60s
  // OR
  // next: { revalidate: false }, // Cache indefinitely until manual revalidation
  // OR for user-specific data:
  // cache: 'no-store', // Always fetch fresh
}).then(r => r.json());
```
Specify cache intent explicitly. Without `next: { revalidate }` or `cache`, each render refetches data, causing unnecessary network calls and slow page loads.

---

## Pass 6: Tests — 0 findings

---

## Overall Verdict

**REQUEST_CHANGES**

Type-safety violations span critical (strict-mode disabled) and high severity (`any` typing, non-null assertions, missing return type, client-side data fetching). These must be resolved before approval.

---

## Anti-Patterns Reference

| Anti-Pattern | Rule | Violation in This File |
|---|---|---|
| `strict-mode-disabled` | All strict-mode flags disabled in `tsconfig.json` | Masks all downstream type errors |
| `as any` / implicit `any` | No implicit `any` allowed | `const data: any` on line ~14 |
| `non-null assertion` | Use optional chaining or guards | `user!.profile.avatar` on line 47 |
| `missing return type on public API` | Public functions must declare return type | `getUserList()` export |
| `client-side data fetching` | Data fetch should occur on server, not in Client Component | `'use client'` + `await fetch()` |
| `cache-unspecified request` | All fetch requests must specify caching intent | Missing `next: { revalidate }` or `cache` |

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.0 (91%) |
| Evaluated | 2026-05-03 |
| Target duration | 30984 ms |
| Target cost | $0.0759 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill executes all six mandatory passes — does not skip any pass including Next.js patterns (Pass 4) | PASS | Per-Pass Summary table lists all six passes: Pass 1 (4), Pass 2 (0), Pass 3 (0), Pass 4 (1), Pass 5 (1), Pass 6 (0). Each has its own section heading with finding content or explicit '0 findings' label. |
| c2 | Data fetching inside a Client Component is flagged as a Pass 4 finding — data fetching belongs in Server Components | PASS | Pass 4 heading 'Next.js App Router — 1 finding' explicitly flags `'use client'` + `await fetch()` inside a Client Component as HIGH severity. |
| c3 | `const data: any` is flagged as a Pass 1 type safety finding with the specific line as evidence | PASS | Pass 1 HIGH finding: `**File:** app/dashboard/UserList.tsx:~14` with `**Evidence:** const data: any = response.json()`. |
| c4 | Missing return type on exported `getUserList` function is flagged as a Pass 1 finding | PASS | Pass 1 HIGH finding: 'Missing return type on exported `getUserList`' with Anti-pattern `missing return type on public API`. |
| c5 | Non-null assertion (`user!.profile.avatar`) is flagged as a Pass 1 finding with the suggestion to use optional chaining or an early return | PASS | Pass 1 HIGH finding at line 47 with two fix options: Option A uses `user?.profile?.avatar ?? '/default-avatar.png'` and Option B is a guard clause early return. |
| c6 | `"strict": false` in tsconfig is flagged as a critical Pass 1 finding | PASS | First finding in Pass 1: `**Severity:** CRITICAL \| **Pass:** 1 \| **File:** tsconfig.json \| **Evidence:** "strict": false \| **Anti-pattern:** strict-mode-disabled`. |
| c7 | Each finding includes severity, pass label, file path with line reference, and a concrete code fix | PARTIAL | Four of six findings include line references (`:~14`, `:47`, `:1-12`, `:~8`). The tsconfig.json CRITICAL finding has no line number, and the missing-return-type finding only says '(function export)' rather than a line. All findings do include severity, pass label, and code fix blocks. |
| c8 | Anti-patterns table at the end of the skill's output references the relevant anti-pattern for each finding type (as vs as any, etc.) | PARTIAL | Anti-Patterns Reference table present with rows for: `strict-mode-disabled`, `as any / implicit any`, `non-null assertion`, `missing return type on public API`, `client-side data fetching`, and `cache-unspecified request`. |
| c9 | Output flags the `'use client'` + data fetching combination in `app/dashboard/UserList.tsx` as a Pass 4 finding — with the fix being to convert to a Server Component (remove `'use client'`, move `await fetch` into the async server component body) or split into a server-fetched parent + client-rendered child | PASS | Pass 4 finding provides both fix options: Option A removes `'use client'` and uses `export default async function UserList()` with the fetch in the server body; Option B shows a server parent `UserListPage` and a `'use client'` child `UserListClient`. |
| c10 | Output flags `const data: any = response.json()` as a Pass 1 type-safety finding — with the fix using `unknown` and a Zod parse, or a typed response interface | PASS | Pass 1 HIGH fix uses Zod: `const userArraySchema = z.array(userSchema); const users = userArraySchema.parse(await fetch(...).then(r => r.json()));` with a full schema definition. |
| c11 | Output flags the missing return type on exported `getUserList` with a concrete suggested signature (e.g. `export async function getUserList(): Promise<User[]>`) | PASS | Fix code block shows `export async function getUserList(): Promise<User[]> { // ... }`. |
| c12 | Output flags `user!.profile.avatar` as a Pass 1 non-null-assertion finding — with the fix using optional chaining (`user?.profile?.avatar`) and an explicit fallback or early return | PASS | Pass 1 HIGH finding at line 47 shows Option A: `const avatarUrl = user?.profile?.avatar ?? '/default-avatar.png'` and Option B: guard clause `if (!user?.profile?.avatar) { return <div>User profile incomplete</div>; }`. |
| c13 | Output flags `"strict": false` in `tsconfig.json` as a CRITICAL Pass 1 finding — explaining that without strict mode, the other type-safety findings can't be caught at compile time, and naming the specific strict flags required | PARTIAL | Output correctly marks it CRITICAL and states 'Without strict mode, TypeScript cannot enforce the downstream type-safety rules. All other violations in this file become undetectable at compile time.' Fix shows `"strict": true`. However, the specific component flags (strictNullChecks, noImplicitAny, noImplicitThis, alwaysStrict, strictBindCallApply, strictFunctionTypes, strictPropertyInitialization) are not named. |
| c14 | Output's findings each include severity, pass label, file path with line reference, and a concrete code fix block — not just descriptions | PARTIAL | All findings include severity, pass label, and code fix blocks. However, the tsconfig.json finding has no line number and the missing-return-type finding uses '(function export)' instead of a line number — two of six findings lack line references. |
| c15 | Output runs all six mandatory passes including Next.js patterns (Pass 4) and reports per-pass finding counts even where zero | PASS | Per-Pass Summary table lists all six passes. Passes 2, 3, and 6 explicitly show 0 findings in the table and each has a section with '— 0 findings' in the heading. |
| c16 | Output's overall verdict is REQUEST_CHANGES — strict-off plus an `any` plus a non-null assertion plus client-component data fetching is too many type-safety violations for APPROVE | PASS | Section '## Overall Verdict' reads '**REQUEST_CHANGES**' and explains 'Type-safety violations span critical (strict-mode disabled) and high severity (`any` typing, non-null assertions, missing return type, client-side data fetching). These must be resolved before approval.' |
| c17 | Output's fetch-on-client critique includes the practical impact — extra round-trip latency, CSR-only data load (poor LCP), no server-side error handling, and exposes the API endpoint to clients | PASS | Pass 4 finding ends with: 'Client Components with await fetch() cause extra round-trip latency, poor LCP (all data loads client-side), no server-side error handling, and expose internal API endpoints to browser clients.' |
| c18 | Output's anti-pattern references include the specific terms from the rules (`as any`, non-null assertion, client-side data fetching, strict-mode-disabled) | PARTIAL | Anti-Patterns Reference table includes all four required terms: `strict-mode-disabled`, `as any / implicit any`, `non-null assertion`, `client-side data fetching`, plus `missing return type on public API` and `cache-unspecified request`. |

### Notes

The output is a strong, well-structured TypeScript review that hits all six mandatory passes, correctly identifies every required finding, assigns appropriate severities (CRITICAL for strict-off, HIGH for the others), provides concrete code fixes throughout, and delivers the expected REQUEST_CHANGES verdict with the full practical impact of client-side data fetching. Two areas fell short of full marks: (1) two findings lack specific line numbers — the tsconfig.json CRITICAL finding and the missing-return-type HIGH finding — dragging both c7 and c14 to PARTIAL; (2) the strict-mode-disabled CRITICAL finding correctly explains compile-time impact but omits the enumerated component flags (strictNullChecks, noImplicitAny, etc.) that the criterion requires, reducing c13 to PARTIAL. The anti-patterns reference table covers all named terms so c8 and c18 achieve their PARTIAL ceiling. Overall the review is thorough and actionable; the gaps are structural precision issues rather than substantive misses.
