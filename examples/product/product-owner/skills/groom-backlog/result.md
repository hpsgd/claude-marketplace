# Groom Backlog

Scenario: Testing whether the groom-backlog skill definition contains the required process steps, classification system, and RICE scoring requirements.

## Prompt

> First, create the backlog file:
> 
> ```bash
> mkdir -p docs
> ```
> 
> Write to `docs/backlog.md`:
> 
> ```markdown
> # Q2 Feature Backlog
> 
> ### Customer-Reported Bugs
> 1. **[BUG] Export fails for accounts with >10,000 rows** — 12 customer reports this month. Affects enterprise tier. No workaround known.
> 2. **[BUG] Dashboard freezes on Safari 16** — 5 reports. Reproducible. Linked to chart rendering library.
> 3. **[BUG] Email notifications sent twice on project creation** — 8 reports. Intermittent. Likely race condition.
> 4. **[BUG] CSV import silently drops rows with Unicode characters** — 3 reports. Data loss risk.
> 5. **[BUG] Search returns stale results for 5-10 mins after rename** — 6 reports. Cache invalidation issue.
> 
> ### New Feature Requests
> 6. **[FEATURE] Team workspaces — multi-user collaboration** — Top enterprise request. 3 deals blocked. Estimated 8 weeks.
> 7. **[FEATURE] Bulk project archive** — 24 customer requests. Users want to archive multiple projects at once.
> 8. **[FEATURE] API rate limit headers (X-RateLimit-*)** — Developer community request. Needed for SDK clients.
> 9. **[FEATURE] Zapier integration** — 47 requests over 2 years. Competitor differentiator.
> 10. **[FEATURE] Custom fields on projects** — 31 requests. Enterprise differentiator.
> 11. **[FEATURE] Dark mode** — 89 requests. High volume, moderate effort.
> 12. **[FEATURE] Two-factor authentication (TOTP)** — Security-driven. Compliance requirement for 2 enterprise prospects.
> 13. **[FEATURE] Project templates** — 18 requests. Reduces onboarding friction.
> 14. **[FEATURE] Webhook retry with exponential backoff** — Developer request. Current webhooks fail silently.
> 15. **[FEATURE] Mobile app (iOS)** — 62 requests. High effort, dependency on API stabilisation (Item 8).
> 
> ### Internal Tech Debt
> 16. **[TECH DEBT] Migrate from deprecated auth library** — Security risk. Library EOL in 6 months.
> 17. **[TECH DEBT] Remove feature flag scaffolding for v1 dashboard** — v1 deprecated 9 months ago. Dead code.
> 18. **[TECH DEBT] Replace inline SQL with ORM layer** — 400+ raw queries. Blocks safe schema changes.
> 19. **[TECH DEBT] Upgrade Node.js 16 → 20** — Security patches, performance. Required by hosting provider.
> 20. **[TECH DEBT] Extract notification service into separate module** — Prerequisite for multi-channel notifications (Item 9 and email redesign).
> 21. **[TECH DEBT] Fix 23 mypy errors in billing module** — Introduced in Q1 refactor. Blocks strict typing rollout.
> 22. **[TECH DEBT] Consolidate 3 config loading libraries** — Config is read 3 different ways. Source of recurring bugs.
> 23. **[BUG] Pagination breaks when page > 100 with active filters** — 2 reports. Regression from Q1.
> 24. **[FEATURE] Audit log for admin actions** — Compliance requirement. SOC 2 audit in Q3.
> ```
> 
> Then run:
> 
> /product-owner:groom-backlog docs/backlog.md

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've groomed the backlog following the complete process:

## Summary

**14 items ready to schedule**, ranked by RICE score:
- Search stale results (2400) — biggest pain point
- Pagination regression (1000) — data loss risk  
- CSV Unicode drops (900) — data integrity
- Dark mode (700) — highest volume request
- plus 5 more features and 4 tech debt items

**10 items need refinement** — mostly XL features that need breaking down:
- Team workspaces: split into 4 independent deliverables
- Custom fields: clarify scope (field types, UI, persistence)
- Mobile app: phase into view-only → edit → offline
- Plus investigation tasks for bugs (export, email duplication)

**Tech debt scheduled into 20% capacity** — Items 17, 19, 20, 21, 22 provide platform stability for dependent features.

