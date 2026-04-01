---
name: review-typescript
description: Review TypeScript and Next.js code against team conventions. Auto-invoked when reviewing .ts/.tsx files.
allowed-tools: Read, Grep, Glob, Bash
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

When reviewing TypeScript / Next.js code, check against these standards:

- No `any` types — must use `unknown` and narrow, or use a specific type
- Exported functions have explicit return types
- Interfaces for extendable object shapes, types for unions/intersections
- Imports grouped: external, internal, relative. Barrel imports for components
- Inline `type` keyword for type-only imports: `import { Foo, type Bar } from '...'`
- ESM only, no CommonJS
- Underscore prefix for private files (`_hero-section.tsx`)
- Server Components for data, Client Components for interactivity only
- No client-side filtering/sorting/pagination — server does the work
- Prefer standard Tailwind classes over arbitrary values
- Coverage target: 80%+ on changed files

For each violation found, report:
1. The file and line
2. Which standard is violated
3. A concrete suggestion for fixing it

Summarize findings grouped by severity: critical, important, suggestion.
