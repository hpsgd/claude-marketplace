---
description: Next.js and React conventions
paths:
  - "**/*.tsx"
  - "**/*.jsx"
  - "**/next.config.*"
---

# [Next.js](https://nextjs.org) & React Conventions

## Framework
- Next.js with App Router
- Server Components for data loading
- Client Components (`'use client'`) for interactivity only
- Server Actions (`'use server'`) for mutations
- Route Handlers for proxy endpoints and binary responses

## Component architecture (Atomic Design)
- Shared components in a UI library package, consumed as TypeScript source (no build step)
- App-specific components in `src/components/` following atomic design: atoms, molecules, organisms

```
src/components/
├── atoms/          # Smallest units: buttons, headings, badges
├── molecules/      # Composed atoms: cards, form groups, charts
├── organisms/      # Complex sections: headers, footers, page sections
└── index.ts        # Barrel re-exporting shared UI + local components
```

## Component conventions
- App-specific components: import via barrel `import { Button, Hero } from '@/components'`
- Shared UI library components: import directly from the package `import { Button } from '@org/ui'` (not via the app barrel)
- Combine type and value imports: `import { Component, type Props } from '@/components'`
- Component variants use `variant` prop (not `background`, `style`, etc.)
- `Button` renders `<Link>` when `href` is provided, `<button>` otherwise
- `ThemeImage` replaces all `dark:hidden` / `hidden dark:block` dual-Image patterns
- Props-based APIs for shared components — accept configuration, don't hardcode app-specific values

## File organisation
- Underscore prefix for private/non-route files: `_hero-section.tsx`, `_contact-action.ts`
- Page sections stay in route folders and compose shared components
- Path alias: `@/*` maps to `./src/*`

```
page-route/
├── page.tsx              # Page component with metadata, composes sections
├── _hero-section.tsx     # Section component
├── _other-section.tsx    # Other section components
├── _my-action.ts         # Server action ('use server')
```

## Content management
- Use [content-collections](https://www.content-collections.dev) for structured content with Zod schemas and MDX transforms
- Content in markdown files with frontmatter, accessed via typed helpers
- Numeric prefix ordering for ordered content: `01-first.md`, `02-second.md`
- `_index.md` for collection-level introductions
- `_summary.md` for section-level summary prose
- Token replacement (e.g., `THE COMPANY` → actual company name) in transforms

## Styling
- [Tailwind CSS](https://tailwindcss.com) via PostCSS
- Prefer standard Tailwind classes over arbitrary values: `py-18` not `py-[72px]`
- Class-based dark mode via `prefers-color-scheme`
- `clsx` for conditional classes

## [Storybook](https://storybook.js.org)
- Stories co-located alongside components
- Style guide as MDX docs pages in the UI library
- Style guide is the source of truth for visual and content decisions
- Shared theme CSS import in `.storybook/preview.ts`

## Links and navigation
- Always use `Link` from `next/link` for all links (internal and external). Never use native `<a>` tags
- Site config centralised in `src/config.ts` — use for URLs, social links, company name
- Environment variable overrides use `NEXT_PUBLIC_*` prefix

## Data patterns
- No client-side filtering, sorting, or pagination — server does the work
- Send `?page=`, `?size=`, `?q=` to the API and render what comes back
- URL search params for pagination/filter state (not `useState`) — survives refresh and back/forward
- Use `DebouncedSearch` for text filters (URL param → server refetch)
- Each paginated table uses a unique query param name to avoid collisions

## PDF generation ([react-pdf](https://react-pdf.org))

When generating PDFs server-side via `@react-pdf/renderer`:

- SVG icons: convert `.svg` files to react-pdf SVG primitives at render time (share icon source with web)
- Gradient headings: SVG text for short titles, native `Text` for long titles that need wrapping
- Markdown content: markdown → HTML via `marked` → react-pdf via `react-pdf-html`
- Two-pass TOC: `PageMarker` + `onPage` callback → `pageMap` for page numbers

### Layout pitfalls (react-pdf / react-pdf-html)

- **Blank overflow pages**: Last item's `mb-N` pushes past page boundary. Fix: `isLast` prop → `mb-0` on final item
- **Orphaned headings**: Heading at page bottom, body on next page. Fix: `wrap={false}` on title row, `minPresenceAhead={20}` to pull body text along
- **`render` prop in `fixed` containers**: Crashes with large number error. Fix: post-render page number stamping via pdf-lib
- **Table column widths ignored**: `react-pdf-html` overrides width. Fix: use `flex-basis` + `flex-grow:0` + `flex-shrink:0` instead of `width`

## SEO
- Dynamic sitemap generation
- Robots.txt configuration per app (allow/deny as appropriate)
- `metadata` export on page components
