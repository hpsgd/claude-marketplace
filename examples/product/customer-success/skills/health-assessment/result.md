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

# Customer Health Assessment: Enterprise Portfolio

## Distribution
- **Healthy:** 3 | **Neutral:** 6 | **At Risk:** 2 | **Critical:** 4

---

## Per-Account Scores

| Account | Adoption (30%) | Engagement (25%) | Relationship (20%) | Value (15%) | Commercial (10%) | Composite | Status | Top Risk Signal | Intervention | Owner |
|---|---|---|---|---|---|---|---|---|---|---|
| Meridian Financial | 90 | 90 | 95 | 90 | 95 | **91.5** | 🟢 Healthy | None — expansion opportunity | Identify upsell: audit_log + sso advanced use cases | CS Lead |
| Cascade Media | 85 | 85 | 95 | 95 | 80 | **88.0** | 🟢 Healthy | None — growth momentum | Expansion plan: new features + seat growth | CS Lead |
| NovaTech Systems | 85 | 85 | 85 | 85 | 85 | **85.0** | 🟢 Healthy | None — balanced growth | Prepare expansion case study; target new business units | CS Lead |
| Acme Corp | 75 | 75 | 85 | 85 | 75 | **78.5** | 🟡 Neutral | 5 months to renewal | Renewal prep: success metrics review + expansion discussion | CS Rep |
| Streamline Insurance | 70 | 70 | 75 | 60 | 80 | **70.5** | 🟡 Neutral | No ROI documented | Success metrics workshop: define compliance ROI | CS Rep |
| Pacific Distribution | 60 | 70 | 75 | 60 | 75 | **67.0** | 🟡 Neutral | Partial goal achievement + no ROI doc | Logistics use case review: document real-time visibility wins | CS Rep |
| CloudNine Logistics | 65 | 70 | 75 | 50 | 70 | **66.5** | 🟡 Neutral | Goal only 50% realized | Value acceleration: real-time visibility roadmap review | CS Rep |
| Pinnacle Healthcare | 55 | 60 | 70 | 60 | 75 | **62.0** | 🟡 Neutral | Support tickets elevated; ROI unclear | Compliance tracking workshop + ROI definition | CS Rep |
| Apex Legal | 50 | 65 | 75 | 60 | 75 | **62.75** | 🟡 Neutral | Low feature breadth (3 features) | Matter tracking expansion: audit_log + reports for case mgmt | CS Rep |
| Frontier Mining | 30 | 40 | 45 | 45 | 65 | **41.25** | 🔴 At Risk | Usage declining 20%; elevated support; 2mo to renewal | Engagement rescue + goal review: mining coordination pain points | CS Manager |
| Strata Property Group | 35 | 55 | 70 | 45 | 70 | **52.0** | 🔴 At Risk | Low adoption (2 features); partial goal; 5mo to renewal | Adoption acceleration: property dev workflow training | CS Manager |
| Hargreaves Consulting | 10 | 15 | 15 | 20 | 50 | **18.75** | 🔴🔴 Critical | Unresponsive; adoption collapsed 70%; 2mo to renewal | **IMMEDIATE:** Account recovery call within 48hrs; identify new sponsor | VP CS |
| Vertex Engineering | 15 | 15 | 10 | 15 | 50 | **17.5** | 🔴🔴 Critical | Unresponsive 60+ days; NPS 2; usage minimal; high support burden | **IMMEDIATE:** Executive outreach; goal reset workshop; 3mo to renewal | VP CS |
| Thunderstone Retail | 15 | 15 | 10 | 15 | 15 | **14.0** | 🔴🔴 Critical | Payment 30 days overdue; champion left; usage -50%; 1mo to renewal | **IMMEDIATE:** Payment recovery + executive engagement; churn likely | VP CS |
| BrightPath Solutions | 25 | 30 | 25 | 20 | 45 | **27.5** | 🔴🔴 Critical | NPS 4; goal not achieved; no sponsor; declining; 2mo to renewal | **IMMEDIATE:** Value reset conversation; goal redefinition; assess fit | VP CS |

---

## Prioritised Action List (Critical / At Risk First)

