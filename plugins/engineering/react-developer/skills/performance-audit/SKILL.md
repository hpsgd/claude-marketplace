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

## Setup

**If code files are provided inline in the prompt:** Write them to disk at their stated paths before running any investigation commands. Investigation commands (grep, ls, wc) operate on files — they produce no output on text in the prompt.

## Process (sequential — every check is MANDATORY)

### Step 1: Bundle Analysis

**Goal:** Identify what is shipped to the client and whether it needs to be.

**Investigation commands:**
```bash
# Check bundle size (Next.js)
npx next info 2>/dev/null
ls -la .next/static/chunks/ 2>/dev/null | sort -k5 -rn | head -20

# Check for large dependencies in client bundles
grep -rn "from '" --include="*.tsx" --include="*.ts" | grep -v "node_modules\|test\|spec" | sed "s/.*from '//;s/'.*//" | sort | uniq -c | sort -rn | head -20

# Check package sizes
npx bundlephobia-cli <package-name> 2>/dev/null
```

**Checklist:**

| Issue | How to detect | Impact | Fix |
|---|---|---|---|
| Large libraries in client bundle | Import of moment, lodash (full), d3 in `'use client'` components | HIGH | Use date-fns, lodash-es/cherry-pick, lighter alternatives |
| Unused imports | Imported but not referenced | LOW-MEDIUM | Remove unused imports (tree-shaking catches some) |
| Full library imports | `import _ from 'lodash'` vs `import { map } from 'lodash-es'` | HIGH | Use named imports from ESM packages |
| Polyfills not needed | Targeting modern browsers but shipping IE polyfills | MEDIUM | Check browserslist config |
| Duplicate dependencies | Multiple versions of the same package | MEDIUM | `npm ls <package>` to find duplication |

**Rules:**
- Every client-side dependency must justify its bundle cost. If a 50KB library saves 10 lines of code, write the 10 lines
- Heavy computation libraries (zod, date-fns, chart.js) should be on the server or dynamically imported
- Tree-shaking only works with ESM. Check that imports use ESM paths

### Step 2: Server vs Client Component Analysis

**Goal:** Minimise the client-side JavaScript by keeping components on the server where possible.

```bash
# Find all 'use client' directives
grep -rn "'use client'" --include="*.tsx" --include="*.ts" | grep -v node_modules

# Find components that could be server components
# (no useState, useEffect, onClick, onChange, or browser APIs)
```

**Decision matrix:**

| Component uses | Server component? | Client component? |
|---|---|---|
| Only props, no state, no effects, no handlers | YES — keep on server | NO |
| `useState`, `useReducer` | NO | YES — `'use client'` required |
| `useEffect`, `useLayoutEffect` | NO | YES |
| Event handlers (`onClick`, `onChange`) | NO | YES |
| Browser APIs (`window`, `document`, `localStorage`) | NO | YES |
| Third-party library requiring browser | NO | YES |
| Data fetching (`fetch`, database query) | YES — prefer server | Possible but suboptimal |
| Static rendering of data | YES | NO |

**Common misplacements:**

| Pattern | Problem | Fix |
|---|---|---|
| Entire page marked `'use client'` | Ships all page code to client | Extract interactive parts into client components, keep page as server component |
| Layout component marked `'use client'` | All children become client components | Move interactivity to a small client wrapper |
| Data-fetching component marked `'use client'` | Fetches on client instead of server | Move fetch to server component, pass data as props |
| Provider wrapper forces `'use client'` up | Cascades client boundary upward | Wrap only the minimal tree that needs the context |

**Rules:**
- The `'use client'` boundary should be pushed as far DOWN the component tree as possible
- A server component can render a client component, but not vice versa
- Data fetching belongs in server components — never `useEffect` + `fetch` for initial data in Next.js App Router
- If a client component only needs one interactive element, extract that element into a tiny client component and keep the rest on the server

### Step 3: Re-Render Analysis

**Goal:** Components only re-render when their actual inputs change.

```bash
# Find potential re-render triggers
grep -rn "useMemo\|useCallback\|React.memo\|memo(" --include="*.tsx" --include="*.ts" | grep -v node_modules
grep -rn "useContext" --include="*.tsx" | grep -v node_modules
```

**Common re-render causes:**

| Cause | Detection | Fix |
|---|---|---|
| New object/array reference in props | `style={{ color: 'red' }}` or `items={data.filter(...)}` inline in JSX | Extract to variable or `useMemo` |
| New function reference in props | `onClick={() => handleClick(id)}` on every render | `useCallback` or extract handler |
| Context updates re-render all consumers | Large context with frequent updates | Split context by update frequency |
| Parent re-render cascades to all children | No memoisation boundary | `React.memo` on expensive children |
| State stored too high | Global state for local concerns | Move state closer to where it's used |

