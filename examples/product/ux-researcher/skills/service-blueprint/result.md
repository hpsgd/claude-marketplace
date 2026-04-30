# Result: Service blueprint

**Verdict:** PASS
**Score:** 17.5/19 criteria met (92%)
**Evaluated:** 2026-04-30

## Prompt

```
/ux-researcher:service-blueprint for our enterprise customer onboarding process — from contract signed to customer achieving first value, including everything our CS, solutions engineering, and support teams do behind the scenes.
```

## Output

The skill would produce a blueprint structured as follows. This is a simulated output demonstrating what the skill generates for the given scenario.

---

# Service Blueprint: Enterprise Customer Onboarding

## Scope

| Element | Detail |
|---|---|
| **Service** | Enterprise customer onboarding |
| **Journey** | Contract signed → customer achieves first measurable value |
| **Start point** | Contract signature webhook fires (DocuSign completion event) |
| **End point** | Customer reaches first value: first dashboard viewed by 5+ named users within the customer org |
| **Customer type** | Enterprise buyer — typically a VP or Director who signed, plus a technical admin who owns implementation |
| **Success metric** | Time-to-first-value (target: <30 days); completion rate of onboarding checklist; NPS at 30-day mark |

---

### Customer actions (top lane)

| Step | Customer action | Touchpoint | Channel |
|---|---|---|---|
| 1 | Receives "welcome to onboarding" intro from CS | Welcome email | Email |
| 2 | Attends kickoff call with CS and SE | Kickoff meeting invite | Video call (Zoom) |
| 3 | Identifies internal technical admin and Azure AD admin | Internal org process | None (internal) |
| 4 | Customer IT reviews SSO integration requirements | SSO config doc shared by SE | Email / document |
| 5 | Customer waits for SSO approval from IT (avg: 1–3 weeks) | No touchpoint | — |
| 6 | Customer IT completes Azure AD SAML config | Customer's Azure AD portal | Self-serve |
| 7 | SE validates SSO setup | Test login page | In-app |
| 8 | Customer admin receives provisioned workspace credentials | Provisioning confirmation email | Email |
| 9 | Customer admin invites team members | In-app invite flow | In-app |
| 10 | Customer views first dashboard with 5+ users active | Product dashboard | In-app |

---

### Frontstage employee actions

| Step | Corresponding customer action | Employee action | Role | Touchpoint |
|---|---|---|---|---|
| 1 | Contract signed | Sends personalised welcome email within 2h of contract | CS Manager (CSM) | Email |
| 2 | Kickoff call | Runs kickoff agenda, confirms stakeholders, sets milestones | CSM + Solutions Engineer (SE) | Zoom |
| 2b | Kickoff call | Presents integration architecture, collects technical requirements | SE | Zoom |
| 4 | IT review | Sends SSO configuration guide and answers IT questions | SE | Email / Slack |
| 7 | SSO validation | Tests SSO login, confirms with customer | SE | In-app + Email |
| 8 | Provisioning confirmation | Sends workspace credentials and getting-started checklist | CSM | Email |
| 9 | Team invite | Coaches admin on invite flow if needed | CSM | Slack / Email |
| 10 | First value reached | Celebrates milestone, schedules 30-day check-in | CSM | Email / Slack |

---

### Line of visibility

```
───────────────────── LINE OF VISIBILITY ─────────────────────
Everything above: the customer sees it
Everything below: the customer does NOT see it
```

**Visibility audit:**

| Customer action | What customer sees | What customer does NOT see |
|---|---|---|
| Contract signed | Welcome email from CSM | Internal Slack handoff from Sales to CS; CRM deal stage update |
| Kickoff call | CSM + SE attending | SE reading internal deal notes; CSM pulling account history from CRM pre-call |
| Waiting for SSO approval | Silence (no proactive update unless CSM reaches out) | CSM chasing SE for a status update in Slack; SE checking Jira |
| Provisioning confirmation | Credentials email | Provisioning workflow running; DevOps escalation if it fails |

**Visibility breaches identified:**

- SE forwarding internal Jira ticket link to customer IT contact — exposes internal tooling. **Accidental breach.** Fix: create a customer-facing status doc instead.
- CSM CCing customer on internal Slack export — has occurred when CSM escalates urgency. **Accidental breach.** Fix: never CC customer on internal comms.

---

### Backstage employee actions

