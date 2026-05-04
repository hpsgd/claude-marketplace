# Health Assessment

Scenario: Testing whether the health-assessment skill scores all 5 dimensions with correct weights, produces a composite health score, and recommends specific interventions rather than generic advice.

## Prompt

> First, create the account health data:
> 
> ```bash
> mkdir -p accounts
> ```
> 
> Write to `accounts/enterprise-portfolio.yaml`:
> 
> ```yaml
> accounts:
>   - name: Acme Corp
>     arr: 84000
>     renewal_date: 2025-03-15
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.62
>       features_used: [projects, tasks, reports, api, export]
>       recent_trend: stable
>     engagement:
>       logins_last_30d: 340
>       trend: increasing
>       support_tickets_last_30d: 2
>     relationship:
>       nps_score: 8
>       exec_sponsor: confirmed
>       last_meeting: 2024-11-10
>     value_realisation:
>       stated_goal: "Replace spreadsheet project tracking"
>       goal_status: achieved
>       roi_documented: true
>     commercial:
>       payment_status: current
>       contract_length_months: 24
>       months_remaining: 5
> 
>   - name: BrightPath Solutions
>     arr: 62000
>     renewal_date: 2025-02-28
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.21
>       features_used: [projects, tasks]
>       recent_trend: declining
>     engagement:
>       logins_last_30d: 45
>       trend: declining_30pct
>       support_tickets_last_30d: 8
>     relationship:
>       nps_score: 4
>       exec_sponsor: "no sponsor identified"
>       last_meeting: 2024-09-03
>     value_realisation:
>       stated_goal: "Improve cross-team visibility"
>       goal_status: not_achieved
>       roi_documented: false
>     commercial:
>       payment_status: current
>       contract_length_months: 12
>       months_remaining: 2
> 
>   - name: Meridian Financial
>     arr: 156000
>     renewal_date: 2025-06-30
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.71
>       features_used: [projects, tasks, reports, api, export, audit_log, sso]
>       recent_trend: stable
>     engagement:
>       logins_last_30d: 820
>       trend: stable
>       support_tickets_last_30d: 1
>     relationship:
>       nps_score: 9
>       exec_sponsor: confirmed
>       last_meeting: 2024-11-20
>     value_realisation:
>       stated_goal: "SOC 2 audit trail and project governance"
>       goal_status: achieved
>       roi_documented: true
>     commercial:
>       payment_status: current
>       contract_length_months: 36
>       months_remaining: 18
> 
>   - name: Thunderstone Retail
>     arr: 48000
>     renewal_date: 2025-01-31
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.18
>       features_used: [projects]
>       recent_trend: declining
>     engagement:
>       logins_last_30d: 22
>       trend: declining_50pct
>       support_tickets_last_30d: 12
>     relationship:
>       nps_score: 3
>       exec_sponsor: "champion left company last month"
>       last_meeting: 2024-08-14
>     value_realisation:
>       stated_goal: "Replace project management tool for ops team"
>       goal_status: stalled
>       roi_documented: false
>     commercial:
>       payment_status: 30_days_overdue
>       contract_length_months: 12
>       months_remaining: 1
> 
>   - name: CloudNine Logistics
>     arr: 72000
>     renewal_date: 2025-04-15
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.55
>       features_used: [projects, tasks, reports, export]
>       recent_trend: stable
>     engagement:
>       logins_last_30d: 210
>       trend: stable
>       support_tickets_last_30d: 3
>     relationship:
>       nps_score: 7
>       exec_sponsor: confirmed
>       last_meeting: 2024-11-01
>     value_realisation:
>       stated_goal: "Real-time shipment project visibility"
>       goal_status: partially_achieved
>       roi_documented: false
>     commercial:
>       payment_status: current
>       contract_length_months: 12
>       months_remaining: 5
> 
>   - name: Pinnacle Healthcare
>     arr: 93000
>     renewal_date: 2025-05-31
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.44
>       features_used: [projects, tasks, reports, api]
>       recent_trend: stable
>     engagement:
>       logins_last_30d: 155
>       trend: stable
>       support_tickets_last_30d: 5
>     relationship:
>       nps_score: 6
>       exec_sponsor: confirmed
>       last_meeting: 2024-10-22
>     value_realisation:
>       stated_goal: "Compliance project tracking"
>       goal_status: on_track
>       roi_documented: false
>     commercial:
>       payment_status: current
>       contract_length_months: 24
>       months_remaining: 7
> 
>   - name: Vertex Engineering
>     arr: 38000
>     renewal_date: 2025-03-01
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.12
>       features_used: [projects]
>       recent_trend: declining
>     engagement:
>       logins_last_30d: 18
>       trend: declining_40pct
>       support_tickets_last_30d: 14
>     relationship:
>       nps_score: 2
>       exec_sponsor: "no response in 60 days"
>       last_meeting: 2024-08-30
>     value_realisation:
>       stated_goal: "Engineering project portfolio"
>       goal_status: not_achieved
>       roi_documented: false
>     commercial:
>       payment_status: current
>       contract_length_months: 12
>       months_remaining: 3
> 
>   - name: Cascade Media
>     arr: 55000
>     renewal_date: 2025-07-15
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.68
>       features_used: [projects, tasks, reports, export, api]
>       recent_trend: increasing
>     engagement:
>       logins_last_30d: 290
>       trend: increasing
>       support_tickets_last_30d: 1
>     relationship:
>       nps_score: 9
>       exec_sponsor: confirmed
>       last_meeting: 2024-11-18
>     value_realisation:
>       stated_goal: "Content production tracking"
>       goal_status: exceeded
>       roi_documented: true
>     commercial:
>       payment_status: current
>       contract_length_months: 24
>       months_remaining: 9
> 
>   - name: Strata Property Group
>     arr: 41000
>     renewal_date: 2025-04-01
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.35
>       features_used: [projects, tasks]
>       recent_trend: stable
>     engagement:
>       logins_last_30d: 88
>       trend: stable
>       support_tickets_last_30d: 4
>     relationship:
>       nps_score: 6
>       exec_sponsor: confirmed
>       last_meeting: 2024-10-15
>     value_realisation:
>       stated_goal: "Property development project tracking"
>       goal_status: partially_achieved
>       roi_documented: false
>     commercial:
>       payment_status: current
>       contract_length_months: 12
>       months_remaining: 5
> 
>   - name: NovaTech Systems
>     arr: 110000
>     renewal_date: 2025-08-31
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.59
>       features_used: [projects, tasks, reports, api, sso, export, audit_log]
>       recent_trend: increasing
>     engagement:
>       logins_last_30d: 480
>       trend: increasing
>       support_tickets_last_30d: 2
>     relationship:
>       nps_score: 8
>       exec_sponsor: confirmed
>       last_meeting: 2024-11-12
>     value_realisation:
>       stated_goal: "IT project portfolio management"
>       goal_status: achieved
>       roi_documented: true
>     commercial:
>       payment_status: current
>       contract_length_months: 24
>       months_remaining: 10
> 
>   - name: Hargreaves Consulting
>     arr: 29000
>     renewal_date: 2025-02-01
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.09
>       features_used: [projects]
>       recent_trend: declining
>     engagement:
>       logins_last_30d: 8
>       trend: declining_70pct
>       support_tickets_last_30d: 0
>     relationship:
>       nps_score: null
>       exec_sponsor: "unknown — contact unresponsive"
>       last_meeting: 2024-07-05
>     value_realisation:
>       stated_goal: "unknown"
>       goal_status: unknown
>       roi_documented: false
>     commercial:
>       payment_status: current
>       contract_length_months: 12
>       months_remaining: 2
> 
>   - name: Pacific Distribution
>     arr: 67000
>     renewal_date: 2025-05-15
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.47
>       features_used: [projects, tasks, reports, export]
>       recent_trend: stable
>     engagement:
>       logins_last_30d: 175
>       trend: stable
>       support_tickets_last_30d: 3
>     relationship:
>       nps_score: 7
>       exec_sponsor: confirmed
>       last_meeting: 2024-10-28
>     value_realisation:
>       stated_goal: "Warehouse and logistics project tracking"
>       goal_status: on_track
>       roi_documented: false
>     commercial:
>       payment_status: current
>       contract_length_months: 12
>       months_remaining: 6
> 
>   - name: Streamline Insurance
>     arr: 88000
>     renewal_date: 2025-09-30
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.53
>       features_used: [projects, tasks, reports, api, audit_log]
>       recent_trend: stable
>     engagement:
>       logins_last_30d: 260
>       trend: stable
>       support_tickets_last_30d: 4
>     relationship:
>       nps_score: 7
>       exec_sponsor: confirmed
>       last_meeting: 2024-11-05
>     value_realisation:
>       stated_goal: "Claims project management and compliance tracking"
>       goal_status: on_track
>       roi_documented: false
>     commercial:
>       payment_status: current
>       contract_length_months: 24
>       months_remaining: 11
> 
>   - name: Frontier Mining
>     arr: 45000
>     renewal_date: 2025-01-15
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.28
>       features_used: [projects, tasks]
>       recent_trend: declining
>     engagement:
>       logins_last_30d: 55
>       trend: declining_20pct
>       support_tickets_last_30d: 7
>     relationship:
>       nps_score: 5
>       exec_sponsor: "confirmed but low engagement"
>       last_meeting: 2024-09-20
>     value_realisation:
>       stated_goal: "Mine site project coordination"
>       goal_status: partially_achieved
>       roi_documented: false
>     commercial:
>       payment_status: current
>       contract_length_months: 12
>       months_remaining: 2
> 
>   - name: Apex Legal
>     arr: 36000
>     renewal_date: 2025-06-01
>     plan: enterprise
>     adoption:
>       dau_mau_ratio: 0.41
>       features_used: [projects, tasks, reports]
>       recent_trend: stable
>     engagement:
>       logins_last_30d: 95
>       trend: stable
>       support_tickets_last_30d: 2
>     relationship:
>       nps_score: 7
>       exec_sponsor: confirmed
>       last_meeting: 2024-10-08
>     value_realisation:
>       stated_goal: "Matter and case project tracking"
>       goal_status: on_track
>       roi_documented: false
>     commercial:
>       payment_status: current
>       contract_length_months: 12
>       months_remaining: 7
> ```
> 
> Then run:
> 
> /customer-success:health-assessment for our top 15 enterprise accounts ahead of our quarterly CS team review — we need to know which accounts need immediate attention.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

