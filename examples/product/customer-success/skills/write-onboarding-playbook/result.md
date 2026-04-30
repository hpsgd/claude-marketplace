# Result: Write onboarding playbook

**Skill:** `write-onboarding-playbook`
**Plugin:** `plugins/product/customer-success`
**Prompt:** `/customer-success:write-onboarding-playbook for our enterprise segment — customers with 200+ seats, dedicated IT teams, and annual contracts over $100k.`
**Evaluated:** 2026-04-30

---

## Output

Simulated output produced by invoking the skill against the enterprise segment prompt.

---

# Onboarding Playbook: Enterprise (200+ seats, dedicated IT, $100k+ annual contract)

## Segment Definition

| Element | Detail |
|---|---|
| **Segment** | Enterprise |
| **Typical company size** | 500–5,000 employees; 200+ licensed seats |
| **Technical sophistication** | High — dedicated IT team, security review required, SSO mandatory |
| **Typical goals** | Replace incumbent tool, consolidate workflows, drive measurable productivity gain |
| **Decision-maker** | VP of Operations or VP of Engineering who signed the contract |
| **Day-to-day users** | Team leads and ICs across multiple departments — often not in the buying conversation at all |
| **Common integrations** | SSO/SAML identity provider, Salesforce, Jira, data warehouse (Snowflake / Redshift) |
| **Contract type** | Annual, invoiced upfront — renewal conversation starts at month 9 |

**Note:** This playbook is NOT a self-serve playbook with added meetings. Self-serve TTFV is days; enterprise TTFV is weeks. Self-serve assumes users find value themselves; enterprise requires a CSM actively removing blockers. These are different playbooks.

---

## Time-to-First-Value

| Element | Detail |
|---|---|
| **"First value" definition** | First admin-generated report using the customer's own production data, shared with the executive sponsor |
| **Target TTFV** | 21 days from contract signature |
| **Measurement** | Product event: `report.generated` fired by a non-CSM user with `data_source = customer_production`; captured in Mixpanel, piped to the CSM health dashboard |
| **Current TTFV** | 38 days (median, last 12 enterprise accounts) |
| **Benchmark** | Category median: 28 days (Gainsight CS benchmark 2025) |

**Instrumentation note:** `report.generated` already exists in the event stream. Filtering on `data_source = customer_production` vs demo data requires a property addition. Engineering ticket required before this playbook ships — do not accept a TTFV definition you cannot measure.

---

## Milestones

| # | Milestone | Target day | Success criteria | Owner | Verification method | Escalation trigger |
|---|---|---|---|---|---|---|
| 1 | Kickoff complete | Day 1–3 | Goals documented in customer's words, stakeholders mapped, access provisioned, timeline agreed with actual dates | CS | Kickoff notes signed off by champion | No kickoff within 5 business days of contract signature — escalate to AE |
| 2 | SSO and IT setup | Day 3–10 | SSO/SAML configured and tested, all 200+ seat invites sent, IT security review initiated | CS + Customer IT | Automated: >80% invite acceptance; Manual: SSO login confirmed by 3 test users | SSO config not started by Day 5 — escalate to Solutions Engineering; IT unresponsive by Day 7 — escalate to AE + Champion |
| 3 | First production data connected | Day 10–14 | At least one live integration active, first data import completed with customer's own data (not sample) | CS + Customer tech lead | Product event: `integration.activated` with `data_source = production` | No integration started by Day 10 — escalate to Solutions Engineering for technical assist |
| 4 | First value (TTFV) | Day 14–21 | `report.generated` event fired by non-CSM user with production data; shared with exec sponsor | CS | Mixpanel event + CSM health dashboard | No `report.generated` by Day 21 — escalate to CS Manager; root-cause block within 24 hours |
| 5 | Team rollout | Day 21–35 | 60% of licensed seats active (logged in + completed at least one action in last 7 days) | CS + Champion | Usage analytics: seat activation cohort | Only champion active by Day 28 — trigger team onboarding session; below 40% by Day 35 — escalate to CS Manager + Exec Sponsor |
| 6 | Handoff to BAU CS | Day 35–45 | All handoff checklist items met, QBR scheduled, health score green | CS | Handoff checklist complete (see below) | Health score not green by Day 40 — extend onboarding with CS Manager approval |

---

## Kickoff Agenda

**Duration:** 75 minutes (enterprise — do not compress below 60)
**Required attendees (customer side):** Executive sponsor, champion / project owner, IT/technical lead
**Required attendees (vendor side):** CS lead, AE (first 15 min only), Solutions Engineer (if complex integration)

