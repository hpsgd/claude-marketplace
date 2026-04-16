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
