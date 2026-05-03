# Performance Audit

Scenario: Developer invokes the performance-audit skill against the `/app/reports/` directory, which contains a dashboard page component with several data visualisations and a large dependency bundle.

## Prompt

> Audit `src/app/reports/` for performance issues. The reports dashboard has been flagged as slow — Lighthouse shows LCP of 4.2s and the JS bundle on this page is unusually large. Users also report it feels sluggish when switching between report tabs.
> 
> Write the files below to disk at `src/app/reports/page.tsx` and `src/app/reports/charts.tsx`, then run investigation commands before writing findings.
> 
> Here is the code for the reports section:
> 
> ```tsx
> // src/app/reports/page.tsx
> 'use client';
> 
> import { useState, useEffect } from 'react';
> import moment from 'moment';
> import { RevenueChart, UsageChart, RetentionChart } from './charts';
> 
> type ReportData = {
>   revenue: { date: string; amount: number }[];
>   usage: { date: string; sessions: number }[];
>   retention: { cohort: string; week: number; rate: number }[];
> };
> 
> export default function ReportsPage() {
>   const [activeTab, setActiveTab] = useState<'revenue' | 'usage' | 'retention'>('revenue');
>   const [data, setData] = useState<ReportData | null>(null);
>   const [loading, setLoading] = useState(true);
> 
>   useEffect(() => {
>     fetch('/api/reports/summary')
>       .then(r => r.json())
>       .then(d => {
>         setData(d);
>         setLoading(false);
>       });
>   }, []);
> 
>   if (loading) return <div>Loading...</div>;
> 
>   return (
>     <div>
>       <div className="flex items-center gap-4 mb-8">
>         <img
>           src="/reports-hero.png"
>           alt="Reports dashboard"
>           width={1200}
>           height={400}
>           className="w-full rounded-lg"
>         />
>       </div>
>       <p className="text-sm text-gray-500">
>         Data as of {moment().format('MMMM Do YYYY, h:mm:ss a')}
>       </p>
>       <div className="flex gap-2 mb-4">
>         {(['revenue', 'usage', 'retention'] as const).map(tab => (
>           <button key={tab} onClick={() => setActiveTab(tab)}
>             className={activeTab === tab ? 'bg-blue-500 text-white px-4 py-2 rounded' : 'px-4 py-2 rounded border'}>
>             {tab}
>           </button>
>         ))}
>       </div>
>       {activeTab === 'revenue' && <RevenueChart data={data!.revenue} />}
>       {activeTab === 'usage' && <UsageChart data={data!.usage} />}
>       {activeTab === 'retention' && <RetentionChart data={data!.retention} />}
>     </div>
>   );
> }
> ```
> 
> ```tsx
> // src/app/reports/charts.tsx
> 'use client';
> 
> import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
> import moment from 'moment';
> 
> type RevenuePoint = { date: string; amount: number };
> type UsagePoint = { date: string; sessions: number };
> type RetentionPoint = { cohort: string; week: number; rate: number };
> 
> export function RevenueChart({ data }: { data: RevenuePoint[] }) {
>   const formatted = data.map(d => ({
>     ...d,
>     label: moment(d.date).format('MMM D'),
>   }));
>   return (
>     <ResponsiveContainer width="100%" height={300}>
>       <LineChart data={formatted}>
>         <XAxis dataKey="label" />
>         <YAxis />
>         <Tooltip />
>         <Line type="monotone" dataKey="amount" stroke="#3b82f6" />
>       </LineChart>
>     </ResponsiveContainer>
>   );
> }
> 
> export function UsageChart({ data }: { data: UsagePoint[] }) {
>   const formatted = data.map(d => ({
>     ...d,
>     label: moment(d.date).format('MMM D'),
>   }));
>   return (
>     <ResponsiveContainer width="100%" height={300}>
>       <BarChart data={formatted}>
>         <XAxis dataKey="label" />
>         <YAxis />
>         <Tooltip />
>         <Bar dataKey="sessions" fill="#10b981" />
>       </BarChart>
>     </ResponsiveContainer>
>   );
> }
> 
> export function RetentionChart({ data }: { data: RetentionPoint[] }) {
>   return (
>     <table className="w-full border-collapse">
>       <thead>
>         <tr>
>           <th>Cohort</th>
>           <th>Week</th>
>           <th>Retention</th>
>         </tr>
>       </thead>
>       <tbody>
>         {data.map((row, i) => (
>           <tr key={i}>
>             <td>{moment(row.cohort).format('MMM YYYY')}</td>
>             <td>{row.week}</td>
>             <td>{(row.rate * 100).toFixed(1)}%</td>
>           </tr>
>         ))}
>       </tbody>
>     </table>
>   );
> }
> ```
> 
> A few specifics for the response:
> 
> - **`useEffect` data fetching on an App Router page is always HIGH priority** — not Medium, not Secondary. Server components should fetch via async boundary; a `useEffect` fetch at the page level blocks LCP and creates a waterfall. Tag this finding HIGH explicitly.
> - **Run these Bash commands and show their output verbatim** in code blocks before stating findings (the source files exist in the workspace at `src/app/reports/`):
>   ```bash
>   grep -rn "'use client'" src/
>   grep -rn "useEffect" src/app/reports/
>   grep -rn "moment" src/
>   ls -la src/app/reports/
>   ```
>   Show actual command output, not paraphrased findings.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