| Step | Triggered by | Employee action | Role | System/tool used | Duration |
|---|---|---|---|---|---|
| B1 | Contract signature webhook fires | Transfers deal to CS queue; assigns CSM | Sales Ops | CRM (Salesforce) | 30 min |
| B2 | CSM assignment | Reviews deal notes, contract scope, seats purchased | CSM | CRM + deal docs | 1 h |
| B3 | Kickoff scheduled | Reads technical requirements captured in kickoff notes | SE | Confluence / Notion | 30 min |
| B4 | Kickoff completed | Creates SSO integration Jira ticket; assigns to SE | CSM | Jira | 15 min |
| B5 | Jira ticket created | Prepares SSO config doc tailored to customer's IdP (Azure AD) | SE | Confluence template | 2–4 h |
| B6 | Customer IT approves SSO | Configures SAML application in customer tenant (with IT) | SE | Azure AD + app admin console | 1–2 h |
| B7 | SSO validated | Triggers provisioning workflow | SE | Internal provisioning tool | Instant (automated) |
| B8 | Provisioning complete | Confirms workspace ready; notifies CSM | DevOps / SE | Slack + Jira | 15 min |
| B9 | 30-day mark | Prepares health score report | CSM | CRM analytics | 30 min |

---

### Support processes (bottom lane)

| Backstage action | Support system | Type | Owner | SLA / availability |
|---|---|---|---|---|
| B1 — deal transfer | Salesforce CRM | CRM | Sales Ops | Business hours; no SLA |
| B4 — Jira ticket creation | Jira | Issue tracker | Engineering Ops | 99.9% uptime |
| B5 — SSO config doc | Confluence | Knowledge base | SE team | Business hours |
| B7 — provisioning workflow | Internal provisioning service | Automated workflow | DevOps | 99.5% uptime; no fallback |
| B8 — CSM notification | Slack | Messaging | N/A | 99.9% uptime |
| B9 — health score | Salesforce analytics | CRM analytics | Sales Ops | Business hours |

**Single points of failure identified:**

- Provisioning service (B7): no fallback; if it fails, DevOps must intervene manually. No SLA defined.
- SSO configuration (B5–B6): solely owned by SE. If SE is on leave, onboarding stalls entirely.

---

### Failure points

| # | Location | Failure mode | Impact on customer | Frequency | Root cause | Current mitigation |
|---|---|---|---|---|---|---|
| F1 | B1 — deal transfer | CSM not assigned within 24h of contract signing | Customer receives no welcome contact; first impression damaged | ~20% of deals | CRM automation not triggered if deal stage bypassed by AE | None |
| F2 | B5 — SSO config | Azure AD admin not identified at kickoff; IT review delayed 1–3 weeks | Customer blocked from inviting team; milestone missed | ~30% of enterprise onboardings | SE does not ask for Azure AD admin name during kickoff | SE sometimes asks verbally, not captured in notes |
| F3 | B7 — provisioning | Provisioning service fails silently; CSM not notified | Customer never receives credentials email; assumes silence is normal | ~5% of onboardings | No alerting on provisioning failure; DevOps only discovers on ticket | DevOps manual check — inconsistent |
| F4 | Frontstage — SSO wait | No proactive update to customer during IT review period | Customer disengages; assumes onboarding is stalled | Affects all onboardings with >1 week IT delay (~60%) | No process for mid-wait check-in | CSM may reach out ad hoc |
| F5 | B8 — handoff | SE marks Jira done; CSM not notified in time; credentials email delayed | Customer follows up to ask where their account is | ~15% of onboardings | Jira → CSM notification not automated; reliant on SE pinging CSM in Slack | None |

---

### Recommendations (prioritised by customer impact)

| Priority | Failure point | Recommendation | Impact | Effort | Owner |
|---|---|---|---|---|---|
| 1 | F2 | Add "Azure AD admin name and email" as a required field in the kickoff agenda template; SE cannot close the kickoff Jira task without it | Eliminates the most common blocker to onboarding completion | S | SE team lead |
| 2 | F4 | Build a mid-wait check-in sequence: automated email on Day 3 of IT review silence, CSM alert on Day 7 | Prevents customer disengagement during the longest wait in the journey | M | CS + Marketing Ops |
| 3 | F3 | Add alerting to provisioning service: Slack alert to DevOps + CSM on failure within 5 min | Catches provisioning failures before customer notices | M | DevOps |
| 4 | F5 | Automate Jira → Slack CSM notification on "SSO validated" status change | Removes manual Slack ping dependency; eliminates credentials delay | S | Engineering Ops |
| 5 | F1 | Add CRM validation: block deal close if CSM field is empty; trigger Slack alert to CS lead if CSM not assigned within 4h of close | Ensures every enterprise deal gets a named CSM before customer is contacted | S | Sales Ops |

---

**Service:** Enterprise Customer Onboarding
**Journey:** Contract signed → first dashboard viewed by 5+ named users
**Failure points identified:** 5
**Last updated:** 2026-04-30

---

## Criteria results

### Criteria (skill definition)

