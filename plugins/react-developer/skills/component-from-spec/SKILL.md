---
name: component-from-spec
description: Implement a React component from a design specification or component-spec output.
argument-hint: "[component spec, description, or reference to spec file]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
paths:
  - "**/*.tsx"
  - "**/*.jsx"
---

Implement a React component from the specification at $ARGUMENTS.

## Process

1. Read the spec completely — props, variants, states, responsive behaviour, accessibility
2. Check existing components for patterns to follow (atomic design level, styling approach, import patterns)
3. Implement the component following project conventions:
   - TypeScript with explicit prop types (`ComponentNameProps`)
   - `clsx` for conditional classes
   - Standard Tailwind classes (no arbitrary values)
   - `variant` prop for visual variants
   - All states handled (loading, error, empty, disabled)
4. Add accessibility: ARIA attributes, keyboard navigation, focus management
5. Write a co-located test file (`component-name.test.ts`)

## Output

The component file, its test file, and an export from the appropriate barrel.
