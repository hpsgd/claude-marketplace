---
name: component-spec
description: Write a component specification — purpose, props, variants, states, responsive behaviour, and accessibility requirements.
argument-hint: "[component name or description]"
user-invocable: true
allowed-tools: Read, Glob, Grep
---

Write a component specification for $ARGUMENTS.

## Specification structure

### 1. Purpose
One sentence: what this component does and when to use it.

### 2. Props / API
| Prop | Type | Default | Description |
|---|---|---|---|
| `variant` | `'primary' \| 'secondary'` | `'primary'` | Visual variant |

### 3. Variants
Describe each visual variant and when to use it.

### 4. States
Document every state: default, hover, focus, active, disabled, loading, error, empty, selected.

### 5. Responsive behaviour
How the component adapts: breakpoints, layout changes, hidden/shown elements.

### 6. Accessibility
- Keyboard navigation (tab order, enter/space activation, escape to close)
- Screen reader behaviour (ARIA role, label, live regions)
- Colour contrast (minimum ratios)
- Focus management (where focus moves on open/close/action)

### 7. Usage examples
Show 2-3 usage patterns with props.
