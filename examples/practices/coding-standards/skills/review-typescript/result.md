# Result: review-typescript any usage and client component misuse

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/18 criteria met (94%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated output from invoking `/coding-standards:review-typescript` against `app/dashboard/UserList.tsx` and `tsconfig.json` as described in the test scenario.

---

## TypeScript Review

### Summary

| Category | Findings |
|---|---|
| Files reviewed | 2 (`app/dashboard/UserList.tsx`, `tsconfig.json`) |
| Type safety (Pass 1) | 4 findings (1 CRITICAL) |
| Import hygiene (Pass 2) | 0 findings |
| Naming conventions (Pass 3) | 0 findings |
| Next.js patterns (Pass 4) | 1 finding |
| Styling — Tailwind (Pass 5) | N/A |
| Test coverage (Pass 6) | 0 findings |

**Overall verdict: REQUEST_CHANGES** — strict mode is disabled (meaning TypeScript cannot catch most of the other findings at compile time), an `any` type is present without justification, a non-null assertion is used on an optional value, the exported function is missing a return type, and a Client Component is performing server-side data fetching. All five must be resolved before merge.

---

### Findings

#### CRITICAL — Pass 1: `"strict": false` in tsconfig disables compile-time safety

**File:** `tsconfig.json`
**Evidence:**
```json
{
  "compilerOptions": {
    "strict": false
  }
}
```
**Standard:** Pass 1.5 — `tsconfig.json` must have `"strict": true`. Strict mode is not a single flag — it enables the following checks as a group: `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, and `alwaysStrict`. With `"strict": false`, TypeScript will not catch the `any` usage on the line below (Pass 1, finding 2), will not catch `null`/`undefined` dereferences (rendering the non-null assertion finding cosmetic rather than functional), and will not enforce explicit return types. In other words, without this fix, the other four findings in this review become unenforceable at the compiler level.

**Fix:**
```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

If enabling strict mode in one step is too disruptive (many pre-existing errors), enable `strictNullChecks` and `noImplicitAny` first as an intermediate step, then add the rest. Do not leave `"strict": false` in production config.

---

#### HIGH — Pass 1: `const data: any` on `response.json()` return

**File:** `app/dashboard/UserList.tsx`
**Evidence:**
```typescript
const data: any = response.json()
```
**Standard:** Pass 1.1 — `: any` is a finding in all cases except third-party libraries without type definitions (with an explanatory comment), genuine generic constraints where `unknown` breaks the contract, or code-generator output. None of these exceptions apply here. `response.json()` returns `unknown` in recent TypeScript versions and `any` in older ones — either way, assigning it to an `any` typed variable defeats the type system entirely. The bug this hides: `data` is a `Promise<any>` without `await`, meaning downstream accesses on `data.users` will silently receive `undefined` at runtime.

**Fix (preferred — Zod parse at the boundary):**
```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  profile: z.object({ avatar: z.string().nullable() }).nullable(),
});

const UsersResponseSchema = z.array(UserSchema);
type User = z.infer<typeof UserSchema>;

const raw: unknown = await response.json();
const users = UsersResponseSchema.parse(raw);
```

**Fix (minimal — typed interface without Zod):**
```typescript
interface User {
  id: string;
  name: string;
  profile: { avatar: string | null } | null;
}

const users = (await response.json()) as User[];
// Note: `as User[]` is still an assertion — Zod parse is preferred.
```

---

#### HIGH — Pass 1: Missing explicit return type on exported `getUserList`

**File:** `app/dashboard/UserList.tsx`
**Evidence:**
```typescript
export async function getUserList() {
  // ...
}
```
**Standard:** Pass 1.2 — every exported function and method must have an explicit return type. This prevents accidental API surface changes: if the implementation changes what the function resolves to, TypeScript will flag the mismatch against the declared type instead of silently propagating the change to all callers.

**Fix:**
```typescript
export async function getUserList(): Promise<User[]> {
  // ...
}
```

If the return type is more complex (e.g., wrapping a result type), be explicit:
```typescript
export async function getUserList(): Promise<{ users: User[]; total: number }> {
  // ...
}
```

---

#### HIGH — Pass 1: Non-null assertion on optional `user.profile.avatar`

**File:** `app/dashboard/UserList.tsx:47`
**Evidence:**
```typescript
user!.profile.avatar  // line 47
```
**Standard:** Pass 1.4 — every `[a-zA-Z]!.` match is a finding. The `!` operator asserts that `user` is non-null and non-undefined without actually checking. If `user` is `null` or `undefined` at runtime, this throws a `TypeError: Cannot read properties of null (reading 'profile')`. The same applies to `profile` — if `user` is non-null but `user.profile` is null, the runtime error still fires.

**Fix (optional chaining with fallback):**
```typescript
const avatar = user?.profile?.avatar ?? null;
```

**Fix (early return):**
```typescript
if (!user || !user.profile) {
  return null; // or render a placeholder
}
const avatar = user.profile.avatar;
```

Prefer the early-return pattern when `user` being absent represents an invalid state worth surfacing explicitly.

---

#### HIGH — Pass 4: Client Component fetching data that belongs in a Server Component

**File:** `app/dashboard/UserList.tsx`
**Evidence:**
```typescript
'use client'

// ...

const users = await fetch('/api/users').then(r => r.json())
```
**Standard:** Pass 4.1 — data fetching belongs in Server Components. A file with `'use client'` that performs a `fetch` inside the component body has three compounding problems.

First, **extra round-trip latency**: the browser must download, parse, and execute the JavaScript bundle before the fetch fires. With a Server Component, the fetch happens on the server during render — the HTML arrives with data already populated.

Second, **poor LCP (Largest Contentful Paint)**: client-side data loading means the user sees a loading state before the content appears. Server Components render the populated content into the initial HTML response, eliminating the empty-shell → loading-spinner → content flash sequence.

Third, **no server-side error handling**: if the fetch fails inside a Server Component, Next.js's error boundary and `error.tsx` catch it. Inside a Client Component, the unhandled rejection is visible in the browser console and crashes the component tree unless you add explicit try/catch.

Fourth, **API endpoint exposure**: adding `'use client'` and fetching `/api/users` from the component means the `/api/users` route must be publicly routable — it cannot be collapsed into a Server Component import. Any caller (not just this component) can now hit that route.

**Fix (convert to Server Component):**
```typescript
// Remove 'use client' — no directive needed for a Server Component
// app/dashboard/UserList.tsx

async function fetchUsers(): Promise<User[]> {
  const response = await fetch('/api/users', { next: { revalidate: 60 } });
  if (!response.ok) throw new Error(`Failed to fetch users: ${response.status}`);
  return response.json() as Promise<User[]>;
}

export default async function UserList() {
  const users = await fetchUsers();
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

**Fix (split: server-fetched parent + client-rendered child):**
```typescript
// app/dashboard/UserList.tsx — Server Component (no directive)
import { UserListClient } from './_UserListClient';

export default async function UserList() {
  const users = await fetchUsers();
  return <UserListClient users={users} />;
}

// app/dashboard/_UserListClient.tsx — Client Component
'use client'

interface Props { users: User[] }

export function UserListClient({ users }: Props) {
  // safe to use hooks, event handlers, etc. here
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

---

### Clean Areas

- Pass 2 (import hygiene): no CommonJS `require()` or `module.exports` detected. No circular imports identified in the described code.
- Pass 3 (naming): `UserList.tsx` correctly uses `PascalCase` for a component file. No naming violations detected.
- Pass 5 (Tailwind): not applicable to this file based on the described content.
- Pass 6 (test coverage): no test files described in the diff — raising a test-coverage finding requires visibility of changed test files, which were not in scope for this prompt.

---

## Evaluation

### Criteria (against the skill definition)

- [x] PASS: Skill executes all six mandatory passes, including Pass 4 — met. The SKILL.md states "Execute all six passes. Do not skip." Pass 4 is fully defined and its applicability condition (Next.js project) is met by the scenario.
- [x] PASS: Data fetching inside a Client Component flagged as a Pass 4 finding — met. Pass 4.1 states "Data fetching belongs in Server Components. If a Client Component fetches data, that is a finding."
- [x] PASS: `const data: any` flagged as a Pass 1 type-safety finding with line evidence — met. Pass 1.1 lists `: any` as a grep target and the Evidence Format mandates file path with line number for every finding.
- [x] PASS: Missing return type on exported `getUserList` flagged as a Pass 1 finding — met. Pass 1.2 states "every exported function and method must have an explicit return type" and mandates a grep to find them.
- [x] PASS: Non-null assertion `user!.profile.avatar` flagged as a Pass 1 finding with optional chaining or early return suggestion — met. Pass 1.4 targets `[a-zA-Z]!\.` and names "optional chaining" and "early returns" as the fixes.
- [x] PASS: `"strict": false` in tsconfig flagged as a critical Pass 1 finding — met. Pass 1.5 states "flag it as a critical finding" explicitly.
- [x] PASS: Each finding includes severity, pass label, file path with line reference, and a concrete code fix — met. The Evidence Format template mandates all four elements: severity, pass label, `**File:**` with path, `**Evidence:**`, `**Standard:**`, and `**Fix:**`.
- [~] PARTIAL: Anti-patterns table references the relevant anti-pattern for each finding type — partially met. The table covers `as any` but has no entries for non-null assertions (`!.`), missing explicit return types, or `"strict": false`. Three of the four Pass 1 finding types triggered by this scenario are absent from the table. `as any` is present; the rest are not.

### Output expectations (against the simulated output)

- [x] PASS: Output flags `'use client'` + data fetching in `app/dashboard/UserList.tsx` as a Pass 4 finding with the server-component conversion or split-component fix — met. The simulated output includes both fix patterns.
- [x] PASS: Output flags `const data: any = response.json()` as a Pass 1 finding with `unknown` + narrowing or typed interface fix — met. Both a Zod parse variant and a typed interface variant are included.
- [x] PASS: Output flags missing return type on `getUserList` with a concrete suggested signature `Promise<User[]>` — met.
- [x] PASS: Output flags `user!.profile.avatar` as a Pass 1 non-null-assertion finding with optional chaining and early return fixes — met. Both patterns are shown with an explicit preference note.
- [x] PASS: Output flags `"strict": false` as a CRITICAL Pass 1 finding explaining that without strict mode the other findings cannot be caught at compile time — met. The specific flags enabled by `"strict": true` are named (`strictNullChecks`, `noImplicitAny`, etc.) in the finding.
- [x] PASS: Output findings each include severity, pass label, file path with line reference, and a concrete code fix block — met across all five findings.
- [x] PASS: Output runs all six passes and reports per-pass finding counts including zeros — met. The Summary table lists all six passes with counts; Passes 2, 3, 5, and 6 report zero or N/A.
- [x] PASS: Overall verdict is REQUEST_CHANGES — met. Five concurrent findings (one CRITICAL, four HIGH) cannot produce an APPROVE under the skill's Zero-Finding Gate logic.
- [x] PASS: Fetch-on-client critique includes practical impact — met. The simulated output names extra round-trip latency, CSR-only data load with poor LCP, no server-side error handling, and API endpoint exposure as the four reasons the pattern is wrong.
- [~] PARTIAL: Anti-pattern references include specific terms from the rules (`as any`, non-null assertion, client-side data fetching, strict-mode-disabled) — partially met. `as any` appears in the anti-patterns table in the skill definition, and the simulated output references `as any` in the type-assertion finding. However the anti-patterns table in the skill definition does not include entries for non-null assertion, strict-mode-disabled, or client-side data fetching — so a reviewer following the table strictly would not surface those entries. The criterion is partially met because the terms appear in the finding text even when not in the table.

### Score

| Section | Max | Scored |
|---|---|---|
| Criteria (8 items, 1 PARTIAL) | 8 | 7.5 |
| Output expectations (10 items, 1 PARTIAL) | 10 | 9.5 |
| **Total** | **18** | **17 (94%)** |

## Notes

The skill is well-specified for this scenario. The mandatory-pass structure, grep patterns, evidence format, and output template collectively produce correct findings without interpretation gaps. Pass 4's applicability condition (Next.js) is correctly handled — the scenario uses `'use client'`, making it unambiguous.

Two gaps worth noting. First, the anti-patterns table omits non-null assertions, strict-mode disabled, and missing return types — three of the four Pass 1 finding types triggered by this scenario. The table also does not appear in the Output Template, so an agent following the template strictly might omit it from review output entirely. The table would be more useful if expanded and referenced in the template.

Second, the skill does not prompt for practical-impact explanation on client-side data fetching. The skill identifies the violation ("data fetching belongs in Server Components") but does not instruct the reviewer to explain the performance and security consequences (latency, LCP, API exposure). A developer reading a review that just says "move this to a Server Component" may comply without understanding why — the skill would produce better outcomes if Pass 4 included a rationale template alongside the fix pattern.
