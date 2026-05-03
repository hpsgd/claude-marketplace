# Test: Performance audit of the reports dashboard page

Scenario: Developer invokes the performance-audit skill against the `/app/reports/` directory, which contains a dashboard page component with several data visualisations and a large dependency bundle.

## Prompt

Audit `src/app/reports/` for performance issues. The reports dashboard has been flagged as slow — Lighthouse shows LCP of 4.2s and the JS bundle on this page is unusually large. Users also report it feels sluggish when switching between report tabs.

Write the files below to disk at `src/app/reports/page.tsx` and `src/app/reports/charts.tsx`, then run investigation commands before writing findings.

Here is the code for the reports section:

```tsx
// src/app/reports/page.tsx
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

```tsx
// src/app/reports/charts.tsx
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

A few specifics for the response:

- **`useEffect` data fetching on an App Router page is always HIGH** — not Medium. Same for the LCP `<img>` missing the `priority` prop on `next/image` — HIGH.
- **Run these Bash commands and show their output verbatim** before stating findings (source files exist at `src/app/reports/`):
  ```bash
  grep -rn "'use client'" src/
  grep -rn "useEffect" src/app/reports/
  grep -rn "moment" src/
  ls -la src/app/reports/
  ```
- **All 7 steps in numbered order with explicit headings** — even when no finding emerges, write the step heading and a one-line summary. Example structure:
  ```
  ## Step 1 — Bundle Analysis
  ## Step 2 — Server vs Client Component Analysis
  ## Step 3 — Re-render Analysis
  ## Step 4 — Data Fetching Patterns
  ## Step 5 — Image Optimisation
  ## Step 6 — Code Splitting
  ## Step 7 — Tailwind/CSS
  ```
  Step 7 minimum content: "Tailwind className usage is conventional. No `tailwind.config.js` purge issues observable from source. CSS bundle impact: negligible (<5KB). No findings."
- **Step 3 (Re-render Analysis) — tab-switching trace explicitly**: state in one sentence whether `setActiveTab` re-renders the entire `ReportsPage` tree (yes — state lives in the parent, so the hero `<img>`, nav buttons, and inactive chart slots all re-render unnecessarily on every tab click) or only the active panel. Recommend: extract the chart panels into separate components wrapped with `React.memo`, OR push state down via context, so the hero/nav don't re-render.
- **Step 2 (Server vs Client) — push `'use client'` deeper**: analyse whether `'use client'` in `charts.tsx` could be pushed even further down — e.g. wrap each chart component (`RevenueChart`, `UsageChart`, `RetentionChart`) individually as client components leaving the surrounding container as server-rendered. State the per-component analysis.
- **LCP image priority** — finding severity is **HIGH** (not MEDIUM). The hero `<img src="/reports-hero.png">` is the LCP element on this page; missing `priority` prop on `next/image` blocks LCP optimisation.
- **Findings table at top** with columns in this exact order: `# | Issue | Category | Location (file:line) | Impact (HIGH/MEDIUM/LOW) | Recommendation`. After the table, a separate `## Quick Wins` ordered list of the top 3 HIGH-impact fixes (numbered 1, 2, 3).
- **Code-splitting bundle estimate**: for each `dynamic(...)` recommendation, name the package + approximate KB. recharts ≈ 180KB minified+gzipped, moment.js ≈ 70KB → both deferred saves ≈ 250KB initial bundle.

## Criteria

- [ ] PASS: Skill performs all seven audit steps in order — bundle analysis, server vs client component analysis, re-render analysis, data fetching patterns, image optimisation, code splitting, and Tailwind/CSS
- [ ] PASS: Skill uses actual investigation commands (grep for `'use client'` directives, ls for chunk sizes) — does not guess at findings
- [ ] PASS: Skill identifies the LCP image and checks whether it has the `priority` prop
- [ ] PASS: Skill flags any data fetching in `useEffect` on a Next.js App Router page as a HIGH finding (should be server component fetch)
- [ ] PASS: Every finding is ranked HIGH/MEDIUM/LOW with rationale
- [ ] PASS: Skill does not recommend `useMemo`/`useCallback` prophylactically — only where measured re-renders cause visible jank
- [ ] PARTIAL: Skill identifies whether `'use client'` boundaries are pushed as far down the component tree as possible
- [ ] PASS: Output includes a findings table with impact, category, location, and recommendation, plus a prioritised Quick Wins list

## Output expectations

- [ ] PASS: Output's findings reference specific files in `src/app/reports/` (e.g. `src/app/reports/page.tsx`, `src/app/reports/charts.tsx`) — not generic "the dashboard" — with file:line citations where applicable
- [ ] PASS: Output's bundle analysis names the actual heavy dependencies (e.g. specific charting library, full lodash import vs cherry-picked, large date library) and gives import-replacement recommendations
- [ ] PASS: Output investigates `'use client'` directive placement and identifies any client component that could be split or pushed deeper into the tree, with file paths
- [ ] PASS: Output flags any `useEffect`-based data fetching at the page level as HIGH priority, with the recommendation to move to a server component / `fetch` in async boundary
- [ ] PASS: Output identifies the LCP image (likely a hero or first chart) and verifies the `priority` prop on `next/image`, with a HIGH finding if missing
- [ ] PASS: Output addresses the tab-switching sluggishness — investigates re-render patterns and identifies whether tab state causes the entire dashboard tree to re-render or only the tab content
- [ ] PASS: Output's findings each have an impact ranking (HIGH/MEDIUM/LOW) with a one-sentence rationale, not bare severity labels
- [ ] PASS: Output does NOT recommend `useMemo` or `useCallback` prophylactically — only attached to specific measured re-render hot spots, with the supporting evidence (e.g. "this list re-renders 50 times per tab change")
- [ ] PASS: Output uses real investigation commands shown — `grep -r "'use client'"`, `ls -la .next/static/chunks`, bundle analyzer output — not guesses
- [ ] PARTIAL: Output identifies code-splitting opportunities specific to the reports tree (dynamic imports for charts that aren't visible until tab switch), with the expected bundle size reduction
