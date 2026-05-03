# Backlog Prioritisation

Scenario: A product manager has 8 feature requests from different stakeholders and needs help deciding what goes into the next sprint.

## Prompt

> I need help prioritising my backlog for next sprint. Here are 8 items that different stakeholders want:
> 
> 1. Dark mode — requested by 3 enterprise customers, CEO thinks it's important
> 2. CSV export — requested by finance team internally, affects ~200 customers per sales team
> 3. SSO/SAML integration — required by 2 enterprise deals worth $180k ARR, blocked in security review
> 4. Mobile app redesign — design team wants to do it, no customer request on record
> 5. API rate limit increase — 1 power user requested, unclear how many others are affected
> 6. Onboarding flow improvements — CS team says new users struggle, no data on where they drop off
> 7. Slack notifications — requested in user forum, 47 upvotes, unknown revenue impact
> 8. Performance improvements (page load) — engineering team flagged, P95 load time is 4.2s
> 
> Which ones should we do next sprint?
> 
> A few specifics for the response:
> 
> - **Open with 3 clarifying questions** at the top: (1) sprint capacity (story points / weeks), (2) team composition (full-stack vs frontend-heavy, devops capacity), (3) any commitments already made (CEO promised dark mode by date X? sales committed SSO to a specific deal?). State the questions, THEN proceed with the full RICE table and recommendation using stated assumptions (e.g. "assuming 2-week sprint, full-stack team of 4, no hard commitments — adjust if these are wrong"). Do NOT defer the analysis pending answers.
> - **Apply RICE** explicitly. Produce a scoring table with columns `Item | Reach (users) | Impact (1/2/3) | Confidence (% based on data quality) | Effort (weeks) | RICE = (R×I×C)/E`. Compute the RICE number for each item even when data is uncertain — flag uncertainty as low Confidence.
> - **Flag missing data per item**: name what data is needed (e.g. "Onboarding: need funnel drop-off data — currently 0% confidence on Reach"; "API rate limit: need affected-user count from logs").
> - **Three-way recommendation buckets** (label them explicitly): (1) **Ship next sprint** (likely SSO + a quick win), (2) **Do data work this sprint, ship next** (onboarding instrumentation), (3) **Do not pull in** (mobile redesign — no evidence).
> - **Frame as proposal, not directive**: end with "This is a proposal — please discuss with the team before committing. Headcount decisions and CEO/board commitments are out of scope for this analysis and should be factored in by the team."

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Three clarifying questions (answer these to refine the recommendations):

1. **Sprint capacity & team shape** — How many developers? What's your typical velocity (story points or weeks of work per sprint)? Do you have dedicated infra/devops capacity, or is that shared with full-stack work?

2. **Pre-existing commitments** — Has the CEO promised dark mode to customers by a specific date? Is the $180k SSO deal with a close date? Are there any sales commitments or board asks that override RICE?

3. **SSO security blocker** — What's the security review hold-up? Is it a showstopper that needs resolving first, or a "to-do before merge"?

---

## RICE analysis (stated assumptions):

**Assumptions:** 2-week sprint, 4 full-time developers (~40 story points available), ~5,000 active users, no prior commitments stated.

| Item | Reach (users) | Impact | Confidence | Effort | RICE | Notes |
|---|---|---|---|---|---|---|
| **Performance (page load)** | 5,000 | 3 | 80% | 3 wks | **4,000** | All users; metric is clear; bottleneck unknown |
| **Onboarding flow** | 1,000 | 3 | 20% | 1 wk discovery | **600** | Need funnel data first; high impact IF problem confirmed |
| **SSO/SAML** | 250 | 3 | 90% | 3.5 wks | **193** | Deal blocker for $180k; high confidence but effort-heavy |
| **CSV export** | 200 | 2 | 60% | 1.5 wks | **160** | Clear user base; mid-impact |
| **Dark mode** | 300 | 3 | 40% | 2.5 wks | **144** | Enterprise request + CEO signal; low adoption confidence |
| **Slack notifications** | 250 | 2 | 50% | 2 wks | **125** | Nice-to-have; 47 upvotes = public demand but unknown revenue impact |
| **Mobile redesign** | 5,000 | 1 | 10% | 5 wks | **100** | No customer signal; lowest confidence |
| **API rate limit** | 5 | 2 | 20% | 1 wk | **2** | Single user mentioned; unclear scope |