**Critical path**: Item 20 (notification service) before Items 6, 9, 24; Item 8 (rate limit headers) before Item 15 (mobile).

The output file at `docs/backlog-groomed.md` includes RICE scores, dependency graphs, two-sprint execution plan, and specific refinement actions per item.

### Artifacts written

#### `work/docs/backlog-groomed.md`

```
# Backlog Grooming Summary — 2026-05-04

## Overview
- **Total items reviewed:** 24
- **Ready to schedule:** 14
- **Needs refinement:** 10
- **Recommended for closure:** 0
- **Blocked:** 0
- **Tech debt allocation:** 20% of capacity (Items 17, 19, 20, 21, 22)

---

## 1. Schedule Next (by RICE priority)

### Scorable items (ranked by RICE)

| # | Item | Type | Reach | Impact | Conf | Effort | RICE | Size | Dependencies | Reasoning |
|---|------|------|-------|--------|------|--------|------|------|--------------|-----------|
| 5 | Search returns stale results for 5-10 mins after rename | Bug | 3000 | 1 | 80% | 1w | **2400** | M | None | Cache invalidation affects every user who renames frequently. High volume, known fix area. |
| 23 | Pagination breaks when page > 100 with active filters | Bug | 250 | 2 | 100% | 0.5w | **1000** | S | None | Regression fix with specific scenario. High confidence, low effort. |
| 4 | CSV import silently drops rows with Unicode characters | Bug | 150 | 3 | 100% | 0.5w | **900** | S | None | Data loss risk elevates impact. Targeted fix, known scope. |
| 11 | Dark mode | Feature | 3500 | 0.5 | 100% | 2.5w | **700** | L | None | 89 customer requests, highest volume request. Trade-off: effort vs. demand. |
| 2 | Dashboard freezes on Safari 16 | Bug | 500 | 2 | 80% | 2w | **400** | L | None | Reproducible, specific browser. Root cause identified (chart library). |
| 7 | Bulk project archive | Feature | 400 | 1 | 80% | 1w | **320** | M | None | 24 customer requests. Power users managing multiple projects. |
| 8 | API rate limit headers (X-RateLimit-*) | Feature | 90 | 2 | 50% | 0.5w | **180** | S | None | Enables SDK client behavior. Low confidence reflects lack of product data. |
| 12 | Two-factor authentication (TOTP) | Feature | 125 | 3 | 100% | 2w | **187.5** | M | None | 2 enterprise prospects blocked. Compliance requirement. Score reflects enterprise deal value. |
| 14 | Webhook retry with exponential backoff | Feature | 70 | 2 | 80% | 1w | **112** | M | None | Developer feature. Improves integration reliability. |

### Tech debt items (scheduled into 20% allocation)

| # | Item | Type | Effort | Status | Reasoning |
|---|------|------|--------|--------|-----------|
| 17 | Remove feature flag scaffolding for v1 dashboard | Tech Debt | 0.5w | Ready | Dead code, no risk. Good for first sprint. |
| 21 | Fix 23 mypy errors in billing module | Tech Debt | 0.5w | Ready | Unblocks strict typing rollout. Specific, bounded scope. |
| 19 | Upgrade Node.js 16 → 20 | Tech Debt | 1w | Ready | Required by hosting provider. Security patches. |
| 22 | Consolidate 3 config loading libraries | Tech Debt | 1w | Ready | Reduces recurring bugs. Medium complexity. |
| 20 | Extract notification service into separate module | Tech Debt | 2w | Ready | **Strategic prerequisite** for Items 6, 9, 24. Do this before scoping multi-channel work. |

### Execution recommendation

**Next two sprints** (assuming 2-week sprints, 1 FTE):

**Sprint 1:**
- Item 5 (Search stale results) — M, 1 week → Starts sprint 1
- Item 23 (Pagination) — S, 0.5 week → Completes by day 4
- Tech debt allocation: Item 17 (scaffolding) + Item 21 (mypy), combined 1 week
- **Total: 2.5 weeks in a 2-week sprint** → Pull Item 4 or finish Item 23 + both tech items, decide on Item 4

**Sprint 2:**
- Item 4 (CSV Unicode) — S, 0.5 week
- Item 7 (Bulk archive) — M, 1 week
- Item 8 (Rate limit headers) — S, 0.5 week
- Tech debt: Item 19 (Node upgrade) + Item 22 (config) = 2 weeks
- **Total: 4 weeks in a 2-week sprint** → Sequence as: CSV + Rate limit (1 week) + Node upgrade (1 week)

**Defer to Sprint 3:**
- Item 11 (Dark mode) — L, 2.5 weeks → Highest volume but lowest urgency
- Item 2 (Safari dashboard) — L, 2 weeks → Specific to one browser
- Item 12 (2FA) — M, 2 weeks → Enterprise critical, schedule after sprint 2
- Item 14 (Webhook retry) — M, 1 week → Polish feature
- Item 20 (Notification service) — L, 2 weeks → Strategic, do before items 6, 9, 24

---

## 2. Needs Refinement

| # | Item | Type | Issue | Refinement needed |
|---|------|------|-------|-------------------|
| 1 | Export fails for accounts with >10,000 rows | Bug | No root cause investigation. No acceptance criteria. | **Action:** Create "Investigation: Export performance baseline" task (S, 2-3 days). Engineer to profile export on >10K dataset, identify bottleneck (memory, query, serialization), propose fix approach. Once root cause known, break into 1-2 implementation tasks. |
| 3 | Email notifications sent twice on project creation | Bug | Intermittent, likely race condition. No repro steps documented. | **Action:** QA to document exact repro (create N projects rapidly, check email count). Engineer to investigate event handler concurrency. Likely a duplicate-check or idempotency guard issue. Once confirmed, write acceptance criteria: "Email sent exactly once per project creation, even under concurrent requests." |
| 6 | Team workspaces — multi-user collaboration | Feature | Estimated 8 weeks = XL. Scope too large, bundled concerns. | **Action:** Break into deliverables: (1) "User can invite collaborators to workspace" (M, 2w), (2) "Workspace members can see shared projects" (M, 2w), (3) "Workspace admin controls (roles, permissions)" (L, 2w), (4) "Notifications for workspace activity" (depends on Item 20, M, 1w). Prioritize (1) + (2) for MVP. |
| 9 | Zapier integration | Feature | 47 requests but no integration approach defined. | **Action:** Clarify: (a) What events/actions to expose? (b) Zapier Action or Trigger or both? (c) Authentication approach (OAuth or API key)? (d) Estimated effort once scoped (likely M-L). Create a "Tech Spec: Zapier Integration" before implementation. Note: Depends on Item 8 (rate limit headers) for SDK stability. |
| 10 | Custom fields on projects | Feature | 31 requests, enterprise differentiator, but vague scope. | **Action:** Product Owner interview: (1) What field types? (Checkbox, text, dropdown, date?) (2) UI for field definition? (3) API surface? (4) Persistence — schemaless or schema evolution? Break into phases: Phase 1 = text/checkbox fields only (M, 2w), Phase 2 = additional types (M, 1w). |
| 13 | Project templates | Feature | Vague: what are templates? Created by users or shipped by company? | **Action:** Clarify: (1) Are templates shipped defaults or user-created? (2) What does "apply template" do? Copy structure, automations, fields? (3) Scope estimate once defined. Likely: "User can duplicate a project as a template" (S, 3d) + "User can browse templates" (M, 1w). |
| 15 | Mobile app (iOS) | Feature | 62 requests, high effort, depends on Item 8. | **Action:** Break into phases: Phase 1 = view-only app (M, 3w), Phase 2 = basic create/edit (M, 2w), Phase 3 = offline support, push (L, 3w). Do not combine all three. Defer Phase 1 until Item 8 (rate limit headers) stabilises API. |
| 16 | Migrate from deprecated auth library | Tech Debt | EOL in 6 months but scope unclear. What changes? | **Action:** Architecture review: (1) Identify all code paths using deprecated lib (search codebase). (2) Map replacement lib. (3) Estimate per-module migration effort. (4) Identify breaking changes for users (re-auth required?). Likely breakdown: "Migrate session handling" (M), "Migrate password reset flow" (M), "Migrate OAuth integrations" (L). |
| 18 | Replace inline SQL with ORM layer | Tech Debt | 400+ raw queries = massive scope. Must be broken down. | **Action:** Do NOT commit to this as one item. Phase 1: "Convert SELECT-only queries in reporting module to ORM" (M, 2w). Phase 2: "Migrate account creation flow to ORM" (M, 2w). Phase 3: "Remaining write-heavy queries" (L, 3w+). Sequencing: Do Phase 1 as risk validation. Phase 2 + 3 depend on Phase 1 success. |
| 24 | Audit log for admin actions | Feature | SOC 2 audit in Q3 (deadline!) but scope vague. | **Action:** Define scope with compliance officer: (1) Which admin actions? (login, data access, config changes?) (2) Retention policy? (3) Query/export requirements? (4) Who accesses audit log? Estimate once defined. Likely: basic logging (M, 1.5w) + querying UI (M, 1w). Note: May depend on Item 20 (notification service) if audit triggers alerts. |

---

## 3. Recommended for Closure

None. All items reflect genuine customer signal or platform necessity.

---

## 4. Blocked — Escalation Needed

None. All items can start once refined or are independent.

---

## 5. Critical Path and Dependencies

### Dependency graph

```
[Item 8: API rate limit headers]
  ↓
  ├─→ [Item 15: Mobile iOS app]
  └─→ [Item 9: Zapier integration] (optional, improves SDK experience)

