# Write Onboarding Playbook

Scenario: Testing whether the write-onboarding-playbook skill defines TTFV as a measurable customer outcome, requires escalation triggers on every milestone, and includes handoff criteria.

## Prompt

> /customer-success:write-onboarding-playbook for our enterprise segment — customers with 200+ seats, dedicated IT teams, and annual contracts over $100k.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The enterprise onboarding playbook is written to `onboarding-playbook-enterprise.md`. Here's what's in it:

**Segment definition** — 200+ seats, high technical sophistication, annual contract urgency, with the buyer/user gap called out explicitly (exec sponsor bought it, ICs don't know why).

**TTFV: 21 days** — defined as 10+ distinct users completing the primary workflow with live data, measurable via a product event. More aggressive than the 28–35 day industry median, achievable by front-loading all technical setup into the first 7 days.

**6 milestones:**
1. Kickoff (Day 1–3)
2. Technical environment ready (Day 3–7) — SSO, integrations, security review all gated here to protect TTFV
3. Champion trained + first workflow live (Day 7–14)
4. First value achieved (Day 14–21) — the TTFV gate
5. Team rollout to 40% of seats (Day 21–35)
6. Handoff to BAU (Day 35–45)

**Kickoff** is 75 minutes with a required executive sponsor — reschedule if they skip rather than proceeding without them.

**7 common blockers** including SSO delays, InfoSec reviews, and low team adoption — each with an early warning sign (before you're told), a specific resolution, and a named escalation path.

**Handoff** requires 8 measurable criteria all green before BAU handover, with a warm introduction call (not email).

### Artifacts written

#### `work/onboarding-playbook-enterprise.md`

```
# Customer Onboarding Playbook: Enterprise

| Field | Value |
|---|---|
| **Segment** | Enterprise |
| **Expected Duration** | 45 days |
| **CS Owner Role** | Onboarding Specialist + Technical Account Manager |
| **Last Updated** | 2026-05-01 |

---

## Segment Definition

| Element | Detail |
|---|---|
| **Segment** | Enterprise |
| **Typical company size** | 500–10,000 employees; 200+ licensed seats; $100k+ ACV |
| **Technical sophistication** | High — dedicated IT/security team, internal IT admin, often a dedicated project lead |
| **Typical goals** | (1) Replace or consolidate a legacy workflow across a large team, (2) meet a compliance or audit requirement, (3) demonstrate measurable ROI within a fiscal quarter to justify the investment to leadership |
| **Decision-maker** | VP / Director who signed the contract — present at kickoff, rarely a daily user |
| **Day-to-day users** | Team leads and ICs who were not in the buying process and may be unaware of the goals discussed during sales |
| **Common integrations** | SSO/SAML (Okta, Azure AD), HRIS or CRM, data warehouse or BI tool, ticketing system (Jira, ServiceNow) |
| **Contract type** | Annual — renewal conversation begins ~90 days before contract end; TTFV must land well before that window |

**Critical gap:** The executive sponsor bought the product to solve a strategic problem. End users don't know that — they see it as a new tool being pushed on them. Bridge this in the kickoff by involving both layers and making the "why" explicit.

---

## Time-to-First-Value

| Element | Detail |
|---|---|
| **"First value" definition** | A team of at least 10 users (not just the champion) has completed the primary use-case workflow using their own live data — not sample or test data — and can demonstrate a measurable improvement against the baseline established at kickoff |
| **Target TTFV** | 21 days from kickoff |
| **Measurement** | Product event: 10+ distinct user IDs have triggered the core workflow event within a 7-day window, AND champion has confirmed the output matches their expected outcome in writing (email or CRM note) |
| **Current TTFV** | Establish at kickoff from sales handoff; if unknown, baseline is 45 days |
| **Benchmark** | Enterprise B2B SaaS median TTFV is 28–35 days; targeting 21 days is aggressive but achievable with a prepared technical environment |

TTFV fails when onboarding stalls at technical setup. The milestone table below front-loads technical work into the first 7 days precisely to protect the 21-day target.

---

## Pre-Onboarding

Complete before the kickoff call:

- [ ] Receive sales handoff: CRM notes, call recordings, success criteria discussed during sales, any commitments made (custom integrations, SLAs, security reviews)
- [ ] Identify and confirm all stakeholders: executive sponsor, project lead, IT/technical admin, champion, and key end-user representatives
- [ ] Review the customer's security requirements (SSO, data residency, infosec questionnaire) and flag any that require internal action before kickoff
- [ ] Send welcome email with kickoff agenda, pre-work checklist, and calendar invite — require executive sponsor attendance
- [ ] Provision sandbox accounts for champion and technical admin; do NOT provision all 200+ seats until technical setup is validated
- [ ] Internal handoff call with AE: confirm deal context, any promises made, stakeholder sensitivities

---

## Milestone Table

| Milestone | Target Day | Success Criteria | Owner | Verification Method | Escalation Trigger |
|---|---|---|---|---|---|
| Kickoff complete | Day 1–3 | Stakeholders identified and introduced, baseline metrics documented in customer's words, milestone dates confirmed on shared calendar, IT requirements list delivered | Onboarding Specialist | Kickoff notes shared and acknowledged by champion within 24h | No executive sponsor at kickoff → reschedule before proceeding; no kickoff by Day 5 → CS Manager notified |
| Technical environment ready | Day 3–7 | SSO configured and tested, primary integration(s) authenticated, security review complete, admin accounts provisioned | TAM + Customer IT Admin | Automated health check passes; TAM confirms no open blockers | IT team unresponsive for 3+ business days → AE engaged for exec escalation |
| Champion trained and first workflow live | Day 7–14 | Champion has completed the primary use-case workflow end-to-end with live data and documented one concrete output | Onboarding Specialist | Product event: primary workflow event fired by champion's user ID; champion confirms output via email | No champion login by Day 10 → re-engage with condensed async path |
| First value achieved | Day 14–21 | 10+ distinct users have completed the primary workflow with live data; champion confirms outcome matches kickoff success criteria | Onboarding Specialist + Champion | Product event: 10+ unique user IDs on primary workflow event within a 7-day window; written confirmation from champion | Fewer than 5 active users by Day 18 → team onboarding session fast-tracked |
| Team rollout to 40% of licensed seats | Day 21–35 | At least 40% of licensed seats (80+ users) have logged in and completed at least one workflow; team leads can self-serve basic use cases | TAM + Champion | Usage analytics: 80+ unique active users in rolling 7 days | Adoption below 20% at Day 28 → escalate to executive sponsor with usage report |
| Handoff to BAU | Day 35–45 | All handoff criteria met (see below), BAU CSM introduced, first QBR scheduled | Onboarding Specialist → BAU CSM | Handoff checklist complete; QBR calendar invite accepted by executive sponsor | Health score not green by Day 40 → extend onboarding with CS Manager approval; root cause documented |

---

## Kickoff Meeting Agenda

**Duration:** 75 minutes
**Required attendees:** Onboarding Specialist, TAM, executive sponsor, project lead / champion, IT/technical admin
**Optional:** AE (for context handoff, first 10 min only), additional end-user team leads

| Time | Topic | Owner | Output |
|---|---|---|---|
| 0–10 min | Introductions and role mapping — who does what on both sides | Onboarding Specialist | Documented RACI: CS contacts, customer contacts, escalation chain |
| 10–25 min | Goals alignment — ask the sponsor to state the problem in their own words; do not paraphrase | Onboarding Specialist | Written success criteria in the customer's words, not product marketing language; baseline metrics established |
| 25–40 min | Technical requirements and integration plan | TAM + IT Admin | Integration scope confirmed; IT requirements doc delivered; SSO/security timeline agreed |
| 40–55 min | Milestone walkthrough with actual calendar dates | Onboarding Specialist | Shared timeline with real dates attached; escalation contacts confirmed for each milestone |
| 55–65 min | Team rollout plan — who trains whom, in what order | Onboarding Specialist + Champion | Rollout sequencing agreed: champion first, team leads second, broader team third |
| 65–75 min | Next steps — 3 actions with owners and deadlines | Onboarding Specialist | Action list sent within 2 hours of call ending |

**Kickoff anti-patterns to avoid:**
- Demoing features: they bought the product — use kickoff time for their goals, not your roadmap
- Skipping the IT admin: technical blockers discovered after kickoff add 5–10 days; find them now
- Vague success criteria: "improve team efficiency" → push for "reduce report generation time from 4 hours to under 30 minutes"
- Accepting the executive sponsor's apology for missing: reschedule the kickoff; their absence at kickoff predicts their absence at QBR

---

## Common Blockers

| Blocker | Early Warning Sign | Resolution | Escalation Path |
|---|---|---|---|
| **SSO / IT approval delay** | No admin access credentials by Day 3; IT team says "working on it" with no date | Deliver the IT requirements checklist at kickoff (not after); schedule a dedicated 30-min IT call with TAM; provide pre-filled SSO setup guide | TAM → Solutions Engineering → AE for executive nudge if still blocked by Day 5 |
| **Security / InfoSec review** | InfoSec team raises questions not covered in sales process; SOC 2 or data residency questions appear | Provide security documentation package immediately (SOC 2 report, data processing agreement, pen test summary); schedule dedicated InfoSec call within 48h | CS → Security team for documentation; AE + CS Manager if review threatens kickoff timeline |
| **Champion unavailable or disengaged** | Missed kickoff or first follow-up meeting; response time exceeds 3 business days | Identify backup contact from kickoff stakeholder list; shift to async check-in cadence with recorded walkthroughs; propose condensed 2-week intensive schedule | CS Manager contacts executive sponsor with specific ask: "We need [name] or a designated backup to unblock milestone X by [date]" |
| **Stakeholder misalignment** | IT, champion, and sponsor describe different goals; scope creep requests appear in Week 1 | Facilitate 30-min alignment call within 24h of detecting divergence; document agreed scope in writing and get sign-off from sponsor | CS Manager → executive sponsor; defer out-of-scope items explicitly to a post-onboarding roadmap discussion |
| **Data quality issues** | Import fails on first attempt; customer's data doesn't match expected schema | Provide data template and field mapping guide at kickoff pre-work; offer a 45-min data preparation call with TAM; assist with first import manually if needed | CS → Support Engineering for data migration support; do not let this block champion training — run with a curated sample dataset in parallel |
| **Low team adoption after champion trained** | Only champion and 1–2 colleagues active by Day 18; team leads not invited to training | Run a team-onboarding session led by the champion (CS facilitates); create a quick-start guide personalised to their workflow; surface usage data to sponsor with a specific ask | CS → Champion + Executive Sponsor; frame as "we need 10 minutes at your next team standup to kick this off" |
| **License over-provisioning confusion** | IT team asks which users to provision; rollout order unclear | Pre-agree rollout sequence at kickoff (champion → team leads → full team); provide provisioning guide with recommended batch sizes | TAM handles directly; no escalation needed unless IT team is blocking provisioning |

---

## Handoff Criteria

**Handoff is complete when ALL of the following are true:**

| Criterion | Measurement | Status |
|---|---|---|
| TTFV achieved | 10+ distinct user IDs on primary workflow event within a 7-day window; champion written confirmation | [ ] |
| 40% seat adoption reached | 80+ unique active users in rolling 7 days per product analytics | [ ] |
| Champion identified and responsive | Named champion, responding within 24h, capable of self-serving basic questions | [ ] |
| Executive sponsor confirmed and engaged | Named sponsor attended kickoff and at least one milestone check-in | [ ] |
| Success criteria documented and agreed | Written, measurable criteria from kickoff on file in CRM; customer has acknowledged these in writing | [ ] |
| Health score green | Composite health score above threshold (product usage + engagement + relationship) | [ ] |
| All milestone escalation triggers resolved | No open escalations; any deferred items documented with agreed owner and date | [ ] |
| First QBR scheduled | Date set within 30 days of handoff; executive sponsor confirmed as attendee | [ ] |

**Handoff process:**

1. Onboarding Specialist completes the handoff document: milestone history, open items, stakeholder map, success criteria, any commitments made
2. BAU CSM reviews the handoff document and account health before the introduction call
3. Warm introduction: Onboarding Specialist introduces BAU CSM to champion via a 30-min call — not email
4. BAU CSM conducts a relationship-building call within 5 days of introduction (not a repeat of kickoff; focus on the path forward)
5. QBR scheduled and accepted within 30 days of handoff

**If handoff criteria not met by Day 40:**

- Onboarding Specialist flags to CS Manager with written root cause
- CS Manager reviews: extend onboarding (up to 15 days) or accept handoff with documented risk
- Root cause feeds back into this playbook — if the same blocker appears three times, it becomes a new row in the Common Blockers table
- AE notified if the delay puts renewal conversation timeline at risk

---

## Metrics

| Metric | Target | Measurement |
|---|---|---|
| Onboarding completion rate | 90% | Completed handoffs / total enterprise onboardings started in quarter |
| Time-to-first-value | 21 days from kickoff | Kickoff date to 10+ user primary workflow event |
| Day 30 adoption | 40% of licensed seats active | Product analytics: unique users with ≥1 session in rolling 7 days |
| Day 60 adoption | 60% of licensed seats active | Product analytics |
| Day 90 adoption | 70% of licensed seats active | Product analytics |
| Kickoff-to-technical-setup | 7 days | Kickoff date to health check passing |
| Customer satisfaction (onboarding) | 8.5/10 | Post-onboarding survey sent at handoff |

---

*Segment: Enterprise (200+ seats, dedicated IT, $100k+ ACV)*
*Target TTFV: 21 days*
*Milestone count: 6*
*Last updated: 2026-05-01*

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/18.0 (86%) |
| Evaluated | 2026-05-01 |
| Target duration | 121576 ms |
| Target cost | $0.2151 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill defines time-to-first-value (TTFV) as a customer-perceived outcome — not 'completed onboarding call' but a specific product event or metric threshold | PASS | TTFV section states: 'A team of at least 10 users (not just the champion) has completed the primary use-case workflow using their own live data — not sample or test data — and can demonstrate a measurable improvement against the baseline established at kickoff.' Clearly a customer-perceived outcome, not an activity. |
| c2 | Skill requires TTFV to be measurable automatically — if it can't be measured, the skill requires building the instrumentation first | PARTIAL | TTFV section names a product event: 'Product event: 10+ distinct user IDs have triggered the core workflow event within a 7-day window.' Automatic measurement is implied. However, the playbook nowhere addresses the case where this instrumentation does not yet exist, and does not require building it before the playbook ships. |
| c3 | Every milestone has an escalation trigger with a specific day threshold — not 'follow up if no response' | PASS | All 6 milestones in the Milestone Table have a populated 'Escalation Trigger' column with specific thresholds: 'no kickoff by Day 5', 'IT team unresponsive for 3+ business days', 'No champion login by Day 10', 'Fewer than 5 active users by Day 18', 'Adoption below 20% at Day 28', 'Health score not green by Day 40'. |
| c4 | Skill requires a segment definition before designing milestones — enterprise playbooks must be distinct from self-serve playbooks | PASS | The 'Segment Definition' table appears before the Milestone Table and covers company size (200+ seats, $100k+ ACV), technical sophistication (dedicated IT/security team), buyer/user gap, goals, decision-maker, and common integrations — all before milestones are presented. |
| c5 | Skill includes a kickoff meeting agenda with timing, owners, and outputs per topic | PASS | Kickoff Meeting Agenda section has a structured table with 6 time blocks (0–10 min, 10–25 min, etc.), named owners (Onboarding Specialist, TAM, IT Admin), and explicit outputs per slot (e.g., 'Written success criteria in the customer's words, not product marketing language; baseline metrics established'). |
| c6 | Skill defines handoff criteria as a checklist — onboarding is not complete until all criteria are met | PASS | Handoff Criteria section opens with 'Handoff is complete when ALL of the following are true:' and lists 8 rows each with a [ ] checkbox and a Measurement column. |
| c7 | Skill maps common blockers with early warning signs — partial credit if blockers are listed but early warning signs are not required per blocker | PARTIAL | Common Blockers table has an 'Early Warning Sign' column populated for all 7 blockers (e.g., 'No admin access credentials by Day 3; IT team says "working on it" with no date' for SSO delay). Full PARTIAL credit awarded — early warning signs are present per blocker. |
| c8 | Skill requires measurable success criteria for every milestone — 'complete onboarding call' is explicitly rejected | PASS | Every milestone has outcome-based Success Criteria: e.g., 'SSO configured and tested, primary integration(s) authenticated, security review complete, admin accounts provisioned'; '10+ distinct users have completed the primary workflow with live data; champion confirms outcome matches kickoff success criteria'. None are activity-based. |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The written artifact 'onboarding-playbook-enterprise.md' begins with a markdown table, not YAML frontmatter. Neither the chat response nor the artifact file contains name, description, or argument-hint YAML fields. No evidence of frontmatter in any captured output. |
| c10 | Output's TTFV definition is a customer-perceived outcome and a specific product event or threshold — e.g. 'first integration completed end-to-end with live data flowing', 'first 10 users active in week 2', 'first business report generated by the customer's own user' — NOT 'kickoff call complete' | PASS | TTFV is 'A team of at least 10 users... has completed the primary use-case workflow using their own live data — not sample or test data — and can demonstrate a measurable improvement against the baseline.' Measured by 'Product event: 10+ distinct user IDs have triggered the core workflow event within a 7-day window.' Matches the example pattern exactly. |
| c11 | Output's TTFV is automatically measurable — names the specific product event, analytics tool, or instrumentation that captures it; if the instrumentation doesn't exist, the playbook requires building it before the playbook ships | PASS | TTFV Measurement: 'Product event: 10+ distinct user IDs have triggered the core workflow event within a 7-day window.' Milestone verification references 'Product event: primary workflow event fired by champion's user ID' and 'Usage analytics: 80+ unique active users in rolling 7 days.' Names the specific product event as the instrumentation. |
| c12 | Output's segment definition explicitly addresses enterprise (200+ seats, dedicated IT teams, $100k+ annual contracts) — and notes how the playbook differs from a self-serve / SMB playbook | PARTIAL | Segment Definition covers '200+ licensed seats; $100k+ ACV', 'dedicated IT/security team', and the buyer/user gap. However, no comparison to self-serve or SMB playbooks is made anywhere in the document. The criterion requires explicitly noting the difference; only the enterprise-specific definition is present. |
| c13 | Output's milestones each have a measurable success criterion — e.g. 'Day 14: 50% of seats invited and active, IT integration completed, first 3 admin reports generated' — not 'had a kickoff call' | PASS | All 6 milestones have measurable success criteria: e.g., Milestone 4 requires '10+ distinct users have completed the primary workflow with live data; champion confirms outcome matches kickoff success criteria'; Milestone 5 requires '80+ users have logged in and completed at least one workflow; team leads can self-serve basic use cases.' |
| c14 | Output's escalation triggers per milestone are concrete with day thresholds — e.g. 'if no admin login by day 7, escalate to AE; if integration incomplete by day 21, escalate to engineering for assistance' | PASS | All 6 milestones have concrete day-threshold escalation triggers with named escalation targets: 'No champion login by Day 10 → re-engage with condensed async path'; 'Fewer than 5 active users by Day 18 → team onboarding session fast-tracked'; 'Adoption below 20% at Day 28 → escalate to executive sponsor with usage report.' |
| c15 | Output's kickoff agenda has timing per topic, named owners (CSM / AE / SE / customer attendees), and outputs (signed RACI, agreed success metrics, integration list, security review status) — not bullet topics without owners | PASS | Kickoff table: 0–10 min / Onboarding Specialist / 'Documented RACI: CS contacts, customer contacts, escalation chain'; 10–25 min / Onboarding Specialist / 'Written success criteria in the customer's words...baseline metrics established'; 25–40 min / TAM + IT Admin / 'Integration scope confirmed; IT requirements doc delivered; SSO/security timeline agreed.' All three required elements present per topic. |
| c16 | Output's handoff criteria is a checklist that ALL items must satisfy before onboarding is 'complete' — e.g. TTFV achieved, all admin users trained, integration in production, executive sponsor confirmed quarterly cadence — with each as a checkbox | PASS | 'Handoff is complete when ALL of the following are true:' followed by 8 rows each with a [ ] checkbox. Includes TTFV achieved, 40% seat adoption, champion identified, executive sponsor confirmed, success criteria documented, health score green, escalation triggers resolved, first QBR scheduled. |
| c17 | Output addresses common enterprise blockers — IT security review timing, SSO/SAML setup, procurement / DPA, multi-region deployment — with early warning signs per blocker | PASS | SSO/SAML: 'SSO / IT approval delay' blocker with early warning sign. IT Security: 'Security / InfoSec review' blocker. DPA/procurement: InfoSec resolution includes 'data processing agreement' and 'SOC 2 report'. Each has an early warning sign column. Multi-region deployment is not explicitly named, but the other three specified categories are covered. |
| c18 | Output's milestone success criteria explicitly REJECT activity-based metrics like 'completed kickoff call' or 'training session held' — every milestone is outcome-based | PARTIAL | All milestone success criteria are outcome-based in practice (no 'had a call' entries), but the playbook does not explicitly state the rejection of activity-based metrics anywhere in the milestone section. The kickoff anti-patterns section addresses meeting conduct but not milestone metric philosophy. Implicit but not explicit rejection. |
| c19 | Output addresses post-onboarding handoff to the AE / sustain CSM with the artefacts that travel forward — what the post-onboarding owner inherits | PARTIAL | Handoff process step 1: 'Onboarding Specialist completes the handoff document: milestone history, open items, stakeholder map, success criteria, any commitments made.' BAU CSM reviews this before introduction call. Artifacts that travel forward are named. AE is notified only if renewal timeline is at risk — not a structured AE handoff artefact. |

### Notes

The playbook output is exceptionally strong overall, scoring 86.1%. TTFV is well-defined as a customer-perceived outcome tied to a specific product event (10+ distinct user IDs on the core workflow event). All six milestones have day-threshold escalation triggers, outcome-based success criteria, and measurable verification methods. The kickoff agenda, common blockers table, and handoff checklist all satisfy their respective criteria with notable depth. The main gaps are: (1) no YAML frontmatter in the skill/output file (c9 failed completely); (2) the playbook doesn't address the 'instrumentation doesn't exist' scenario for TTFV (c2 partial); (3) the segment definition doesn't explicitly contrast with self-serve/SMB playbooks (c12 partial); (4) activity-based metrics are avoided in practice but never explicitly rejected (c18 partial). The handoff section covers artefacts passed to BAU CSM but the AE handoff path is minimal.
