# Test: Component design

Scenario: A product team needs a multi-step onboarding wizard designed for their B2B SaaS product. The designer agent is asked to produce a component specification.

## Prompt


We need to design a multi-step onboarding wizard for Clearpath, our B2B project management tool. New users need to:
1. Set up their workspace (name, logo, timezone)
2. Invite team members (up to 5 emails)
3. Connect their first integration (GitHub, Jira, or Slack — or skip)
4. Create their first project from a template

We have a design system with existing Input, Button, Avatar, and Card components. The wizard should work on desktop and tablet. Can you design this?

## Criteria


- [ ] PASS: Checks the existing design system first and explicitly identifies which existing components (Input, Button, Avatar, Card) can be reused versus what needs to be created
- [ ] PASS: Documents all 8 required component states for the wizard: Default, Hover, Focus, Active, Disabled, Loading, Error, Empty
- [ ] PASS: Specifies ARIA roles, labels, and keyboard navigation requirements — not deferred to a future accessibility pass
- [ ] PASS: Addresses the step indicator / progress component as either a Reuse, Extend, or Create decision with justification
- [ ] PASS: Specifies responsive behaviour for both desktop and tablet breakpoints
- [ ] PASS: Documents the error state for each step (e.g. invalid email format in team invite, workspace name taken)
- [ ] PARTIAL: Specifies loading states for async operations — partial credit if loading state is mentioned but not fully specified for each async step (integration connection, form submission)
- [ ] PASS: Produces output in a structured component specification format with named sections, not a prose description