I'll work through this assessment systematically following the health-assessment framework.

## Step 1: Data Sources ✓
All required dimensions present in the portfolio data: product usage metrics, engagement patterns, relationship indicators, value realisation signals, and commercial status.

## Step 2-3: Score Each Account & Calculate Composite

Let me assess all 15 accounts:

| Account | Adoption (30%) | Engagement (25%) | Relationship (20%) | Value (15%) | Commercial (10%) | Composite | Status |
|---|---|---|---|---|---|---|---|
| Acme Corp | 78 | 82 | 85 | 85 | 80 | **81.65** | Healthy |
| BrightPath Solutions | 35 | 38 | 32 | 28 | 65 | **37.1** | Critical |
| Meridian Financial | 88 | 90 | 92 | 90 | 95 | **90.3** | Healthy |
| Thunderstone Retail | 25 | 28 | 20 | 25 | 25 | **24.75** | Critical |
| CloudNine Logistics | 72 | 75 | 78 | 62 | 75 | **72.75** | Neutral |
| Pinnacle Healthcare | 65 | 70 | 72 | 65 | 80 | **69.15** | Neutral |
| Vertex Engineering | 22 | 25 | 18 | 22 | 70 | **26.75** | Critical |
| Cascade Media | 85 | 88 | 90 | 92 | 85 | **87.8** | Healthy |
| Strata Property Group | 45 | 60 | 72 | 58 | 75 | **59.1** | Neutral |
| NovaTech Systems | 88 | 88 | 85 | 88 | 85 | **87.1** | Healthy |
| Hargreaves Consulting | 18 | 15 | 15 | 30 | 70 | **23.65** | Critical |
| Pacific Distribution | 68 | 72 | 78 | 62 | 78 | **71.1** | Neutral |
| Streamline Insurance | 75 | 75 | 78 | 62 | 85 | **74.65** | Neutral |
| Frontier Mining | 38 | 45 | 58 | 52 | 75 | **49.55** | At Risk |
| Apex Legal | 60 | 70 | 78 | 62 | 78 | **68.2** | Neutral |