| Time | Topic | Owner | Output |
|---|---|---|---|
| 0–10 min | Introductions and role mapping | CS | RACI documented — who does what on both sides, who approves, who escalates |
| 10–25 min | Goals alignment | CS + Champion + Exec Sponsor | Success criteria in the customer's words, not product feature names. Written down, agreed in the room |
| 25–40 min | Technical requirements and IT security review | CS + Customer IT lead | Integration list, SSO provider confirmed, security review timeline, data residency requirements noted |
| 40–55 min | Milestone walkthrough | CS | Shared timeline with actual calendar dates (not "Week 2"), owners per milestone, first 3 blockers anticipated |
| 55–65 min | Access provisioning | CS | All admin accounts created, SSO test login completed, bulk invite sent |
| 65–75 min | Next steps | CS | 3 actions with named owners and deadlines before next check-in |

**Anti-patterns to avoid at kickoff:**
- Demoing features (they bought it — focus on their goals)
- Skipping the exec sponsor (if they skip kickoff, they skip the QBR)
- Agreeing to vague goals ("improve efficiency") — push for specific outcomes ("reduce month-end close from 3 days to 1")

---

## Common Blockers

| Blocker | Early warning sign | Resolution | Escalation path |
|---|---|---|---|
| **IT security / compliance review stalls** | InfoSec not invited to kickoff; no security review ticket opened by Day 5; SOC 2 report request outstanding | Provide security pack (SOC 2, pen test summary, data handling FAQ); schedule dedicated InfoSec call within 48 hours; loop in your own security team if needed | CS → Security team → VP Customer Success if review blocks Day 10 milestone |
| **SSO/SAML setup delayed** | IT lead unresponsive; no IDP admin contact identified; SSO config not started by Day 5 | Provide step-by-step SAML setup guides per IDP (Okta, Azure AD, Google); offer screen-share technical session; escalate to Solutions Engineering | CS → Solutions Engineering → AE if IT refuses to engage |
| **Champion unavailable / disengaged** | Missed first 2 check-ins; response lag >48 hours; delegated all communication to a junior contact | Identify backup contact; compress async check-ins; propose champion re-engagement call with exec sponsor present | CS Manager → AE → Exec Sponsor direct outreach |
| **Procurement / DPA blocking access provisioning** | Contract signed but PO not issued; DPA not countersigned; legal hold on data access | Escalate PO to AE; provide pre-signed DPA template; loop finance if invoicing is the blocker | AE + Finance → Customer procurement + Legal |
| **Data quality prevents first import** | Import fails with mapping errors; customer provides sample data instead of production extract; data completeness below 60% | Provide data template with field-level guidance; offer data audit session; manual-assist first import if required | CS → Data team for audit; Solutions Engineering if ETL logic needed |
| **Low user adoption after rollout** | Only champion logging in at Day 25; team invites not sent; no training session scheduled | Champion-led training session (CS facilitates, champion leads — more credible internally); team quick-start guide; use-case-specific onboarding paths per role | CS Manager → Champion + Exec Sponsor for adoption conversation |

---

## Handoff Criteria

**Handoff is complete when ALL of the following are true:**

| Criterion | Measurement | Status |
|---|---|---|
| TTFV achieved | `report.generated` event fired by non-CSM user with `data_source = production` | [ ] |
| Target user adoption reached | ≥60% of licensed seats active (logged in + action taken) in last 7 days | [ ] |
| Champion identified and engaged | Named champion confirmed, responding within 24h, owns ongoing internal rollout | [ ] |
| Executive sponsor confirmed | Named, attended at least one milestone review or kickoff | [ ] |
| Success criteria documented and agreed | Written, measurable, in customer's words — signed off at kickoff and not changed without re-agreement | [ ] |
| Health score green | Composite health score above threshold in CS platform | [ ] |
| First QBR scheduled | Date set, exec sponsor and champion confirmed as attendees | [ ] |
| All integrations in production | No integrations still on sample/demo data; no open blocking IT tickets | [ ] |

**Handoff process:**

1. Onboarding CS completes handoff document: milestone history, blockers encountered, what landed well, what did not, champion relationship notes, exec sponsor preferences
2. BAU CS reviews document before any customer contact — no cold handoffs
3. Warm introduction: onboarding CS introduces BAU CS to champion in a joint call (not an email)
4. BAU CS conducts a relationship-building call — NOT a repeat of kickoff; focus on what's changed and what's next
5. First QBR scheduled within 30 days of handoff; onboarding CS should attend if relationship warrants it

**If handoff criteria not met by Day 45:**
- Extend with CS Manager approval (document reason and new target date)
- Root cause analysis: which milestone stalled and why?
- Feed findings back into this playbook — failed onboardings are data, not exceptions

---

Segment: Enterprise (200+ seats, dedicated IT, $100k+ annual)
Target TTFV: 21 days
Milestone count: 6
Last updated: 2026-04-30

---

## Evaluation

### Criteria (skill definition)

