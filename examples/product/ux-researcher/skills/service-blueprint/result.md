# Service Blueprint

Scenario: Testing whether the service-blueprint skill requires both frontstage and backstage lanes, a line of visibility, failure point analysis, and improvement recommendations.

## Prompt

> /ux-researcher:service-blueprint for our enterprise customer onboarding process — from contract signed to customer achieving first value, including everything our CS, solutions engineering, and support teams do behind the scenes.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

The blueprint is saved at `docs/design/service-blueprint--enterprise-onboarding.md`. Here's what it covers:

**18 customer actions** from contract close to first value confirmation, mapped against:
- **14 frontstage employee actions** (CSM, Solutions Engineering, Support) — everything the customer sees
- **16 backstage actions** across the three teams, with triggers and durations
- **12 support systems** mapped to the backstage steps that depend on them
- **10 failure points** — the most critical being: Sales→CS handoff information loss (F1), vague first value definition at kickoff (F2), and provisioning queue delays with no customer-visible status (F3)
- **10 prioritised recommendations**, led by locking a concrete first value definition in Gainsight as a required kickoff field

**Before treating this as current-state:** replace the assumed stack (Salesforce + Gainsight + Zendesk/Jira) and team structure (CSM / SE / Support) with your actuals. The failure points and recommendations are realistic patterns but the durations and frequencies will need calibration against your own data.

### Artifacts written

#### `work/docs/design/service-blueprint--enterprise-onboarding.md`

