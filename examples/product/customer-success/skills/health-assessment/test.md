# Test: Health assessment

Scenario: Testing whether the health-assessment skill scores all 5 dimensions with correct weights, produces a composite health score, and recommends specific interventions rather than generic advice.

## Prompt

First, create the account health data:

```bash
mkdir -p accounts
```

Write to `accounts/enterprise-portfolio.yaml`:

```yaml
accounts:
  - name: Acme Corp
    arr: 84000
    renewal_date: 2025-03-15
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.62
      features_used: [projects, tasks, reports, api, export]
      recent_trend: stable
    engagement:
      logins_last_30d: 340
      trend: increasing
      support_tickets_last_30d: 2
    relationship:
      nps_score: 8
      exec_sponsor: confirmed
      last_meeting: 2024-11-10
    value_realisation:
      stated_goal: "Replace spreadsheet project tracking"
      goal_status: achieved
      roi_documented: true
    commercial:
      payment_status: current
      contract_length_months: 24
      months_remaining: 5

  - name: BrightPath Solutions
    arr: 62000
    renewal_date: 2025-02-28
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.21
      features_used: [projects, tasks]
      recent_trend: declining
    engagement:
      logins_last_30d: 45
      trend: declining_30pct
      support_tickets_last_30d: 8
    relationship:
      nps_score: 4
      exec_sponsor: "no sponsor identified"
      last_meeting: 2024-09-03
    value_realisation:
      stated_goal: "Improve cross-team visibility"
      goal_status: not_achieved
      roi_documented: false
    commercial:
      payment_status: current
      contract_length_months: 12
      months_remaining: 2

  - name: Meridian Financial
    arr: 156000
    renewal_date: 2025-06-30
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.71
      features_used: [projects, tasks, reports, api, export, audit_log, sso]
      recent_trend: stable
    engagement:
      logins_last_30d: 820
      trend: stable
      support_tickets_last_30d: 1
    relationship:
      nps_score: 9
      exec_sponsor: confirmed
      last_meeting: 2024-11-20
    value_realisation:
      stated_goal: "SOC 2 audit trail and project governance"
      goal_status: achieved
      roi_documented: true
    commercial:
      payment_status: current
      contract_length_months: 36
      months_remaining: 18

  - name: Thunderstone Retail
    arr: 48000
    renewal_date: 2025-01-31
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.18
      features_used: [projects]
      recent_trend: declining
    engagement:
      logins_last_30d: 22
      trend: declining_50pct
      support_tickets_last_30d: 12
    relationship:
      nps_score: 3
      exec_sponsor: "champion left company last month"
      last_meeting: 2024-08-14
    value_realisation:
      stated_goal: "Replace project management tool for ops team"
      goal_status: stalled
      roi_documented: false
    commercial:
      payment_status: 30_days_overdue
      contract_length_months: 12
      months_remaining: 1

  - name: CloudNine Logistics
    arr: 72000
    renewal_date: 2025-04-15
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.55
      features_used: [projects, tasks, reports, export]
      recent_trend: stable
    engagement:
      logins_last_30d: 210
      trend: stable
      support_tickets_last_30d: 3
    relationship:
      nps_score: 7
      exec_sponsor: confirmed
      last_meeting: 2024-11-01
    value_realisation:
      stated_goal: "Real-time shipment project visibility"
      goal_status: partially_achieved
      roi_documented: false
    commercial:
      payment_status: current
      contract_length_months: 12
      months_remaining: 5

  - name: Pinnacle Healthcare
    arr: 93000
    renewal_date: 2025-05-31
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.44
      features_used: [projects, tasks, reports, api]
      recent_trend: stable
    engagement:
      logins_last_30d: 155
      trend: stable
      support_tickets_last_30d: 5
    relationship:
      nps_score: 6
      exec_sponsor: confirmed
      last_meeting: 2024-10-22
    value_realisation:
      stated_goal: "Compliance project tracking"
      goal_status: on_track
      roi_documented: false
    commercial:
      payment_status: current
      contract_length_months: 24
      months_remaining: 7

  - name: Vertex Engineering
    arr: 38000
    renewal_date: 2025-03-01
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.12
      features_used: [projects]
      recent_trend: declining
    engagement:
      logins_last_30d: 18
      trend: declining_40pct
      support_tickets_last_30d: 14
    relationship:
      nps_score: 2
      exec_sponsor: "no response in 60 days"
      last_meeting: 2024-08-30
    value_realisation:
      stated_goal: "Engineering project portfolio"
      goal_status: not_achieved
      roi_documented: false
    commercial:
      payment_status: current
      contract_length_months: 12
      months_remaining: 3

  - name: Cascade Media
    arr: 55000
    renewal_date: 2025-07-15
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.68
      features_used: [projects, tasks, reports, export, api]
      recent_trend: increasing
    engagement:
      logins_last_30d: 290
      trend: increasing
      support_tickets_last_30d: 1
    relationship:
      nps_score: 9
      exec_sponsor: confirmed
      last_meeting: 2024-11-18
    value_realisation:
      stated_goal: "Content production tracking"
      goal_status: exceeded
      roi_documented: true
    commercial:
      payment_status: current
      contract_length_months: 24
      months_remaining: 9

  - name: Strata Property Group
    arr: 41000
    renewal_date: 2025-04-01
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.35
      features_used: [projects, tasks]
      recent_trend: stable
    engagement:
      logins_last_30d: 88
      trend: stable
      support_tickets_last_30d: 4
    relationship:
      nps_score: 6
      exec_sponsor: confirmed
      last_meeting: 2024-10-15
    value_realisation:
      stated_goal: "Property development project tracking"
      goal_status: partially_achieved
      roi_documented: false
    commercial:
      payment_status: current
      contract_length_months: 12
      months_remaining: 5

  - name: NovaTech Systems
    arr: 110000
    renewal_date: 2025-08-31
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.59
      features_used: [projects, tasks, reports, api, sso, export, audit_log]
      recent_trend: increasing
    engagement:
      logins_last_30d: 480
      trend: increasing
      support_tickets_last_30d: 2
    relationship:
      nps_score: 8
      exec_sponsor: confirmed
      last_meeting: 2024-11-12
    value_realisation:
      stated_goal: "IT project portfolio management"
      goal_status: achieved
      roi_documented: true
    commercial:
      payment_status: current
      contract_length_months: 24
      months_remaining: 10

  - name: Hargreaves Consulting
    arr: 29000
    renewal_date: 2025-02-01
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.09
      features_used: [projects]
      recent_trend: declining
    engagement:
      logins_last_30d: 8
      trend: declining_70pct
      support_tickets_last_30d: 0
    relationship:
      nps_score: null
      exec_sponsor: "unknown — contact unresponsive"
      last_meeting: 2024-07-05
    value_realisation:
      stated_goal: "unknown"
      goal_status: unknown
      roi_documented: false
    commercial:
      payment_status: current
      contract_length_months: 12
      months_remaining: 2

  - name: Pacific Distribution
    arr: 67000
    renewal_date: 2025-05-15
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.47
      features_used: [projects, tasks, reports, export]
      recent_trend: stable
    engagement:
      logins_last_30d: 175
      trend: stable
      support_tickets_last_30d: 3
    relationship:
      nps_score: 7
      exec_sponsor: confirmed
      last_meeting: 2024-10-28
    value_realisation:
      stated_goal: "Warehouse and logistics project tracking"
      goal_status: on_track
      roi_documented: false
    commercial:
      payment_status: current
      contract_length_months: 12
      months_remaining: 6

  - name: Streamline Insurance
    arr: 88000
    renewal_date: 2025-09-30
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.53
      features_used: [projects, tasks, reports, api, audit_log]
      recent_trend: stable
    engagement:
      logins_last_30d: 260
      trend: stable
      support_tickets_last_30d: 4
    relationship:
      nps_score: 7
      exec_sponsor: confirmed
      last_meeting: 2024-11-05
    value_realisation:
      stated_goal: "Claims project management and compliance tracking"
      goal_status: on_track
      roi_documented: false
    commercial:
      payment_status: current
      contract_length_months: 24
      months_remaining: 11

  - name: Frontier Mining
    arr: 45000
    renewal_date: 2025-01-15
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.28
      features_used: [projects, tasks]
      recent_trend: declining
    engagement:
      logins_last_30d: 55
      trend: declining_20pct
      support_tickets_last_30d: 7
    relationship:
      nps_score: 5
      exec_sponsor: "confirmed but low engagement"
      last_meeting: 2024-09-20
    value_realisation:
      stated_goal: "Mine site project coordination"
      goal_status: partially_achieved
      roi_documented: false
    commercial:
      payment_status: current
      contract_length_months: 12
      months_remaining: 2

  - name: Apex Legal
    arr: 36000
    renewal_date: 2025-06-01
    plan: enterprise
    adoption:
      dau_mau_ratio: 0.41
      features_used: [projects, tasks, reports]
      recent_trend: stable
    engagement:
      logins_last_30d: 95
      trend: stable
      support_tickets_last_30d: 2
    relationship:
      nps_score: 7
      exec_sponsor: confirmed
      last_meeting: 2024-10-08
    value_realisation:
      stated_goal: "Matter and case project tracking"
      goal_status: on_track
      roi_documented: false
    commercial:
      payment_status: current
      contract_length_months: 12
      months_remaining: 7
```