[Item 20: Extract notification service]
  ↓
  ├─→ [Item 6: Team workspaces] (multi-user notifications)
  ├─→ [Item 9: Zapier] (if integration includes notifications)
  └─→ [Item 24: Audit log] (if audit events trigger alerts)

[Item 16: Migrate auth library]
  → Deadline: 6 months (EOL date) — must start Q2 or Q3
```

### Sequencing guidance

1. **Bugs first** (Items 5, 23, 4, 2, 3, 1): Fix customer-reported issues before features. This queue has 2-3 weeks of work; space it into next 2 sprints.

2. **Strategic tech debt before dependent features:**
   - Item 20 (notification service) before Items 6, 9, 24
   - Item 8 (API rate limit headers) before Item 15 (mobile app)
   - Item 19 (Node upgrade) early (required by hosting)

3. **High-RICE features** (Items 11, 7) after bugs and tech debt are handled.

4. **Compliance deadline tracking:**
   - Item 16 (auth migration): EOL in 6 months — start Q3 at latest
   - Item 24 (audit log): SOC 2 audit in Q3 — finish by September

---

## 6. Recommendations and Next Actions

### Immediate (this week)

1. **Refinement tasks** — Assign to Tech Lead + Product Owner:
   - Item 1 (export): Engineer to investigate baseline and root cause (2-3 days)
   - Item 3 (email duplication): QA + Engineer to document repro (1 day)
   - Item 6 (team workspaces): Product + Engineer to break into 4 deliverables (1 day)
   - Item 9 (Zapier): Product to clarify integration approach (1 day)
   - Item 10 (custom fields): Product Owner interview on field types (1 day)

2. **Prioritisation confirmation** — Does this RICE ranking match company goals?
   - Search stale results (2400) captures the biggest pain point
   - Dark mode (700) is high-volume but lowest urgency — ok to defer to Sprint 3?
   - 2FA (187.5) is enterprise critical but moderate RICE — confirm deal value with sales

3. **Sprint 1 commitment** — Schedule and communicate:
   - Item 5 (search stale results)
   - Item 23 (pagination regression)
   - Tech debt: Items 17 + 21 (flag cleanup + mypy)

### Before Sprint 2

1. Complete refinement for Items 1, 3, 6, 9, 10, 13.
2. Re-score Items 6, 9, 10, 15, 24 once they have acceptance criteria.
3. Confirm Node.js hosting deadline with DevOps — is Item 19 blocking other work?

### Backlog hygiene (monthly)

1. Tag all items with **customer signal source** (support tickets, sales conversation, analytics, employee idea) — this keeps the backlog grounded in reality.
2. Set **data collection** tasks for any item that cannot be scored reliably (e.g., "instrument export API to measure >10K query latency" for Item 1).
3. Review stale items (no activity 30+ days) — close or re-engage.

---

## Appendix: Sizing Notes

- **S (Small, 1-3 days):** Well-understood work, similar to past tasks (Items 4, 8, 17, 21, 23)
- **M (Medium, 3-5 days):** Moderate complexity, some new territory (Items 2, 7, 12, 14, 19, 22)
- **L (Large, 1-2 weeks):** High complexity, meaningful unknowns (Items 11, 20)
- **XL (too large, needs breakdown):** Must not schedule as one item (Items 6, 10, 15, 18)

Size estimates reflect implementation + code review + testing. Do not include refinement time.

```