---

## Command Output

```bash
$ grep -rn "'use client'" src/
src/app/reports/charts.tsx:1:'use client';
src/app/reports/page.tsx:1:'use client';

$ grep -rn "useEffect" src/app/reports/
src/app/reports/page.tsx:3:import { useState, useEffect } from 'react';
src/app/reports/page.tsx:18:  useEffect(() => {

$ grep -rn "moment" src/
src/app/reports/charts.tsx:4:import moment from 'moment';
src/app/reports/charts.tsx:13:    label: moment(d.date).format('MMM D'),
src/app/reports/charts.tsx:30:    label: moment(d.date).format('MMM D'),
src/app/reports/charts.tsx:57:            <td>{moment(row.cohort).format('MMM YYYY')}</td>
src/app/reports/page.tsx:4:import moment from 'moment';
src/app/reports/page.tsx:41:        Data as of {moment().format('MMMM Do YYYY, h:mm:ss a')}

$ ls -la src/app/reports/
total 16
drwxr-xr-x  4 martin  staff   128  3 May 17:07 .
drwxr-xr-x  3 martin  staff    96  3 May 17:07 ..
-rw-r--r--  1 martin  staff  1755  3 May 17:07 charts.tsx
-rw-r--r--  1 martin  staff  1766  3 May 17:07 page.tsx
```

---

## Performance Audit Findings

### HIGH Priority

**1. useEffect data fetch blocks LCP (page.tsx:18)**

The page-level `useEffect` that calls `/api/reports/summary` creates a request waterfall. The page renders, hydrates, then fetches — nothing displays to the user until the fetch completes. This is why LCP is 4.2s.

**Fix:** Convert `page.tsx` to a server component. Remove `'use client'`, make the component `async`, and fetch data at the component level. The data is then available before the page sends to the browser.

```tsx
// Instead of useEffect
async function ReportsPage() {
  const data = await fetch('/api/reports/summary').then(r => r.json());
  // render immediately with data
}
```

---

**2. moment library bloat (4 imports across 2 files)**

moment is a 70KB library (minified). You're using it 4 times for basic date formatting:
- `moment().format('MMMM Do YYYY, h:mm:ss a')` — current timestamp
- `moment(d.date).format('MMM D')` — date abbreviations (used twice)
- `moment(row.cohort).format('MMM YYYY')` — month/year abbreviations

**Fix:** Replace with native `Intl.DateTimeFormat` or `date-fns` (~13KB). For your use cases:

```tsx
// Current timestamp
new Date().toLocaleDateString('en-US', { 
  year: 'numeric', month: 'long', day: 'numeric', 
  hour: '2-digit', minute: '2-digit', second: '2-digit' 
})

// Date abbreviations
new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })

// Month/year abbreviations  
new Date(row.cohort).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
```

Removes 70KB from the bundle.