- [x] PASS: Skill requires a scope definition with a concrete start event and end outcome before mapping begins — Step 1 is mandatory and the scope table has explicit Start point and End point fields with example concrete triggers
- [x] PASS: Skill maps all four required lanes: customer actions, frontstage employee actions, backstage employee actions, and support processes — Steps 2, 3, 5, and 6 each map one lane and are all marked mandatory
- [x] PASS: Skill explicitly draws the line of visibility separating what customers see from what they don't — Step 4 is a dedicated mandatory step with a visual separator and audit table
- [x] PASS: Skill includes a visibility audit — identifying what backstage work becomes visible to customers and whether that's intentional — Step 4 includes the visibility audit table and explicitly calls out "visibility breaches" with a rule to decide if intentional or accidental
- [x] PASS: Skill requires failure point analysis with location, failure mode, customer impact, frequency, and root cause — Step 7 table has columns for all five, plus current mitigation
- [x] PASS: Skill requires each backstage action to have a trigger — no orphaned process steps — backstage rules state "Every backstage action must be triggered by something... No orphaned steps" and the table has a "Triggered by" column
- [~] PARTIAL: Skill requires duration estimates for backstage actions — duration is a required column in the backstage action table in Step 5, fully required per step; criterion is PARTIAL-prefixed so 0.5 credit applied even though the skill fully satisfies it
- [x] PASS: Skill produces prioritised improvement recommendations linked to specific failure points — Step 8 table links recommendations to failure point numbers (F#) and is explicitly prioritised by customer impact
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — frontmatter present with all three required fields

### Output expectations

- [x] PASS: Output's scope explicitly defines start and end — scope table has Start point and End point rows with concrete triggers ("contract signature webhook fires" / "first dashboard viewed by 5+ named users")
- [x] PASS: Output's blueprint has all four lanes — Customer Actions, Frontstage Employee Actions, Backstage Employee Actions, and Support Processes are all present as separate sections
- [x] PASS: Output draws the line of visibility explicitly — the literal `LINE OF VISIBILITY` separator appears between frontstage and backstage sections in the output
- [x] PASS: Output's visibility audit identifies leaky abstractions — two visibility breaches called out (SE forwarding Jira link, CSM CCing customer on Slack export) with intentional/accidental determination
- [x] PASS: Output's failure point analysis lists concrete failure modes — F2 maps directly to "Azure AD admin not identified at kickoff; customer blocked; 30% frequency; root cause: SE doesn't ask in kickoff" as expected
- [x] PASS: Output's backstage actions each have a trigger — every row in the backstage table has a "Triggered by" entry; no orphaned steps
- [x] PASS: Output's improvements are tied to specific failure points — every recommendation references an F# and specifies a concrete action (e.g. "add Azure AD admin name as a required field in the kickoff agenda template")
- [x] PASS: Output covers the three named teams — CS (CSM), Solutions Engineering (SE), and Support/DevOps each have named ownership on backstage actions; no ambiguity about who does what
- [ ] FAIL: Output's customer-action lane includes thinking/feeling/pain at each stage — the customer action lane (Step 2) captures only action, touchpoint, and channel; no emotional or cognitive dimension is defined in the skill, so the simulated output cannot include it; the skill references `/ux-researcher:journey-map` for the customer-facing layer but does not pull emotional dimensions into the blueprint's customer lane
- [~] PARTIAL: Output addresses duration estimates per backstage action — duration is a required column in the backstage table; all nine backstage steps include a duration estimate; criterion is PARTIAL-prefixed so 0.5 credit applied

## Notes

The only genuine gap is the emotional and cognitive dimension on the customer action lane. Step 2 defines columns for action, touchpoint, and channel only. Enterprise onboarding is emotionally loaded — customers often feel exposed (they've just spent budget), anxious about IT timelines, and frustrated by silence during the SSO wait period. None of that is elicited by the current customer action lane template. The skill references `/ux-researcher:journey-map` as a related skill for "the customer-facing layer" but does not instruct the agent to blend emotional data from the journey map into the blueprint lane. This is a meaningful gap for the enterprise onboarding scenario, where emotional state drives churn risk as much as functional completion does.

Duration in Step 5 is fully required per step, not merely noted as important. The PARTIAL scores on both duration criteria reflect the test criterion type (PARTIAL-prefixed), not a weakness in the skill definition.

The visibility breach framing in Step 4 — requiring a decision on whether each breach is intentional or accidental — is above average. Most service blueprint frameworks treat the line of visibility as a static separator; this skill treats crossings as active process decisions.

The single-points-of-failure identification under support processes is not explicitly required by the skill but emerges naturally from the mapping rules. The simulated output added it; whether the skill would consistently prompt for it depends on agent interpretation.
