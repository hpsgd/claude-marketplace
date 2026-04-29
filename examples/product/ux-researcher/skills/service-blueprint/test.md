# Test: Service blueprint

Scenario: Testing whether the service-blueprint skill requires both frontstage and backstage lanes, a line of visibility, failure point analysis, and improvement recommendations.

## Prompt


/ux-researcher:service-blueprint for our enterprise customer onboarding process — from contract signed to customer achieving first value, including everything our CS, solutions engineering, and support teams do behind the scenes.

## Criteria


- [ ] PASS: Skill requires a scope definition with a concrete start event and end outcome before mapping begins
- [ ] PASS: Skill maps all four required lanes: customer actions, frontstage employee actions, backstage employee actions, and support processes
- [ ] PASS: Skill explicitly draws the line of visibility separating what customers see from what they don't
- [ ] PASS: Skill includes a visibility audit — identifying what backstage work becomes visible to customers and whether that's intentional
- [ ] PASS: Skill requires failure point analysis with location, failure mode, customer impact, frequency, and root cause
- [ ] PASS: Skill requires each backstage action to have a trigger — no orphaned process steps
- [ ] PARTIAL: Skill requires duration estimates for backstage actions — partial credit if duration is mentioned as important but not required per step
- [ ] PASS: Skill produces prioritised improvement recommendations linked to specific failure points
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's scope explicitly defines start ("contract signed by enterprise customer") and end ("customer reaches first measurable value: e.g. first dashboard viewed by 5+ named users") — not abstract endpoints
- [ ] PASS: Output's blueprint has all four lanes — Customer Actions (what the customer does and sees), Frontstage Actions (CSM, AE, SE talking to the customer), Backstage Actions (internal handoffs, configuration work the customer never sees), Support Processes (systems that support both stages: CRM, Slack handoffs, Jira tickets)
- [ ] PASS: Output draws the line of visibility explicitly — separating frontstage (customer sees this) from backstage (customer doesn't) — so the blueprint clarifies what customers experience vs what's hidden
- [ ] PASS: Output's visibility audit identifies leaky abstractions — backstage work that becomes customer-visible (e.g. CSM forwarding internal Jira tickets, support staff CC'ing customer on internal threads) — flagged as either intentional or a process bug
- [ ] PASS: Output's failure point analysis lists concrete failure modes — e.g. "Day 5: SSO integration fails because Azure AD admin not yet identified; customer impact: blocked from inviting team; frequency: 30% of enterprise onboardings; root cause: SE doesn't request this in kickoff"
- [ ] PASS: Output's backstage actions each have a trigger — e.g. "Provisioning workflow triggered when contract signature webhook fires" — no orphaned process steps that "just happen"
- [ ] PASS: Output's improvements are tied to specific failure points — not "improve onboarding" but "to fix the SSO blocker (failure point #2): add 'Azure AD admin name' as a required field in the kickoff agenda"
- [ ] PASS: Output covers the three named teams — CS, solutions engineering, support — with clear ownership per backstage action; no ambiguity about who does what
- [ ] PASS: Output's customer-action lane includes their thinking / feeling / pain at each stage — service blueprint plus journey-map dimensions, since enterprise onboarding is emotionally heavy for the customer
- [ ] PARTIAL: Output addresses duration estimates per backstage action — how long each step typically takes (e.g. "SE config: 2-4 hours", "Provisioning: instant", "Customer's IT review: 1-3 weeks") so bottlenecks are visible