## Step 4: Classification & Portfolio Distribution

| Health Tier | Count | ARR at Risk |
|---|---|---|
| **Healthy** | 4 | $397k (nurture & expand) |
| **Neutral** | 6 | $467k (monitor) |
| **At Risk** | 1 | $45k (intervene) |
| **Critical** | 4 | $179k (escalate) |

## Step 5: Active Risk Signals by Account

### 🔴 CRITICAL (Immediate action required)

**Thunderstone Retail** — $48k ARR, renewal in ~2 months
- **Composite:** 24.75 (lowest portfolio score)
- **Critical signals:** Payment 30 days overdue ⚠️ | Champion left company | Usage declining 50% | NPS 3 | Only 1 feature adopted
- **Trend:** Actively churning
- **Root cause:** Loss of executive sponsor + product misfit for ops team

**Vertex Engineering** — $38k ARR, renewal in ~1 month
- **Composite:** 26.75
- **Critical signals:** Renewal imminent | Unresponsive (no contact 60 days) | Usage declining 40% | NPS 2 | High support load (14 tickets)
- **Root cause:** Minimal adoption, relationship broken, likely already decided to leave

**Hargreaves Consulting** — $29k ARR, renewal in ~1 month
- **Composite:** 23.65 (second lowest)
- **Critical signals:** Renewal imminent | Completely unresponsive | Usage declined 70% | Abandoned (8 logins/month) | No NPS signal
- **Root cause:** Unknown — account is silent
- **Risk:** Likely a churn without notice

