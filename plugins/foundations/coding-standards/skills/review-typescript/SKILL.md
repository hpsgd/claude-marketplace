---
name: review-typescript
description: Review TypeScript and Next.js code against team conventions. Auto-invoked when reviewing .ts/.tsx files.
allowed-tools: Read, Grep, Glob, Bash
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

Review TypeScript and Next.js code against team standards. This is the complete TypeScript review methodology — every check has a specific grep or read pattern, and every finding requires evidence.

## Mandatory Process

Execute all six passes. Do not skip. Mark each pass complete as you finish it.

### Pass 1: Type Safety

The type system exists to catch bugs at compile time. Every `any` defeats that purpose.

1. **`any` usage** — grep for `: any`, `as any`, `<any>`, `any[]`, `any)`, `Record<string, any>`:
   ```bash
   grep -rn '\bany\b' --include='*.ts' --include='*.tsx' [changed files]
   ```
   Every hit is a finding unless it meets one of these exceptions:
   - Third-party library with no type definitions (must have a comment explaining)
   - Generic constraint where `unknown` genuinely breaks the contract (rare — explain why)
   - Generated code from a code generator that outputs `any`

   The fix is always one of: use `unknown` and narrow, define a specific type, or use a generic parameter.

2. **Missing explicit return types on exports** — every exported function and method must have an explicit return type. This prevents accidental API changes.
   ```bash
   grep -rn 'export.*function\|export.*=.*=>' --include='*.ts' --include='*.tsx' [changed files]
   ```
   Then read each match and verify the return type is specified. Arrow functions assigned to exported `const` also need return types.

3. **Type assertions (`as`)** — grep for `as [A-Z]` in changed files. Each assertion is a potential lie to the compiler:
   - `as unknown as X` — almost always wrong. Find the real type.
   - `as X` where a type guard or narrowing would work — prefer narrowing.
   - `as const` — acceptable, not a finding.

4. **Non-null assertions (`!`)** — grep for patterns like `variable!.`, `array![0]`, `result!`:
   ```bash
   grep -rn '[a-zA-Z]!\.' --include='*.ts' --include='*.tsx' [changed files]
   ```
   Each is a finding. Replace with proper null checks, optional chaining, or early returns.

5. **Strict mode compliance** — verify `tsconfig.json` has `"strict": true`. If the project does not use strict mode, flag it as a critical finding.

### Pass 2: Import Hygiene

1. **Import order** — imports must follow this grouping (separated by blank lines):
   - External packages (`react`, `next`, `lodash`)
   - Internal packages (`@org/shared`, `@/lib`)
   - Relative imports (`./`, `../`)

2. **Type-only imports** — when importing something used only as a type, use the inline `type` keyword:
   ```typescript
   // correct
   import { useState, type FC } from 'react';
   import { type User } from '@/types';

   // wrong — imports the value at runtime unnecessarily
   import { FC } from 'react';
   ```
   Grep for imported names and check if they appear only in type positions (`: Type`, `<Type>`, `as Type`, `extends Type`).

3. **Barrel exports** — component directories should use `index.ts` barrel files. But barrel files must not re-export everything from deep paths. Each barrel should export only the public API of that directory.

4. **No CommonJS** — grep for `require(`, `module.exports`, `exports.`:
   ```bash
   grep -rn 'require(\|module\.exports\|exports\.' --include='*.ts' --include='*.tsx' [changed files]
   ```
   Every hit is a finding. Use ESM `import`/`export` exclusively.

5. **Circular imports** — if you suspect a circular dependency (runtime errors, undefined values), trace the import chain. Two files importing from each other is always a finding.

### Pass 3: Naming Conventions

1. **Files**:
   - Components: `PascalCase.tsx` (e.g., `UserProfile.tsx`)
   - Non-component modules: `kebab-case.ts` (e.g., `api-client.ts`)
   - Private/internal files: underscore prefix (`_hero-section.tsx`, `_utils.ts`)
   - Test files: `[name].test.ts` or `[name].spec.ts`, colocated with source

