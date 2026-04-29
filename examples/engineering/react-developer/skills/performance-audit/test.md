# Test: Performance audit of the reports dashboard page

Scenario: Developer invokes the performance-audit skill against the `/app/reports/` directory, which contains a dashboard page component with several data visualisations and a large dependency bundle.

## Prompt

Audit `src/app/reports/` for performance issues. The reports dashboard has been flagged as slow — Lighthouse shows LCP of 4.2s and the JS bundle on this page is unusually large. Users also report it feels sluggish when switching between report tabs.

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
