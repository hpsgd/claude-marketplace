# Test: Groom backlog

Scenario: Testing whether the groom-backlog skill definition contains the required process steps, classification system, and RICE scoring requirements.

## Prompt

First, create the backlog file:

```bash
mkdir -p docs
```

Write to `docs/backlog.md`:

```markdown
# Q2 Feature Backlog

### Customer-Reported Bugs
1. **[BUG] Export fails for accounts with >10,000 rows** — 12 customer reports this month. Affects enterprise tier. No workaround known.
2. **[BUG] Dashboard freezes on Safari 16** — 5 reports. Reproducible. Linked to chart rendering library.
3. **[BUG] Email notifications sent twice on project creation** — 8 reports. Intermittent. Likely race condition.
4. **[BUG] CSV import silently drops rows with Unicode characters** — 3 reports. Data loss risk.
5. **[BUG] Search returns stale results for 5-10 mins after rename** — 6 reports. Cache invalidation issue.

### New Feature Requests
6. **[FEATURE] Team workspaces — multi-user collaboration** — Top enterprise request. 3 deals blocked. Estimated 8 weeks.
7. **[FEATURE] Bulk project archive** — 24 customer requests. Users want to archive multiple projects at once.
8. **[FEATURE] API rate limit headers (X-RateLimit-*)** — Developer community request. Needed for SDK clients.
9. **[FEATURE] Zapier integration** — 47 requests over 2 years. Competitor differentiator.
10. **[FEATURE] Custom fields on projects** — 31 requests. Enterprise differentiator.
11. **[FEATURE] Dark mode** — 89 requests. High volume, moderate effort.
12. **[FEATURE] Two-factor authentication (TOTP)** — Security-driven. Compliance requirement for 2 enterprise prospects.
13. **[FEATURE] Project templates** — 18 requests. Reduces onboarding friction.
14. **[FEATURE] Webhook retry with exponential backoff** — Developer request. Current webhooks fail silently.
15. **[FEATURE] Mobile app (iOS)** — 62 requests. High effort, dependency on API stabilisation (Item 8).

### Internal Tech Debt
16. **[TECH DEBT] Migrate from deprecated auth library** — Security risk. Library EOL in 6 months.
17. **[TECH DEBT] Remove feature flag scaffolding for v1 dashboard** — v1 deprecated 9 months ago. Dead code.
18. **[TECH DEBT] Replace inline SQL with ORM layer** — 400+ raw queries. Blocks safe schema changes.
19. **[TECH DEBT] Upgrade Node.js 16 → 20** — Security patches, performance. Required by hosting provider.
20. **[TECH DEBT] Extract notification service into separate module** — Prerequisite for multi-channel notifications (Item 9 and email redesign).
21. **[TECH DEBT] Fix 23 mypy errors in billing module** — Introduced in Q1 refactor. Blocks strict typing rollout.
22. **[TECH DEBT] Consolidate 3 config loading libraries** — Config is read 3 different ways. Source of recurring bugs.
23. **[BUG] Pagination breaks when page > 100 with active filters** — 2 reports. Regression from Q1.
24. **[FEATURE] Audit log for admin actions** — Compliance requirement. SOC 2 audit in Q3.
```

Then run:

/product-owner:groom-backlog docs/backlog.md

## Criteria


- [ ] PASS: Skill defines a structured multi-step process (not a single-step instruction)
- [ ] PASS: Skill requires RICE scoring (Reach, Impact, Confidence, Effort) for items being evaluated for prioritisation
- [ ] PASS: Skill defines a classification system with at least these states: Ready, Needs Refinement, and Blocked
- [ ] PASS: Skill requires dependency mapping — identifying which items block or are blocked by others
- [ ] PASS: Skill specifies what "Ready" means — criteria a story must meet before it can be pulled into a sprint
- [ ] PASS: Skill requires output as a structured table or list with status, score, and reasoning — not prose
- [ ] PARTIAL: Skill addresses how to handle items that lack sufficient data to score — partial credit if data gaps are mentioned but no specific guidance on how to proceed
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output works through all 24 backlog items — not a top-N subset — assigning each a state (Ready / Needs Refinement / Blocked) and either a RICE score or a "data needed" flag
- [ ] PASS: Output classifies items by type — customer-reported bugs, internal tech debt, new features — and applies prioritisation logic appropriately (bugs with revenue impact compete with features; pure tech debt sits in its own track)
- [ ] PASS: Output's RICE scoring shows the four columns numerically — Reach, Impact (0.25 / 0.5 / 1 / 2 / 3), Confidence (% based on evidence quality), Effort (person-weeks or story points) — with the formula `(R × I × C) / E` applied per scorable item
- [ ] PASS: Output flags items with insufficient data to score — naming the missing data per item ("need usage analytics for X feature", "need sales-team interview for Y customer-reported bug") rather than assigning made-up confidence
- [ ] PASS: Output's "Ready" definition is concrete — has user story + acceptance criteria + estimate + dependencies identified — not just "looks fine"
- [ ] PASS: Output's dependency map identifies blocking relationships — e.g. "Item 12 (mobile feature) blocked by Item 7 (auth refactor)" — so the team can plan in the right order
- [ ] PASS: Output's recommended sprint candidates are based on RICE ranking + team capacity + dependencies — not "the top 5 by RICE" (which may be all blocked)
- [ ] PASS: Output's data-gap recommendations are actionable — e.g. "instrument feature X before scoring", "interview 3 enterprise customers about Y" — with effort estimates so the data work itself can be prioritised
- [ ] PASS: Output produces the result as a structured table — Item | Type | State | RICE | Dependencies | Reasoning — not prose paragraphs
- [ ] PARTIAL: Output addresses how stale backlog items are handled — items >6 months old without movement should be archived or reconfirmed, not silently kept on the list
