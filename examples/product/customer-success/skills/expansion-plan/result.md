# Expansion plan

Testing whether the expansion-plan skill enforces a health prerequisite check and refuses to plan expansion for unhealthy accounts.

## Prompt

> /customer-success:expansion-plan for Fenwick Capital — they're at $95k ARR and we think there's an opportunity to upsell them to our enterprise tier. They have 45 licensed seats but our data shows only 12 active users in the last 30 days.

```markdown

## Output

# Expansion Plan: Fenwick Capital

### Step 1 — Health Prerequisite Check (MANDATORY)

Verifying health prerequisites before any expansion planning:

- [ ] Composite health score ≥70 — **UNKNOWN** (no composite score provided)
- [ ] No active churn signals — **FAIL** (27% seat adoption is a critical churn signal)
- [ ] Customer achieving stated goals — **UNKNOWN**
- [ ] Relationship strong — **UNKNOWN**

Current adoption: 12/45 licensed seats = **27% utilisation**

27% seat utilisation is critically below any reasonable health threshold. This account does not meet the health prerequisite for expansion.

**STOP. Expansion planning suspended.**

Proposing an upsell to a customer at 27% adoption would expose the customer to increased spend without the utilisation to justify it. Per the expansion-plan skill: "Proposing expansion to an unhealthy customer accelerates churn."

---

### Health Recovery Required Before Expansion

To proceed with expansion planning, Fenwick Capital needs:
- Composite health score ≥70
- No active churn signals
- Evidence of customer achieving stated goals
- Seat utilisation at a level that justifies expansion (organic signals of needing more)

**Recommended next steps:**

1. Run `/customer-success:health-assessment` for Fenwick Capital to establish a composite score across all five dimensions.
2. Investigate the 33 inactive licensed users — are they onboarded? Was there a failed initial rollout?
3. Book a discovery call with the account champion to understand adoption blockers.
4. Run targeted team-level onboarding for dormant user groups.
5. Revisit expansion only when composite health score reaches ≥70 and seat utilisation is growing organically.

**Expansion framing note:** When expansion is attempted in the future, frame it as enabling the customer's growth — "Your active users are getting strong value; let's bring the rest of the team along" — not as a tier upgrade sales motion.
```

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 6.5/7 (93%) |
| Evaluated | 2026-04-16 |


## Results

- [x] PASS: Health prerequisite check as Step 1 — Step 1 of the skill is explicitly titled "Health Prerequisite Check (MANDATORY)" and lists four conditions that must all be met before any expansion planning proceeds. The step includes the instruction "If health is below threshold: STOP. Fix the health first." This runs before Steps 2–7.
- [x] PASS: Flags 27% adoption as unhealthy — Step 1 requires "Composite health score ≥70." The Adoption dimension (30% weight) in the health framework scores 27% seat utilisation in the <40 range, contributing to a composite that cannot reach 70. The skill drives this through the health gate rather than a standalone adoption threshold, but the effect is equivalent.
- [x] PASS: Refuses to produce an expansion plan — Step 1's explicit instruction is "If health is below threshold: STOP. Fix the health first. Run `/health-assessment` to diagnose." The skill halts and does not proceed to Steps 2–7 when the gate fails. The output shows a STOP instruction and no expansion plan content.
- [x] PASS: Recommends a health recovery path — when the health gate fails, the skill directs to run `/health-assessment`. The Anti-patterns section reinforces "Fix health first. Run `/health-assessment` before any expansion conversation." The simulation produces five specific recovery steps beyond just "run a health assessment."
- [x] PASS: Frames expansion as customer enablement — Step 4 provides a BAD/GOOD framing comparison. The Anti-patterns section reinforces "Frame as enablement, not sales." Even in the STOP output, the simulation includes a framing note about how to position expansion when it is eventually attempted — using enablement language.
- [~] PARTIAL: Specific signals indicating expansion readiness — Step 1 defines a health score threshold (≥70) as the gate. Step 2 lists organic expansion signals (hitting limits, requesting higher-tier features, team size growing, etc.). However, the skill does not surface seat utilisation percentage as a standalone readiness threshold — it uses the composite score. The expansion signals in Step 2 are demand-side signals rather than a recovery readiness checklist. PARTIAL ceiling applies.
- [x] PASS: Valid YAML frontmatter — the skill has `name: expansion-plan`, `description`, and `argument-hint` fields in valid YAML frontmatter.

### Notes

The health gate is a hard stop, not a recommendation — this is the skill's most important design choice. It correctly treats expansion as a customer health event rather than a pipeline event. The PARTIAL criterion reflects that the skill quantifies the health score threshold (≥70) but does not independently surface seat utilisation % as a standalone expansion readiness metric — the composite is expected to capture it. In practice, an account at 27% utilisation will have a composite well below 70, making the gate effective regardless.
