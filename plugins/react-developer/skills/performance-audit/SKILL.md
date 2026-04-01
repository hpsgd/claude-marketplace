---
name: performance-audit
description: Audit a React/Next.js application or component for performance issues — bundle size, rendering, Core Web Vitals.
argument-hint: "[page, component, or directory to audit]"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep
paths:
  - "**/*.tsx"
  - "**/*.jsx"
---

Audit $ARGUMENTS for performance issues.

## Checks

- **Client bundle** — are large libraries pulled into the client? Should they be server-only?
- **Server vs Client Components** — are components marked `'use client'` that don't need to be?
- **Re-renders** — are components re-rendering unnecessarily? Check for missing memoisation, unstable references in props
- **Data fetching** — is data fetched at the right level? Waterfalls (sequential fetches that could be parallel)?
- **Images** — are images optimised? Using `next/image`? Appropriate sizes and formats?
- **Bundle splitting** — are dynamic imports used for heavy components? Code splitting at route level?
- **Tailwind** — are arbitrary values used where standard classes exist?

## Output

Present findings ranked by impact (high/medium/low) with specific file locations and fix recommendations.
