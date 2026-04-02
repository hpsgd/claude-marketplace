# Design Tokens: {{system_name}}

| Field | Value |
|---|---|
| **System** | {{system_name}} |
| **Version** | {{version}} |
| **Last Updated** | {{date}} |

## Colour Primitives

Reference only from semantic tokens, never directly in components.

| Token Name | Hex | Usage Notes |
|---|---|---|
| `color-blue-500` | `#3B82F6` | Primary blue |
| `color-neutral-0` | `#FFFFFF` | White |
| `color-neutral-900` | `#111827` | Near-black |
| `color-red-500` | `#EF4444` | Error red |
| `color-green-500` | `#22C55E` | Success green |
| `color-amber-500` | `#F59E0B` | Warning amber |

## Semantic Colour Tokens

Map primitives to usage. Override per theme.

| Token Name | Light Value | Dark Value | Usage |
|---|---|---|---|
| `color-text-primary` | `neutral-900` | `neutral-50` | Body text, headings |
| `color-text-secondary` | `neutral-600` | `neutral-400` | Supporting text |
| `color-bg-surface` | `neutral-0` | `neutral-900` | Card and panel backgrounds |
| `color-bg-page` | `neutral-50` | `neutral-950` | Page background |
| `color-border-default` | `neutral-200` | `neutral-700` | Default borders |
| `color-interactive-primary` | `blue-500` | `blue-400` | Buttons, links |
| `color-feedback-error` | `red-500` | `red-400` | Error states |
| `color-feedback-success` | `green-500` | `green-400` | Success states |

## Spacing Scale

| Token Name | Value | Usage |
|---|---|---|
| `space-1` | `0.25rem` (4px) | Tight inline spacing |
| `space-2` | `0.5rem` (8px) | Icon-to-label gap |
| `space-4` | `1rem` (16px) | Default padding, stack gap |
| `space-6` | `1.5rem` (24px) | Section padding |
| `space-8` | `2rem` (32px) | Card padding |
| `space-16` | `4rem` (64px) | Page-level spacing |

## Typography Scale

| Token Name | Font Family | Size | Weight | Line-Height | Letter-Spacing | Usage |
|---|---|---|---|---|---|---|
| `type-display` | `{{sans}}` | `2.25rem` | `700` | `1.2` | `-0.02em` | Hero headings |
| `type-heading-1` | `{{sans}}` | `1.5rem` | `600` | `1.3` | `-0.01em` | Page titles |
| `type-heading-2` | `{{sans}}` | `1.25rem` | `600` | `1.3` | `0` | Section headings |
| `type-body` | `{{sans}}` | `0.875rem` | `400` | `1.5` | `0` | Body text |
| `type-body-small` | `{{sans}}` | `0.75rem` | `400` | `1.5` | `0` | Captions, help text |
| `type-code` | `{{mono}}` | `0.8125rem` | `400` | `1.6` | `0` | Code blocks |

## Border Radius

| Token Name | Value | Usage |
|---|---|---|
| `radius-sm` | `0.25rem` (4px) | Badges, tags |
| `radius-md` | `0.5rem` (8px) | Buttons, inputs |
| `radius-lg` | `0.75rem` (12px) | Cards, dialogs |
| `radius-full` | `9999px` | Avatars, pills |

## Shadow / Elevation

| Token Name | Value | Usage |
|---|---|---|
| `shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Cards at rest |
| `shadow-md` | `0 4px 6px rgba(0,0,0,0.07)` | Dropdowns, hover |
| `shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, popovers |

## Breakpoints

| Token Name | Min-Width | Usage |
|---|---|---|
| `bp-sm` | `640px` | Large phones |
| `bp-md` | `768px` | Tablets |
| `bp-lg` | `1024px` | Desktops |
| `bp-xl` | `1280px` | Wide screens |

## Motion / Duration

| Token Name | Duration | Easing | Usage |
|---|---|---|---|
| `motion-fast` | `100ms` | `ease-out` | Hover, focus, micro-interactions |
| `motion-normal` | `200ms` | `ease-in-out` | Expand/collapse, fade |
| `motion-slow` | `350ms` | `ease-in-out` | Slide-in panels, modals |
| `motion-reduced` | `0ms` | -- | When `prefers-reduced-motion` is set |

## Usage Rules

1. **Never use primitives directly in components.** Always reference semantic tokens.
2. **Extending**: Add primitives first, then semantic mappings. Get design-system review before merging.
3. **Naming**: `{category}-{property}-{variant}` (e.g., `color-bg-surface`, `space-4`).
4. **Dark mode**: All semantic colour tokens must define both light and dark values.
5. **Accessibility**: All text/background pairings must meet WCAG 2.1 AA (4.5:1 body, 3:1 large text).
