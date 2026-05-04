# Expansion Plan

Scenario: Testing whether the expansion-plan skill enforces a health prerequisite check and refuses to plan expansion for unhealthy accounts.

## Prompt

> /customer-success:expansion-plan for Fenwick Capital — they're at $95k ARR and we think there's an opportunity to upsell them to our enterprise tier. They have 45 licensed seats but our data shows only 12 active users in the last 30 days.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

# Expansion Plan: Fenwick Capital

## Health Check

- **Seat utilisation:** 12 active users ÷ 45 licensed seats = **26.7%**
- **Health score:** Not formally assessed, but utilisation alone disqualifies expansion
- **Status:** **Unhealthy**
- **Clear to expand:** **No** — expansion hold recommended

---

## Unhealthy-Path Response

**This customer is not ready for expansion.** At 26.7% seat utilisation, Fenwick Capital is severely underutilising their current capacity. Upselling them to an enterprise tier before fixing adoption would increase complexity without proportional value and risks further degrading the relationship.

### Recovery Targets

**Adoption baseline:** Active users must reach **27 (60% of 45 seats) sustained over a 60-day window** before expansion can be reconsidered.

- Target: 27 active users by [date ~90 days from now]
- Measurement window: sustained over 60 days (not a spike)
- Reassessment date: [date ~120 days from now]

### Sequence

1. **Recover** (next 60–90 days) — diagnose why 33 seats are unused and restore adoption
2. **Reassess** (date) — confirm they've reached 27 active users sustained for 60+ days
3. **Plan expansion** — only if health signals align AND they've proven they can adopt what they have

Do not collapse these. Expansion conversation now would be perceived as tone-deaf and risk the relationship.

### Right-Sizing Consideration

**Fenwick Capital is significantly over-licensed.** With only 12 active users, they're paying for 33 unused seats.

**Recommendation:** Before any expansion conversation, consider proposing a **right-sizing conversation**: "We've noticed your team is using about 12 seats actively. Would you like to right-size your license to match your current usage and reinvest that savings into adoption support or advanced features?" 

This protects the relationship by:
- Showing we're aligned with their actual needs, not just revenue
- Reducing their cost while maintaining or improving value
- Creating a foundation of efficient usage before expanding scope

**Do not frame this as a reduction.** Frame it as optimization: "Let's make sure you're only paying for what you use, and let's invest in getting your team fully onboarded so you can expand later from a position of strength."

### Internal Communication (for AE / CS Lead)

**Subject:** Fenwick Capital — Expansion on hold pending adoption recovery

---

Hi [AE name],

Fenwick Capital is currently at $95k ARR with 45 licensed seats, but only 12 active users in the last 30 days (26.7% utilisation). Expanding them to enterprise tier at this stage would compound an adoption problem, not solve a growth opportunity.

**Recommendation:** Pause the enterprise upsell conversation. Instead, propose a 90-day adoption recovery plan:

1. Diagnose why 33 seats are unused — is this a change-management gap, feature awareness gap, or genuine over-licensing?
2. Get them to 27 active users (60% of current seats) sustained over 60 days
3. Consider right-sizing their current license to match actual usage (potential cost savings for them, simplified billing for us)
4. Reassess expansion fit on [date] once adoption is proven

