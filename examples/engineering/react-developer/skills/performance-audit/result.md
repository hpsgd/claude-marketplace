# performance-audit: Performance audit of the reports dashboard page

Developer invokes the skill against `src/app/reports/` — a dashboard with data visualisations, a large JS bundle, and reported tab-switching sluggishness (Lighthouse LCP 4.2s).

## Prompt

> Audit `src/app/reports/` for performance issues. The reports dashboard has been flagged as slow — Lighthouse shows LCP of 4.2s and the JS bundle on this page is unusually large. Users also report it feels sluggish when switching between report tabs.

## Output

Skill invoked as `/react-developer:performance-audit src/app/reports/`

---

## Performance Audit: `src/app/reports/`

### Summary

| | Count |
|---|---|
| Critical issues | 0 |
| High impact | 4 |
| Medium impact | 3 |
| Low impact | 2 |

---

### Step 1: Bundle Analysis

**Commands run:**

```bash
ls -la .next/static/chunks/ | sort -k5 -rn | head -20
grep -rn "from '" src/app/reports --include="*.tsx" --include="*.ts" | grep -v "node_modules\|test\|spec" | sed "s/.*from '//;s/'.*//" | sort | uniq -c | sort -rn | head -20
```

**Findings:**

Chunk output shows `reports-[hash].js` at 892KB (gzipped: 287KB) — significantly above the 150KB recommended budget for a single route.

Import scan reveals:

| Package | Count | Gzipped size | Problem |
|---|---|---|---|
| `recharts` | 14 | ~180KB | Full library imported — `import { ... } from 'recharts'` includes tree-shaking barriers |
| `lodash` | 6 | ~71KB | Full CommonJS import: `import _ from 'lodash'` — not tree-shakeable |
| `date-fns` | 3 | ~18KB | Named imports — acceptable |
| `moment` | 1 | ~67KB | `import moment from 'moment'` in `src/app/reports/utils/formatDate.ts:1` — ships full locale data |

**Key finding:** `src/app/reports/utils/formatDate.ts` imports `moment` for a single `format()` call. `date-fns/format` would reduce this dependency to ~2KB.

---

### Step 2: Server vs Client Component Analysis

**Commands run:**

```bash
grep -rn "'use client'" src/app/reports --include="*.tsx" --include="*.ts"
```

**Output:**

```
src/app/reports/page.tsx:1:'use client'
src/app/reports/components/ReportTabs.tsx:1:'use client'
src/app/reports/components/charts/RevenueChart.tsx:1:'use client'
src/app/reports/components/charts/ConversionChart.tsx:1:'use client'
src/app/reports/components/charts/FunnelChart.tsx:1:'use client'
src/app/reports/components/filters/DateRangePicker.tsx:1:'use client'
```

**Analysis:**

`src/app/reports/page.tsx` is marked `'use client'` at line 1. Reading the file shows the page component calls `useEffect` to fetch report data on mount — but the page itself has no event handlers or browser APIs. The `'use client'` boundary exists only because the data fetch was written as a client-side hook.

The page containing all chart components is a client component, which means Recharts, Lodash, and all chart code ship to the client as a single blocking bundle.

`src/app/reports/components/filters/DateRangePicker.tsx` legitimately requires `'use client'` (uses `useState` and `onChange` handlers). This boundary is correct.

`ReportTabs.tsx` uses `useState` for active tab — legitimate.

---

### Step 3: Re-Render Analysis

**Commands run:**

```bash
grep -rn "useMemo\|useCallback\|React.memo\|memo(" src/app/reports --include="*.tsx"
grep -rn "useContext" src/app/reports --include="*.tsx"
```

**Output:**

No `useMemo`, `useCallback`, or `React.memo` calls found in the reports tree.

`useContext` found at `src/app/reports/components/ReportTabs.tsx:8` — reading the file shows `ReportsContext` holds the full reports dataset and re-provides it on every tab change. All three chart components consume this context directly.

**Analysis:**

Tab switching updates `activeTab` in `ReportTabs`, which calls the context setter with a new object reference on every switch. All three chart components (`RevenueChart`, `ConversionChart`, `FunnelChart`) are context consumers — they re-render on every tab switch regardless of whether their data changed. React DevTools profiling would confirm each chart re-renders 3× per tab switch even when the tab does not contain that chart.

The fix is not `useMemo` sprayed everywhere — it's restructuring: move the chart-specific data slice into props passed only to the relevant chart, removing the shared context dependency for data.

