---
name: launch-plan
description: Create a launch plan checklist for a product or feature release.
argument-hint: "[product or feature being launched]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Create a launch plan for $ARGUMENTS.

## Checklist

### Pre-launch
- [ ] Positioning and messaging finalised
- [ ] Landing page / announcement page ready
- [ ] Documentation updated (user docs, API docs, changelog)
- [ ] Support team briefed (FAQ, known issues, escalation paths)
- [ ] Email sequence drafted (announcement, onboarding)
- [ ] Social media content prepared
- [ ] Analytics and tracking in place (events, conversion goals)
- [ ] Feature flags configured (gradual rollout plan if applicable)

### Launch day
- [ ] Deploy to production
- [ ] Verify deployment (smoke tests, monitoring)
- [ ] Publish landing page / announcement
- [ ] Send announcement email
- [ ] Post on social channels
- [ ] Monitor metrics (errors, support volume, sign-ups)

### Post-launch
- [ ] Review first 24h metrics
- [ ] Address critical bugs or support issues
- [ ] Collect initial user feedback
- [ ] Update roadmap based on reception
- [ ] Write retrospective (what went well, what didn't)

Customise the checklist based on the launch scope. Not every launch needs every item.
