# Customer Onboarding Playbook: {{segment_name}}

| Field | Value |
|---|---|
| **Segment** | {{segment — e.g., Enterprise, Mid-Market, SMB}} |
| **Expected Duration** | {{number}} days |
| **CS Owner Role** | {{CSM, Onboarding Specialist, TAM}} |
| **Last Updated** | {{date}} |

## Pre-Onboarding

Complete before the kickoff call:

- [ ] Receive sales handoff (CRM notes, call recordings, success criteria discussed during sales)
- [ ] Identify stakeholders: executive sponsor, project lead, technical admin, end users
- [ ] Define success criteria with the customer (quantitative targets, qualitative outcomes)
- [ ] Send welcome email with kickoff agenda and calendar invite
- [ ] Provision accounts and prepare environment

## Milestone Table

| Milestone | Target Day | Success Criteria | Owner | Verification Method | Escalation Trigger |
|---|---|---|---|---|---|
| Kickoff complete | Day 0 | Stakeholders aligned, goals documented | CSM | Meeting notes signed off | No executive sponsor identified |
| Technical setup | Day {{n}} | Environment configured, integrations live | Technical admin | Smoke test checklist passes | Setup blocked > 3 business days |
| First value achieved | Day {{n}} | {{defined first-value metric}} | CSM + customer | Dashboard metric or customer confirmation | No engagement after day {{n}} |
| Core workflow adopted | Day {{n}} | {{primary use case}} active with {{x}} users | CSM | Usage analytics | Adoption < {{threshold}}% at day {{n}} |
| Onboarding complete | Day {{n}} | All success criteria met, handoff accepted | CSM | Completion scorecard | Any milestone missed by > 5 days |

## Kickoff Meeting Agenda

| Duration | Topic | Owner |
|---|---|---|
| 5 min | Introductions and roles | CSM |
| 10 min | Recap goals and success criteria from sales process | CSM |
| 10 min | Walkthrough onboarding timeline and milestones | CSM |
| 10 min | Access provisioning and technical setup plan | Technical admin |
| 5 min | Communication cadence, escalation contacts, next steps | CSM |

## Time-to-First-Value

- **Definition of "First Value"**: {{what the customer considers their first meaningful outcome — e.g., first report generated, first workflow automated}}
- **Target**: {{n}} days from kickoff
- **Measurement**: {{how you verify — product event, customer confirmation, metric threshold}}

## Common Blockers

| Blocker | Early Warning Sign | Resolution | Escalation Path |
|---|---|---|---|
| SSO/IT approval delays | No admin access by day 3 | Provide IT requirements doc upfront, offer direct call with IT | CSM -> CS Manager -> AE for exec nudge |
| Stakeholder disengagement | Missed meetings, no replies within 48h | Reconfirm value prop, engage exec sponsor | CSM -> CS Manager |
| Data migration issues | Import errors, incomplete data | Provide migration guide, offer assisted import | CSM -> Support Engineering |
| Scope creep | Requests beyond agreed onboarding goals | Document in parking lot, redirect to post-onboarding | CSM -> CS Manager |

## Handoff to BAU

Criteria for completing onboarding:

- [ ] All milestones in the milestone table are met or explicitly deferred
- [ ] Customer confirms satisfaction with onboarding in a written check-in
- [ ] Ongoing CSM or AM is introduced and has context
- [ ] First QBR is scheduled for day {{n}} post-kickoff
- [ ] Support channel and self-service resources are confirmed with the customer

## Metrics

| Metric | Target | Measurement |
|---|---|---|
| Onboarding completion rate | {{n}}% | Completed onboardings / total started |
| Time-to-first-value | {{n}} days | Kickoff date to first-value event |
| Day 30 adoption | {{n}}% of licensed users active | Product analytics |
| Day 60 adoption | {{n}}% of licensed users active | Product analytics |
| Day 90 adoption | {{n}}% of licensed users active | Product analytics |
| Customer satisfaction (onboarding) | {{n}}/10 | Post-onboarding survey |
