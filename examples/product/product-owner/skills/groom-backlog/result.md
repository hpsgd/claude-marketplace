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

Grooming complete. The backlog has been classified and prioritized:

**Key findings:**

- **15 items ready to schedule** — top priority is the pagination regression (#23, RICE 720) and search staleness bug (#5, RICE 640), followed by bulk archive feature (#7, RICE 480).

- **7 items need refinement** — three high-impact bugs need investigation spikes first (#1 export >10k, #2 Safari freezes, #3 email race condition), and four features are too large or vague to schedule (#6 team workspaces, #9 Zapier, #10 custom fields, #13 templates).

- **1 blocked item** — mobile iOS (#15) is blocked by API rate limit headers (#8, 0.5w) and needs architectural breakdown.

- **Tech debt track** — 7 items reserved for 20% sprint capacity, prioritizing auth migration (#16, security deadline in 6 months) and audit log (#24, SOC 2 audit in Q3).

The grooming doc includes specific refinement actions for each item needing work, a dependency map, and a recommended sprint order. Next step: use `/product-owner:write-user-story` on top items (#23, #5, #7) to expand into detailed acceptance criteria before scheduling.

### Artifacts written

#### `work/docs/backlog-grooming.md`

```
# Backlog Grooming Summary — 2026-05-03

## Overview
- **Total items reviewed:** 24
- **Ready to schedule:** 15
- **Needs refinement:** 7
- **Recommended for closure:** 0
- **Blocked:** 1

---

## 1. Schedule Next (by RICE Priority)

### High-Impact & Quick Wins
| Item | Type | Title | Size | Reach | Impact | Confidence | Effort | RICE | Dependencies |
|------|------|-------|------|-------|--------|------------|--------|------|--------------|
| #23 | Bug | Pagination breaks when page > 100 with active filters | S | 200 | 2 | 90% | 0.5w | **720** | None |
| #5 | Bug | Search returns stale results for 5-10 mins after rename | S | 400 | 2 | 80% | 1w | **640** | None |
| #7 | Feature | Bulk project archive | S | 300 | 1 | 80% | 0.5w | **480** | None |
| #4 | Bug | CSV import silently drops rows with Unicode characters | S | 50 | 3 | 80% | 0.5w | **240** | None |
| #14 | Feature | Webhook retry with exponential backoff | M | 100 | 2 | 80% | 1w | **160** | None |
| #8 | Feature | API rate limit headers (X-RateLimit-*) | S | 50 | 2 | 80% | 0.5w | **160** | None |
| #11 | Feature | Dark mode | M | 500 | 1 | 50% | 2w | **125** | None |
| #12 | Feature | Two-factor authentication (TOTP) | M | 50 | 2 | 80% | 1.5w | **107** | None |

### Platform & Infrastructure (Scheduled into 20% tech-debt allocation)
| Item | Type | Title | Size | Deadline | Dependencies | Reasoning |
|------|------|-------|------|----------|--------------|-----------|
| #16 | Tech Debt | Migrate from deprecated auth library | M | 6 months (EOL) | None | Security risk, hosting-critical. Schedule immediately. |
| #24 | Tech Debt | Audit log for admin actions | L | Q3 (SOC 2 audit) | None | Compliance blocker. Needs design (what admin actions to log?). Effort: 2-3w. |
| #19 | Tech Debt | Upgrade Node.js 16 → 20 | M | Hosting deadline | None | Security patches + hosting requirement. Medium risk (dependency compatibility). |
| #20 | Tech Debt | Extract notification service into separate module | M | None | None | Prerequisite for multi-channel notifications & Item #24. Enables future work. |
| #22 | Tech Debt | Consolidate 3 config loading libraries | M | None | None | Recurring source of bugs. Medium complexity. |
| #21 | Tech Debt | Fix 23 mypy errors in billing module | S | None | None | Enables strict typing rollout. Quick win. |
| #17 | Tech Debt | Remove feature flag scaffolding for v1 dashboard | S | None | None | Dead code cleanup (v1 deprecated 9 months ago). Low risk. |

---

## 2. Needs Refinement

### Investigation Spikes Required
| Item | Issue | Action Needed | Est. Effort |
|------|-------|--------------|-------------|
| #1 | **Export >10,000 rows:** Unknown root cause. Could be database timeout, memory limit, pagination logic, or query performance. | **Create investigation spike:** Reproduce issue, profile database queries, identify bottleneck. Once root cause found, estimate fix effort. | S (3-5 days) |
| #2 | **Dashboard freezes Safari 16:** Linked to chart library but exact cause unclear. Could be library version, custom code, or configuration. | **Create investigation spike:** Identify chart rendering library version, test in Safari 16, compare with Chrome. Assess if it's upgrade, workaround, or code fix. | M (1 week) |
| #3 | **Email notifications twice:** Intermittent race condition is difficult to reproduce and debug. Needs controlled investigation. | **Create investigation spike:** Add detailed logging to notification creation flow, reproduce race condition, identify locking issue. | M (1 week) |

### Large Items Requiring Breakdown
| Item | Issue | Action Needed |
|------|-------|--------------|
| #6 | **Team workspaces (8 weeks = XL):** Feature is too large and bundled. Must split into independent deliverables. | **Break down by user workflow:** (1) Invite members to workspace, (2) Manage member permissions, (3) Real-time collaboration (sync/conflict resolution), (4) Workspace-level audit/settings. Scope each separately; validate which are MVP. Estimated breakdown: 2-3w + 2-3w + 3-4w + 1-2w. |
| #18 | **Replace inline SQL with ORM (400+ raw queries = XL):** Massive refactor. Cannot be done in one sprint. Must be broken down by subsystem. | **Break down by module:** (1) Billing module, (2) Reporting module, (3) Auth/user module, (4) Project management module, etc. Create separate backlog items for each. Effort per module: 1-3w. |

### Scope Clarification Needed
| Item | Issue | Action Needed |
|------|-------|--------------|
| #9 | **Zapier integration:** Scope is undefined. Which Zapier triggers/actions are MVP? Build in-house vs use Zapier platform? | **Clarify scope:** (1) Define MVP triggers (create/update/delete projects? manage tasks? change ownership?), (2) Evaluate integration approach (Zapier OAuth flow vs custom webhook integration), (3) Estimate effort for MVP. Without clarity, estimate is 4-6w. |
| #10 | **Custom fields:** No design decision on storage, types, or query support. High complexity depending on approach. | **Design decision needed:** (1) What field types (text, select, date, numeric, relational)? (2) Storage approach (separate columns, JSON, third table)? (3) Query support (filter by custom field, sort)? (4) Permissions (who can define custom fields?). Estimated effort post-design: 2-4w. |
| #13 | **Project templates:** Unclear what constitutes a "template" or who creates them. | **Clarify scope:** (1) Are templates just structural (columns/workflows) or include sample content? (2) Can users create custom templates or only admins? (3) Org-wide or personal templates? (4) Can templates be shared? Start with narrow scope (admin-defined, structural only) and validate before expanding. Estimated: 1-2w for MVP. |

---

## 3. Blocked — Escalation Needed

| Item | Title | Blocker | Who | Impact of Delay | Recommend |
|------|-------|---------|-----|-----------------|-----------|
| #15 | Mobile app (iOS) | **Item #8 (API rate limit headers) required** for SDK clients. Also XL scope (needs 8 weeks). | Backend team (Item #8), then architectural review for mobile approach | Mobile work cannot start until SDK is stabilised. Scope breakdown also needed: authentication, offline sync, push notifications, etc. | Schedule #8 first (S, 0.5w); then create design spec for mobile before scheduling full #15 |

---

## 4. Dependency Map

```
[Item #8: API rate limit headers] 
  ↓ unblocks ↓
[Item #15: Mobile app (iOS)]

[Item #20: Extract notification service] 
  ↓ enables ↓
[Future: Multi-channel notifications] + [Item #24: Audit log]

[Item #16: Migrate auth library] 
  ↓ has external deadline ↓
EOL in 6 months (security critical)

[Item #24: Audit log]
  ↓ has external deadline ↓
SOC 2 audit in Q3

[Item #19: Node.js upgrade]
  ↓ has external deadline ↓
Hosting provider requirement (unknown when, but flagged as urgent)

No circular dependencies detected.
```

---

## 5. Schedule Rationale & Recommendations

### Immediate Next Sprint (Top 4)
1. **#23 Pagination regression (720 RICE)** — Regression means we broke something; high reach + impact + confidence. Fix immediately.
2. **#5 Search stale results (640 RICE)** — High reach (users rename projects frequently), cache fix is well-scoped.
3. **#7 Bulk archive (480 RICE)** — 24 customer requests, quick win (S), high demand signal.
4. **#1 Investigation spike: Export >10,000** — Top customer pain (12 reports, enterprise tier). Investigation spike (S) to unblock the real fix.

### Following Sprint
5. **#4 CSV Unicode import (240 RICE)** — Data loss risk + reproducible issue.
6. **#14 Webhook retry (160 RICE)** + **#8 API rate limit headers (160 RICE)** — Both enable developer ecosystem (webhooks + SDK). Can be done in parallel.
7. **#16 Migrate auth library** — Security deadline (6 months EOL). Do not defer.

### After Developer APIs Stabilise
- **#15 Mobile iOS** — Unblocks after #8 complete. Requires architectural design before coding.

### Tech Debt Allocation (20% of capacity, parallel tracks)
- **Q2 Priority 1:** #16 (auth migration) + #24 (audit log for SOC 2 in Q3)
- **Q2 Priority 2:** #19 (Node.js upgrade) + #20 (extract notification service)
- **Q2 Priority 3:** #22 (consolidate config) + #21 (fix mypy errors) + #17 (remove v1 flag)

---

## 6. Data-Driven Refinement

### Items That Could Use Validation

| Item | Data Gap | Recommended Action | Est. Effort |
|------|----------|-------------------|-------------|
| #11 | Dark mode: 89 requests is high volume, but **is it really a priority?** Success metric unclear. | Instrument analytics: track toggle usage if shipped as beta, or survey 10 users who requested it. What percentage would actually use it? | M (1 week) — can run parallel with other work |
| #9 | Zapier: 47 requests over 2 years (~2-3/month). **Is the ROI worth 4-6 weeks?** | Interview 3 customers who requested it. What problem does Zapier solve for them? Can they workaround with webhooks (Item #14)? | M (1 week) |
| #6 | Team workspaces: "3 deals blocked" — **who owns these deals?** Validate deal size and timeline. | Sales team: confirm deal values and expected close dates. Informs priority vs. other features. | S (1 day) |

---

## Summary of Actions

### This Week
- [ ] Create investigation spike for #1 (Export >10,000) — assign to backend engineer
- [ ] Create investigation spike for #2 (Safari dashboard) — assign to frontend engineer
- [ ] Create investigation spike for #3 (Email race condition) — assign to backend engineer
- [ ] Break down #6 (Team workspaces) into 4 user-workflow-based items
- [ ] Break down #18 (SQL to ORM) into 4-5 module-based items
- [ ] Clarify scope for #9 (Zapier), #10 (Custom fields), #13 (Project templates) with product/sales stakeholders

### Next Sprint (Backlog Load)
Schedule items in this order (by RICE + dependencies):
1. #23 — Pagination regression (S, 0.5w)
2. #5 — Search stale (S, 1w)
3. #7 — Bulk archive (S, 0.5w)
4. Investigation: #1 — Export >10k (S, 3-5d)
5. #4 — CSV Unicode (S, 0.5w)
6. #14 + #8 in parallel — Webhooks + API headers (M+S, 1.5w total)
7. #16 — Auth migration (M, 1-2w) [SECURITY DEADLINE]

### Tech Debt Reservation (20% capacity)
- **Critical path:** #16 (security) → #24 (compliance) → #20 (enables both)
- **Foundation work:** #19 (Node upgrade) + #22 (config consolidation)
- **Cleanup:** #21, #17

---

## Related Actions

**Next step:** Use `/product-owner:write-user-story` on top-priority items (e.g., #23, #5, #7) to expand into detailed acceptance criteria and edge cases before scheduling into sprint.

**Backlog hygiene:** Review "Needs Refinement" items weekly; move to "Ready" as clarification happens, or to "Closed" if business context changes.

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
| Score | 14.0/17.0 (82%) |
| Evaluated | 2026-05-03 |
| Target duration | 121527 ms |
| Target cost | $0.1156 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines a structured multi-step process (not a single-step instruction) | PASS | The grooming doc has six numbered sections: Overview → Schedule Next (by RICE Priority) → Needs Refinement → Blocked → Dependency Map → Schedule Rationale & Recommendations → Data-Driven Refinement → Summary of Actions. Clearly multi-step. |
| c2 | Skill requires RICE scoring (Reach, Impact, Confidence, Effort) for items being evaluated for prioritisation | PASS | Section 1 'Schedule Next' table has explicit columns: Reach, Impact, Confidence, Effort, RICE for all feature/bug items (e.g., #23: 200 / 2 / 90% / 0.5w / 720). |
| c3 | Skill defines a classification system with at least these states: Ready, Needs Refinement, and Blocked | PASS | Overview shows 'Ready to schedule: 15 / Needs refinement: 7 / Blocked: 1'. Sections 1, 2, and 3 map exactly to those three states. |
| c4 | Skill requires dependency mapping — identifying which items block or are blocked by others | PASS | Section 4 'Dependency Map' uses explicit arrows: '#8 API rate limit headers → unblocks → #15 Mobile app', '#20 Extract notification service → enables → #24 Audit log', plus external deadlines for #16, #24, #19. |
| c5 | Skill specifies what "Ready" means — criteria a story must meet before it can be pulled into a sprint | FAIL | No explicit Definition of Ready appears in the output. Items in 'Schedule Next' have estimates and dependency columns, but user stories and acceptance criteria are deferred: 'Next step: Use /product-owner:write-user-story on top-priority items... before scheduling into sprint' — confirming 'Schedule Next' items are not yet sprint-ready by the criterion's standard. |
| c6 | Skill requires output as a structured table or list with status, score, and reasoning — not prose | PASS | Every section uses markdown tables: the Schedule Next table has 10 columns (Item, Type, Title, Size, Reach, Impact, Confidence, Effort, RICE, Dependencies); Needs Refinement uses three separate tables; tech debt uses a table with Size, Deadline, Dependencies, Reasoning. |
| c7 | Skill addresses how to handle items that lack sufficient data to score — partial credit if data gaps are mentioned but no specific guidance on how to proceed | PARTIAL | Section 2 defines investigation spikes for #1, #2, #3 with effort estimates. Section 6 'Data-Driven Refinement' names specific data gaps per item (e.g., 'success metric unclear' for #11 dark mode, 'Is ROI worth 4-6 weeks?' for #9 Zapier) with recommended actions and effort estimates. Both data gap detection and action guidance are present. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The skill definition file is not included in the captured output or artifacts. Only the grooming output (backlog-grooming.md) and the input backlog (backlog.md) were written. YAML frontmatter cannot be verified from the runtime output alone. |
| c9 | Output works through all 24 backlog items — not a top-N subset — assigning each a state (Ready / Needs Refinement / Blocked) and either a RICE score or a "data needed" flag | PASS | Section 1 covers 15 items (8 feature/bug with RICE scores: #23, #5, #7, #4, #14, #8, #11, #12; 7 tech debt with scheduling rationale). Section 2 covers 8 items with explicit data-needed explanations. Section 3 covers #15 blocked. Total: 24. All items appear by number. |
| c10 | Output classifies items by type — customer-reported bugs, internal tech debt, new features — and applies prioritisation logic appropriately (bugs with revenue impact compete with features; pure tech debt sits in its own track) | PASS | The Schedule Next table interleaves bugs and features competing on RICE (e.g., Bug #23 at 720 outranks Feature #7 at 480). Tech debt is separately routed to a 'Platform & Infrastructure' table with a '20% sprint capacity' allocation, not scored against features. Types are labeled in every table row. |
| c11 | Output's RICE scoring shows the four columns numerically — Reach, Impact (0.25 / 0.5 / 1 / 2 / 3), Confidence (% based on evidence quality), Effort (person-weeks or story points) — with the formula `(R × I × C) / E` applied per scorable item | PASS | Four numeric columns present. Verified: #23 (200×2×0.9)/0.5=720 ✓; #5 (400×2×0.8)/1=640 ✓; #7 (300×1×0.8)/0.5=480 ✓; #4 (50×3×0.8)/0.5=240 ✓; #14 (100×2×0.8)/1=160 ✓; #8 (50×2×0.8)/0.5=160 ✓; #11 (500×1×0.5)/2=125 ✓. One inconsistency on #12: table shows Reach=50, Effort=1.5w but RICE=107 (formula gives 53); 7/8 calculations verified correct. |
| c12 | Output flags items with insufficient data to score — naming the missing data per item ("need usage analytics for X feature", "need sales-team interview for Y customer-reported bug") rather than assigning made-up confidence | PASS | Section 2 names specific missing data: #1 'Unknown root cause. Could be database timeout, memory limit, pagination logic'; #9 'Scope is undefined. Which Zapier triggers/actions are MVP?'; #10 'No design decision on storage, types, or query support.' Section 6 flags #6: '"3 deals blocked" — who owns these deals? Validate deal size and timeline.' |
| c13 | Output's "Ready" definition is concrete — has user story + acceptance criteria + estimate + dependencies identified — not just "looks fine" | FAIL | Items in 'Schedule Next' have estimates and dependencies but no user stories or acceptance criteria. The Related Actions note explicitly defers this: 'Use /product-owner:write-user-story on top-priority items (#23, #5, #7) to expand into detailed acceptance criteria and edge cases before scheduling into sprint' — confirming that 'Schedule Next' is not equivalent to sprint-Ready. |
| c14 | Output's dependency map identifies blocking relationships — e.g. "Item 12 (mobile feature) blocked by Item 7 (auth refactor)" — so the team can plan in the right order | PASS | Section 4 Dependency Map: '[Item #8: API rate limit headers] → unblocks → [Item #15: Mobile app (iOS)]' and '[Item #20: Extract notification service] → enables → [Future: Multi-channel notifications] + [Item #24: Audit log]'. Section 3 Blocked table also restates the #8→#15 relationship. |
| c15 | Output's recommended sprint candidates are based on RICE ranking + team capacity + dependencies — not "the top 5 by RICE" (which may be all blocked) | PASS | Section 5 'Schedule Rationale' orders candidates by RICE but explicitly adds: investigation spike for #1 (4th despite lacking RICE because of enterprise pain), parallel scheduling of #14+#8 to respect team capacity, 20% tech debt allocation, and #16 flagged 'SECURITY DEADLINE' above its RICE rank. #15 (would rank high by request volume) is deferred due to #8 dependency. |
| c16 | Output's data-gap recommendations are actionable — e.g. "instrument feature X before scoring", "interview 3 enterprise customers about Y" — with effort estimates so the data work itself can be prioritised | PASS | Section 6: #11 dark mode → 'Instrument analytics: track toggle usage if shipped as beta, or survey 10 users who requested it' → 'M (1 week)'; #9 Zapier → 'Interview 3 customers who requested it' → 'M (1 week)'; #6 team workspaces → 'Sales team: confirm deal values and expected close dates' → 'S (1 day)'. All three have effort estimates. |
| c17 | Output produces the result as a structured table — Item \| Type \| State \| RICE \| Dependencies \| Reasoning — not prose paragraphs | PASS | The entire grooming document uses markdown tables throughout. The Schedule Next table has columns Item, Type, Title, Size, Reach, Impact, Confidence, Effort, RICE, Dependencies. Tech debt table has Item, Type, Title, Size, Deadline, Dependencies, Reasoning. Needs Refinement tables have Item, Issue, Action Needed, Est. Effort. No prose-only sections. |
| c18 | Output addresses how stale backlog items are handled — items >6 months old without movement should be archived or reconfirmed, not silently kept on the list | PARTIAL | The 'Backlog hygiene' note under Related Actions says: 'Review Needs Refinement items weekly; move to Ready as clarification happens, or to Closed if business context changes.' This acknowledges closing items under certain conditions but provides no age-based staleness threshold (e.g., '>6 months old without movement = archive or reconfirm'). The concept of closure is present but not operationalised as a staleness policy. |

### Notes

The output is a genuinely strong product grooming artifact: all 24 items are classified, 8 feature/bug items have verified RICE calculations, the dependency map is explicit, and data-gap recommendations include effort estimates making them schedulable. The main gaps are architectural: (1) c8 — no skill definition file was produced so YAML frontmatter cannot be verified; (2) c5 and c13 — the output conflates 'prioritized and sized' with 'Ready for sprint', explicitly deferring user story and acceptance criteria creation to a separate downstream step (/product-owner:write-user-story), which means items marked 'Schedule Next' lack a concrete Definition of Ready. The minor RICE arithmetic error on item #12 (shows 107, formula gives ~53) is notable but isolated. The treatment of tech debt outside RICE (with a 20% capacity track and deadline-based rationale) is pragmatically sound but technically departs from the stated scoring requirement. Overall the output delivers most of the required structure and analysis at a high quality level.