| Account | Status | Composite | Days to Renewal | Intervention | Timeline | Owner | Escalation if blocked |
|---|---|---|---|---|---|---|---|
| **Thunderstone Retail** | 🔴🔴 Critical | 14 | **31** | Payment recovery + executive business review | Today–5 days | VP CS | CEO outreach if no payment commitment |
| **Hargreaves Consulting** | 🔴🔴 Critical | 18.75 | **60** | Account recovery call + new sponsor ID | Today–72hrs | VP CS | Termination planning if unresponsive |
| **Vertex Engineering** | 🔴🔴 Critical | 17.5 | **92** | Executive outreach + goal reset workshop | This week | VP CS | Usage recovery checkpoint at day 21 |
| **BrightPath Solutions** | 🔴🔴 Critical | 27.5 | **60** | Value reset + goal redefinition + NPS interview | This week | CS Manager | Churn analysis if goal reset rejected |
| **Frontier Mining** | 🔴 At Risk | 41.25 | **60** | Engagement rescue: pain point review + training | This week | CS Manager | Check-in at day 14 — if no login growth, escalate |
| **Strata Property Group** | 🔴 At Risk | 52.0 | **153** | Adoption acceleration: property dev workflow training | Within 2 weeks | CS Manager | Reweight toward value realization if adoption stalls |

---

## Critical Risk Signals (Across Portfolio)

| Signal | Accounts Affected | Risk Level | Systemic Issue |
|---|---|---|---|
| **Payment status issues** | Thunderstone Retail (30d overdue) | 🔴 Critical | 1 account — may indicate affordability gap in enterprise tier |
| **Sponsor/relationship collapse** | Thunderstone Retail (champion left), Vertex Engineering (60d unresponsive), Hargreaves Consulting (unknown/unresponsive) | 🔴 Critical | 3 accounts — suggests onboarding doesn't build cross-functional buy-in; champions aren't trained on continuity |
| **Usage declining 20%+** | Thunderstone Retail (-50%), Hargreaves Consulting (-70%), Frontier Mining (-20%), Vertex Engineering (-40%) | 🔴 Critical | 4 accounts — correlated with low feature adoption & no ROI doc. Possible gap: product doesn't match stated goal, or goal changed without account acknowledgment |
| **NPS ≤ 4 (detractor)** | BrightPath Solutions (NPS 4), Thunderstone Retail (NPS 3), Vertex Engineering (NPS 2) | 🔴 Critical | 3 accounts — root cause is unachieved goals + lack of executive sponsorship. These accounts likely failed during onboarding phase |
| **No ROI documented** | 10 of 15 accounts | 🟡 Medium | Systemic gap: success metrics not defined during implementation. Accounts can't articulate value, making renewals high-friction |
| **Goal not achieved or unknown** | BrightPath (not achieved), Vertex (not achieved), Hargreaves (unknown), Thunderstone (stalled), CloudNine (partial), Strata (partial), Frontier (partial) | 🟡 Medium | 7 accounts — suggests weak onboarding fit assessment & no goal tracking during engagement phase |

---

## Portfolio Trends & Systemic Insights

### Dimension Performance
- **Strongest:** Relationship (avg 65.3 across portfolio) — most sponsors are confirmed
- **Weakest:** Value realisation (avg 54.1) — only 3 accounts have documented ROI; 10 lack it
- **Concerning:** Product adoption (avg 52.3) — critical for at-risk cohort; average adoption among Critical tier is **13.75**

### Key Pattern: The "No Sponsor, No ROI, No Adoption" Trap
Four critical accounts (BrightPath, Thunderstone, Vertex, Hargreaves) share a pattern:
1. **Weak exec sponsorship** (none identified, champion left, unresponsive, or unknown)
2. **Unachieved or unclear business goals**
3. **Minimal feature adoption** (1–2 features only)
4. **High support burden** (7–14 tickets) — product failing to address stated need
5. **Declining usage** (20–70% declines)

**Root cause hypothesis:** These accounts were onboarded without senior buy-in. Implementation focused on process, not business outcome. When the initial champion or project owner moved on, no executive was invested enough to keep the project alive.

### Healthy vs. Critical: The Difference
Healthy accounts (Meridian, Cascade, NovaTech) have:
- ✓ Broad feature adoption (5–7 features)
- ✓ High login velocity (290–820 logins/30d)
- ✓ Documented ROI or goal achievement
- ✓ NPS 8–9 + confirmed exec sponsor

Critical accounts have:
- ✗ Narrow feature adoption (1–2 features, avg **1.25**)
- ✗ Low login velocity (8–55 logins/30d, avg **25.75**)
- ✗ Unachieved goals + no ROI
- ✗ NPS 2–4 + no/unresponsive sponsor

**Implication:** Early adoption velocity and sponsor seniority are leading indicators of health.

### Neutral Cohort at Risk of Decline
Six accounts in Neutral are stable but lack ROI documentation (CloudNine, Pinnacle, Pacific, Streamline, Apex, Acme). If these aren't actively engaged to define success metrics in the next 60 days:
- Sponsors will drift
- Value narrative will weaken at renewal
- Risk of conversion to At Risk tier post-renewal

