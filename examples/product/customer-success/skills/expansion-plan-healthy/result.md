# Result: expansion plan for a healthy account

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 14/14 criteria met (100%) |
| **Evaluated** | 2026-04-29 |
| **Skill source** | `plugins/product/customer-success/skills/expansion-plan/SKILL.md` |

## Results

### Criteria section

- [x] PASS: Health prerequisite check passes and expansion planning proceeds — Step 1 is a mandatory gate with an explicit >= 70 threshold and four sub-conditions. Meridian's score (85), no churn signals, goals achieved (40% time savings), and three QBRs of engagement all clear the gate.
- [x] PASS: Expansion is framed as customer enablement, not a sales motion — Step 4 is a dedicated "Frame as Enablement" section with a BAD/GOOD contrast table. Anti-Patterns explicitly prohibit "Sales framing."
- [x] PASS: The specific signal (customer asking about API tier) is used as the expansion anchor — Step 2 maps "Requesting higher-tier features" to Upsell; signal rules require organic, customer-driven signals as the entry point.
- [x] PASS: Revenue impact is estimated with assumptions stated — Step 3 explicitly instructs "Show the math. Don't just give a single ARR figure. Document the pricing assumption, the relevant volume, and at least two adoption scenarios. State each assumption explicitly."
- [x] PASS: A timeline with milestones is produced — Step 6 requires phased milestones (discovery, scoping, trial, rollout, post-rollout review) at week/month granularity rather than generic steps.
- [x] PASS: Risk factors for the expansion are identified — Step 7 is a named deliverable section that explicitly covers API tier risk: "does the customer have engineering capacity to consume it? If not, the tier becomes shelfware. Gate the upsell on confirming technical readiness."
- [x] PASS: The plan references the customer's demonstrated value as proof of readiness — Step 6 Step 1 explicitly instructs "connect demonstrated outcomes to the readiness narrative explicitly: they've already proven X with the current tier, which is why they're ready for Y."

### Output expectations section

- [x] PASS: Output's health prerequisite check passes explicitly citing four signals — Step 1's four conditions map directly to the four signals in the prompt (score 85, no churn, 3 QBRs, customer-initiated inquiry). Output template has an explicit "Clear to expand: Yes/No" field.
- [x] PASS: Output uses customer's API tier request as the expansion anchor — "Requesting higher-tier features" signal type matches; Steps 5 and 6 keep the plan grounded in what the customer asked for, not a pivot to another tier.
- [x] PASS: Output's revenue impact estimate is shown with assumptions and math — Step 3 requires pricing assumption (per-seat, flat, tier delta), volume (seats in scope), and at least two adoption scenarios with each assumption stated.
- [x] PASS: Output's enablement-not-sales framing is visible — Step 4 framing table and Anti-Patterns collectively direct the output to discuss what API integration unlocks for Meridian, not revenue growth.
- [x] PASS: Output's timeline has milestones at week/month granularity — Step 6 names five phases and instructs "weeks for technical work, months for org-wide rollout" explicitly.
- [x] PASS: Output references the 40% time-savings as the readiness signal — Step 6 Step 1 instructs connecting demonstrated outcomes to the readiness narrative, which maps directly to using the QBR-proven time savings as the "ready for more" anchor.
- [x] PASS: Output identifies adoption risks with a technical readiness gate — Step 7 names the API tier / integration risk type and the gating action: confirm engineering capacity before proceeding.

## Notes

The SKILL.md was updated since the previous evaluation (2026-04-24). Two changes are material: Step 3 now includes an explicit "show the math" instruction with pricing assumption, volume, and two adoption scenarios; and Step 6 now requires phased milestones at week/month granularity with named phases. These additions resolve the two deepest failures from the previous run. Step 7 was also added as a named risk section, resolving the partial on risk identification. The skill now satisfies all criteria in the current test.md at full strength.
