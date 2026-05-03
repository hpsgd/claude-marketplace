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

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Here's my read, ranked by confidence:

**Do this sprint:**

1. **SSO/SAML (#3)** — $180k ARR is blocked right now. Enterprise deals have shelf life. This is the highest-ROI item and the answer is obvious once you see the number. Note: SAML is typically a 2–3 sprint effort; confirm you can ship *enough* to unblock the security review this sprint specifically.

2. **Performance (#8)** — 4.2s P95 is objectively bad (2s is the common threshold before users bail). It affects everyone silently, not just the people who complain. Engineering already has context, so scoping should be fast.

3. **CSV export (#2)** — ~200 customers is a real, countable number. Finance teams blocking on missing exports tend to escalate. Probably a contained build.

**Don't do this sprint:**

- **Dark mode (#1)** — CEO pressure without revenue attached is opinion, not signal. Park it unless the enterprise customers say it's blocking renewal.
- **Onboarding (#6)** — Right instinct, wrong action. You don't know *where* users drop off. Sprint 0 here is adding funnel instrumentation, not redesigning the flow. Redesigning blind will likely make it worse.
- **Slack notifications (#7)** — 47 forum upvotes is engagement, not revenue. Good signal to watch; weak signal to build from.
- **API rate limit (#5)** — One confirmed request, scope unknown. Needs a quick customer survey before committing sprint capacity.
- **Mobile redesign (#4)** — Zero customer demand, design-team push. Classic supply-side project. Don't do it.

**One flag:** before committing to SSO/SAML, verify whether the security review needs the feature *complete* or just a credible roadmap/architecture document. Sometimes that buys you the deal without a 3-sprint commitment.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 11.5/17.5 (66%) |
| Evaluated | 2026-05-01 |
| Target duration | 23729 ms |
| Target cost | $0.0951 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Asks clarifying questions before prioritising — at minimum: what problem are we solving, what does success look like, and what data exists on impact | FAIL | The output jumps directly into a prioritised ranking with no clarifying questions asked — no sprint capacity, no success metrics, no baseline data questions are raised before the recommendation. |
| c2 | Flags that RICE scoring cannot be completed without reach/impact data, and identifies which items are missing key data (e.g. onboarding flow drop-off data, API rate limit affected users) | PARTIAL | The output identifies missing data for onboarding ('you don't know where users drop off'), API rate limit ('One confirmed request, scope unknown'), and Slack notifications ('47 forum upvotes is engagement, not revenue'). However, RICE scoring is never mentioned or referenced by name. |
| c3 | Identifies SSO/SAML as likely highest priority given $180k ARR at risk and hard dependency | PASS | SSO/SAML is ranked #1 in 'Do this sprint' with the explicit rationale: '$180k ARR is blocked right now. Enterprise deals have shelf life. This is the highest-ROI item.' |
| c4 | Flags the mobile redesign as lacking customer evidence and questions whether it belongs in the sprint | PASS | 'Zero customer demand, design-team push. Classic supply-side project. Don't do it.' explicitly flags lack of customer evidence and excludes it. |
| c5 | Applies RICE or equivalent prioritisation framework — partial credit if framework is referenced but not fully scored due to missing data | FAIL | No framework is named or referenced. The output uses informal reasoning about revenue, user counts, and effort but never applies or names RICE or any equivalent prioritisation framework. |
| c6 | Distinguishes between items with revenue impact evidence (SSO, CSV export) and items with only social proof (dark mode, Slack notifications) | PASS | SSO gets '$180k ARR'; CSV gets '~200 customers is a real, countable number'; dark mode is 'CEO pressure without revenue attached is opinion, not signal'; Slack is '47 forum upvotes is engagement, not revenue.' |
| c7 | Recommends data gathering actions for items that cannot be scored yet (e.g. instrument onboarding funnel before building improvements) | PASS | Onboarding: 'Sprint 0 here is adding funnel instrumentation, not redesigning the flow.' API rate limit: 'Needs a quick customer survey before committing sprint capacity.' |
| c8 | Produces a prioritised output with reasoning, not just a ranked list | PASS | Each item in both 'Do this sprint' and 'Don't do this sprint' sections has explicit reasoning referencing data, deal risk, customer counts, or lack thereof. |
| c9 | Output ranks SSO/SAML as highest priority — citing the $180k ARR at risk, blocked-in-security-review status, and the pattern that enterprise SSO is a hard requirement (deals don't progress without it) — not a guess | PASS | '$180k ARR is blocked right now' (ARR + blocked status). 'confirm you can ship enough to unblock the security review this sprint specifically' references the security review. 'Enterprise deals have shelf life' implies hard dependency. Three elements substantively present. |
| c10 | Output applies a RICE-style scoring with explicit numbers per item — Reach (users affected), Impact (1/2/3 scale), Confidence (% based on data quality), Effort (story points or weeks) — even when fields are uncertain, with the uncertainty flagged | FAIL | No RICE-style scoring table or explicit numeric fields appear anywhere in the output. Reasoning is qualitative throughout. |
| c11 | Output flags the Mobile App Redesign explicitly as having NO customer evidence — 'design team wants this; no recorded customer request' — and questions whether it should be in the next sprint at all | PASS | 'Zero customer demand, design-team push. Classic supply-side project. Don't do it.' directly mirrors the criterion's requirement. |
| c12 | Output flags the Onboarding Flow Improvements as needing data BEFORE building — 'no drop-off data; CS team's perception alone insufficient' — with a recommendation to instrument the funnel first (a 1-2 day data task) | PASS | 'You don't know where users drop off. Sprint 0 here is adding funnel instrumentation, not redesigning the flow. Redesigning blind will likely make it worse.' |
| c13 | Output flags the API Rate Limit Increase as needing scope discovery — '1 power user requested; unclear how many others affected' — recommending a quick analytics query to size the impact before committing engineering time | PASS | 'One confirmed request, scope unknown. Needs a quick customer survey before committing sprint capacity.' Covers all elements of the criterion. |
| c14 | Output's reasoning per item shows the source of the score — for items with revenue evidence (SSO $180k, CSV export ~200 customers), the math is shown; for items with social signal (Slack notifications 47 upvotes), the lack of revenue evidence is acknowledged | PASS | SSO: '$180k ARR is blocked'; CSV: '~200 customers is a real, countable number'; Slack: '47 forum upvotes is engagement, not revenue'. Source of reasoning is explicit for each category. |
| c15 | Output asks at least 2-3 clarifying questions before the prioritisation — sprint capacity, team composition (full-stack vs frontend-heavy), any commitments already made — rather than assuming | FAIL | Zero clarifying questions appear in the output. The response proceeds directly to 'Here's my read, ranked by confidence:' with no preamble questions about capacity, team, or commitments. |
| c16 | Output addresses Performance Improvements as a candidate for inclusion — p95 4.2s is a quantified problem with broad impact, but lacks a tied business outcome; output rates it medium priority pending a customer-impact view | PARTIAL | Performance is addressed and ranked #2 in 'Do this sprint,' citing '4.2s P95 is objectively bad' and broad impact. However it is rated high (not medium), and the criterion's requirements — 'lacks a tied business outcome' and 'pending a customer-impact view' — are not mentioned. |
| c17 | Output's recommendation distinguishes 'ship in next sprint' (likely SSO and a quick win) from 'do data work now, ship next sprint' (onboarding instrumentation), from 'do not pull in' (mobile redesign without evidence) | PARTIAL | The output has a 'Do this sprint' / 'Don't do this sprint' binary. Onboarding is implicitly 'data work first' ('Sprint 0 here is adding funnel instrumentation') and mobile redesign is 'Don't do it.' The three-way distinction is present in substance but not labeled as a separate explicit category. |
| c18 | Output does not unilaterally prioritise — frames the recommendation as a proposal to discuss with the team, since headcount and CEO-pet-feature politics are out of scope for the agent | FAIL | The output is directive throughout: 'Do this sprint:' and 'Don't do this sprint:' with imperatives like 'Don't do it.' There is no framing as a proposal, no invitation to discuss with the team, and no acknowledgment of team-specific constraints like headcount or CEO politics. |

### Notes

The output is operationally strong on the object-level prioritisation: it correctly identifies SSO as #1, flags mobile redesign as evidence-free, recommends instrumentation before building onboarding improvements, and cleanly separates revenue evidence from social proof. Where it falls short is on the meta-level of the task: it skips clarifying questions entirely (c1, c15), applies no named or numerical prioritisation framework (c5, c10), presents itself as a directive verdict rather than a team proposal (c18), and overrates Performance improvements without noting the absence of a business outcome tie (c16). The biggest gaps — no clarifying questions and no RICE scoring — together account for most of the score loss.