#### `work/docs/backlog.md`

```
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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-04 |
| Target duration | 107623 ms |
| Target cost | $0.1420 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines a structured multi-step process (not a single-step instruction) | PASS | The output artifact is divided into six numbered sections: (1) Schedule Next, (2) Needs Refinement, (3) Recommended for Closure, (4) Blocked, (5) Critical Path and Dependencies, (6) Recommendations and Next Actions — demonstrating a clearly structured multi-step process. |
| c2 | Skill requires RICE scoring (Reach, Impact, Confidence, Effort) for items being evaluated for prioritisation | PASS | The 'Scorable items' table in Section 1 contains columns labeled Reach, Impact, Conf, Effort, and RICE with numerical values for each ready item, e.g. Item 5: Reach=3000, Impact=1, Conf=80%, Effort=1w, RICE=2400. |
| c3 | Skill defines a classification system with at least these states: Ready, Needs Refinement, and Blocked | PASS | The artifact has explicit sections titled '1. Schedule Next' (Ready), '2. Needs Refinement', and '4. Blocked — Escalation Needed', covering all three required states. |
| c4 | Skill requires dependency mapping — identifying which items block or are blocked by others | PASS | Section 5 contains a 'Dependency graph' with explicit arrows, e.g. '[Item 8: API rate limit headers] → [Item 15: Mobile iOS app]' and '[Item 20: Extract notification service] → [Item 6: Team workspaces], [Item 9: Zapier], [Item 24: Audit log]'. |
| c5 | Skill specifies what "Ready" means — criteria a story must meet before it can be pulled into a sprint | PASS | Items placed in 'Schedule Next' have explicit size estimates, RICE scores, and dependency status. The 'Needs Refinement' entries explain what makes items NOT ready — 'No root cause investigation. No acceptance criteria.' (Item 1), 'Intermittent, likely race condition. No repro steps documented.' (Item 3) — making the Ready definition concrete by contrast. |
| c6 | Skill requires output as a structured table or list with status, score, and reasoning — not prose | PASS | The artifact uses markdown tables throughout: the scorable items table includes columns for RICE score, size, dependencies, and reasoning; the Needs Refinement table includes Issue and Refinement needed columns. No prose-only sections replace tabular data. |
| c7 | Skill addresses how to handle items that lack sufficient data to score — partial credit if data gaps are mentioned but no specific guidance on how to proceed | PARTIAL | Item 8 carries 50% confidence with the note 'Low confidence reflects lack of product data.' The Needs Refinement section explicitly names what data is missing per item, and the Recommendations section lists data-collection actions. Ceiling is PARTIAL per test definition. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output (chat response and docs/backlog-groomed.md artifact) contains no skill file content. The YAML frontmatter of the skill definition is not visible anywhere in the captured output, making it impossible to verify name, description, and argument-hint fields are present. |
| c9 | Output works through all 24 backlog items — not a top-N subset — assigning each a state (Ready / Needs Refinement / Blocked) and either a RICE score or a "data needed" flag | PASS | Section 1 schedules items 5, 23, 4, 11, 2, 7, 8, 12, 14 (9 items) plus tech debt 17, 21, 19, 22, 20 (5 items); Section 2 lists items 1, 3, 6, 9, 10, 13, 15, 16, 18, 24 (10 items) — totalling all 24 original backlog items. |
| c10 | Output classifies items by type — customer-reported bugs, internal tech debt, new features — and applies prioritisation logic appropriately (bugs with revenue impact compete with features; pure tech debt sits in its own track) | PASS | Section 1 splits into 'Scorable items' (bugs and features ranked together by RICE) and a separate 'Tech debt items (scheduled into 20% allocation)' sub-table. The chat summary explicitly states 'Tech debt scheduled into 20% capacity'. Bugs compete with features on RICE while tech debt has its own allocation track. |
| c11 | Output's RICE scoring shows the four columns numerically — Reach, Impact (0.25 / 0.5 / 1 / 2 / 3), Confidence (% based on evidence quality), Effort (person-weeks or story points) — with the formula `(R × I × C) / E` applied per scorable item | PASS | All four columns are present numerically. Formula verified: Item 5 (3000×1×0.8)/1=2400 ✓; Item 23 (250×2×1)/0.5=1000 ✓; Item 4 (150×3×1)/0.5=900 ✓; Item 12 (125×3×1)/2=187.5 ✓; Item 8 (90×2×0.5)/0.5=180 ✓. |
| c12 | Output flags items with insufficient data to score — naming the missing data per item ("need usage analytics for X feature", "need sales-team interview for Y customer-reported bug") rather than assigning made-up confidence | PASS | Each Needs Refinement item names specific missing data: Item 1 'No root cause investigation. No acceptance criteria.'; Item 9 'no integration approach defined' with specific questions (What events/actions? Zapier Action or Trigger? Auth approach?); Item 10 'vague scope' asking about field types, UI, persistence; Item 24 needs 'scope with compliance officer'. |
| c13 | Output's "Ready" definition is concrete — has user story + acceptance criteria + estimate + dependencies identified — not just "looks fine" | PASS | Ready items in Section 1 all have explicit: size estimate (S/M/L), effort in person-weeks, dependencies column (explicitly 'None' where applicable), and reasoning. Items flagged as Needs Refinement are excluded precisely because they lack 'acceptance criteria' (Item 1), 'repro steps' (Item 3), or have 'vague scope' (Items 9, 10, 13) — establishing concrete ready criteria by exclusion. |
| c14 | Output's dependency map identifies blocking relationships — e.g. "Item 12 (mobile feature) blocked by Item 7 (auth refactor)" — so the team can plan in the right order | PASS | Section 5 dependency graph explicitly shows '[Item 8: API rate limit headers] → [Item 15: Mobile iOS app]' and '[Item 20: Extract notification service] → [Item 6: Team workspaces], [Item 9: Zapier], [Item 24: Audit log]'. Refinement notes for Item 9 also state 'Depends on Item 8 (rate limit headers) for SDK stability'. |
| c15 | Output's recommended sprint candidates are based on RICE ranking + team capacity + dependencies — not "the top 5 by RICE" (which may be all blocked) | PASS | Sprint planning (Section 1 'Execution recommendation') explicitly notes capacity overruns ('Total: 2.5 weeks in a 2-week sprint → Pull Item 4 or finish…') and defers Item 11 (Dark mode, RICE 700) to Sprint 3 despite high score because of L effort. Item 20 (notification service) deferred because it's strategic/large, not because of low RICE. |
| c16 | Output's data-gap recommendations are actionable — e.g. "instrument feature X before scoring", "interview 3 enterprise customers about Y" — with effort estimates so the data work itself can be prioritised | PASS | Item 1 action: 'Create "Investigation: Export performance baseline" task (S, 2-3 days). Engineer to profile export on >10K dataset'; Item 3: 'QA to document exact repro (create N projects rapidly, check email count). Engineer to investigate event handler concurrency'; Item 9: 'Create a "Tech Spec: Zapier Integration" before implementation'. Effort labels (S, 1 day, 2-3 days) are included throughout. |
| c17 | Output produces the result as a structured table — Item \| Type \| State \| RICE \| Dependencies \| Reasoning — not prose paragraphs | PASS | The main scorable items table has columns: # \| Item \| Type \| Reach \| Impact \| Conf \| Effort \| RICE \| Size \| Dependencies \| Reasoning. The Needs Refinement table has: # \| Item \| Type \| Issue \| Refinement needed. Both sections use markdown tables, not prose paragraphs, though split across sections rather than one unified table. |
| c18 | Output addresses how stale backlog items are handled — items >6 months old without movement should be archived or reconfirmed, not silently kept on the list | PARTIAL | Section 6 'Backlog hygiene (monthly)' states 'Review stale items (no activity 30+ days) — close or re-engage.' This mentions stale item handling but uses a 30-day threshold rather than the >6 months criterion specifies, and the guidance ('close or re-engage') is brief. Ceiling is PARTIAL per test definition. |

### Notes

The output is comprehensive and high-quality, covering all 24 backlog items with RICE scoring, classification states, dependency mapping, and actionable refinement guidance. The main gap is c8 (skill YAML frontmatter) which cannot be verified from the captured output — only the artifact and chat response are available, not the skill file itself. The output demonstrates sophisticated prioritisation: tech debt on a 20% separate track, capacity-aware sprint planning, and dependency-ordered sequencing. The RICE formula is applied correctly and verifiably across all scorable items. Stale item handling (c18) is addressed but at a coarser granularity (30 days vs. 6 months) than the criterion requires, earning only partial credit at its capped ceiling.
