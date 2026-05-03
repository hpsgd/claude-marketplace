# Expansion Plan

Scenario: Testing whether the expansion-plan skill enforces a health prerequisite check and refuses to plan expansion for unhealthy accounts.

## Prompt

> /customer-success:expansion-plan for Fenwick Capital — they're at $95k ARR and we think there's an opportunity to upsell them to our enterprise tier. They have 45 licensed seats but our data shows only 12 active users in the last 30 days.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Running the health prerequisite check before anything else.

**Seat utilisation: 12 ÷ 45 = 26.7% — well below the 60% gate.**

The expansion health check fires. Producing the unhealthy-path response.

---

# Expansion Plan: Fenwick Capital

## Health Check

| Metric | Value | Threshold | Status |
|---|---|---|---|
| **Seat utilisation** | 12 / 45 = **26.7%** | ≥ 60% | **FAIL** |
| **Composite health score** | Unknown — requires `/health-assessment` | ≥ 70 | **Unverified** |
| **Active churn signals** | Ambiguous — 33 idle seats is a latent churn signal | — | **Flag** |

- **Status: Unhealthy**
- **Clear to expand: No**

---

## Unhealthy-Path Response

### Recovery Targets

Active users must reach **27 (60% of 45 licensed seats)**, sustained over a **60-day window**, before expansion can be reconsidered. Sustained means the trailing 30-day active count stays at or above 27 for two consecutive measurement periods — a single spike does not qualify.

Recommended reassessment date: **2026-07-01** (60 days from today, 2026-05-01).

Run `/health-assessment` now to diagnose root cause before any outreach. The utilisation gap could be:
- Onboarding failure — seats provisioned but users never activated
- Champion departure — original sponsor left, adoption collapsed
- Value not landing — product doesn't fit the actual workflow
- External freeze — internal budget/headcount hold (common in financial services)

Each has a different recovery playbook. Don't guess.

---

### Sequence: Recover → Reassess → Plan

**Do not collapse these into one motion.**

1. **Recover (now → 2026-07-01):** Diagnose root cause via health assessment. Execute targeted re-onboarding or re-engagement for the 33 inactive seats. Define a named activation milestone for each idle user cohort.
2. **Reassess (2026-07-01):** Check if utilisation has crossed 60% and held for 30+ days. Recheck composite health score. Only if both gates clear, advance to step 3.
3. **Plan (post-reassessment, if signals align):** Run this expansion plan skill again with current data. Do not plan now.

---

### Right-Sizing Consideration

Fenwick Capital is paying for **45 seats but actively using 12** — 73% of licensed capacity is idle. At $95k ARR, that implies roughly **$2,111/seat/year**. The 33 unused seats represent ~$69.7k in theoretical shelfware.

**If adoption does not recover to 27+ active users by 2026-07-01, the right conversation is a seat reduction, not an expansion.** A reduction from 45 → 15 seats (protecting the 12 active users with a 25% buffer) would bring ARR to approximately $31.7k — a painful near-term revenue hit but far preferable to losing the account entirely at renewal.

Protecting the relationship beats protecting ARR. Flag this scenario for the AE now so it is not a surprise at renewal.

---

### AE / Sales Communication

> **Subject: Fenwick Capital — Expansion on hold, recovery plan in motion**
>
> Fenwick are at $95k ARR / 45 seats with only 12 active users in the last 30 days (26.7% utilisation). We are not in a position to have an expansion conversation right now — doing so would damage trust and accelerate churn risk.
>
> We are pausing expansion and running a health assessment to diagnose the adoption gap. Recovery target: 27+ active users sustained over 60 days. Reassessment date: **1 July 2026**.
>
> If utilisation recovers, we'll revisit the enterprise upsell at that point. If it does not, we will need to discuss right-sizing the contract at renewal to protect the relationship.
>
> **What would unblock expansion:** sustained active utilisation ≥ 60%, confirmed executive sponsor, at least two organic usage signals. None of these are present today.
>
> Will keep you updated after the health assessment.

---

### Upstream Feedback

The sold/used gap (45 seats sold, 12 ever active) warrants a handoff review. Specific questions to surface with the AE and CS lead:

1. **Was the 45-seat count driven by a use-case that materialised?** If seats were sold based on a projected team size or rollout plan that never happened, this is a scoping issue — not a product issue.
2. **Was onboarding completed?** If licences were provisioned without structured onboarding, this pattern will repeat in future accounts.
3. **Did CS receive a clear success plan at handoff?** If the account went straight to "managed" status without a defined activation milestone, the handoff process needs a checkpoint.

Recommend flagging this account as a case study in the next CS / Sales sync — not punitively, but to close the loop on what the expected activation plan was and whether it was ever defined.

---

