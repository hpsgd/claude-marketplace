---
description: TypeScript coding conventions — applied to all .ts and .tsx files
paths:
  - "**/*.ts"
  - "**/*.tsx"
---

# TypeScript Conventions

## Language settings
- TypeScript ES2022, bundler module resolution, strict mode
- ESM throughout (`"type": "module"`)
- Key compiler options: `strict`, `strictNullChecks`, `noUncheckedIndexedAccess`, `noEmit`, `isolatedModules`
- Monorepo tsconfig pattern: root `tsconfig.json` extends `tsconfig.options.json` (shared compiler options), each workspace has its own tsconfig referenced via `references`

## Formatting
- Prettier — single quotes, `quoteProps: 'consistent'`, JSX single quotes, one attribute per line
- 2 spaces indentation, LF line endings, UTF-8, max line length 120
- Two Prettier presets: base (no plugins) for packages/libraries, tailwind (base + Tailwind class sorting + import organizing) for applications

## ESLint
- Shared ESLint configuration in a dedicated package with presets:
  - **base**: `typescript-eslint` `recommendedTypeChecked` + `eslint-config-prettier` + `projectService: true`
  - **nextjs**: base + `eslint-config-next` (core-web-vitals + typescript)
- Each project's `eslint.config.js` is a one-liner re-export: `export { default } from '@org/eslint-config/base'`
- Underscore-prefixed unused vars are allowed (`_myVar`)
- Ignores: `node_modules`, `dist`, `.next`, `.content-collections`

## Types
- Prefer `interface` over `type` for object shapes that may be extended
- Use `type` for unions, intersections, and mapped types
- Avoid `any` — use `unknown` when the type is truly unknown, then narrow
- Export types that are part of the public API; keep internal types unexported
- Combine type and value imports on one line using inline `type` keyword:
  `import { IconDetailSection, type IconDetailItem } from '@/components'`

## Naming
- PascalCase for types, interfaces, enums, and React components
- camelCase for variables, functions, and methods
- UPPER_SNAKE_CASE for true constants (compile-time known values)
- Prefix interfaces for React props with the component name: `ButtonProps`
- Underscore-prefixed unused vars are allowed (`_myVar`)

## Functions
- Prefer named function declarations over arrow functions for top-level exports
- Use arrow functions for callbacks and inline functions
- Add explicit return types to exported functions
- Keep functions focused — if a function does two things, split it

## Imports
- Group imports: external packages, then internal modules, then relative imports
- Use named imports over default imports where possible
- Avoid circular imports — if needed, restructure the module boundary
- Use barrel exports (`index.ts`) for component directories
- Use path aliases (`@/*` maps to `./src/*`) for non-co-located imports; relative imports for co-located files

## Module system
- ESM only — no CommonJS
- One-liner re-export configs where possible (e.g., `export { default } from '@org/eslint-config/base'`)

## Error handling
- Use typed errors or error classes rather than throwing strings
- Handle errors at the appropriate boundary — don't catch and re-throw without adding context
- Use Result/Either patterns for expected failure cases in utility functions