---

### MEDIUM Priority

**3. All charts imported upfront, only one visible (page.tsx:5, charts.tsx:1)**

You import `RevenueChart`, `UsageChart`, and `RetentionChart` unconditionally, plus recharts. Only one chart renders based on the active tab. The tab switch doesn't lazy-load; recharts is always in the bundle even when not needed.

**Fix:** Lazy-load charts with `React.lazy()` and `Suspense`:

```tsx
import { lazy, Suspense } from 'react';

const RevenueChart = lazy(() => import('./charts').then(m => ({ default: m.RevenueChart })));
const UsageChart = lazy(() => import('./charts').then(m => ({ default: m.UsageChart })));
const RetentionChart = lazy(() => import('./charts').then(m => ({ default: m.RetentionChart })));

// In render:
<Suspense fallback={<div>Loading chart...</div>}>
  {activeTab === 'revenue' && <RevenueChart data={data!.revenue} />}
  {activeTab === 'usage' && <UsageChart data={data!.usage} />}
  {activeTab === 'retention' && <RetentionChart data={data!.retention} />}
</Suspense>
```

Defers recharts bundle until a chart is actually needed.

---

**4. Image not using Next.js Image component (page.tsx:27)**

The hero image uses a raw `<img>` tag. Next.js Image provides automatic optimization, lazy-loading, and responsive sizing.

**Fix:**

```tsx
import Image from 'next/image';

<Image
  src="/reports-hero.png"
  alt="Reports dashboard"
  width={1200}
  height={400}
  className="w-full rounded-lg"
  priority // LCP image
/>
```

---

### LOW Priority

**5. 'use client' on charts.tsx is unnecessary if charts become lazy-loaded**

Once charts are lazy-loaded via `React.lazy()`, the chart components themselves still need `'use client'` (recharts is a client lib), but the page becomes a server component. No change needed if you fix #1 and #3.

---

## Summary

| Issue | Impact | Fix Effort | Est. LCP Gain |
|---|---|---|---|
| useEffect waterfall | Blocks rendering on page load | High | 2-3s |
| moment bloat | 70KB bundle | Low | 0.3s |
| All charts loaded | Bundle size | Medium | 0.5-1s |
| Image optimization | LCP metric + delivery | Low | 0.2-0.5s |

**The 4.2s LCP is dominated by the useEffect waterfall.** Moving to a server component fixes that immediately. The other issues compound to another 1-2s in bundle and image delivery.

### Artifacts written

#### `work/src/app/reports/charts.tsx`

```
'use client';

import { LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import moment from 'moment';

type RevenuePoint = { date: string; amount: number };
type UsagePoint = { date: string; sessions: number };
type RetentionPoint = { cohort: string; week: number; rate: number };

export function RevenueChart({ data }: { data: RevenuePoint[] }) {
  const formatted = data.map(d => ({
    ...d,
    label: moment(d.date).format('MMM D'),
  }));
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={formatted}>
        <XAxis dataKey="label" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="amount" stroke="#3b82f6" />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function UsageChart({ data }: { data: UsagePoint[] }) {
  const formatted = data.map(d => ({
    ...d,
    label: moment(d.date).format('MMM D'),
  }));
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={formatted}>
        <XAxis dataKey="label" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="sessions" fill="#10b981" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export function RetentionChart({ data }: { data: RetentionPoint[] }) {
  return (
    <table className="w-full border-collapse">
      <thead>
        <tr>
          <th>Cohort</th>
          <th>Week</th>
          <th>Retention</th>
        </tr>
      </thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i}>
            <td>{moment(row.cohort).format('MMM YYYY')}</td>
            <td>{row.week}</td>
            <td>{(row.rate * 100).toFixed(1)}%</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

```

#### `work/src/app/reports/page.tsx`

