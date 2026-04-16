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