---

## Missing data (flag these before committing):

- **Performance**: *Root cause unknown.* Is it database queries, frontend rendering, network? Effort estimate is a wild guess (could be 1 week, could be 6). Do a profiling spike first (~2 days) to identify the bottleneck.
- **Onboarding**: *Zero data on where users drop off.* CS team says they struggle, but we don't know if it's signup UX, onboarding tutorial, or first action. Add Hotjar/session replay or funnel analytics this sprint, then ship next sprint.
- **Dark mode**: *Adoption rate unknown.* 3 enterprise customers want it, but will the other 97% of users use it? Set up a feature flag to measure adoption after launch.
- **API rate limit**: *Affected-user count unknown.* The request came from 1 power user. Are 10 others hitting the limit silently? Check API logs for 429 responses this week.
- **Slack notifications**: *Revenue impact unclear.* 47 upvotes is a signal, but does it drive retention? Is it a nice-to-have or a deal requirement?
- **Mobile redesign**: *No problem statement.* What's wrong with the current design? Add this to your next user research sprint.

---

## Recommendation buckets:

### Ship next sprint (top of RICE + non-negotiables):

**Performance + Onboarding discovery** (~18 points)
- Launch performance investigation spike (2–3 days of profiling)
- Instrument onboarding funnel (analytics + session replay)
- Leaves ~22 points for a quick win

**Quick wins to fill the gap:**
- **API rate limit** (1 week, 5 points) — quick config fix if it's just a threshold; ship while you understand it
- **CSV export** (1.5 weeks, 8 points) — straightforward, clear reach, fits into gap

**This gets you:** 40 points allocated, visibility into your two biggest unknowns (perf bottleneck, onboarding friction), and a customer-facing win (CSV).

---

### Do data work this sprint, ship next:

**Onboarding improvements** — CTA: Set up Hotjar/Amplitude to track signup-to-first-action funnel. Once you know *where* users drop off (signup form? tutorial? first feature discovery?), you can design a proper fix next sprint.

**Performance profiling** — CTA: Profile the app (Chrome DevTools, server-side APM). Identify the actual bottleneck (rendering? API latency? bundle size?). Then re-estimate the fix.

---

### Do not pull in this sprint:

- **Mobile redesign** (100 RICE, no customer signal) — Design team wants it, but there's no evidence it solves a problem. Add to roadmap contingent on user research.
- **Dark mode** (144 RICE, low confidence) — This is sticky. CEO interest + 3 enterprise asks is real, but it's not deal-blocking and adoption is uncertain. **Conditional:** If dark mode is a pre-requisite for a deal or CEO commitment, move it to Ship Next Sprint and bump CSV export instead.
- **Slack notifications** (125 RICE) — Nice-to-have. If you have extra capacity after the above, this is a good third choice.

---

## Decision factors for your team:

1. **Business opportunity vs. customer experience trade-off**: RICE says Performance wins. But SSO is deal-blocking $180k. How much headroom is in the budget if those deals slip?

2. **CEO priority signal**: "CEO thinks it's important" (dark mode) suggests there may be a customer or board ask not stated here. Confirm whether dark mode is a requirement or a preference.

3. **Infra complexity wildcard**: Performance could be 1 week or 6 weeks depending on the bottleneck. Don't commit to the full fix in this sprint — commit to the investigation sprint first.

4. **Data dependencies**: Onboarding and API rate limit both need data before you can build confidently. Adding 1 week of data work now prevents building the wrong thing.

---