```
'use client';

import { useState, useEffect } from 'react';
import moment from 'moment';
import { RevenueChart, UsageChart, RetentionChart } from './charts';

type ReportData = {
  revenue: { date: string; amount: number }[];
  usage: { date: string; sessions: number }[];
  retention: { cohort: string; week: number; rate: number }[];
};

export default function ReportsPage() {
  const [activeTab, setActiveTab] = useState<'revenue' | 'usage' | 'retention'>('revenue');
  const [data, setData] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/reports/summary')
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <div className="flex items-center gap-4 mb-8">
        <img
          src="/reports-hero.png"
          alt="Reports dashboard"
          width={1200}
          height={400}
          className="w-full rounded-lg"
        />
      </div>
      <p className="text-sm text-gray-500">
        Data as of {moment().format('MMMM Do YYYY, h:mm:ss a')}
      </p>
      <div className="flex gap-2 mb-4">
        {(['revenue', 'usage', 'retention'] as const).map(tab => (
          <button key={tab} onClick={() => setActiveTab(tab)}
            className={activeTab === tab ? 'bg-blue-500 text-white px-4 py-2 rounded' : 'px-4 py-2 rounded border'}>
            {tab}
          </button>
        ))}
      </div>
      {activeTab === 'revenue' && <RevenueChart data={data!.revenue} />}
      {activeTab === 'usage' && <UsageChart data={data!.usage} />}
      {activeTab === 'retention' && <RetentionChart data={data!.retention} />}
    </div>
  );
}

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 13.0/17.0 (76%) |
| Evaluated | 2026-05-03 |
| Target duration | 31702 ms |
| Target cost | $0.0777 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill performs all seven audit steps in order — bundle analysis, server vs client component analysis, re-render analysis, data fetching patterns, image optimisation, code splitting, and Tailwind/CSS | FAIL | Tailwind/CSS is entirely absent. Re-render analysis (step 3) is not performed — the output conflates 'all charts loaded upfront' with sluggishness but never traces whether tab state causes a full dashboard re-render. Only four of the seven steps are meaningfully covered. |
| c2 | Skill uses actual investigation commands (grep for `'use client'` directives, ls for chunk sizes) — does not guess at findings | PASS | All four commands specified in the test prompt are shown verbatim with real output: `grep -rn "'use client'" src/`, `grep -rn "useEffect" src/app/reports/`, `grep -rn "moment" src/`, and `ls -la src/app/reports/`. Output is not paraphrased. |
| c3 | Skill identifies the LCP image and checks whether it has the `priority` prop | PASS | Finding #4 identifies the raw `<img>` at page.tsx:27 and explicitly recommends `<Image ... priority // LCP image />` in the fix snippet, confirming the priority prop is missing. |
| c4 | Skill flags any data fetching in `useEffect` on a Next.js App Router page as a HIGH finding (should be server component fetch) | PASS | Finding #1 is listed under the 'HIGH Priority' heading and explicitly states 'useEffect data fetch blocks LCP (page.tsx:18)' with a waterfall explanation and server component async fix. |
| c5 | Every finding is ranked HIGH/MEDIUM/LOW with rationale | PASS | All five findings are placed under HIGH, MEDIUM, or LOW section headings. Each includes a description of why it matters (e.g. 'request waterfall', '70KB library', 'Next.js Image provides automatic optimization'). The summary table also assigns Impact and Fix Effort labels. |
| c6 | Skill does not recommend `useMemo`/`useCallback` prophylactically — only where measured re-renders cause visible jank | PASS | Neither `useMemo` nor `useCallback` appears anywhere in the output. |
| c7 | Skill identifies whether `'use client'` boundaries are pushed as far down the component tree as possible | PARTIAL | Finding #5 notes that page.tsx should drop 'use client' (become a server component) and charts.tsx retains it for recharts. This covers the top-level boundary shift but does not analyse whether the boundary within charts.tsx could be pushed deeper (e.g. isolating each chart component individually). |
| c8 | Output includes a findings table with impact, category, location, and recommendation, plus a prioritised Quick Wins list | PARTIAL | A summary table exists with Issue, Impact, Fix Effort, and Est. LCP Gain columns. However, 'category' and 'location' columns are absent, and there is no separately labelled 'Quick Wins' list — the HIGH-first ordering is present but not explicitly marketed as Quick Wins. |
| c9 | Output's findings reference specific files in `src/app/reports/` (e.g. `src/app/reports/page.tsx`, `src/app/reports/charts.tsx`) — not generic 'the dashboard' — with file:line citations where applicable | PASS | Findings cite page.tsx:18, page.tsx:5, page.tsx:27, page.tsx:3, page.tsx:4, charts.tsx:1, charts.tsx:4 throughout the analysis. |
| c10 | Output's bundle analysis names the actual heavy dependencies (e.g. specific charting library, full lodash import vs cherry-picked, large date library) and gives import-replacement recommendations | PASS | Finding #2 names moment as ~70KB and provides exact native Intl.DateTimeFormat replacements for all three usage patterns. Finding #3 names recharts and recommends React.lazy() to defer it. |
| c11 | Output investigates `'use client'` directive placement and identifies any client component that could be split or pushed deeper into the tree, with file paths | PASS | The output identifies 'use client' in both page.tsx:1 and charts.tsx:1 via grep output, recommends removing it from page.tsx entirely (convert to server component), and notes charts.tsx retains it because recharts requires it. |
| c12 | Output flags any `useEffect`-based data fetching at the page level as HIGH priority, with the recommendation to move to a server component / `fetch` in async boundary | PASS | Finding #1 is explicit: 'HIGH Priority — useEffect data fetch blocks LCP (page.tsx:18)' and provides an async server component fix showing `async function ReportsPage()` with `await fetch(...)` instead of the useEffect. |
| c13 | Output identifies the LCP image (likely a hero or first chart) and verifies the `priority` prop on `next/image`, with a HIGH finding if missing | PARTIAL | The image is identified and the missing priority prop is called out with a fix code block. However, the finding is classified MEDIUM, not HIGH as required by the criterion. |
| c14 | Output addresses the tab-switching sluggishness — investigates re-render patterns and identifies whether tab state causes the entire dashboard tree to re-render or only the tab content | FAIL | Finding #3 attributes tab-switching sluggishness to all chart bundles loading upfront and recommends lazy-loading, but never analyses whether the `setActiveTab` state change triggers a full dashboard re-render vs. just the conditional chart slots. No re-render investigation is performed. |
| c15 | Output's findings each have an impact ranking (HIGH/MEDIUM/LOW) with a one-sentence rationale, not bare severity labels | PASS | Each finding has a section heading (HIGH/MEDIUM/LOW) and opens with a sentence explaining the impact, e.g. 'creates a request waterfall... nothing displays to the user until the fetch completes' and '70KB library (minified). You're using it 4 times for basic date formatting'. |
| c16 | Output does NOT recommend `useMemo` or `useCallback` prophylactically — only attached to specific measured re-render hot spots, with the supporting evidence (e.g. 'this list re-renders 50 times per tab change') | PASS | Neither useMemo nor useCallback appears anywhere in the output. |
| c17 | Output uses real investigation commands shown — `grep -r "'use client'"`, `ls -la .next/static/chunks`, bundle analyzer output — not guesses | PARTIAL | The grep commands are shown with real output. However, `ls -la .next/static/chunks` is not run (only `ls -la src/app/reports/` was run) and no bundle analyzer output is shown. The 70KB moment figure reads as training-data knowledge, not measured output. |
| c18 | Output identifies code-splitting opportunities specific to the reports tree (dynamic imports for charts that aren't visible until tab switch), with the expected bundle size reduction | PARTIAL | Finding #3 identifies React.lazy() for all three chart components and explains recharts is deferred until a chart is needed. The summary table estimates '0.5-1s' LCP gain but does not quantify the expected KB reduction from deferring the recharts bundle. |

### Notes

The output is strong on the core findings (useEffect waterfall correctly HIGH, moment bundle correctly named with replacements, file:line citations throughout, no prophylactic memoisation). Key gaps: Tailwind/CSS audit is entirely absent; re-render analysis for tab switching is conflated with bundle loading rather than traced through component state propagation; the LCP image finding is correctly identified but incorrectly ranked MEDIUM instead of HIGH; the findings table is missing category and location columns and has no Quick Wins section; and bundle sizing relies on training-data knowledge rather than running .next/static/chunks inspection or a bundle analyser.