**Rules:**
- Do NOT add `useMemo`/`useCallback`/`React.memo` everywhere prophylactically. Only where measured re-renders cause visible jank
- Measure first with React DevTools Profiler — don't guess
- Context is NOT a re-render problem by default. It's a problem only when the context value changes frequently AND many consumers exist
- Prefer restructuring (moving state down, lifting content up) over memoisation

### Step 4: Data Fetching Patterns

**Goal:** No waterfalls, no over-fetching, no client-side fetches that could be server-side.

```bash
# Find data fetching patterns
grep -rn "useEffect.*fetch\|useQuery\|useSWR\|useInfiniteQuery\|getServerSideProps\|getStaticProps" --include="*.tsx" --include="*.ts" | grep -v node_modules
grep -rn "async function.*Page\|async function.*Layout\|export async" --include="*.tsx" | grep -v node_modules
```

**Waterfall detection:**

| Pattern | Problem | Fix |
|---|---|---|
| Sequential fetches in `useEffect` | Fetch A, wait, then fetch B | `Promise.all([fetchA(), fetchB()])` |
| Parent fetches, child fetches on mount | Child waits for parent render before starting its fetch | Parallel fetch in parent, pass data as props |
| Client-side fetch after server render | Empty shell rendered, then data filled in | Move fetch to server component |
| N+1 fetches in a list | One fetch per list item | Batch into single query, use DataLoader pattern |

**Rules:**
- In Next.js App Router, fetch data in server components with `async/await` — not in client components with `useEffect`
- **`useEffect` + `fetch` for initial page data is a HIGH finding** in Next.js App Router — it causes an empty shell render before data loads, directly harming LCP
- Parallel fetches: `const [a, b] = await Promise.all([fetchA(), fetchB()])`
- Deduplicate identical requests — Next.js auto-deduplicates `fetch`, but custom calls need manual dedup
- Cache appropriately — `unstable_cache` for expensive computations, `revalidate` for time-based freshness
- Never fetch in `useEffect` for data that's known at request time

### Step 5: Image Optimisation

**Goal:** Images are right-sized, right-format, and lazy-loaded.

```bash
# Find image usage
grep -rn "<img\|<Image\|background-image\|backgroundImage" --include="*.tsx" --include="*.css" | grep -v node_modules
```

**Checklist:**

| Check | Pass | Fail |
|---|---|---|
| Using `next/image` | `<Image>` component with `width`/`height` or `fill` | Raw `<img>` tags without optimisation |
| `sizes` attribute | `sizes="(max-width: 768px) 100vw, 50vw"` | Missing `sizes` (serves full-width image to all viewports) |
| Priority for LCP image | `priority` prop on the largest above-the-fold image | LCP image lazy-loaded |
| No layout shift | `width`/`height` provided or `fill` with aspect-ratio container | Images pop in and shift content |
| Format | WebP/AVIF via `next/image` automatic optimisation | Unoptimised PNG/JPEG served directly |
| Lazy loading | Default in `next/image` (or explicit `loading="lazy"`) | All images loaded eagerly |

**Rules:**
- Every `<img>` should be a `<Image>` from `next/image` (or equivalent optimisation)
- The LCP (Largest Contentful Paint) image gets `priority` — never lazy-loaded
- `sizes` attribute is mandatory for responsive images — without it, the browser downloads the largest size
- SVGs used for icons and illustrations — not for photos
- Large hero images: consider `placeholder="blur"` with `blurDataURL`

### Step 6: Code Splitting

**Goal:** Only load the JavaScript needed for the current view.

```bash
# Find dynamic imports
grep -rn "dynamic(\|lazy(\|import(" --include="*.tsx" --include="*.ts" | grep -v node_modules

# Find large components that should be split
wc -l **/*.tsx 2>/dev/null | sort -rn | head -20
```

**Candidates for dynamic import:**

| Component type | Why split | Example |
|---|---|---|
| Modals/dialogs | Not visible on page load | `const Modal = dynamic(() => import('./modal'))` |
| Charts/graphs | Heavy library, below the fold | `const Chart = dynamic(() => import('./chart'), { ssr: false })` |
| Rich text editors | Very large bundle, interactive only | `dynamic(() => import('./editor'), { ssr: false })` |
| Admin panels | Rarely accessed by most users | Route-based splitting (automatic in Next.js) |
| Heavy form components | Only visible after user interaction | Dynamic import on interaction trigger |