**BrightPath Solutions** — $62k ARR, renewal in ~3 months
- **Composite:** 37.1
- **Critical signals:** Usage declining | Low engagement (45 logins/month) | No exec sponsor | NPS 4 (detractor) | High support load (8 tickets)
- **Root cause:** Product not delivering cross-team visibility promise; no relationship structure to course-correct

### 🟡 AT RISK (Intervention within 1 week)

**Frontier Mining** — $45k ARR, renewal in ~1.5 months
- **Composite:** 49.55
- **Signals:** Usage declining 20% | NPS 5 (passable but trending down) | Sponsor exists but low engagement | Partially achieving goals | Renewal in 6 weeks
- **Root cause:** Underperforming against stated goal ("mine site project coordination"); sponsor not engaged

---

## Step 6: Prioritised Intervention Plan

### TIER 1: Escalate Immediately (within 48 hours)

| Account | Issue | Intervention | Owner | Timeline | Success Criteria |
|---|---|---|---|---|---|
| **Thunderstone Retail** | Payment overdue + champion gone | Executive escalation + retention call | VP CS | By May 6 | Either: payment received + new sponsor identified, OR churn formally acknowledged + wind-down plan |
| **Vertex Engineering** | Silent with renewal in 1 month | Outbound executive call (bypass normal contacts) | VP CS | By May 5 | Live conversation about renewal intent + usage barriers |
| **Hargreaves Consulting** | Completely dark 60 days before renewal | Multi-channel outreach: phone + email + LinkedIn | CS Manager | By May 5 | Make contact + understand status (staying / leaving / inactive) |

### TIER 2: Proactive Intervention (within 1 week)

| Account | Issue | Intervention | Owner | Timeline | Success Criteria |
|---|---|---|---|---|---|
| **BrightPath Solutions** | No sponsor + declining usage | Org chart analysis + sponsor identification | CS Manager | By May 10 | Identify new sponsor + schedule business review with exec |
| **Frontier Mining** | Declining usage, weak sponsor | Usage review call + goal reset | CS Manager | By May 9 | Understand why adoption plateaued + define 90-day success metrics |

---

## Step 7: Portfolio Trends & Systemic Observations

### Weakest Dimensions Across At-Risk Cohort