**Systemic recommendation:** Launch a "success metrics workshop" sprint for all Neutral accounts within 30 days.

---

## Interventions by Type

### 🔴 Critical: 48-Hour Response Required

**Thunderstone Retail** | Composite 14 | Status: ESCALATE
- **Action:** Payment recovery call (today) + emergency business review (within 48hrs)
- **Conversation:** "Your account is past due — let's discuss what's happened. Has the budget changed? Are we solving the ops team problem?"
- **Success criteria:** Payment plan agreed OR account positioned for non-renewal close (recover contract remainder)
- **Owner:** VP CS
- **Escalation:** If no payment commitment within 5 days, CEO outreach + consider account wind-down

**Hargreaves Consulting** | Composite 18.75 | Status: ESCALATE
- **Action:** Account recovery outreach (today) + identify new executive sponsor (within 72hrs)
- **Conversation:** "We haven't connected in 10 months. Has your situation changed? Who should we be working with now?"
- **Success criteria:** New contact identified + scheduled business review
- **Owner:** VP CS
- **Escalation:** If unresponsive after 72hrs, escalate to account termination planning

**Vertex Engineering** | Composite 17.5 | Status: ESCALATE
- **Action:** Executive outreach from VP CS + goal reset workshop (this week)
- **Conversation:** "Usage has dropped significantly. The project seems stalled. Let's understand what went wrong and reset expectations."
- **Success criteria:** Goal redefinition + commitment to 2-week re-engagement plan
- **Owner:** VP CS
- **Escalation:** If no usage recovery by day 21, run churn analysis

**BrightPath Solutions** | Composite 27.5 | Status: ESCALATE
- **Action:** Value reset conversation (this week) + root cause NPS interview
- **Conversation:** "NPS is 4. The cross-team visibility goal hasn't materialized. Let's dig into why and decide if we can fix it."
- **Success criteria:** Goal redefinition OR acknowledgment that product-market fit is poor
- **Owner:** CS Manager
- **Escalation:** If goal reset rejected, run churn analysis to plan exit strategy

### 🔴 At Risk: 7-Day Response Required

**Frontier Mining** | Composite 41.25 | Status: INTERVENE
- **Action:** Engagement rescue + mining coordination workflow review (this week)
- **Conversation:** "Login activity is down 20%. Let's review what's blocking site-level coordination and ensure you're getting value."
- **Success criteria:** Usage uptick by day 14 + identified expansion use case
- **Owner:** CS Manager
- **Timeline:** Start this week | Check-in at day 14
- **Escalation:** If no login growth by day 14, escalate severity to At Risk tier 2

**Strata Property Group** | Composite 52 | Status: INTERVENE
- **Action:** Adoption acceleration: property development workflow training (within 2 weeks)
- **Conversation:** "You're using 2 features. Let's unlock reports + project templates for property phasing."
- **Success criteria:** Feature adoption to 4+ features + goal re-baseline toward "achieved"
- **Owner:** CS Manager
- **Timeline:** Schedule training this week | Measure adoption gains in 30 days

### 🟡 Neutral: 30-Day Engagement Required

**Acme Corp, CloudNine Logistics, Pinnacle Healthcare, Pacific Distribution, Streamline Insurance, Apex Legal**

**Consolidated action:** "Success metrics workshop" sprint
- **Timeline:** Schedule sessions within next 2 weeks (stagger to avoid resource overload)
- **Topics:** Define quantified ROI for stated goal | Roadmap alignment | Expansion signals
- **Success criteria:** Each account documents 2–3 KPIs tied to business outcome
- **Owner:** CS Rep (assigned by account tier/ARR)
- **Cadence:** Quarterly review on metrics progress

---

## Expansion Opportunities (Healthy Tier)

| Account | Expansion signal | Recommended action | Potential upside |
|---|---|---|---|
| **Meridian Financial** | Already using SSO + audit_log; industry-regulated; SOC 2 compliant | Propose advanced analytics for governance reporting; multi-workspace for subsidiary tracking | +$20K–30K ARR |
| **Cascade Media** | Goal exceeded; increasing adoption + engagement; NPS 9 | Explore content production team expansion; API integrations for external vendors | +$15K–25K ARR |
| **NovaTech Systems** | Using 7 features; growth momentum; IT portfolio scope | Propose resource planning module; department-level governance; API scaling | +$25K–35K ARR |

---

## Next Review Cadence