**Rules:**
- Route-level splitting is automatic in Next.js — don't manually split at the page level
- Dynamic import components that are below the fold, behind interactions, or conditionally shown
- Use `{ ssr: false }` for components that require browser APIs
- Provide a loading fallback: `dynamic(() => import('./x'), { loading: () => <Skeleton /> })`
- Do NOT split tiny components — the network overhead of a separate chunk exceeds the savings

### Step 7: Tailwind and CSS Audit (MANDATORY — report even if no findings)

```bash
# Find arbitrary Tailwind values (code smell)
grep -rn "\[.*px\]\|\[.*rem\]\|\[.*em\]\|\[.*%\]\|\[#" --include="*.tsx" | grep "className" | grep -v node_modules
```

**Checklist:**

| Issue | Impact | Fix |
|---|---|---|
| Arbitrary values (`w-[347px]`) | Breaks design system consistency | Use standard Tailwind scale values |
| Inline styles | Not purged, not responsive, not themeable | Convert to Tailwind classes |
| Unused CSS | Larger stylesheet | Tailwind purges automatically in production — verify build config |
| `@apply` overuse | Defeats Tailwind's utility model | Use `@apply` only for base element styles, not component classes |

## Impact Scoring

Rank every finding by impact:

| Level | Criteria | Examples |
|---|---|---|
| **HIGH** | Affects Core Web Vitals (LCP, CLS, INP), visible to users, measurable | Large client bundle, waterfall data fetching, unoptimised LCP image |
| **MEDIUM** | Measurable performance impact but not immediately visible | Unnecessary re-renders, missing code splitting, suboptimal caching |
| **LOW** | Minor inefficiency, cosmetic, or developer experience only | Arbitrary Tailwind values, unused imports, missing `useMemo` on cheap computation |

## Output Format

The output MUST follow this exact structure. Each of the 7 audit steps gets its own `## Step N` section, even when no findings emerge in that step (write `No findings — verified clean.` for empty steps). Do NOT collapse steps into a flat priority-grouped findings list.

```markdown
## Performance Audit: [scope]

### Summary
- **Critical issues:** [count]
- **High impact:** [count]
- **Medium impact:** [count]
- **Low impact:** [count]

### Findings Table

| # | Impact | Category | Finding | Location | Recommendation |
|---|---|---|---|---|---|
| 1 | HIGH | Bundle | moment.js (300KB) in client bundle | `src/utils/date.ts:1` | Replace with date-fns (20KB) |
| 2 | HIGH | Data fetching | Waterfall: 3 sequential fetches | `src/app/page.tsx:15-25` | Use `Promise.all()` |
| 3 | MEDIUM | Server/Client | Dashboard page entirely `'use client'` | `src/app/dashboard/page.tsx:1` | Extract interactive widget to client component |

### Quick Wins
[Numbered list of the top 3 high-impact, low-effort fixes from the table above. Even if there are fewer than 3 quick wins, label this section explicitly.]

---

## Step 1 — Bundle Analysis
[Findings or "No findings — bundle within budget, no oversized libraries observed."]

## Step 2 — Server vs Client Component Analysis
[Findings or "No findings — `'use client'` boundaries are pushed as deep as practical." For each `'use client'` location, state whether the boundary could be pushed deeper (e.g. by isolating an interactive child as the only client component).]

## Step 3 — Re-Render Analysis
[Findings or "No findings — no unnecessary re-renders observed." When state lives in a parent and is consumed by sibling components, trace whether the state change triggers re-renders of unrelated siblings (e.g. `setActiveTab` re-rendering hero, nav, and inactive panels). State the answer either way.]

## Step 4 — Data Fetching Patterns
[Findings or "No findings — fetches are server-side or batched."]

## Step 5 — Image Optimisation
[Findings or "No findings — images use `next/image` with appropriate `priority`/`sizes`." For the LCP image specifically, missing `priority` is a HIGH finding.]

## Step 6 — Code Splitting
[Findings or "No findings — split points align with route boundaries." For each `dynamic(...)` recommendation, name the package and approximate KB saved.]

## Step 7 — Tailwind/CSS Audit
[Findings or "No findings — Tailwind class usage is conventional, no `@apply` overuse, no arbitrary values, purge config verified."]

---

### Detailed Analysis
[For each HIGH finding: current behaviour, measured impact, specific fix with code example.]

### Recommendations (prioritised)
1. [Highest impact fix]
2. [Second highest]
3. [Third highest]
```

## Related Skills

- `/react-developer:component-from-spec` — when performance issues require rebuilding a component, use the component spec skill to design the replacement.