---

### Step 4: Data Fetching Patterns

**Commands run:**

```bash
grep -rn "useEffect.*fetch\|useQuery\|useSWR" src/app/reports --include="*.tsx" --include="*.ts"
grep -rn "async function.*Page\|export async" src/app/reports --include="*.tsx"
```

**Output:**

```
src/app/reports/page.tsx:14:  useEffect(() => {
src/app/reports/page.tsx:15:    fetch('/api/reports/summary').then(res => res.json()).then(setData)
src/app/reports/page.tsx:20:    fetch('/api/reports/revenue').then(res => res.json()).then(setRevenue)
src/app/reports/page.tsx:25:    fetch('/api/reports/conversion').then(res => res.json()).then(setConversion)
```

Three sequential `fetch` calls inside a single `useEffect` at `src/app/reports/page.tsx:14-28`. Each fetch waits for the previous to complete (waterfall). No `Promise.all`. No server-side fetch.

`export async function` not found in `src/app/reports/page.tsx` — confirms the page is not an async server component.

---

### Step 5: Image Optimisation

**Commands run:**

```bash
grep -rn "<img\|<Image\|background-image\|backgroundImage" src/app/reports --include="*.tsx" --include="*.css"
```

**Output:**

```
src/app/reports/components/ReportHeader.tsx:12:  <Image src="/reports-hero.png" width={1200} height={400} alt="Reports" />
src/app/reports/components/charts/EmptyState.tsx:8:  <img src="/empty-chart.svg" alt="" />
```

`ReportHeader.tsx` uses `next/image` — correct. However, no `priority` prop is present. The `reports-hero.png` at 1200×400px is the largest above-the-fold element and is almost certainly the LCP element Lighthouse is measuring at 4.2s. It is currently lazy-loaded (default Next.js behaviour without `priority`).

`EmptyState.tsx` uses a raw `<img>` for an SVG — acceptable for inline SVG, but should be checked for size.

---

### Step 6: Code Splitting

**Commands run:**

```bash
grep -rn "dynamic(\|lazy(\|import(" src/app/reports --include="*.tsx" --include="*.ts" | grep -v node_modules
wc -l src/app/reports/**/*.tsx | sort -rn | head -10
```

**Output:**

No dynamic imports found in `src/app/reports/`.

Line counts:
```
 312 src/app/reports/components/charts/RevenueChart.tsx
 287 src/app/reports/components/charts/ConversionChart.tsx
 241 src/app/reports/components/charts/FunnelChart.tsx
 198 src/app/reports/page.tsx
```

All three chart components load eagerly. `RevenueChart` and `ConversionChart` are not visible on the default tab — they load regardless of which tab the user opens. Dynamic imports with `{ ssr: false }` would defer Recharts instantiation for off-screen charts until the user switches to that tab.

---

### Step 7: Tailwind and CSS Audit

**Commands run:**

```bash
grep -rn "\[.*px\]\|\[.*rem\]\|\[.*%\]\|\[#" src/app/reports --include="*.tsx" | grep "className"
```

**Output:**

```
src/app/reports/components/charts/RevenueChart.tsx:34:  className="w-[624px] h-[312px]"
src/app/reports/components/filters/DateRangePicker.tsx:12:  className="mt-[18px] mb-[22px]"
```

Two instances of arbitrary values — minor. `w-[624px]` breaks responsiveness and should use `w-full` with a max-width container. `mt-[18px]` should use the nearest standard spacing token (`mt-4` = 16px or `mt-5` = 20px).

---

### Findings

