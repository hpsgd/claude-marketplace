# Test: Account review

Scenario: A CS manager needs to prepare for a QBR with an enterprise customer that has shown a significant usage drop over the past 6 weeks.

## Prompt


I need to prep for a QBR with Hartwell Manufacturing next week. They're one of our largest accounts — $420k ARR, 3-year contract, renewal comes up in 8 months.

Here's what I know:
- They have 340 licensed seats, but only 89 active users in the last 30 days (was 210 six weeks ago)
- Their champion, Sarah Kowalski (VP of Operations), went on maternity leave 6 weeks ago
- A new IT director started 2 months ago and has been "reviewing all software spend"
- They haven't logged a support ticket in 45 days (they used to log 8-12/month)
- They attended our last QBR but the exec sponsor didn't show up

What should I be doing, and what should this QBR cover?

## Criteria


- [ ] PASS: Identifies the health status as red or at-risk based on the signals — 57% usage drop, champion absence, new IT director reviewing spend, exec sponsor no-show
- [ ] PASS: Connects the usage drop to the champion's maternity leave (6 weeks aligns exactly) rather than treating it as a product problem
- [ ] PASS: Flags the new IT director as a risk and recommends a strategy to identify and engage this stakeholder before the QBR
- [ ] PASS: Does NOT recommend an expansion conversation — this account is unhealthy and expansion would be inappropriate per the CS agent's constraints
- [ ] PASS: Recommends specific pre-QBR actions: re-engaging day-to-day users, identifying who has backfilled Sarah's role, getting an exec sponsor confirmed before the meeting
- [ ] PASS: Frames the QBR agenda around value realised and risk mitigation — not a product demo or upsell
- [ ] PARTIAL: Recommends a health score review across all 5 dimensions — partial credit if health is assessed qualitatively but not scored across adoption/engagement/relationship/value/commercial dimensions
- [ ] PASS: Identifies the 8-month renewal timeline as creating urgency and recommends a recovery milestone before the renewal conversation