**This approach:**
- Protects the relationship (we're prioritising their success, not our quota)
- Reduces risk of post-expansion churn (they'll actually use what they have)
- Creates the foundation for a sustainable, higher-value expansion later

**Reassessment date:** [date ~120 days from now]

---

### Upstream Feedback

**Flag for AE and CS Lead:** Fenwick Capital shows signs of **initial oversell or handoff misalignment**. 45 licensed seats was positioned at sale, but the customer is only actively using 12 months in.

**Questions to surface:**
- What was the initial customer org size / stated growth plan at sale? Has that changed?
- Was there a CS handoff issue? Did the customer receive onboarding or adoption support?
- Was the seat count driven by the customer's request or by sales expansion assumptions?

**Prevent repeat:** If this pattern appears in other accounts (licensed high, using low), it's a signal to tighten the sales-to-CS handoff. Recommend [you / CS lead] audit a few other accounts for the same pattern — if it's systemic, it's worth a process fix.

---

## Next Steps

**CSM action:** 
1. Schedule a discovery call with Fenwick Capital: "We want to make sure you're getting full value from your current plan before considering upgrades."
2. Run a usage audit: which features are being used by whom? Which 33 seats are dark? Why?
3. Design a 60-day adoption plan to get to 27 active users, or propose right-sizing if the original seat count was a planning error
4. Calendar the reassessment meeting for [date]

**Do not proceed to Step 2 (Expansion Signals) until adoption recovery is complete and reassessed.**

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/16.0 (91%) |
| Evaluated | 2026-05-04 |
| Target duration | 20196 ms |
| Target cost | $0.0887 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill performs a health prerequisite check as the FIRST step — before any expansion planning begins | PASS | The output opens with '## Health Check' as its very first section, computing seat utilisation and issuing a status verdict before any other content appears. |
| c2 | Skill flags that 12/45 active users (27% adoption) indicates an unhealthy account and recommends against expansion | PASS | 'Seat utilisation: 12 active users ÷ 45 licensed seats = 26.7%' ... 'Status: Unhealthy' ... 'Clear to expand: No — expansion hold recommended' |
| c3 | Skill refuses to produce an expansion plan for an unhealthy account — or explicitly labels any output as conditional on health improvement first | PASS | 'This customer is not ready for expansion.' The output produces a recovery plan rather than an expansion plan, and ends with 'Do not proceed to Step 2 (Expansion Signals) until adoption recovery is complete and reassessed.' |
| c4 | Skill recommends a health recovery path before expansion can be attempted — what needs to improve and by how much | PASS | 'Recovery Targets: Active users must reach 27 (60% of 45 seats) sustained over a 60-day window before expansion can be reconsidered.' A three-step sequence (Recover → Reassess → Plan) is also provided. |
| c5 | Skill frames expansion as customer enablement rather than a sales motion — the reason to expand should be that the customer needs more to get more value | PASS | Internal comms section: 'we're prioritising their success, not our quota'. Right-sizing section frames optimization as 'Let's make sure you're only paying for what you use... invest in getting your team fully onboarded so you can expand later from a position of strength.' |
| c6 | Skill identifies what specific signals would indicate the account is ready for expansion — partial credit if health criteria for expansion readiness are mentioned but not quantified | PARTIAL | Quantified adoption threshold is stated ('27 active users (60% of 45 seats) sustained over 60 days') but the criterion ceiling is PARTIAL, capping at 0.5. |
| c7 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is a chat response only. No YAML frontmatter is present or visible in the output; the skill definition file itself is not shown. |
| c8 | Output's FIRST action is a health prerequisite check — not 'let's plan the expansion' first then add caveats; the gate runs before any plan is written | PASS | The output's very first section is '## Health Check', containing the utilisation calculation and the 'Status: Unhealthy / Clear to expand: No' verdict before any other content. |
| c9 | Output computes the adoption rate explicitly — 12 active users / 45 licensed seats = 27% — and flags this as below the healthy threshold (typically 60-70%+ for enterprise expansion readiness) | PASS | '12 active users ÷ 45 licensed seats = 26.7%' with status 'Unhealthy'; the 60% threshold is referenced when setting the recovery target of 27 active users. |
| c10 | Output explicitly REFUSES to produce a normal expansion plan — either declines and recommends a recovery plan first, or labels the expansion plan as conditional ('only valid after adoption returns to >60%') | PASS | 'This customer is not ready for expansion.' No expansion plan is produced; the output is entirely a recovery and recovery-prerequisite plan. 'Do not proceed to Step 2 (Expansion Signals) until adoption recovery is complete and reassessed.' |
| c11 | Output's recovery path lists what needs to improve and quantified targets — e.g. 'active user count needs to reach 27 (60% of 45) over a 60-day window before expansion is safe to discuss' | PASS | 'Active users must reach 27 (60% of 45 seats) sustained over a 60-day window before expansion can be reconsidered.' Matches the criterion example almost verbatim. |
| c12 | Output frames expansion as customer enablement — the right reason to expand is 'the customer needs more capacity / features to extract more value' — NOT 'we have a quota gap' or 'they have budget' | PASS | Entire output avoids revenue/quota framing. Internal comms explicitly states 'we're prioritising their success, not our quota' and frames the pause as protecting the customer relationship. |
| c13 | Output addresses the wasted-spend risk — Fenwick is paying for 33 unused seats; reducing seat count back to 12-15 may be the right call before any expansion conversation | PASS | 'Right-Sizing Consideration: Fenwick Capital is significantly over-licensed. With only 12 active users, they're paying for 33 unused seats.' Recommends proposing a right-sizing conversation before any expansion. |
| c14 | Output names the expansion-readiness signals quantitatively — adoption rate >=60%, active engagement on multiple features, positive health score on relationship and value dimensions, executive buy-in confirmed — not generic 'they should be doing well' | PARTIAL | Adoption rate threshold is quantified (60%, 27 users, 60-day window). However, the output does not address 'active engagement on multiple features', 'positive health score on relationship and value dimensions', or 'executive buy-in confirmed' — the other dimensions listed in the criterion. |
| c15 | Output proposes a sequence — first restore adoption (90 days), then assess expansion fit (review post-recovery), then build a plan if signals align — rather than collapsing all three into a single recommendation | PASS | Explicit 'Sequence' section: '1. Recover (next 60–90 days) … 2. Reassess (date) … 3. Plan expansion — only if health signals align.' Followed by 'Do not collapse these.' |
| c16 | Output's recommended communication to the AE / sales team explains why expansion is on hold — protecting the customer relationship rather than blocking revenue arbitrarily | PASS | 'Internal Communication (for AE / CS Lead)' section explains: 'Expanding them to enterprise tier at this stage would compound an adoption problem, not solve a growth opportunity' and lists how the approach 'Protects the relationship (we're prioritising their success, not our quota)'. |
| c17 | Output flags the underlying issue — Fenwick was sold 45 seats but only used 12 — as a symptom of a sales/CS handoff or scoping problem worth feeding back upstream | PARTIAL | 'Upstream Feedback' section: 'Fenwick Capital shows signs of initial oversell or handoff misalignment. 45 licensed seats was positioned at sale, but the customer is only actively using 12 months in.' Asks whether a CS handoff issue occurred and recommends auditing other accounts for the same pattern. |

### Notes

The output is strong across nearly all criteria. The health gate fires first, the adoption rate is computed explicitly, expansion is refused rather than hedged, the recovery path is quantified to the exact threshold the criterion expected, the right-sizing risk is called out, a sequenced three-step plan is provided, and the internal AE communication is framed around relationship protection. The two partial scores reflect: c14 missing multi-dimensional expansion-readiness signals beyond adoption rate (feature engagement, executive buy-in, relationship health score are absent), and c6 which is capped at PARTIAL by the test author. The only outright failure is c7 — the YAML frontmatter of the skill definition itself is not visible in the captured chat output, so it cannot be confirmed. Overall the output is well-structured, customer-centric, and operationally specific.