| # | Impact | Category | Finding | Location | Recommendation |
|---|---|---|---|---|---|
| 1 | HIGH | Data fetching | Page fetches data in `useEffect` — three sequential fetches, no `Promise.all`, all client-side | `src/app/reports/page.tsx:14-28` | Convert page to async server component; use `Promise.all([fetchSummary(), fetchRevenue(), fetchConversion()])` at the server boundary |
| 2 | HIGH | Server/Client | Entire page marked `'use client'` due to `useEffect` fetch — ships all chart code to client unnecessarily | `src/app/reports/page.tsx:1` | Remove `'use client'` from page; move data fetch to server; `DateRangePicker` and `ReportTabs` keep their own `'use client'` boundaries |
| 3 | HIGH | Bundle | `moment` imported for a single `format()` call (67KB gzipped) | `src/app/reports/utils/formatDate.ts:1` | Replace `import moment from 'moment'` with `import { format } from 'date-fns'` |
| 4 | HIGH | Image | LCP image (`reports-hero.png`) lacks `priority` prop — lazy-loaded, causing 4.2s LCP | `src/app/reports/components/ReportHeader.tsx:12` | Add `priority` to the `<Image>` component; this should halve measured LCP |
| 5 | MEDIUM | Re-render | `ReportsContext` re-provides full dataset on every tab switch; all three charts re-render on every tab change | `src/app/reports/components/ReportTabs.tsx:8`, chart consumers | Restructure: pass chart-specific data slices as props rather than consuming shared context; no memoisation needed |
| 6 | MEDIUM | Code splitting | `RevenueChart` and `ConversionChart` load eagerly — Recharts instantiated on every page load even when those tabs aren't viewed | `src/app/reports/page.tsx` | Wrap off-screen charts in `dynamic(() => import('./charts/RevenueChart'), { ssr: false, loading: () => <Skeleton /> })` |
| 7 | MEDIUM | Bundle | Full lodash import (`import _ from 'lodash'`) — CommonJS, not tree-shakeable (71KB gzipped) | 6 files in `src/app/reports` | Replace with `import { pick, groupBy } from 'lodash-es'` or native equivalents |
| 8 | LOW | CSS | Arbitrary Tailwind values (`w-[624px]`, `mt-[18px]`) breaking design system tokens | `RevenueChart.tsx:34`, `DateRangePicker.tsx:12` | Use standard scale: `w-full max-w-2xl`, `mt-4` |
| 9 | LOW | Bundle | `import _ from 'lodash'` in `src/app/reports/utils/aggregations.ts` — only `groupBy` and `pick` are used | `src/app/reports/utils/aggregations.ts:1` | `import { groupBy, pick } from 'lodash-es'` or rewrite without lodash (both are 5-line functions) |

---

### Detailed Analysis

**Finding 1 + 2 — `useEffect` fetch + `'use client'` page (HIGH)**

Current behaviour: `page.tsx` marks itself `'use client'` because it calls `useEffect` to fetch three endpoints sequentially. The browser renders an empty shell, then fires three fetches in sequence — each waits for the previous. With a p95 API latency of ~300ms per call, the data waterfall alone costs ~900ms before any chart renders.

Fix:

```tsx
// src/app/reports/page.tsx — AFTER
export default async function ReportsPage() {
  const [summary, revenue, conversion] = await Promise.all([
    fetchSummary(),
    fetchRevenue(),
    fetchConversion(),
  ])

  return (
    <main>
      <ReportHeader />        {/* server component */}
      <ReportTabs             {/* 'use client' — owns tab state */}
        summary={summary}
        revenue={revenue}
        conversion={conversion}
      />
    </main>
  )
}
```

This removes `'use client'` from the page, moves the fetch to the server, runs all three in parallel, and eliminates the empty-shell render.

**Finding 4 — LCP image missing `priority` (HIGH)**

```tsx
// BEFORE
<Image src="/reports-hero.png" width={1200} height={400} alt="Reports" />

// AFTER
<Image src="/reports-hero.png" width={1200} height={400} alt="Reports" priority />
```

Adding `priority` preloads the image and removes it from the lazy-load queue. Based on the 4.2s LCP, this is likely to be the single highest-impact fix.

---

### Quick Wins

1. Add `priority` to `ReportHeader` image — one prop, likely halves LCP (Finding 4)
2. Replace `moment` with `date-fns/format` — removes 67KB from the bundle (Finding 3)
3. Replace `import _ from 'lodash'` with named lodash-es imports — removes 71KB (Finding 7)
4. Wrap `RevenueChart` and `ConversionChart` in `dynamic()` — defers Recharts until needed (Finding 6)

### Recommendations (prioritised)

1. Convert page to async server component with `Promise.all` fetches — eliminates 900ms+ data waterfall and removes unnecessary `'use client'` boundary (Findings 1 + 2)
2. Add `priority` to LCP image — directly addresses the 4.2s Lighthouse finding (Finding 4)
3. Replace moment + full lodash with ESM alternatives — removes ~140KB from the client bundle (Findings 3 + 7)
4. Dynamic-import off-screen chart components — defers Recharts for tabs not initially visible (Finding 6)
5. Restructure `ReportsContext` to pass chart data as props — fixes tab-switching re-render cascade without memoisation (Finding 5)

---

## Evaluation

| Verdict | Score | Evaluated |
|---|---|---|
| PASS | 14.5/15 (97%) | 2026-04-30 |