2. **Exports**:
   - Types and interfaces: `PascalCase` (`UserProfile`, `ApiResponse`)
   - Functions: `camelCase` (`getUserById`, `formatDate`)
   - Constants: `UPPER_SNAKE_CASE` for true constants, `camelCase` for configuration objects
   - Enums: `PascalCase` name, `PascalCase` members
   - Boolean variables/props: `is`/`has`/`should`/`can` prefix (`isLoading`, `hasError`)

3. **Interfaces vs types**:
   - `interface` for object shapes that could be extended (props, API contracts)
   - `type` for unions, intersections, mapped types, utility types
   - Never use `interface` for unions. Never use `type` for a plain object shape that represents a contract.

### Pass 4: Next.js Patterns (if applicable)

Skip this pass if the project does not use Next.js.

1. **Server vs Client Components**:
   - Default is Server Component. Files must have `'use client'` only when they use hooks, event handlers, browser APIs, or state.
   - Grep for `'use client'` and verify each file actually needs it. A file that imports `useState` or `useEffect` needs it. A file that only renders props does not.
   - Data fetching belongs in Server Components. If a Client Component fetches data, that is a finding.

2. **No client-side data operations**:
   - Filtering, sorting, and pagination must happen server-side (database query or API).
   - Grep for `.filter(`, `.sort(`, `.slice(` on data arrays in Client Components. Each hit on a dataset (not a small static array) is a finding.

3. **Server Actions** — prefer server actions over API routes for mutations. Server actions colocate the mutation with the form.

4. **Image optimization** — use `next/image`, not raw `<img>` tags.

5. **Metadata** — pages should export `metadata` or `generateMetadata`, not set `<title>` manually.

### Pass 5: Styling (Tailwind)

Skip if the project does not use Tailwind.

1. **Arbitrary values** — grep for `[` in className strings: `text-[14px]`, `w-[327px]`, `bg-[#ff0000]`. Each is a finding unless no standard Tailwind class exists for that value.
2. **Inline styles** — `style=` attributes alongside Tailwind classes. Pick one approach.
3. **Responsive design** — changed UI components should handle `sm:`, `md:`, `lg:` breakpoints. If a component has no responsive modifiers and renders content, verify it works on mobile.
4. **Dark mode** — if the project supports dark mode, new UI must include `dark:` variants.

### Pass 6: Test Coverage

1. **Changed code has tests** — every new function, component, or API endpoint needs at least one test covering the happy path and one covering an error case.
2. **Coverage target** — 80%+ line coverage on changed files. Run or check coverage reports if available.
3. **Test quality** — tests should assert behavior, not implementation. Tests that mock everything and assert mock calls are fragile.
4. **Snapshot tests** — acceptable only for small, stable components. Large snapshot tests are findings — they pass until they don't, then everyone clicks "update."

## Anti-Patterns to Flag

| Pattern | Why it's wrong | Fix |
|---------|---------------|-----|
| `as any` | Defeats type checking | Use `unknown` + narrowing |
| `// @ts-ignore` | Hides real errors | Fix the type error or use `@ts-expect-error` with explanation |
| `useEffect` for derived state | Causes extra renders | Compute during render |
| `key={index}` on dynamic lists | Breaks reconciliation | Use stable unique ID |
| `export default` | Makes refactoring harder | Use named exports |
| `enum` for simple unions | Generates runtime code | Use `as const` union |

## Patterns to Encourage (Not Findings)

- Discriminated unions for state machines
- `satisfies` operator for type-safe object literals
- Zod schemas for runtime validation at boundaries
- Custom hooks extracting complex state logic
- Colocation of components, tests, and styles

## Evidence Format

```
### [SEVERITY] [Pass]: [Short description]

**File:** `path/to/file.tsx:42`
**Evidence:** [grep output or code showing the violation]
**Standard:** [which rule is violated]
**Fix:** [concrete code change]
```

## Output Template

```
## TypeScript Review

### Summary
- Files reviewed: N
- Type safety: X findings (Y `any`, Z missing return types)
- Import hygiene: X findings
- Naming: X findings
- Next.js patterns: X findings (or N/A)
- Styling: X findings (or N/A)
- Tests: X findings

### Findings
[grouped by severity: critical, important, suggestion]

### Clean Areas
[what was done well]
```

## Zero-Finding Gate

If everything passes, say so: "No findings. TypeScript review complete — all changed files comply with team standards." Do not invent issues.