**Next action:** Run `/health-assessment` for Fenwick Capital to diagnose the adoption root cause before any customer-facing outreach.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/16.0 (94%) |
| Evaluated | 2026-05-01 |
| Target duration | 42312 ms |
| Target cost | $0.0726 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill performs a health prerequisite check as the FIRST step — before any expansion planning begins | PASS | Output opens with 'Running the health prerequisite check before anything else.' and immediately computes seat utilisation before any plan content appears. |
| c2 | Skill flags that 12/45 active users (27% adoption) indicates an unhealthy account and recommends against expansion | PASS | Health check table shows 'Seat utilisation: 12 / 45 = 26.7% — FAIL' against a ≥60% threshold, with Status: Unhealthy and 'Clear to expand: No'. |
| c3 | Skill refuses to produce an expansion plan for an unhealthy account — or explicitly labels any output as conditional on health improvement first | PASS | 'Clear to expand: No' and under the sequence: 'Only if both gates clear, advance to step 3... Do not plan now.' The skill produces a recovery plan, not an expansion plan. |
| c4 | Skill recommends a health recovery path before expansion can be attempted — what needs to improve and by how much | PASS | Recovery Targets section: 'Active users must reach 27 (60% of 45 licensed seats), sustained over a 60-day window, before expansion can be reconsidered. Recommended reassessment date: 2026-07-01.' |
| c5 | Skill frames expansion as customer enablement rather than a sales motion — the reason to expand should be that the customer needs more to get more value | PASS | 'Protecting the relationship beats protecting ARR.' AE communication states 'doing so would damage trust and accelerate churn risk' — the frame is relationship/value protection, not quota attainment. |
| c6 | Skill identifies what specific signals would indicate the account is ready for expansion — partial credit if health criteria for expansion readiness are mentioned but not quantified | PARTIAL | AE communication lists 'sustained active utilisation ≥ 60%, confirmed executive sponsor, at least two organic usage signals.' Health table also lists composite health score ≥70. Quantified signals are present. |
| c7 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output is a chat response only. No YAML frontmatter is present anywhere in the output — the skill file structure cannot be verified from this output. |
| c8 | Output's FIRST action is a health prerequisite check — not 'let's plan the expansion' first then add caveats; the gate runs before any plan is written | PASS | First line: 'Running the health prerequisite check before anything else.' Second line computes the utilisation ratio. The gate fires before any plan section is produced. |
| c9 | Output computes the adoption rate explicitly — 12 active users / 45 licensed seats = 27% — and flags this as below the healthy threshold (typically 60-70%+ for enterprise expansion readiness) | PASS | 'Seat utilisation: 12 ÷ 45 = 26.7%' computed inline and in the health table, compared against a ≥60% threshold marked as FAIL. |
| c10 | Output explicitly REFUSES to produce a normal expansion plan — either declines and recommends a recovery plan first, or labels the expansion plan as conditional ('only valid after adoption returns to >60%') | PASS | 'Clear to expand: No' in the health table. Sequence step 3: 'Run this expansion plan skill again with current data. Do not plan now.' No expansion plan is produced. |
| c11 | Output's recovery path lists what needs to improve and quantified targets — e.g. 'active user count needs to reach 27 (60% of 45) over a 60-day window before expansion is safe to discuss' | PASS | 'Active users must reach 27 (60% of 45 licensed seats), sustained over a 60-day window, before expansion can be reconsidered.' Matches the example criterion almost verbatim. |
| c12 | Output frames expansion as customer enablement — the right reason to expand is 'the customer needs more capacity / features to extract more value' — NOT 'we have a quota gap' or 'they have budget' | PASS | Recovery plan focuses on activation and adoption. 'Protecting the relationship beats protecting ARR.' No mention of quota, pipeline, or budget as reasons to expand. |
| c13 | Output addresses the wasted-spend risk — Fenwick is paying for 33 unused seats; reducing seat count back to 12-15 may be the right call before any expansion conversation | PASS | Right-Sizing Consideration section: 'A reduction from 45 → 15 seats (protecting the 12 active users with a 25% buffer) would bring ARR to approximately $31.7k' and '33 unused seats represent ~$69.7k in theoretical shelfware.' |
| c14 | Output names the expansion-readiness signals quantitatively — adoption rate >=60%, active engagement on multiple features, positive health score on relationship and value dimensions, executive buy-in confirmed — not generic 'they should be doing well' | PASS | AE section: 'sustained active utilisation ≥ 60%, confirmed executive sponsor, at least two organic usage signals.' Health table: composite health score ≥70. Recovery target: 27+ active users. |
| c15 | Output proposes a sequence — first restore adoption (90 days), then assess expansion fit (review post-recovery), then build a plan if signals align — rather than collapsing all three into a single recommendation | PASS | Explicit section 'Sequence: Recover → Reassess → Plan' with three numbered steps and the instruction 'Do not collapse these into one motion.' |
| c16 | Output's recommended communication to the AE / sales team explains why expansion is on hold — protecting the customer relationship rather than blocking revenue arbitrarily | PASS | AE / Sales Communication section explains: 'doing so would damage trust and accelerate churn risk' and 'Protecting the relationship beats protecting ARR' — rationale is customer-relationship-based, not arbitrary. |
| c17 | Output flags the underlying issue — Fenwick was sold 45 seats but only used 12 — as a symptom of a sales/CS handoff or scoping problem worth feeding back upstream | PARTIAL | Upstream Feedback section asks three specific questions: was the 45-seat count driven by a use-case that materialised, was onboarding completed, did CS receive a clear success plan at handoff — framed as a case study for the CS/Sales sync. |

### Notes

The output is exceptionally strong on execution criteria: the health gate fires first, adoption rate is computed explicitly (26.7% vs 60% threshold), expansion is clearly refused, recovery targets are quantified to the exact numbers cited in the rubric (27 users over 60 days), and the three-step sequence is explicit and well-labeled. The right-sizing / seat-reduction risk is addressed with dollar figures. The only criterion the output cannot satisfy is c7 (YAML frontmatter), because the captured output is a chat response — the skill file's metadata structure is invisible. All other gaps are minor: c6 and c17 hit their PARTIAL ceilings as intended.
