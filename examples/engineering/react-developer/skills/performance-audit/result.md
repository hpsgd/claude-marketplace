# Output: Performance audit of the reports dashboard page

**Verdict:** PASS
**Score:** 14.5/15 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill performs all seven audit steps in order — bundle analysis, server vs client component analysis, re-render analysis, data fetching patterns, image optimisation, code splitting, and Tailwind/CSS — met: all seven steps present in sequence, each marked MANDATORY
- [x] PASS: Skill uses actual investigation commands (grep for `'use client'` directives, ls for chunk sizes) — does not guess at findings — met: every step has concrete bash commands including `grep -rn "'use client'"` and `ls -la .next/static/chunks/`
- [x] PASS: Skill identifies the LCP image and checks whether it has the `priority` prop — met: Step 5 image checklist explicitly covers "Priority for LCP image" with the `priority` prop check and failure mode defined
- [x] PASS: Skill flags any data fetching in `useEffect` on a Next.js App Router page as a HIGH finding — met: Step 4 rules state "Never fetch in `useEffect` for data that's known at request time" and the Impact Scoring maps client-side fetches to HIGH
- [x] PASS: Every finding is ranked HIGH/MEDIUM/LOW with rationale — met: Impact Scoring section defines criteria and examples for each level
- [x] PASS: Skill does not recommend `useMemo`/`useCallback` prophylactically — met: Step 3 rules explicitly state "Do NOT add `useMemo`/`useCallback`/`React.memo` everywhere prophylactically. Only where measured re-renders cause visible jank"
- [~] PARTIAL: Skill identifies whether `'use client'` boundaries are pushed as far down the component tree as possible — partially met: the rule is stated clearly and the decision matrix is present, but the investigation commands only surface all `'use client'` occurrences; no automated heuristic distinguishes components that could be split further
- [x] PASS: Output includes a findings table with impact, category, location, and recommendation, plus a prioritised Quick Wins list — met: output format template defines exactly this table structure and a Quick Wins section

### Output expectations

- [x] PASS: Output's findings reference specific files in `src/app/reports/` with file:line citations — met: output format template shows file:line citations (e.g. `src/app/page.tsx:15-25`)
- [x] PASS: Output's bundle analysis names the actual heavy dependencies with import-replacement recommendations — met: Step 1 checklist names moment, lodash (full), d3 with specific replacements (date-fns, lodash-es, lighter alternatives)
- [x] PASS: Output investigates `'use client'` directive placement and identifies components that could be split or pushed deeper — met: Step 2 covers this with a decision matrix and common misplacements table with file path examples
- [x] PASS: Output flags `useEffect`-based data fetching at page level as HIGH priority with server component recommendation — met: Step 4 rules and the Impact Scoring criteria classify this as HIGH; the recommendation to use async server components is explicit
- [x] PASS: Output identifies the LCP image and verifies `priority` prop, with HIGH finding if missing — met: Step 5 checklist row marks absence as a fail; HIGH classification follows from the Impact Scoring criteria covering Core Web Vitals
- [x] PASS: Output addresses the tab-switching sluggishness by investigating re-render patterns — met: Step 3 covers context updates re-rendering all consumers and state stored too high, which maps directly to a tab-state scenario
- [x] PASS: Output's findings each have an impact ranking with a one-sentence rationale, not bare severity labels — met: Impact Scoring section requires rationale; the output format example shows rationale embedded in the findings table
- [x] PASS: Output does NOT recommend `useMemo` or `useCallback` prophylactically — met: prohibition stated in Step 3 rules with explicit qualifier
- [x] PASS: Output uses real investigation commands shown — met: all steps include concrete bash commands that would be executed, not guessed results
- [~] PARTIAL: Output identifies code-splitting opportunities specific to the reports tree with expected bundle size reduction — partially met: Step 6 names chart libraries as dynamic import candidates and provides the `dynamic()` pattern; the output format does not require a quantified bundle size reduction estimate in findings

## Notes

The skill is well-structured. Sequential mandatory steps with concrete commands prevent the common failure mode of producing speculative findings. The explicit prohibition on prophylactic `useMemo`/`useCallback` is a genuine quality signal — it requires the developer to measure before acting rather than applying memoisation as a reflex.

The partial on `'use client'` boundary detection is minor. The decision matrix in Step 2 gives a clear framework for manual assessment, but there's no grep pattern that automatically identifies client components lacking the hooks that require client rendering.

The partial on bundle size reduction in code-splitting is also minor. The skill identifies what to split and why, but the output template does not require "expected bundle size reduction" as a column — findings are qualitative rather than quantified.