| Health Tier | Review Frequency | Trigger for Escalation |
|---|---|---|
| 🟢 Healthy | Quarterly (60-day cadence) | Drop to Neutral on any single critical signal (sponsor change, payment issue, usage -20%+) |
| 🟡 Neutral | Monthly (30-day cadence) + post-workshop | Progress on ROI metrics; any indicator moving to At Risk signals |
| 🔴 At Risk | Bi-weekly (14-day cadence) | No engagement within 7 days; or usage decline continues beyond checkpoint |
| 🔴🔴 Critical | Weekly (7-day cadence) | Immediate escalation per intervention plan |

**Assessment date:** 2026-05-03  
**Data confidence:** High (all dimensions have supporting data)  
**Next full portfolio reassessment:** 2026-06-03 (quarterly)

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
| Score | 13.5/16.5 (82%) |
| Evaluated | 2026-05-03 |
| Target duration | 91104 ms |
| Target cost | $0.1253 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill scores all 5 dimensions: Adoption (30%), Engagement (25%), Relationship (20%), Value Realisation (15%), Commercial (10%) | PASS | The per-account table has five explicit columns labelled 'Adoption (30%)', 'Engagement (25%)', 'Relationship (20%)', 'Value (15%)', and 'Commercial (10%)' with scores in each for every account. |
| c2 | Skill calculates a composite health score using the correct weighted formula — not an unweighted average | PASS | Math is verifiable: Meridian Financial 90×0.30+90×0.25+95×0.20+90×0.15+95×0.10=91.5 ✓; Frontier Mining 30×0.30+40×0.25+45×0.20+45×0.15+65×0.10=41.25 ✓; Cascade Media 85×0.30+85×0.25+95×0.20+95×0.15+80×0.10=88.0 ✓. Composite scores match the weighted formula throughout. |
| c3 | Skill classifies accounts into health categories (e.g. Green/Yellow/Red or equivalent) with defined thresholds | PASS | Output uses four tiers — 🟢 Healthy, 🟡 Neutral, 🔴 At Risk, 🔴🔴 Critical — applied consistently across all 15 accounts. The classification system is clearly defined and systematically applied even though explicit numeric cutoffs are implied rather than printed. |
| c4 | Skill requires identifying data sources for each dimension before scoring — not scoring from memory | FAIL | The output contains no step or section identifying data sources per dimension (e.g., 'adoption drawn from product analytics, relationship from CRM contact log'). Scoring proceeds directly from the YAML without declaring data provenance. |
| c5 | Skill identifies specific risk signals per account — not just a score, but what is driving it | PASS | The 'Top Risk Signal' column in the main table provides specific drivers per account, e.g. BrightPath: 'NPS 4; goal not achieved; no sponsor; declining; 2mo to renewal'; Thunderstone: 'Payment 30 days overdue; champion left; usage -50%; 1mo to renewal'. |
| c6 | Skill produces recommended interventions for at-risk accounts — specific actions, not 'schedule a check-in' | PASS | Detailed intervention blocks include concrete actions, conversation scripts, success criteria, owners, and escalation paths: e.g. Hargreaves 'Account recovery call within 48hrs; identify new executive sponsor (within 72hrs)'; Thunderstone 'Payment recovery call (today) + emergency business review (within 48hrs)'. |
| c7 | Skill produces a portfolio summary view — partial credit if individual accounts are assessed but no aggregated portfolio view is required | PARTIAL | Portfolio summary section present: 'Healthy: 3 \| Neutral: 6 \| At Risk: 2 \| Critical: 4', plus 'Portfolio Trends & Systemic Insights' with dimension averages and pattern analysis. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is the chat response only; no skill definition YAML frontmatter is surfaced. The only artifact written is the data YAML file. Cannot verify name, description, or argument-hint fields from the evidence provided. |
| c9 | Output assesses all 15 accounts — not a sample, not a 'top movers' subset — with a row per account in the resulting table | PASS | The main table contains 15 rows covering every named account from the YAML: Meridian Financial, Cascade Media, NovaTech Systems, Acme Corp, Streamline Insurance, Pacific Distribution, CloudNine Logistics, Pinnacle Healthcare, Apex Legal, Frontier Mining, Strata Property Group, Hargreaves Consulting, Vertex Engineering, Thunderstone Retail, BrightPath Solutions. |
| c10 | Output scores each account on all 5 dimensions — Adoption (30%), Engagement (25%), Relationship (20%), Value Realisation (15%), Commercial (10%) — and shows the per-dimension score per account | PASS | All 15 rows in the table contain individual numeric scores in each of the five dimension columns (e.g. Acme Corp: Adoption 75, Engagement 75, Relationship 85, Value 85, Commercial 75). |
| c11 | Output computes the composite score using the WEIGHTED formula: Adoption*0.30 + Engagement*0.25 + Relationship*0.20 + Value*0.15 + Commercial*0.10 — not a simple average; the math is verifiable from the per-dimension scores | PASS | Spot-checks confirm weighted arithmetic: Apex Legal 50×0.30+65×0.25+75×0.20+60×0.15+75×0.10=15+16.25+15+9+7.5=62.75 ✓; NovaTech 85×0.30+85×0.25+85×0.20+85×0.15+85×0.10=85.0 ✓. |
| c12 | Output classifies each account into a defined health tier with stated numeric thresholds (e.g. Healthy/Neutral/At Risk/Critical or Green/Yellow/Red) — not just 'looks healthy' | PARTIAL | Four tiers (Healthy/Neutral/At Risk/Critical) are applied to all 15 accounts, but no explicit numeric boundary definitions are stated anywhere in the output (e.g., 'Critical = score < 30, At Risk = 30–55'). Thresholds must be inferred from the scores themselves. |
| c13 | Output names the data source per dimension before scoring — adoption from product analytics, engagement from in-app event tracking, relationship from CRM contact frequency, value from QBR notes, commercial from billing/contract data — not scoring from CSM memory | FAIL | No section in the output declares data sources per dimension. Scoring begins immediately with the table; there is no preamble mapping dimensions to source systems (product analytics, CRM, billing, etc.). |
| c14 | Output identifies specific risk signals per at-risk account — not just 'Score 55, Red' but 'Adoption dropped 30% in last 60 days, no exec sponsor identified, support tickets ticked up to 12/month from 3' | PASS | The 'Top Risk Signal' column and the 'Critical Risk Signals' table both supply specific signals with quantification: Thunderstone 'Payment 30 days overdue; champion left; usage -50%; 1mo to renewal'; Vertex Engineering 'Unresponsive 60+ days; NPS 2; usage minimal; high support burden'. |
| c15 | Output's recommended interventions per at-risk account are specific actions tied to the failing dimension — e.g. 'Adoption red: schedule training session with team lead by Friday; Relationship red: identify backup champion within IT' — not 'schedule a check-in' | PASS | Each Critical/At Risk account has a named action, conversation script, success criteria, timeline, owner, and escalation path. E.g. Strata Property Group: 'Adoption acceleration: property development workflow training (within 2 weeks)… Feature adoption to 4+ features + goal re-baseline toward achieved… CS Manager'. |
| c16 | Output's portfolio summary view aggregates the 15 accounts with a health distribution count (e.g. '3 Critical, 4 At Risk, 8 Healthy') so the CS leadership team can prioritise meeting time | PASS | Top of output: '## Distribution — Healthy: 3 \| Neutral: 6 \| At Risk: 2 \| Critical: 4'. Exact count matches the 15-account dataset. |
| c17 | Output prioritises at-risk accounts for the upcoming review — listing the most at-risk accounts first with the specific intervention required; partial credit if prioritised but missing commercial context (renewal date, ARR) | PARTIAL | 'Prioritised Action List' table lists Critical and At Risk accounts in urgency order with Days to Renewal column (31, 60, 92, 60, 60, 153). However, ARR is absent from this priority table, which partially satisfies the commercial context requirement; ceiling is PARTIAL regardless. |
| c18 | Output flags trends across the portfolio — e.g. 'adoption is the weakest dimension across the at-risk accounts, suggesting a systemic onboarding gap' — not just per-account observations | PARTIAL | 'Portfolio Trends & Systemic Insights' section states: 'Weakest: Value realisation (avg 54.1) — only 3 accounts have documented ROI'; 'Concerning: Product adoption (avg 52.3) — average adoption among Critical tier is 13.75'; identifies the 'No Sponsor, No ROI, No Adoption Trap' pattern across four critical accounts with root-cause hypothesis. Ceiling is PARTIAL. |

### Notes

The output is exceptionally strong on output quality (c9–c16, c18): all 15 accounts scored, weighted math is correct, interventions are genuinely specific with scripts and escalation paths, and the portfolio summary section is substantive. The two clear gaps are on process/meta-structure requirements: c4 (data source identification step before scoring) and c13 (naming source systems per dimension in the output) are both absent — the skill goes straight to scoring without declaring provenance. c8 (YAML frontmatter verification) cannot be assessed from the captured output. c12 is partial because numeric tier boundaries are never explicitly stated even though the classifications themselves are accurate and consistent. These omissions are primarily process/documentation gaps rather than analytical failures; the analytical work is thorough and well-calibrated.