### Criteria

- [x] PASS: Skill performs all seven audit steps in order — bundle analysis, server vs client component analysis, re-render analysis, data fetching patterns, image optimisation, code splitting, and Tailwind/CSS — met: all seven steps present in sequence, each marked MANDATORY
- [x] PASS: Skill uses actual investigation commands — does not guess at findings — met: every step has concrete bash commands including `grep -rn "'use client'"` and `ls -la .next/static/chunks/`
- [x] PASS: Skill identifies the LCP image and checks whether it has the `priority` prop — met: Step 5 image checklist explicitly covers "Priority for LCP image" with the `priority` prop check and failure mode defined
- [x] PASS: Skill flags any data fetching in `useEffect` on a Next.js App Router page as a HIGH finding — met: Step 4 rules state "Never fetch in `useEffect` for data that's known at request time"; Impact Scoring maps client-side fetches to HIGH
- [x] PASS: Every finding is ranked HIGH/MEDIUM/LOW with rationale — met: Impact Scoring section defines criteria and examples for each level
- [x] PASS: Skill does not recommend `useMemo`/`useCallback` prophylactically — met: Step 3 rules explicitly state "Do NOT add `useMemo`/`useCallback`/`React.memo` everywhere prophylactically. Only where measured re-renders cause visible jank"
- [~] PARTIAL: Skill identifies whether `'use client'` boundaries are pushed as far down the component tree as possible — partially met: the rule is stated clearly and the decision matrix is present, but investigation commands only surface all `'use client'` occurrences; no automated heuristic distinguishes components that could be split further
- [x] PASS: Output includes a findings table with impact, category, location, and recommendation, plus a prioritised Quick Wins list — met: output format template defines exactly this structure

### Output expectations

- [x] PASS: Output's findings reference specific files in `src/app/reports/` with file:line citations — met: simulated output cites `page.tsx:14-28`, `ReportHeader.tsx:12`, `utils/formatDate.ts:1`, etc.
- [x] PASS: Output's bundle analysis names the actual heavy dependencies with import-replacement recommendations — met: moment (67KB), lodash full import (71KB), and recharts named with specific replacements
- [x] PASS: Output investigates `'use client'` directive placement and identifies components that could be split or pushed deeper — met: Step 2 decision matrix applied; `page.tsx` identified as incorrectly marked, `DateRangePicker` and `ReportTabs` confirmed as legitimate
- [x] PASS: Output flags `useEffect`-based data fetching at page level as HIGH priority with server component recommendation — met: Finding 1 rated HIGH with async server component + `Promise.all` fix
- [x] PASS: Output identifies the LCP image and verifies `priority` prop, with HIGH finding if missing — met: Finding 4 identifies `reports-hero.png` in `ReportHeader.tsx:12` as LCP candidate, rated HIGH
- [x] PASS: Output addresses the tab-switching sluggishness — investigates re-render patterns and identifies whether tab state causes the entire dashboard tree to re-render — met: Step 3 traces `ReportsContext` re-providing on tab switch causing all chart consumers to re-render; fix is structural (props not memoisation)
- [x] PASS: Output's findings each have an impact ranking with a one-sentence rationale, not bare severity labels — met: each finding in the table includes a description that explains why it has that impact level
- [x] PASS: Output does NOT recommend `useMemo` or `useCallback` prophylactically — met: re-render finding explicitly recommends structural restructuring over memoisation
- [x] PASS: Output uses real investigation commands shown — met: all commands are concrete and runnable (`grep -rn`, `ls -la .next/static/chunks/`, `wc -l`)
- [~] PARTIAL: Output identifies code-splitting opportunities specific to the reports tree with expected bundle size reduction — partially met: `RevenueChart` and `ConversionChart` identified as dynamic import candidates with correct `{ ssr: false }` pattern; no quantified bundle size reduction estimate provided (the skill's output template does not require this column)

### Notes

The skill is well-structured. Sequential mandatory steps with concrete commands prevent the common failure mode of speculative findings. The explicit prohibition on prophylactic `useMemo`/`useCallback` is a genuine quality signal — it requires the developer to measure before acting.

The partial on `'use client'` boundary detection is minor: the decision matrix gives a clear framework for manual assessment, but there is no grep heuristic that automatically identifies client components lacking the hooks that justify their boundary.

The partial on bundle size quantification is also minor. The skill identifies what to split and why; the output template does not require an "expected bundle size reduction" column, so findings remain qualitative on code splitting.
