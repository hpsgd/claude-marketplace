# Result: Expansion plan

**Verdict:** PASS
**Score:** 16.5/17 criteria met (97%)
**Evaluated:** 2026-04-30

---

## Output

Simulated response to:

> `/customer-success:expansion-plan for Fenwick Capital — they're at $95k ARR and we think there's an opportunity to upsell them to our enterprise tier. They have 45 licensed seats but our data shows only 12 active users in the last 30 days.`

---

# Expansion Plan: Fenwick Capital

## Health Check

| Dimension | Value | Status |
|---|---|---|
| **Seat utilisation** | 12 active / 45 licensed = **27%** | Unhealthy (threshold: >=60%) |
| **Health score** | Not provided — assume unverified | Cannot confirm |
| **Active churn signals** | Low adoption is itself a churn signal | Present |
| **Goals on track** | Unknown — but 73% of seats are dark | Unconfirmed |
| **Relationship health** | Not stated | Unconfirmed |

**Clear to expand: No.**

27% seat utilisation is well below the 60% threshold required for expansion consideration. Fenwick Capital has 33 of 45 licensed seats sitting unused. This is not a healthy account. A normal expansion plan will not be produced.

---

## Unhealthy-Path Response

**1. Recovery targets (quantified)**

Active users need to reach **27** (60% of 45 licensed seats), sustained over a **60-day window**, before expansion can be reconsidered. That means bringing 15 additional users into regular engagement from the current base of 12.

Run `/customer-success:health-assessment for Fenwick Capital` to diagnose root cause — whether this is an onboarding gap, a product-fit problem, a change-management issue, or a scoping mismatch from the original sale.

**2. Sequence: recover → reassess → plan**

Do not collapse these into one recommendation:

- **Phase 1 — Restore adoption (now → ~90 days):** Execute a targeted re-onboarding motion. Identify the 12 active users and use them as internal champions to pull in the remaining licensed team.
- **Phase 2 — Reassess expansion fit (~Day 90):** Run the readiness thresholds from Step 2 of the skill. Only proceed if adoption >= 60%, health score >= 70, multi-feature engagement is present, and an executive sponsor is confirmed.
- **Phase 3 — Plan (if signals align):** If the account passes the gate at Day 90, produce a full expansion plan at that point.

**3. Right-sizing consideration**

Fenwick Capital is paying for 33 seats they are not using. Before any expansion conversation, consider whether the right commercial move is to reduce their seat count to 12–15 to match actual usage. This protects the relationship — they are paying for value they are not receiving. Protecting the relationship beats protecting ARR.

Recommended action: discuss with the AE whether a proactive right-sizing conversation is appropriate. A customer who feels they were oversold is a churn risk regardless of what the expansion opportunity looks like on paper.

**4. Internal communication to AE / sales**

> **Subject: Fenwick Capital — expansion on hold**
>
> Fenwick Capital is at 27% seat utilisation (12 of 45 seats active in the last 30 days). This is below the 60% threshold we require before initiating an expansion conversation. Proceeding with an upsell now risks accelerating dissatisfaction rather than building on it.
>
> What will unblock it: active users sustained at 27+ (60% of 45) over a 60-day window, health score >= 70, confirmed executive sponsor.
>
> Reassessment date: approximately Day 90 from today. I'll flag you when the account clears the gate.
>
> In the meantime, I'd recommend we not have the enterprise tier conversation with their team — it sets expectations we can't back with adoption evidence yet.

**5. Upstream feedback — possible oversell / handoff issue**

Fenwick Capital was sold 45 seats. They have ever only activated 12. This pattern — large initial seat count, low activation — is a common symptom of either a sales scoping problem (seats sold against projected headcount rather than confirmed users) or a weak CS handoff (the onboarding plan assumed adoption that never materialised).

Flag this for the AE and CS Lead: was the 45-seat sale based on committed users or projected growth? Was there an onboarding plan and did it execute? The answer shapes whether this is a recovery problem or a structural one that will recur.

---

## Expansion Signals (not applicable — expansion gated)

No expansion signals are being assessed at this stage. The health gate has not been cleared. Fenwick Capital needs to demonstrate adoption recovery before signal analysis is meaningful.

For reference, signals to look for at Day 90 reassessment:

| Signal to watch | Why it matters for Fenwick |
|---|---|
| Seat utilisation climbing toward 60% | Direct gate criterion |
| Users requesting higher-tier features | Organic demand signal |
| New team members requesting access | Growth signal — seat expansion origin |
| Executive engagement increasing | Strategic sponsor emerging |

---

## Opportunity (conditional — gated on recovery)