**This is a proposal — discuss with your team before committing.** RICE scores the impact per unit of effort, but it doesn't know:
- Whether the CEO has customer commitments on dark mode
- Whether the SSO deal has a hard close date (if Jan 2027, maybe it's next sprint instead)
- Whether your team has a performance specialist on staff
- Whether your org has a data/analytics practice that can instrument onboarding quickly

Headcount decisions and board-level priorities are out of scope for RICE — the team should layer those on top.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/17.5 (83%) |
| Evaluated | 2026-05-03 |
| Target duration | 57143 ms |
| Target cost | $0.0649 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Asks clarifying questions before prioritising — at minimum: what problem are we solving, what does success look like, and what data exists on impact | PASS | Output opens with three explicit clarifying questions before any analysis: sprint capacity/team shape, pre-existing commitments (CEO/sales), and SSO security blocker status. Analysis then proceeds with stated assumptions. |
| c2 | Flags that RICE scoring cannot be completed without reach/impact data, and identifies which items are missing key data (e.g. onboarding flow drop-off data, API rate limit affected users) | PASS | Dedicated 'Missing data' section calls out specific gaps per item: 'Zero data on where users drop off' for Onboarding; 'The request came from 1 power user. Are 10 others hitting the limit silently? Check API logs for 429 responses' for API rate limit; 'Root cause unknown' for Performance. |
| c3 | Identifies SSO/SAML as likely highest priority given $180k ARR at risk and hard dependency | FAIL | SSO/SAML is ranked third in the RICE table (193) behind Performance (4,000) and Onboarding (600). The 'Ship next sprint' recommendation bucket contains Performance + Onboarding + CSV export + API rate limit — not SSO. SSO appears only in 'Decision factors' as a question: 'How much headroom is in the budget if those deals slip?' |
| c4 | Flags the mobile redesign as lacking customer evidence and questions whether it belongs in the sprint | PASS | RICE table notes 'No customer signal; lowest confidence' for mobile redesign. 'Do not pull in this sprint' bucket states: 'Design team wants it, but there's no evidence it solves a problem. Add to roadmap contingent on user research.' |
| c5 | Applies RICE or equivalent prioritisation framework — partial credit if framework is referenced but not fully scored due to missing data | PARTIAL | Full RICE table produced with all 8 items scored across Reach, Impact (1/2/3), Confidence (%), Effort (weeks), and computed RICE = (R×I×C)/E. Ceiling is PARTIAL by test design. |
| c6 | Distinguishes between items with revenue impact evidence (SSO, CSV export) and items with only social proof (dark mode, Slack notifications) | PASS | SSO noted as 'Deal blocker for $180k; high confidence' (90% Confidence). CSV export: 'Clear user base; mid-impact' (60%). Slack notifications: '47 upvotes = public demand but unknown revenue impact' (50%). Dark mode: 'low adoption confidence' (40%). |
| c7 | Recommends data gathering actions for items that cannot be scored yet (e.g. instrument onboarding funnel before building improvements) | PASS | Explicit data actions per item: Onboarding — 'Set up Hotjar/Amplitude to track signup-to-first-action funnel'; Performance — 'Profile the app (Chrome DevTools, server-side APM)'; API rate limit — 'Check API logs for 429 responses this week'; Dark mode — 'Set up a feature flag to measure adoption after launch'. |
| c8 | Produces a prioritised output with reasoning, not just a ranked list | PASS | Output includes RICE table with per-item notes, a Missing data section with context and actions, three labeled recommendation buckets with narrative reasoning, decision factors, and a closing framing statement. Far exceeds a bare ranked list. |
| c9 | Output ranks SSO/SAML as highest priority — citing the $180k ARR at risk, blocked-in-security-review status, and the pattern that enterprise SSO is a hard requirement (deals don't progress without it) — not a guess | FAIL | Performance ranks #1 in RICE (4,000). SSO ranks #3 (193). The Ship-next-sprint bucket recommends Performance + Onboarding investigation + CSV export + API rate limit. SSO does not appear in any recommendation bucket; it surfaces only as a decision-factor question about deal timing. |
| c10 | Output applies a RICE-style scoring with explicit numbers per item — Reach (users affected), Impact (1/2/3 scale), Confidence (% based on data quality), Effort (story points or weeks) — even when fields are uncertain, with the uncertainty flagged | PASS | RICE table has all required columns for all 8 items. Uncertainty is flagged inline (e.g., Mobile redesign 10% Confidence, API rate limit 20% Confidence with note 'Single user mentioned; unclear scope'). Formula (R×I×C)/E is stated in column header. |
| c11 | Output flags the Mobile App Redesign explicitly as having NO customer evidence — "design team wants this; no recorded customer request" — and questions whether it should be in the next sprint at all | PASS | 'Do not pull in this sprint' section: 'Mobile redesign (100 RICE, no customer signal) — Design team wants it, but there's no evidence it solves a problem.' RICE table also notes: 'No customer signal; lowest confidence'. |
| c12 | Output flags the Onboarding Flow Improvements as needing data BEFORE building — "no drop-off data; CS team's perception alone insufficient" — with a recommendation to instrument the funnel first (a 1-2 day data task) | PASS | 'Do data work this sprint, ship next' bucket: 'Set up Hotjar/Amplitude to track signup-to-first-action funnel. Once you know where users drop off, you can design a proper fix next sprint.' Missing data section: 'Zero data on where users drop off. CS team says they struggle, but we don't know if it's signup UX, onboarding tutorial, or first action.' |
| c13 | Output flags the API Rate Limit Increase as needing scope discovery — "1 power user requested; unclear how many others affected" — recommending a quick analytics query to size the impact before committing engineering time | PASS | Missing data section: 'The request came from 1 power user. Are 10 others hitting the limit silently? Check API logs for 429 responses this week.' RICE table Reach = 5 users with note 'Single user mentioned; unclear scope'. |
| c14 | Output's reasoning per item shows the source of the score — for items with revenue evidence (SSO $180k, CSV export ~200 customers), the math is shown; for items with social signal (Slack notifications 47 upvotes), the lack of revenue evidence is acknowledged | PASS | SSO: 'Deal blocker for $180k; high confidence but effort-heavy' (Reach 250, Impact 3, Confidence 90%). CSV: 'Clear user base; mid-impact' (Reach 200). Slack: '47 upvotes = public demand but unknown revenue impact' (Confidence 50%). Revenue evidence vs social signal distinction is explicit throughout. |
| c15 | Output asks at least 2-3 clarifying questions before the prioritisation — sprint capacity, team composition (full-stack vs frontend-heavy), any commitments already made — rather than assuming | PASS | Three clarifying questions before the analysis: Q1 covers sprint capacity and team shape (dev count, velocity, infra/devops capacity); Q2 covers pre-existing commitments (CEO dark mode date, SSO deal close date, board asks); Q3 covers SSO security blocker nature. |
| c16 | Output addresses Performance Improvements as a candidate for inclusion — p95 4.2s is a quantified problem with broad impact, but lacks a tied business outcome; output rates it medium priority pending a customer-impact view | PARTIAL | Output does address Performance (p95 4.2s mentioned implicitly via all-user Reach = 5,000 and 80% Confidence) and recommends a profiling spike. However it rates Performance #1 by RICE (4,000) — the highest of all 8 items — not medium priority. The criterion's expectation that it 'lacks a tied business outcome' and should be rated medium is not reflected. |
| c17 | Output's recommendation distinguishes "ship in next sprint" (likely SSO and a quick win) from "do data work now, ship next sprint" (onboarding instrumentation), from "do not pull in" (mobile redesign without evidence) | PARTIAL | Three explicitly labeled buckets exist: 'Ship next sprint', 'Do data work this sprint, ship next', and 'Do not pull in this sprint'. Structure matches the criterion. However SSO is absent from bucket 1 (Performance + CSV + API rate limit fill it instead), which was the expected content per the criterion's parenthetical '(likely SSO and a quick win)'. |
| c18 | Output does not unilaterally prioritise — frames the recommendation as a proposal to discuss with the team, since headcount and CEO-pet-feature politics are out of scope for the agent | PASS | Closing paragraph: 'This is a proposal — discuss with your team before committing.' Lists four things RICE doesn't know including CEO commitments and headcount. Final sentence: 'Headcount decisions and board-level priorities are out of scope for RICE — the team should layer those on top.' |

### Notes

The output is strong overall — it follows the requested structure (clarifying questions first, full RICE table, three-bucket recommendation, proposal framing), and excels at flagging missing data per item with specific remediation actions. The main gap is the treatment of SSO/SAML: despite the $180k ARR evidence and deal-blocking status, the output never ranks SSO as the highest priority. Performance dominates the RICE table (4,000 vs SSO's 193) and the 'Ship next sprint' bucket omits SSO entirely in favour of performance investigation + CSV export + API rate limit. This is a genuine prioritisation call the output gets wrong relative to c3 and c9. Secondarily, Performance is rated #1 rather than medium pending business-outcome data (c16), and the three-bucket structure is present but doesn't put SSO in bucket 1 as expected (c17). All other criteria — RICE mechanics, data flagging, mobile redesign dismissal, onboarding instrumentation recommendation, API rate limit scope discovery, and proposal framing — are fully met.
