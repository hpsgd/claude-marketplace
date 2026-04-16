# Test: company-lookup skill

Scenario: a business analyst needs to research an unfamiliar company before a client meeting.

## Prompt

"Can you look up Palantir Technologies for me? I need to understand what they do, their business model, and any recent developments before a meeting tomorrow."

## Criteria

- [ ] PASS: Skill defines a clear trigger or usage context (when to invoke this skill)
- [ ] PASS: Skill specifies what sources to check (e.g. company website, LinkedIn, Crunchbase, news)
- [ ] PASS: Skill defines an output structure with named sections (not freeform)
- [ ] PASS: Output structure includes business model or "what they do" section
- [ ] PASS: Output structure includes financials or funding section
- [ ] PASS: Output structure includes recent news or developments section
- [ ] PARTIAL: Skill includes guidance on assessing source credibility or recency
- [ ] SKIP: Skill references collaboration with other agents (only relevant if plugin includes multiple agents)