1. **Relationship (20% weight)** — The critical cohort has an average relationship score of **21** vs portfolio average of **67**
   - **Pattern:** 3 of 4 critical accounts have NO exec sponsor or unresponsive sponsor
   - **Action:** Add sponsor identification to onboarding; require confirmed sponsor before contract close

2. **Product Adoption (30% weight)** — Critical cohort averaging **25** vs portfolio average of **63**
   - **Pattern:** All 4 critical accounts using 1-2 features only; no feature breadth
   - **Action:** Onboarding is not reaching power users. Build feature adoption workflow for first 30 days

3. **Value Realisation (15% weight)** — Critical cohort averaging **26** vs portfolio average of **65**
   - **Pattern:** Goals either unknown, not defined, or stalled. No customer has documented ROI
   - **Action:** Customer success playbook missing "goal definition workshop" before first 30 days end

### Systemic Patterns

**Renewal risk cluster:** 6 of 15 accounts renewing within 60 days (Thunderstone, Vertex, Hargreaves, Frontier, BrightPath, Pacific)
- Of these, 4 are critical/at-risk → **67% of near-term renewals at risk**
- Current portfolio trending to **~$200k ARR churn** in next 2 months if critical accounts don't convert

**No-value-documented baseline:** 10 of 15 accounts have "roi_documented: false"
- Healthy accounts document ROI; at-risk accounts don't
- **Inference:** If customers can't articulate ROI themselves, they can't defend renewal internally

**Sponsorship gap:** 5 accounts lack confirmed exec sponsor or have unresponsive sponsor
- All 5 are Neutral or Critical
- **No Healthy account lacks a confirmed sponsor**

### Recommended Portfolio Actions

1. **Immediate (this week):**
   - Escalate 4 critical accounts per intervention plan
   - Conduct win/loss analysis on Thunderstone, Vertex, Hargreaves to learn why adoption failed

2. **Short-term (next 30 days):**
   - Launch "Value Realisation Workshop" for all Neutral accounts (goal definition + success metrics + ROI framework)
   - Add sponsor health check to all accounts renewing in 60 days
   - Create adoption playbook targeting feature breadth in first 30 days (currently critical accounts use only 1-2 features)

3. **Medium-term (next quarter):**
   - Implement "sponsor confirmation" as gate before go-live (prevent unsponsored deals from closing)
   - Build proactive value tracking: auto-measure adoption against customer-stated goals, surface gaps monthly

---

## At a Glance: Who Needs What, By When

**By May 5 (Tomorrow):** Reach Vertex, Hargreaves, Thunderstone
**By May 9:** Frontier Mining value reset call
**By May 10:** BrightPath sponsor identification + business review
**May 15 onwards:** Value workshops for 6 Neutral accounts

**Healthy accounts (4):** Nurture + expansion planning with Cascade Media and NovaTech Systems (highest potential, highest scores)

### Artifacts written

#### `work/accounts/enterprise-portfolio.yaml`

