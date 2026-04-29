# Test: review-typescript any usage and client component misuse

Scenario: A developer submits a Next.js PR where a Client Component fetches data server-side work should handle, several `any` types appear without justification, and a non-null assertion is used on an optional value.

## Prompt

Review `app/dashboard/UserList.tsx`. It has `'use client'` at the top, then fetches user data with `const users = await fetch('/api/users').then(r => r.json())` inside the component. The return type of the exported `getUserList` function is missing. There's `const data: any = response.json()` and a `user!.profile.avatar` non-null assertion on line 47. The `tsconfig.json` has `"strict": false`.

## Criteria

- [ ] PASS: Skill executes all six mandatory passes — does not skip any pass including Next.js patterns (Pass 4)
- [ ] PASS: Data fetching inside a Client Component is flagged as a Pass 4 finding — data fetching belongs in Server Components
- [ ] PASS: `const data: any` is flagged as a Pass 1 type safety finding with the specific line as evidence
- [ ] PASS: Missing return type on exported `getUserList` function is flagged as a Pass 1 finding
- [ ] PASS: Non-null assertion (`user!.profile.avatar`) is flagged as a Pass 1 finding with the suggestion to use optional chaining or an early return
- [ ] PASS: `"strict": false` in tsconfig is flagged as a critical Pass 1 finding
- [ ] PASS: Each finding includes severity, pass label, file path with line reference, and a concrete code fix
- [ ] PARTIAL: Anti-patterns table at the end of the skill's output references the relevant anti-pattern for each finding type (as vs as any, etc.)

## Output expectations

- [ ] PASS: Output flags the `'use client'` + data fetching combination in `app/dashboard/UserList.tsx` as a Pass 4 finding — with the fix being to convert to a Server Component (remove `'use client'`, move `await fetch` into the async server component body) or split into a server-fetched parent + client-rendered child
- [ ] PASS: Output flags `const data: any = response.json()` as a Pass 1 type-safety finding — with the fix using `unknown` and a Zod parse, or a typed response interface
- [ ] PASS: Output flags the missing return type on exported `getUserList` with a concrete suggested signature (e.g. `export async function getUserList(): Promise<User[]>`)
- [ ] PASS: Output flags `user!.profile.avatar` as a Pass 1 non-null-assertion finding — with the fix using optional chaining (`user?.profile?.avatar`) and an explicit fallback or early return
- [ ] PASS: Output flags `"strict": false` in `tsconfig.json` as a CRITICAL Pass 1 finding — explaining that without strict mode, the other type-safety findings can't be caught at compile time, and naming the specific strict flags required
- [ ] PASS: Output's findings each include severity, pass label, file path with line reference, and a concrete code fix block — not just descriptions
- [ ] PASS: Output runs all six mandatory passes including Next.js patterns (Pass 4) and reports per-pass finding counts even where zero
- [ ] PASS: Output's overall verdict is REQUEST_CHANGES — strict-off plus an `any` plus a non-null assertion plus client-component data fetching is too many type-safety violations for APPROVE
- [ ] PASS: Output's fetch-on-client critique includes the practical impact — extra round-trip latency, CSR-only data load (poor LCP), no server-side error handling, and exposes the API endpoint to clients
- [ ] PARTIAL: Output's anti-pattern references include the specific terms from the rules (`as any`, non-null assertion, client-side data fetching, strict-mode-disabled)