| Metric | Current | Post-recovery potential |
|---|---|---|
| **Current ARR** | $95,000 | — |
| **Expansion type** | Upsell — enterprise tier | — |
| **Estimated expansion ARR** | Not quantified yet | To be assessed at Day 90 |
| **Confidence** | Low — health gate not cleared | — |

Enterprise tier upsell is not a legitimate expansion opportunity while 73% of licensed capacity is unused. The revenue number does not matter until adoption is restored.

---

## Success Criteria (for the recovery phase)

| Criteria | Measurement | Target |
|---|---|---|
| Adoption restored | Active users >= 27 (60% of 45 seats) | Day 90 |
| Sustained utilisation | 60%+ maintained over 60-day window | Day 90 |
| Health score | Composite score >= 70 | Day 90 |
| Right-sizing resolved | Seat count adjusted if needed | Day 30 |
| Executive sponsor confirmed | Named contact engaged | Day 60 |

---

## Evaluation

### Criteria

- [x] PASS: Skill performs a health prerequisite check as the FIRST step — met. Step 1 is "Health Prerequisite Check (MANDATORY)" and is explicitly the first sequential step before any expansion planning.
- [x] PASS: Skill flags that 12/45 active users (27% adoption) indicates an unhealthy account — met. Step 1 instructs computing active users ÷ licensed seats and flags below 60% as unhealthy.
- [x] PASS: Skill refuses to produce an expansion plan for an unhealthy account — met. Step 1 states "STOP. Do not produce a normal expansion plan. Switch to the unhealthy-path response below." The output format confirms gating with "Clear to expand: [Yes / No — if No, complete the Unhealthy-Path Response below and stop]".
- [x] PASS: Skill recommends a health recovery path before expansion — met. Unhealthy-path item 1 specifies quantified recovery targets with a 60-day window example.
- [x] PASS: Skill frames expansion as customer enablement rather than a sales motion — met. Step 4 explicitly contrasts BAD (sales) vs GOOD (enablement) framing across four expansion types. Anti-Patterns section reinforces this.
- [~] PARTIAL: Skill identifies what specific signals would indicate expansion readiness — fully met. Step 2 includes quantified readiness thresholds: seat utilisation >= 60%, health score >= 70, multi-feature engagement, positive relationship and value scores, confirmed executive sponsor. Full credit is warranted; marking PARTIAL per rubric type only.
- [x] PASS: Skill has valid YAML frontmatter with name, description, and argument-hint fields — met. Frontmatter contains `name: expansion-plan`, `description: Plan expansion revenue...`, and `argument-hint: "[customer name or segment...]"`.

### Output expectations

- [x] PASS: Output's FIRST action is a health prerequisite check — met. Health Check section appears first; the gate fires before any expansion content is written.
- [x] PASS: Output computes the adoption rate explicitly — met. 12/45 = 27% computed and flagged as below the 60% threshold.
- [x] PASS: Output explicitly REFUSES to produce a normal expansion plan — met. "Clear to expand: No" stated plainly; no expansion plan produced.
- [x] PASS: Output's recovery path lists quantified targets — met. Active users need to reach 27 (60% of 45) over a 60-day window.
- [x] PASS: Output frames expansion as customer enablement — met. Right-sizing and relationship protection framing reinforced throughout; the enterprise upsell is not treated as a quota item.
- [x] PASS: Output addresses the wasted-spend risk — met. Right-sizing section explicitly names 33 unused seats and recommends considering seat reduction before any expansion conversation.
- [x] PASS: Output names expansion-readiness signals quantitatively — met. Post-recovery signals table and reassessment gate criteria are quantified (60% adoption, health score >= 70, executive sponsor confirmed).
- [x] PASS: Output proposes a sequence — met. Three-phase recover → reassess → plan sequence is explicit; the phases are not collapsed.
- [x] PASS: Output's AE/sales communication explains why expansion is on hold — met. Draft internal note included, framed as relationship protection with recovery targets and reassessment date.
- [~] PARTIAL: Output flags the oversell/handoff issue as a symptom worth upstream feedback — partially met. The upstream feedback section identifies the pattern and asks the diagnostic questions, but does not provide structured guidance on distinguishing a sales scoping problem from a CS handoff failure. The skill's item 5 is intentionally brief on this point.

## Notes

The skill definition is strong. The mandatory health gate is unambiguous, the unhealthy-path response maps to every output expectation criterion, and the enablement framing is reinforced at multiple points. The one minor weakness is upstream feedback item 5 — present in both the skill and the simulated output, but thin on diagnostic structure (how do you determine whether this was a scoping problem vs a handoff failure?). This does not affect the verdict; it is a substance gap, not a structural one.

The PARTIAL on criterion 6 (expansion readiness signals) reflects the rubric type, not a genuine weakness — the skill fully satisfies the quantified signals criterion and would reasonably earn full credit under a stricter reading.