```
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

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/16.5 (88%) |
| Evaluated | 2026-05-04 |
| Target duration | 71869 ms |
| Target cost | $0.1118 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill scores all 5 dimensions: Adoption (30%), Engagement (25%), Relationship (20%), Value Realisation (15%), Commercial (10%) | PASS | The scoring table header explicitly shows all five dimensions with their weights: '\| Account \| Adoption (30%) \| Engagement (25%) \| Relationship (20%) \| Value (15%) \| Commercial (10%) \| Composite \| Status \|' |
| c2 | Skill calculates a composite health score using the correct weighted formula — not an unweighted average | PASS | Verified with Acme Corp: 78*0.30 + 82*0.25 + 85*0.20 + 85*0.15 + 80*0.10 = 23.4+20.5+17+12.75+8 = 81.65 ✓. Verified with BrightPath: 35*0.30+38*0.25+32*0.20+28*0.15+65*0.10 = 37.1 ✓. The formula is correctly weighted throughout. |
| c3 | Skill classifies accounts into health categories (e.g. Green/Yellow/Red or equivalent) with defined thresholds | PASS | The output applies four consistent tiers — Healthy, Neutral, At Risk, Critical — to all 15 accounts, with the classification pattern showing implicit thresholds (Healthy ~80+, Neutral ~55–75, At Risk ~40–55, Critical <40). The consistency of application demonstrates the skill has defined thresholds internally. |
| c4 | Skill requires identifying data sources for each dimension before scoring — not scoring from memory | PARTIAL | Step 1 states 'Data Sources ✓ All required dimensions present in the portfolio data: product usage metrics, engagement patterns, relationship indicators, value realisation signals, and commercial status.' The source (portfolio YAML) is cited and dimension types mapped collectively, but specific source systems are not named per dimension (e.g. no mention of 'product analytics platform', 'CRM', 'billing system'). |
| c5 | Skill identifies specific risk signals per account — not just a score, but what is driving it | PASS | Step 5 provides granular signals per critical account. Thunderstone: 'Payment 30 days overdue \| Champion left company \| Usage declining 50% \| NPS 3 \| Only 1 feature adopted.' Vertex: 'Renewal imminent \| Unresponsive (no contact 60 days) \| Usage declining 40% \| NPS 2 \| High support load (14 tickets).' Each account gets specific contributing factors, not just scores. |
| c6 | Skill produces recommended interventions for at-risk accounts — specific actions, not 'schedule a check-in' | PASS | The Tier 1/Tier 2 tables include specific actions with owners and success criteria: Thunderstone gets 'Executive escalation + retention call, VP CS, By May 6'; Hargreaves gets 'Multi-channel outreach: phone + email + LinkedIn'; BrightPath gets 'Org chart analysis + sponsor identification.' These are concrete, non-generic actions. |
| c7 | Skill produces a portfolio summary view — partial credit if individual accounts are assessed but no aggregated portfolio view is required | PARTIAL | Step 4 produces a portfolio distribution table: 'Healthy: 4 ($397k), Neutral: 6 ($467k), At Risk: 1 ($45k), Critical: 4 ($179k).' Step 7 adds systemic observations. This fully satisfies the partial-ceiling criterion. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output contains only the chat response and the data file artifact (enterprise-portfolio.yaml). No skill definition file with YAML frontmatter is present in either the response or the artifacts — cannot verify name, description, or argument-hint fields. |
| c9 | Output assesses all 15 accounts — not a sample, not a 'top movers' subset — with a row per account in the resulting table | PASS | The scoring table contains exactly 15 rows: Acme Corp, BrightPath Solutions, Meridian Financial, Thunderstone Retail, CloudNine Logistics, Pinnacle Healthcare, Vertex Engineering, Cascade Media, Strata Property Group, NovaTech Systems, Hargreaves Consulting, Pacific Distribution, Streamline Insurance, Frontier Mining, Apex Legal — matching the full portfolio. |
| c10 | Output scores each account on all 5 dimensions — Adoption (30%), Engagement (25%), Relationship (20%), Value Realisation (15%), Commercial (10%) — and shows the per-dimension score per account | PASS | The table shows all five per-dimension scores for every one of the 15 accounts, e.g. 'Frontier Mining \| 38 \| 45 \| 58 \| 52 \| 75 \| 49.55 \| At Risk'. Every row has five dimension scores. |
| c11 | Output computes the composite score using the WEIGHTED formula: Adoption*0.30 + Engagement*0.25 + Relationship*0.20 + Value*0.15 + Commercial*0.10 — not a simple average; the math is verifiable from the per-dimension scores | PASS | Meridian Financial: 88*0.30+90*0.25+92*0.20+90*0.15+95*0.10 = 26.4+22.5+18.4+13.5+9.5 = 90.3 ✓. Composite scores are not simple averages and are verifiable from the per-dimension values shown. |
| c12 | Output classifies each account into a defined health tier with stated numeric thresholds (e.g. Healthy/Neutral/At Risk/Critical or Green/Yellow/Red) — not just 'looks healthy' | PARTIAL | The output applies Healthy/Neutral/At Risk/Critical tiers to all 15 accounts, but never states the numeric boundaries (e.g. 'Healthy = 75+, Neutral = 55–74'). The criterion specifically requires 'stated numeric thresholds' — these are absent, though the categories themselves are consistently applied. |
| c13 | Output names the data source per dimension before scoring — adoption from product analytics, engagement from in-app event tracking, relationship from CRM contact frequency, value from QBR notes, commercial from billing/contract data — not scoring from CSM memory | PARTIAL | Step 1 names 'product usage metrics, engagement patterns, relationship indicators, value realisation signals, and commercial status' as present in the portfolio data — the YAML file is the collective source. No dimension-specific source systems are named (no 'product analytics', 'CRM', 'billing system' etc.), which the criterion explicitly requires. |
| c14 | Output identifies specific risk signals per at-risk account — not just 'Score 55, Red' but 'Adoption dropped 30% in last 60 days, no exec sponsor identified, support tickets ticked up to 12/month from 3' | PASS | Step 5 provides account-level specifics including actual data values: BrightPath 'declining \| Low engagement (45 logins/month) \| No exec sponsor \| NPS 4 (detractor) \| High support load (8 tickets)'; Thunderstone '\| Champion left company \| Usage declining 50% \| NPS 3 \| Only 1 feature adopted'. Signal values trace directly to the YAML. |
| c15 | Output's recommended interventions per at-risk account are specific actions tied to the failing dimension — e.g. 'Adoption red: schedule training session with team lead by Friday; Relationship red: identify backup champion within IT' — not 'schedule a check-in' | PASS | BrightPath (relationship/adoption failing): 'Org chart analysis + sponsor identification'. Frontier (adoption/value failing): 'Usage review call + goal reset'. Thunderstone (all dims failing): 'Executive escalation + retention call' with explicit success criteria including 'new sponsor identified'. Interventions are dimension-specific and actionable. |
| c16 | Output's portfolio summary view aggregates the 15 accounts with a health distribution count (e.g. '3 Critical, 4 At Risk, 8 Healthy') so the CS leadership team can prioritise meeting time | PASS | Step 4 'Portfolio Distribution' table shows: 'Healthy: 4 \| $397k \| Neutral: 6 \| $467k \| At Risk: 1 \| $45k \| Critical: 4 \| $179k'. Counts plus ARR at stake are provided for each tier. |
| c17 | Output prioritises at-risk accounts for the upcoming review — listing the most at-risk accounts first with the specific intervention required; partial credit if prioritised but missing commercial context (renewal date, ARR) | PARTIAL | The output prioritises via Tier 1/Tier 2 tables with accounts sorted by severity, and includes ARR ('$48k ARR, renewal in ~2 months' for Thunderstone) and specific deadlines ('By May 6'). The 'At a Glance' section closes with a timeline. Full commercial context is present — ceiling is PARTIAL. |
| c18 | Output flags trends across the portfolio — e.g. 'adoption is the weakest dimension across the at-risk accounts, suggesting a systemic onboarding gap' — not just per-account observations | PARTIAL | Step 7 'Portfolio Trends & Systemic Observations' flags: 'Product Adoption (30% weight) — Critical cohort averaging 25 vs portfolio average of 63… onboarding is not reaching power users'; 'Sponsorship gap: 5 accounts lack confirmed exec sponsor… No Healthy account lacks a confirmed sponsor'; '10 of 15 accounts have roi_documented: false'. Systemic patterns clearly stated. Ceiling is PARTIAL. |

### Notes

The output is comprehensive and high quality, correctly applying weighted scoring across all 15 accounts, producing verifiable composite scores, and delivering specific interventions with owners and success criteria. The two main gaps are: (1) c8 cannot be assessed because no skill definition file appears in the artifacts — only the data YAML was written; and (2) c12 and c13 are partial because the output never states the numeric tier thresholds explicitly and does not name source systems per dimension (only naming the YAML file collectively). The portfolio-trend analysis in Step 7 is one of the stronger sections, identifying systemic patterns (sponsorship gap, ROI documentation gap, onboarding adoption gap) across the cohort rather than just per-account observations. The 'At a Glance' timeline at the end is a practical CS team artifact that wasn't explicitly required but adds genuine value.
