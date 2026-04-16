# Test: Backlog prioritisation

Scenario: A product manager has 8 feature requests from different stakeholders and needs help deciding what goes into the next sprint.

## Prompt


I need help prioritising my backlog for next sprint. Here are 8 items that different stakeholders want:

1. Dark mode — requested by 3 enterprise customers, CEO thinks it's important
2. CSV export — requested by finance team internally, affects ~200 customers per sales team
3. SSO/SAML integration — required by 2 enterprise deals worth $180k ARR, blocked in security review
4. Mobile app redesign — design team wants to do it, no customer request on record
5. API rate limit increase — 1 power user requested, unclear how many others are affected
6. Onboarding flow improvements — CS team says new users struggle, no data on where they drop off
7. Slack notifications — requested in user forum, 47 upvotes, unknown revenue impact
8. Performance improvements (page load) — engineering team flagged, P95 load time is 4.2s

Which ones should we do next sprint?

## Criteria


- [ ] PASS: Asks clarifying questions before prioritising — at minimum: what problem are we solving, what does success look like, and what data exists on impact
- [ ] PASS: Flags that RICE scoring cannot be completed without reach/impact data, and identifies which items are missing key data (e.g. onboarding flow drop-off data, API rate limit affected users)
- [ ] PASS: Identifies SSO/SAML as likely highest priority given $180k ARR at risk and hard dependency
- [ ] PASS: Flags the mobile redesign as lacking customer evidence and questions whether it belongs in the sprint
- [ ] PARTIAL: Applies RICE or equivalent prioritisation framework — partial credit if framework is referenced but not fully scored due to missing data
- [ ] PASS: Distinguishes between items with revenue impact evidence (SSO, CSV export) and items with only social proof (dark mode, Slack notifications)
- [ ] PASS: Recommends data gathering actions for items that cannot be scored yet (e.g. instrument onboarding funnel before building improvements)
- [ ] PASS: Produces a prioritised output with reasoning, not just a ranked list