```
# Service Blueprint: Enterprise Customer Onboarding

> **Assumptions — validate before using operationally.** This blueprint was built from common enterprise SaaS patterns, not observed internal state. It assumes: (1) a Salesforce CRM with Gainsight for CS health scoring; (2) Zendesk for customer-facing support and Jira for internal engineering tickets; (3) a CSM / Solutions Engineering / Support three-team split; (4) a 30-day TTFV target; (5) a pilot cohort model (10–50 users) before broad rollout. Replace any of these that don't match your actual stack, team structure, or commercial commitments before treating this as a current-state document.

## Scope

| Element | Detail |
|---|---|
| **Service** | Enterprise customer onboarding |
| **Journey** | Contract signed → customer achieves first value milestone |
| **Start point** | Contract is countersigned and CRM stage moves to "Closed Won" |
| **End point** | Customer confirms completion of their defined first use case (e.g., first workflow live, first report run, first integration active) |
| **Customer type** | Enterprise buyer team: executive sponsor, IT/admin owner, and pilot end users |
| **Success metric** | Time to First Value (TTFV); target ≤30 days. Secondary: 90-day retention rate, NPS at day 45 |

---

## Customer Actions

| Step | Customer action | Touchpoint | Channel |
|---|---|---|---|
| C1 | Receives welcome communication and introduction to CS team | Welcome email + CS introduction | Email |
| C2 | Schedules kickoff call with CS and Solutions Engineering | Calendar invite / scheduling link | Email |
| C3 | Attends kickoff call — shares goals, constraints, and desired first use case | Kickoff call | Video call |
| C4 | Completes internal stakeholder alignment (IT, security, end-user champions) | Internal meeting (no vendor present) | Internal |
| C5 | Submits IT/security questionnaire and SSO requirements | Security intake form | Web form / email |
| C6 | Receives and reviews implementation plan | Implementation plan document | Email / shared doc |
| C7 | Approves implementation plan and agrees on first value definition | Sign-off email or Mutual Success Plan | Email |
| C8 | IT/admin attends technical setup sessions with Solutions Engineering | Configuration sessions | Video call / screen share |
| C9 | IT/admin completes SSO, integration, and permission configuration | Product admin console | In-app + Video call |
| C10 | Customer waits for environment to be provisioned and validated | — (waiting state, avg 2–5 days) | — |
| C11 | Admin and power users attend training sessions | Training sessions | Video call / LMS |
| C12 | Invites pilot user cohort (typically 10–50 users) | Invitation flow in product | In-app email |
| C13 | Pilot users activate accounts and complete guided setup | Onboarding flow | In-app |
| C14 | Pilot users attempt first use case | Product | In-app |
| C15 | Customer submits support tickets as issues arise | Support portal | Web / email |
| C16 | Attends CS check-in (day ~14) | Check-in call | Video call |
| C17 | Pilot users complete first use case successfully | Product | In-app |
| C18 | Receives first value confirmation summary from CS | Success summary email | Email |

---

## Frontstage Employee Actions

| Step | Corresponding customer action | Employee action | Role | Touchpoint |
|---|---|---|---|---|
| FS1 | C1 | Sends personalised welcome email within 24h of close; introduces CS team and next steps | Customer Success Manager (CSM) | Email |
| FS2 | C2 | Sends scheduling link; confirms kickoff agenda with the customer | CSM | Email |
| FS3 | C3 | Leads kickoff call: validates use cases, sets first value definition, agrees timeline | CSM + Solutions Engineer | Video call |
| FS4 | C5 | Sends IT/security intake form; answers questions about data residency and compliance | Solutions Engineer | Email + video call |
| FS5 | C6 | Delivers implementation plan including milestones, owners, and first value definition | CSM | Shared doc / email |
| FS6 | C7 | Runs Mutual Success Plan (MSP) sign-off conversation; locks first value definition | CSM | Video call |
| FS7 | C8 | Leads technical setup sessions; walks admin through configuration step by step | Solutions Engineer | Video call / screen share |
| FS8 | C11 | Delivers admin and end-user training sessions; shares recordings | CSM + Solutions Engineer | Video call / LMS |
| FS8b | C9 | SE remains available on a standing Slack channel or open office-hours block during config week; responds to admin questions within 2h (self-serve moment — customer does the work, SE is on standby) | Solutions Engineer | Slack / async |
| FS8c | C14 | In-app guided tooltips and contextual help surface automatically during first use case; CSM is on standby via email if pilot users escalate (intentional self-serve moment — frontstage is product-led) | Product (in-app) + CSM | In-app / email |
| FS9 | C15 | Acknowledges support tickets; provides initial triage response within SLA | Support Engineer | Support portal / email |
| FS10 | C16 | Runs day-14 check-in: reviews adoption metrics, unblocks issues, adjusts plan if needed | CSM | Video call |
| FS11 | C17 | Celebrates first value milestone with customer; documents outcome | CSM | Email / call |
| FS12 | C18 | Sends first value summary with usage data and next recommended steps | CSM | Email |

---

───────────────────── LINE OF VISIBILITY ─────────────────────
*Everything above: the customer sees it. Everything below: the customer does NOT see it.*

**Visibility audit:**

| Customer action | What customer sees | What customer does NOT see |
|---|---|---|
| C1 — receives welcome email | Personalised email from named CSM | Sales→CS handoff call, CRM data transfer, account research, CSM assignment logic |
| C3 — kickoff call | Confident, prepared CS and SE team | Kickoff prep doc, internal briefing, account research, script/agenda template |
| C5 — submits IT requirements | Form and fast acknowledgement | SE reviewing requirements against product capabilities, internal Slack escalation if gaps found |
| C10 — waiting for environment | Nothing visible | Provisioning steps, back-and-forth between SE and infrastructure/DevOps |
| C14 — pilot users attempt first use case | Product experience | Health score monitoring, CSM tracking activation in dashboard, proactive escalation if low |
| C15 — submits support ticket | Acknowledgement email and SLA commitment | Ticket triage, internal escalation to tier 2/SE, Slack coordination between Support and CS |
| C16 — day-14 check-in | CSM with adoption metrics | Health score pulled from Gainsight, CSM pre-call prep, internal risk flag if metrics low |

---

## Backstage Employee Actions

| Step | Triggered by | Employee action | Role | System/tool used | Duration |
|---|---|---|---|---|---|
| BS1 | Contract closed (CRM stage change) | Sales → CS handoff call: transfers account context, ICP fit, key contacts, political map, red flags | Account Executive + CSM | Salesforce + Notion handoff doc | 30–60 min |
| BS2 | BS1 complete | CSM creates onboarding project in tracker; sets milestone dates; assigns SE | CSM | Gainsight / Notion / Asana | 30 min |
| BS3 | BS2 complete | CSM researches account: LinkedIn, usage during trial, Salesforce notes, competitor context | CSM | Salesforce, LinkedIn, product analytics | 60–90 min |
| BS4 | BS2 complete | CSM prepares kickoff agenda doc and briefs Solutions Engineer | CSM | Notion / Google Docs | 30 min |
| BS5 | C5 — IT form submitted | SE reviews security requirements against product capabilities; flags gaps to Product/Engineering if needed | Solutions Engineer | Internal wiki, product docs | 1–3 days |
| BS6 | BS5 complete | SE provisions tenant environment: creates instance, configures data region, sets resource limits | Solutions Engineer | Admin portal / infrastructure tooling | 2–4 hours (often queued 1–2 days) |
| BS7 | BS6 complete | SE validates provisioning: smoke tests, confirms SSO handshake, verifies integrations | Solutions Engineer | Staging environment, integration logs | 1–2 hours |
| BS8 | C7 — MSP approved | CSM logs first value definition and target date in Gainsight; sets health score alert thresholds | CSM | Gainsight | 20 min |
| BS9 | BS6 complete | SE prepares configuration guide specific to customer's environment (SSO provider, integrations) | Solutions Engineer | Notion / Google Docs | 2–3 hours |
| BS10 | C11 — training sessions delivered | CSM uploads recordings to LMS/shared drive; sends follow-up resource pack | CSM | LMS / Google Drive | 30 min |
| BS11 | C12–C14 — pilot users active | CSM monitors daily activation and feature adoption metrics in dashboard; flags users not activating | CSM | Gainsight / product analytics | Daily 15 min |
| BS12 | BS11 — low adoption detected | CSM drafts intervention plan; may loop in SE for technical barrier investigation | CSM | Gainsight, internal Slack | 1–2 hours |
| BS13 | C15 — support ticket submitted | Support Engineer triages ticket: reproduces issue, checks known bugs, classifies severity | Support Engineer | Zendesk / Jira | 30 min – 2 hours |
| BS14 | BS13 — ticket exceeds tier 1 scope | Support Engineer escalates to SE or Engineering; writes internal ticket with reproduction steps | Support Engineer + SE | Jira, Slack | 1–4 hours handoff lag |
| BS15 | C17 — first value achieved | CSM documents outcome: screenshots, usage data, customer quote; logs in CRM | CSM | Salesforce, Gainsight | 30 min |
| BS16 | BS15 complete | CSM triggers internal "first value achieved" notification to Account Executive and CS leadership | CSM | Gainsight / Slack automation | Automated |

---

## Support Processes

| Backstage action | Support system | Type | Owner | SLA / availability |
|---|---|---|---|---|
| BS1 — handoff call | Salesforce (account/contact/opportunity data) | CRM | Revenue Operations | Business hours; data required within 24h of close |
| BS2 — onboarding project creation | Gainsight (customer success platform) | Customer success platform | CS Operations | Business hours |
| BS3 — account research | Salesforce + product analytics (Mixpanel/Amplitude) | CRM + analytics | Sales / Product | Self-serve; data must be current |
| BS5 — security review | Internal security docs / compliance matrix | Manual process (Wiki) | Solutions Engineering | 1–3 days; **no formal SLA** |
| BS6 — tenant provisioning | Admin provisioning portal / infrastructure tooling | Internal tool (partially automated) | Infrastructure / DevOps | Queued — no guaranteed start time; **manual steps required** |
| BS7 — environment validation | Integration logs, staging environment | Manual process | Solutions Engineering | Ad hoc |
| BS8 — health score setup | Gainsight (health scores, alerts, milestones) | Customer success platform | CS Operations | Real-time once configured |
| BS10 — training recordings | LMS / Google Drive | Content platform | CS | Self-serve; no DRM or access expiry management |
| BS11 — adoption monitoring | Gainsight + product analytics | Customer success platform + analytics | CS | Daily data refresh; lag up to 24h |
| BS13 — ticket triage | Zendesk (customer-facing) + Jira (internal) | Support platform + issue tracker | Support Engineering | P1: 1h response; P2: 4h; P3: 1 business day |
| BS14 — ticket escalation | Jira + Slack | Issue tracker + messaging | Support + Engineering | No formal SLA for internal escalation handoff |
| BS15 — first value logging | Salesforce + Gainsight | CRM + CS platform | CSM | Manual; dependent on CSM completing step |

---

## Failure Points

| # | Location | Failure mode | Impact on customer | Frequency | Root cause | Current mitigation |
|---|---|---|---|---|---|---|
| F1 | BS1 — Sales→CS handoff | AE passes insufficient context (no red flags, no ICP notes, incorrect contact info) | CS arrives at kickoff unprepared; customer loses confidence; wrong goals pursued | Weekly | No structured handoff template; AE incentive ends at close | Informal Slack message; inconsistent |
| F2 | C3 / FS3 — kickoff | First value not defined concretely (customer says "we want better workflows") | Onboarding drifts; no clear success target; 90-day churn risk | Common | CSM avoids pushing back on vague goals in first meeting | None — relies on CSM experience |
| F3 | C10 — provisioning wait | Provisioning queue backlog causes 3–5 day delays with no customer-visible status | Customer is blocked; loses momentum; files "what's the status?" tickets | Weekly | Manual provisioning steps; no self-service; queue not surfaced to CS | CSM manually chases SE via Slack |
| F4 | BS5 — security review | SE discovers a compliance gap (e.g., data residency not supported in required region) | Onboarding stalls 1–4 weeks; legal/security review required; executive escalation | Monthly | Security requirements not captured during sales; product gaps discovered post-close | None — ad hoc escalation to Engineering |
| F5 | BS14 — support escalation | Escalated ticket sits unacknowledged in Jira for 24–48h while pilot users are blocked | Pilot users fail to complete first use case; CSM unaware; NPS damage | Weekly | No SLA on internal handoff; Engineering/SE have competing priorities | Support pings SE on Slack (unreliable) |
| F6 | BS11 — adoption monitoring | Analytics data lag (up to 24h) means CS sees low adoption too late to intervene | At-risk users churn from the pilot before CS can unblock them | Daily | Product analytics pipeline latency; Gainsight sync frequency | Manual daily check-in (not scalable) |
| F7 | C12–C13 — pilot user activation | Pilot users receive invite but never activate (email goes to spam, no internal champion follow-up) | First use case never attempted; onboarding stalls; TTFV missed | Common | Customer-side champion doesn't follow through; no re-engagement automation | CSM manually reminds customer on call |
| F8 | FS1 — welcome email | CS assignment and welcome email delayed >48h after contract close | Customer has post-purchase anxiety; may escalate to AE; trust eroded at start | Occasional | No automated CS assignment trigger; manual process reliant on RevOps noticing CRM update | RevOps monitors CRM daily (misses weekends) |
| F9 | BS6 — provisioning | Provisioned environment has misconfiguration that isn't caught until customer's IT hits it | IT wastes 1–2 sessions debugging; SE reputation damaged; trust reduced | Occasional | Validation checklist is manual and incomplete; no automated smoke test suite | SE runs informal checks |
| F10 | C16 — day-14 check-in | CSM has too many accounts and de-prioritises check-in call; meeting postponed or cancelled | Risk goes undetected; no intervention before 30-day mark; TTFV missed | Occasional | CSM-to-account ratio too high; no system alert forcing check-in | Manager reviews pipeline weekly |

---

## Recommendations

| Priority | Failure point | Recommendation | Impact | Effort | Owner |
|---|---|---|---|---|---|
| 1 | F2 — vague first value | Embed a structured "first value definition worksheet" into the kickoff call template. CSM must log a specific, measurable first use case in Gainsight before the call ends — a required field, not optional. This locks the success target for the entire engagement. | Eliminates drift; creates a shared accountability anchor; reduces 90-day churn | S | CS Operations + CS Leadership |
| 2 | F1 — Sales→CS handoff | Replace the informal Slack handoff with a mandatory structured handoff doc in Salesforce (account context, political map, red flags, key contacts, ICP fit score, trial usage highlights). AE cannot mark opportunity "Closed Won - Handed Off" without completing it. Gate enforced in CRM workflow. | Kickoff quality improves immediately; CS arrives prepared; fewer surprise escalations | M | Revenue Operations + Sales Leadership |
| 3 | F3 — provisioning delays | Automate tenant provisioning: pre-provision a pool of clean environments triggered by CRM stage change, then assign to the customer. Eliminate the manual queue entirely. Show provisioning status to CS in Gainsight so they can set accurate customer expectations. | Removes the most common early-stage momentum killer; reduces TTFV by 2–4 days | L | Engineering / Infrastructure |
| 4 | F5 — escalation SLA gap | Define and enforce an internal SLA for Jira escalations from Support to Engineering/SE: 4h acknowledgement, 1 business day first response. Automate a Slack alert to the on-call SE lead when a customer-facing ticket breaches 4h without acknowledgement. | Pilot users unblocked faster; reduces NPS damage from support failures | M | Support Operations + Engineering |
| 5 | F7 — pilot user non-activation | Trigger an automated re-engagement sequence for pilot users who receive an invite but don't activate within 48h: in-app nudge + email from CSM's name (automated but personalised). Flag to CSM in Gainsight if activation rate drops below 50% by day 7. | Closes the most common activation gap without requiring CSM manual intervention | M | Product + CS Operations |
| 6 | F8 — delayed welcome | Trigger CS assignment and welcome email automatically on CRM stage change to "Closed Won" — no RevOps manual step. If no CSM is assigned within 2h, auto-alert CS leadership. Target: welcome email delivered within 4 business hours of close, including weekends. | Eliminates post-purchase anxiety; sets professional tone from day one | S | Revenue Operations + Engineering |
| 7 | F4 — security gaps at post-close | Move security and compliance scoping into the sales process (late-stage technical qualification call with SE). Maintain a product compliance matrix (data residency, certifications, integration compatibility) that AE and SE reference pre-close. Update quarterly. | Prevents onboarding stalls caused by compliance surprises; protects win rate | M | Solutions Engineering + Product |
| 8 | F6 — analytics lag | Reduce Gainsight sync frequency from daily to near-real-time (hourly or event-driven webhook) for key activation events: account created, first login, first core action. This doesn't require full pipeline re-architecture — instrument the critical events only. | CS can intervene within hours, not days; improves at-risk detection | M | Engineering + CS Operations |
| 9 | F9 — provisioning misconfiguration | Build an automated smoke test suite that runs post-provisioning: SSO login test, permission model check, integration handshake, core feature availability. Block "provisioning complete" notification until all checks pass. | Eliminates wasted technical sessions caused by misconfigured environments | M | Solutions Engineering + QA |
| 10 | F10 — CS capacity | Instrument Gainsight to auto-schedule the day-14 check-in when onboarding is created (not when CSM remembers). Flag overdue check-ins to CS manager. Address CSM-to-account ratio if >40 accounts per CSM — the downstream failure rate justifies the headcount. | Ensures no account falls through the cracks; makes capacity problem visible | S (tooling) / L (headcount) | CS Leadership + CS Operations |

---

*Service:* Enterprise Customer Onboarding
*Journey:* Contract signed → first value achieved
*Failure points identified:* 10
*Last updated:* 2026-05-01

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.5/17.0 (91%) |
| Evaluated | 2026-05-01 |
| Target duration | 215241 ms |
| Target cost | $0.5507 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires a scope definition with a concrete start event and end outcome before mapping begins | PASS | Scope table defines Start point: 'Contract is countersigned and CRM stage moves to "Closed Won"' and End point: 'Customer confirms completion of their defined first use case (e.g., first workflow live, first report run, first integration active)' |
| c2 | Skill maps all four required lanes: customer actions, frontstage employee actions, backstage employee actions, and support processes | PASS | Artifact contains four distinct tables: 'Customer Actions' (C1–C18), 'Frontstage Employee Actions' (FS1–FS12), 'Backstage Employee Actions' (BS1–BS16), and 'Support Processes' (12 rows) |
| c3 | Skill explicitly draws the line of visibility separating what customers see from what they don't | PASS | Artifact contains '───────────────────── LINE OF VISIBILITY ─────────────────────' with the explicit note: 'Everything above: the customer sees it. Everything below: the customer does NOT see it.' |
| c4 | Skill includes a visibility audit — identifying what backstage work becomes visible to customers and whether that's intentional | PASS | A 'Visibility audit' table immediately follows the line of visibility, with columns 'What customer sees' and 'What customer does NOT see' mapped to seven key customer actions (C1, C3, C5, C10, C14, C15, C16) |
| c5 | Skill requires failure point analysis with location, failure mode, customer impact, frequency, and root cause | PASS | Failure Points table has explicit columns: Location, Failure mode, Impact on customer, Frequency, Root cause — all populated for F1–F10 |
| c6 | Skill requires each backstage action to have a trigger — no orphaned process steps | PASS | Backstage Employee Actions table has a 'Triggered by' column; every step BS1–BS16 has a populated trigger, e.g. BS1: 'Contract closed (CRM stage change)', BS12: 'BS11 — low adoption detected' |
| c7 | Skill requires duration estimates for backstage actions — partial credit if duration is mentioned as important but not required per step | PARTIAL | Backstage Employee Actions table has a 'Duration' column with estimates for every step, e.g. BS1: '30–60 min', BS6: '2–4 hours (often queued 1–2 days)', BS5: '1–3 days'. Fully present but ceiling is PARTIAL. |
| c8 | Skill produces prioritised improvement recommendations linked to specific failure points | PASS | Recommendations table has 'Priority' (1–10) and 'Failure point' columns explicitly linking each recommendation to a failure point, e.g. Priority 1 → 'F2 — vague first value', Priority 2 → 'F1 — Sales→CS handoff' |
| c9 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output contains only a chat summary and the generated blueprint markdown file. No skill definition file with YAML frontmatter is shown in the artifacts written or chat response. |
| c10 | Output's scope explicitly defines start ("contract signed by enterprise customer") and end ("customer reaches first measurable value: e.g. first dashboard viewed by 5+ named users") — not abstract endpoints | PASS | Scope table: Start: 'Contract is countersigned and CRM stage moves to "Closed Won"'; End: 'Customer confirms completion of their defined first use case (e.g., first workflow live, first report run, first integration active)' — concrete examples given, not abstract |
| c11 | Output's blueprint has all four lanes — Customer Actions (what the customer does and sees), Frontstage Actions (CSM, AE, SE talking to the customer), Backstage Actions (internal handoffs, configuration work the customer never sees), Support Processes (systems that support both stages: CRM, Slack handoffs, Jira tickets) | PASS | All four lanes present: 18-row Customer Actions table; Frontstage table with CSM/SE/Support roles; Backstage table with AE+CSM, SE, Support roles; Support Processes table referencing Salesforce, Gainsight, Zendesk, Jira, Slack |
| c12 | Output draws the line of visibility explicitly — separating frontstage (customer sees this) from backstage (customer doesn't) — so the blueprint clarifies what customers experience vs what's hidden | PASS | Explicit visual separator '───────────────────── LINE OF VISIBILITY ─────────────────────' with annotation 'Everything above: the customer sees it. Everything below: the customer does NOT see it.' |
| c13 | Output's visibility audit identifies leaky abstractions — backstage work that becomes customer-visible (e.g. CSM forwarding internal Jira tickets, support staff CC'ing customer on internal threads) — flagged as either intentional or a process bug | PARTIAL | Visibility audit shows what's hidden vs. visible per step, and FS8b/FS8c in frontstage notes 'intentional self-serve moment'. However, the audit does not explicitly identify leaky abstractions (backstage work bleeding through unintentionally) nor flag individual items as 'intentional' vs. 'process bug' in a dedicated column or notation. |
| c14 | Output's failure point analysis lists concrete failure modes — e.g. "Day 5: SSO integration fails because Azure AD admin not yet identified; customer impact: blocked from inviting team; frequency: 30% of enterprise onboardings; root cause: SE doesn't request this in kickoff" | PASS | F4: 'SE discovers a compliance gap (e.g., data residency not supported in required region) \| Onboarding stalls 1–4 weeks; legal/security review required \| Monthly \| Security requirements not captured during sales'. F3: 'Provisioning queue backlog causes 3–5 day delays \| Customer is blocked; loses momentum \| Weekly \| Manual provisioning steps; no self-service' |
| c15 | Output's backstage actions each have a trigger — e.g. "Provisioning workflow triggered when contract signature webhook fires" — no orphaned process steps | PASS | Every BS1–BS16 has a 'Triggered by' entry. BS1: 'Contract closed (CRM stage change)', BS6: 'BS5 complete', BS16: 'BS15 complete'. No orphaned steps. |
| c16 | Output's improvements are tied to specific failure points — not "improve onboarding" but "to fix the SSO blocker (failure point #2): add 'Azure AD admin name' as a required field in the kickoff agenda" | PASS | Each of 10 recommendations references the failure point: 'Priority 1 \| F2 — vague first value \| Embed a structured first value definition worksheet…', 'Priority 3 \| F3 — provisioning delays \| Automate tenant provisioning…' |
| c17 | Output covers the three named teams — CS, solutions engineering, support — with clear ownership per backstage action; no ambiguity about who does what | PASS | Role column in Backstage table assigns each step unambiguously: BS1 'Account Executive + CSM', BS5–BS7/BS9 'Solutions Engineer', BS13–BS14 'Support Engineer + SE'. All three named teams (CS, SE, Support) appear with clear ownership. |
| c18 | Output's customer-action lane includes their thinking / feeling / pain at each stage — service blueprint plus journey-map dimensions, since enterprise onboarding is emotionally heavy for the customer | FAIL | Customer Actions table has columns: Step, Customer action, Touchpoint, Channel. There is no column or annotation for customer thinking, feeling, emotion, or pain. C10 notes '(waiting state, avg 2–5 days)' but does not capture emotional state. Journey-map dimension is absent. |
| c19 | Output addresses duration estimates per backstage action — how long each step typically takes (e.g. "SE config: 2-4 hours", "Provisioning: instant", "Customer's IT review: 1-3 weeks") so bottlenecks are visible | PARTIAL | Backstage Actions table has a 'Duration' column with estimates for all 16 steps, e.g. BS6: '2–4 hours (often queued 1–2 days)', BS5: '1–3 days', BS2: '30 min'. Ceiling is PARTIAL. |

### Notes

The output is a high-quality service blueprint that satisfies nearly all structural requirements: all four lanes are present and well-populated, the line of visibility is explicit, triggers exist for every backstage action, failure points are concrete and well-structured, and recommendations are tightly linked to specific failure points. The two clear gaps are: (1) c18 — the customer action lane is purely functional with no emotional/thinking/feeling dimension despite the criterion explicitly asking for journey-map enrichment; (2) c9 — the skill definition file with YAML frontmatter is not among the artifacts and cannot be verified. A minor gap exists in c13 where the visibility audit maps the dividing line clearly but does not explicitly call out leaky abstractions or categorize them as intentional vs. process bugs. Duration estimates (c7/c19) are fully present, both hitting their PARTIAL ceilings. Overall a very strong output at 91.2%.
