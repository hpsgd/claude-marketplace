# Test: Write battle card

Scenario: Testing whether the write-battle-card skill produces at least 4 objection/response pairs, includes landmine questions, and fits on a single page for sales use.

## Prompt

First, set up product and competitive context:

```bash
mkdir -p sales/competitive product
```

Write to `product/positioning.md`:

```markdown
# Clearpath — Product Positioning

Clearpath is a project management platform built for operations teams at mid-market companies (50–500 employees).

### Core Differentiators
- **Executive reporting:** Native roll-up views across all projects for leadership teams. No manual exports required.
- **Custom calculations:** Formula fields that aggregate data across multiple projects in a single dashboard view.
- **Operations focus:** Built-in process templates for ops workflows (procurement, vendor management, facilities).
- **Compliance audit trail:** Full activity log with user attribution. SOC 2 certified.

### Pricing
- Starter: $12/user/month (up to 10 users)
- Professional: $22/user/month (unlimited users, custom fields, API access)
- Enterprise: $38/user/month (SSO, audit log, dedicated CSM, SLA)

### Where Clearpath Wins
- Reporting-heavy workflows where teams present to executives weekly
- Operations teams managing cross-functional processes
- Companies with compliance requirements (financial services, healthcare adjacent)

### Where Clearpath Loses
- Very small teams (<10 users) doing simple task tracking
- Creative agencies preferring visual kanban over table views
- Teams already deep in Monday ecosystem with automations built
```

Write to `sales/competitive/monday-win-loss.md`:

```markdown
# Monday.com Win/Loss Analysis — Last Quarter

### Lost to Monday (8 deals)
Reasons cited:
- "Monday's UI felt more modern and the trial was easier to set up" (4 deals)
- "Monday was cheaper per user for our team size" (2 deals — both <15 users)
- "Our IT team already uses Monday for another department" (2 deals)

### Won Against Monday (5 deals)
Reasons cited:
- "Clearpath's executive dashboard was a decisive factor — Monday required manual exports for our weekly board report" (3 deals)
- "Custom formula fields across projects — Monday couldn't do that in their standard tier" (2 deals)

### Common Late-Stage Monday Objections
1. "Monday is cheaper" — often true for small teams, comparable at 25+ users with analytics tier
2. "Monday is easier to use" — onboarding friction is real for Clearpath ops templates
3. "Our team already knows Monday" — switching cost objection
4. "Monday has more integrations" — 200+ vs Clearpath's 45 native integrations
```

Then run:

/gtm:write-battle-card for competing against Monday.com — our sales team keeps losing deals when Monday comes up late in the evaluation and we don't have a consistent response.

## Criteria


- [ ] PASS: Skill requires a competitor research step before writing — not synthesising from assumptions about Monday.com
- [ ] PASS: Skill requires win/loss analysis — understanding why deals were won or lost against this competitor specifically
- [ ] PASS: Skill produces at least 4 objection/response pairs — covering the most common objections sales encounters
- [ ] PASS: Skill includes landmine questions — questions reps can ask to surface issues where Clearpath wins and Monday loses
- [ ] PASS: Skill produces output that fits on a single page — the battle card must be scannable in under 60 seconds
- [ ] PASS: All messaging is labelled DRAFT and flagged for human review before sales use
- [ ] PARTIAL: Skill differentiates between objection responses for different buyer types or stages — partial credit if responses are provided but not segmented by buyer persona or deal stage
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's research notes on Monday.com are sourced — pricing tiers, target segment, recent positioning shifts (e.g. Monday's CRM expansion), recent product gaps — not generic "Monday is popular"
- [ ] PASS: Output's win/loss analysis identifies WHY Clearpath has lost to Monday late in deals — late-stage objections, pricing comparisons, feature checklist battles — and the corresponding wins
- [ ] PASS: Output produces at least 4 objection / response pairs — each starting with the actual objection in the customer's voice (e.g. "Monday is cheaper") and a confident, specific response (e.g. "On per-user cost yes, but Monday's reporting tier costs an additional X — total cost for analytics-grade workflow is comparable")
- [ ] PASS: Output's landmine questions are designed to surface issues where Monday struggles — e.g. "How do you currently roll up project status across teams to your exec team?" (Monday lacks native exec rollup) or "What's your process when an OPS dashboard needs custom calculations across multiple boards?"
- [ ] PASS: Output fits a single page — visually scannable in under 60 seconds — with sections clearly delimited (Strengths, Their Weakness, Objections, Questions, Pricing) — not a multi-page narrative
- [ ] PASS: Output's competitive truth is honest — does NOT claim Clearpath wins on every dimension; names where Monday legitimately wins (e.g. "Monday's UI is more polished for first-time users") so reps don't get caught off-guard
- [ ] PASS: Output labels all messaging as DRAFT — flagged for human review (sales enablement, marketing leadership) before deployment to the sales team
- [ ] PASS: Output's tone is calm and confident — not defensive, not bashing — competitor-respect with clear differentiation
- [ ] PASS: Output's responses include proof points — case studies, specific numbers, customer quotes — not just "we're better at X" without backup
- [ ] PARTIAL: Output addresses different buyer types — IT decision-maker (focuses on integration, security), Operations leader (focuses on reporting, exec visibility), End-user team lead (focuses on day-to-day usability) — with at least different-emphasis responses per type