Then run:

/customer-success:health-assessment for our top 15 enterprise accounts ahead of our quarterly CS team review — we need to know which accounts need immediate attention.

## Criteria


- [ ] PASS: Skill scores all 5 dimensions: Adoption (30%), Engagement (25%), Relationship (20%), Value Realisation (15%), Commercial (10%)
- [ ] PASS: Skill calculates a composite health score using the correct weighted formula — not an unweighted average
- [ ] PASS: Skill classifies accounts into health categories (e.g. Green/Yellow/Red or equivalent) with defined thresholds
- [ ] PASS: Skill requires identifying data sources for each dimension before scoring — not scoring from memory
- [ ] PASS: Skill identifies specific risk signals per account — not just a score, but what is driving it
- [ ] PASS: Skill produces recommended interventions for at-risk accounts — specific actions, not "schedule a check-in"
- [ ] PARTIAL: Skill produces a portfolio summary view — partial credit if individual accounts are assessed but no aggregated portfolio view is required
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output assesses all 15 accounts — not a sample, not a "top movers" subset — with a row per account in the resulting table
- [ ] PASS: Output scores each account on all 5 dimensions — Adoption (30%), Engagement (25%), Relationship (20%), Value Realisation (15%), Commercial (10%) — and shows the per-dimension score per account
- [ ] PASS: Output computes the composite score using the WEIGHTED formula: Adoption*0.30 + Engagement*0.25 + Relationship*0.20 + Value*0.15 + Commercial*0.10 — not a simple average; the math is verifiable from the per-dimension scores
- [ ] PASS: Output classifies each account into a defined health tier with stated numeric thresholds (e.g. Healthy/Neutral/At Risk/Critical or Green/Yellow/Red) — not just "looks healthy"
- [ ] PASS: Output names the data source per dimension before scoring — adoption from product analytics, engagement from in-app event tracking, relationship from CRM contact frequency, value from QBR notes, commercial from billing/contract data — not scoring from CSM memory
- [ ] PASS: Output identifies specific risk signals per at-risk account — not just "Score 55, Red" but "Adoption dropped 30% in last 60 days, no exec sponsor identified, support tickets ticked up to 12/month from 3"
- [ ] PASS: Output's recommended interventions per at-risk account are specific actions tied to the failing dimension — e.g. "Adoption red: schedule training session with team lead by Friday; Relationship red: identify backup champion within IT" — not "schedule a check-in"
- [ ] PASS: Output's portfolio summary view aggregates the 15 accounts with a health distribution count (e.g. "3 Critical, 4 At Risk, 8 Healthy") so the CS leadership team can prioritise meeting time
- [ ] PARTIAL: Output prioritises at-risk accounts for the upcoming review — listing the most at-risk accounts first with the specific intervention required; partial credit if prioritised but missing commercial context (renewal date, ARR)
- [ ] PARTIAL: Output flags trends across the portfolio — e.g. "adoption is the weakest dimension across the at-risk accounts, suggesting a systemic onboarding gap" — not just per-account observations