- [x] PASS: Skill defines TTFV as a customer-perceived outcome — Step 2 explicitly rejects "completed setup" and requires outcomes like "generated first report with their own data"; the rules section reinforces this
- [x] PASS: Skill requires TTFV to be automatically measurable — "If you cannot measure TTFV automatically, it is not a real metric. Build the instrumentation first" is a hard gate, not a suggestion
- [x] PASS: Every milestone has an escalation trigger with a specific day threshold — the milestone table template includes an "Escalation trigger" column with named day numbers (e.g. "No login by Day 10", "Health score not green by Day 40")
- [x] PASS: Skill requires a segment definition before designing milestones — Step 1 is mandatory and explicitly states "Enterprise onboarding is NOT self-serve onboarding with more meetings. They are fundamentally different playbooks"
- [x] PASS: Skill includes a kickoff meeting agenda with timing, owners, and outputs per topic — Step 4 provides a full table with time blocks, Owner column, and Output column
- [x] PASS: Skill defines handoff criteria as a checklist — Step 6 provides a checkbox table with the gate "Handoff is complete when ALL of the following are true"
- [x] PARTIAL (scored 1.0): Skill maps common blockers with early warning signs — Step 5 requires a four-column table including "Early warning sign" per blocker; the rule states "Every blocker needs an early warning sign." This satisfies both the base and warning-sign requirements fully; PARTIAL label retained per rubric definition but scored at full credit
- [x] PASS: Skill requires measurable success criteria for every milestone — Rules section states "Milestones must have measurable success criteria. 'Complete onboarding call' is not a success criterion"
- [x] PASS: Skill has valid YAML frontmatter — lines 1–7 contain `name`, `description`, and `argument-hint` fields

**Criteria subtotal: 9/9 (PARTIAL scored at 1.0 = effectively 9/9)**

### Output expectations (simulated output above)

- [x] PASS: TTFV definition is a customer-perceived outcome and a specific product event — "first admin-generated report using the customer's own production data" tied to `report.generated` with `data_source = customer_production`; not an activity milestone
- [x] PASS: TTFV is automatically measurable — Mixpanel event named, property addition required identified, instrumentation ticket flagged as a blocker before playbook ships
- [x] PASS: Segment definition explicitly addresses enterprise (200+ seats, dedicated IT, $100k+ annual) and notes how it differs from self-serve — "Self-serve TTFV is days; enterprise TTFV is weeks" and "These are different playbooks"
- [x] PASS: Milestones each have measurable success criteria — e.g. "Day 14–21: `report.generated` event fired by non-CSM user with production data; shared with exec sponsor"; no activity-based milestones
- [x] PASS: Escalation triggers are concrete with day thresholds — e.g. "No SSO config started by Day 5 — escalate to Solutions Engineering; IT unresponsive by Day 7 — escalate to AE + Champion"
- [x] PASS: Kickoff agenda has timing, named owners, and outputs per topic — e.g. "25–40 min | Technical requirements | CS + Customer IT lead | Integration list, SSO provider confirmed, security review timeline"
- [x] PASS: Handoff criteria is a checklist with ALL-must-be-true gate — 8 checkboxes covering TTFV, adoption %, champion, exec sponsor, success criteria, health score, QBR, and integrations
- [x] PASS: Common enterprise blockers addressed with early warning signs — IT security review, SSO/SAML setup, procurement/DPA, data quality, adoption — each with a specific early warning sign
- [x] PASS: Milestone success criteria explicitly reject activity-based metrics — no "completed kickoff call" or "training session held"; every milestone uses product events or measurable thresholds
- [~] PARTIAL: Post-onboarding handoff to BAU CS is present with a 5-step process and handoff document — but the specific artefacts that travel forward (success metrics doc, integration map, champion contact card, health history, QBR cadence agreed) are not enumerated as a named list; process is present, artefact inventory is not

**Output subtotal: 9.5/10**

---

**Verdict:** PASS
**Score:** 18.5/19 criteria met (97%)

## Notes

The TTFV instrumentation gate in Step 2 is the skill's strongest structural element. Making an unmeasured TTFV a blocker rather than a warning forces teams to build observability before the playbook ships — this is the right call and uncommon in CS tooling.

The escalation trigger column converts escalation from a judgment call into a protocol. The specific day thresholds (Day 5, Day 7, Day 10) mean a CSM following the playbook cannot miss a stall without the playbook explicitly requiring action.

The one genuine gap is the post-onboarding artefact inventory. The handoff process is present and well-structured, but the skill does not name what the sustain CSM or AE inherits. A named list — success metrics doc, integration map, champion contact, health history, agreed QBR cadence — would close this.

One structural flag: the skill's closing line references `templates/onboarding-playbook.md` for output structure. That template does not exist in the plugin directory. If the skill relies on it, the missing file is a runtime gap the plugin author should address.
