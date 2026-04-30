# Result: Ticket handling

| Field | Value |
|---|---|
| **Verdict** | PARTIAL |
| **Score** | 16/17.5 criteria met (91%) |
| **Evaluated** | 2026-04-30 |

## Scenario

A support agent receives a ticket about a data export timing out. The customer (Marcus) needs data for an upcoming board meeting. The dataset is 180,000 records and the export is failing with a timeout. The agent must classify, investigate, and respond appropriately under time pressure.

Note: the test prompt is structurally incomplete — the ticket body is absent (the prompt ends at "New ticket just came in:"). Evaluation relies on the scenario described in the test header and the criteria themselves, which supply the specifics (Marcus, 180,000 records, board deadline).

## Output

The following is the simulated output a well-formed support agent response would produce for this scenario, given the agent definition.

---

### Ticket classification

| Field | Value |
|---|---|
| **Ticket ID** | SUP-4821 |
| **Customer** | Marcus Chen |
| **Category** | Bug / Performance issue — data export timeout |
| **Severity** | High — major feature broken, time-bound business impact (board meeting tomorrow) |
| **Routing** | Engineering escalation — 180K record dataset likely exceeds export timeout threshold |
| **Workaround** | Yes — date-range slice exports (see below) |
| **Pattern** | Unknown — check ticket queue for "export timeout" / "export failed" in last 30-60 days |

---

### Customer-facing reply

> Hi Marcus,
>
> I can see how stressful this is — a board meeting tomorrow and your export failing is about the worst timing possible. I'm treating this as high priority and working on it right now.
>
> **What I think is happening:** Your dataset is around 180,000 records, which can push up against our export timeout window. This is a likely cause, not a confirmed one yet — I'm escalating to engineering to check the export logs and confirm.
>
> **What you can do right now to unblock yourself:**
>
> The fastest path to getting your data before the meeting is to split the export into smaller date ranges. For example:
>
> 1. Export January – March first.
> 2. Then April – June, July – September, October – December.
> 3. Combine the four files in Excel or Sheets.
>
> Each slice should be well under the threshold that's causing the issue. This workaround gets you the same data — just in a few passes rather than one.
>
> If date-range filtering isn't available for your export type, let me know and I'll check whether we can queue an async export that runs in the background without hitting the interactive timeout.
>
> **What happens next:** I've flagged this to our engineering team with your account details and a target to respond within 2 hours. I'll send you an update by [time — 2 hours from now] with what we find, even if it's still in progress. Once we've confirmed the root cause I'll follow up with a permanent fix timeline.
>
> You've got a board meeting to get ready for — please use the workaround above now and I'll keep you posted.
>
> Cheers,
> [Support agent name]

---

### Internal escalation note (to engineering)

**Bug report: Export timeout on large dataset — High severity**

**Title:** Data export fails silently on 180,000+ record queries — timeout not surfaced to user

**Severity:** High — time-bound business impact, customer has board meeting tomorrow

**Steps to reproduce:**
1. Log in as user_id [Marcus's user_id — check account]
2. Navigate to Data Export
3. Select full dataset (approx. 180,000 records), no date filter
4. Initiate export
5. Observe: export hangs or returns generic failure; no timeout error surfaced to customer

**Expected:** Export succeeds or returns a clear "dataset too large — try a smaller range" error with guidance

**Actual:** Export silently fails or times out with no actionable message

**Investigation steps:**
1. Check export timeout config — what is the current threshold (rows or seconds)?
2. Query the export job table for Marcus's account — look for failed runs with a timeout error code in the last 48 hours
3. Check recent error logs for this user_id — is the failure a timeout, a query plan issue, or something else?
4. Check whether async/queued export is available and whether it bypasses the timeout

**Customer impact:** One confirmed customer affected. Board meeting deadline creates same-day urgency. Workaround (date-range slicing) provided, but customer should not need to do this.

**Frequency:** Unknown — run pattern check below before responding to Marcus with a timeline.

**Target response:** Within 2 hours given board meeting context.

---

### Pattern detection check

Search the ticket queue for:
- "export timeout", "export failed", "export not working", "download failed"
- Filter: last 30-60 days

If 3+ tickets on the same issue are found: this is a pattern, not an incident. Escalate to product-owner with frequency data. File a known issue. Consider adding a temporary notice to the export UI while engineering investigates.

If Marcus is the first report: treat as isolated, monitor over the next week for recurrence.

---

### Follow-up trigger

Once engineering confirms root cause — send Marcus a follow-up regardless of whether he asks. This is a high-stakes interaction. Closing the loop here converts a frustrated user into one who trusts the support process.

If pattern detection confirms recurrence: recommend creating a KB article titled "How to export large datasets" covering the date-range slicing workaround and noting the row-count threshold once confirmed.

---

## Results

### Criteria

- [x] PASS: Leads with empathy first — the Communication Principles section mandates the order explicitly: "Empathy first, solution second. 'I can see why that's frustrating' before 'Here's how to fix it'." The board deadline makes urgency recognition mandatory under "One contact resolution: If escalating, tell the customer what happens next and when."

- [x] PASS: Classifies across all dimensions — the Ticket Triage section states classification is "MANDATORY for every ticket" and lists five required fields: Category, Severity, Routing, Workaround, and Pattern. The Severity table places "major feature broken" at High with a same-business-day response target, which fits an export failure with a named time constraint.

- [x] PASS: Root cause as hypothesis — Communication Principles include "Be honest about timelines." The Decision Checkpoints table blocks "Promising a fix timeline to a customer" without engineering input. These constraints prevent presenting an unconfirmed diagnosis as fact.

- [x] PASS: Immediate workaround provided — the Classification table requires "Workaround: Known workaround? Include it." This is a mandatory field. Date-range slicing is the natural workaround for a large-dataset timeout.

- [x] PASS: Customer response empathetic, concrete, no internal uncertainty — three Communication Principles converge: empathy-first ordering, "One contact resolution," and the Decision Checkpoint blocking "Sharing internal technical details with a customer."

- [~] PARTIAL: Flags for pattern detection — the Pattern Detection section requires escalation when "3+ tickets on the same issue within a week" and the mandatory Classification table includes a Pattern field. The mechanism exists and is required. However, the criterion asks whether this also warrants a bug report or known issue designation — that outcome depends on ticket history not present in this test. 0.5 points.

- [x] PASS: Internal next steps with owners — the Escalation Rules specify who receives bug escalations (engineering), under what conditions, and in what format. The Bug Report Format requires structured fields including Customer impact and Frequency. The Collaboration table defines engineering, QA, and Customer Success roles with explicit handoff patterns.

### Output expectations

- [x] PASS: Customer-facing reply opens with empathy naming the board meeting deadline — the simulated output opens with "a board meeting tomorrow and your export failing is about the worst timing possible."

- [x] PASS: Reply provides at least one immediate workaround — date-range slicing described with numbered steps, with async export as a second path if the first is unavailable.

- [x] PASS: Classification labels the ticket consistently across category (data export / performance issue), severity (high — time-bound business impact), and routing (engineering escalation given 180K records).

- [x] PASS: Root-cause hypothesis names "180,000 records pushing against our export timeout window" but is framed explicitly as "a likely cause, not a confirmed one yet."

- [x] PASS: Reply does not expose internal uncertainty or technical-debt admissions — language stays confident and customer-facing while acknowledging the issue is real.

- [x] PASS: Internal escalation note names engineering as the owner, lists specific investigation steps (export timeout config, export job table, error logs, async export availability), and sets a 2-hour target given urgency.

- [x] PASS: Output flags for pattern detection with specific search terms ("export timeout", "export failed") and a 30-60 day window, with explicit instructions for what to do if pattern is confirmed vs. isolated.

- [x] PASS: Customer reply includes a time anchor — "I'll send you an update by [time — 2 hours from now]" with explicit commitment to update even if still in progress.

- [x] PASS: Output addresses follow-up communication proactively — explicit "close the loop" trigger once root cause is confirmed, independent of whether Marcus asks.

- [~] PARTIAL: Output recommends creating a KB article conditional on pattern detection confirming recurrence — the definition states "Every resolved ticket is a KB candidate" and the KB trigger includes "the question is likely to recur." The conditional framing is correct given the scenario, but full credit would require an unconditional KB recommendation. 0.5 points.

## Notes

The missing ticket body is a test authoring issue, not an agent definition issue. The criteria supply enough specifics (Marcus, 180,000 records, board deadline) for a complete evaluation.

Both PARTIAL scores are structural: they depend on ticket history not available in an isolated test. The definition's mechanisms are sound — pattern detection is mandatory, KB creation is triggered by recurrence — but full-pass conditions require data the agent cannot have here.

The definition is strong. The Decision Checkpoints table is unusually precise about what requires a pause, which matters for a time-pressured scenario. The mandatory classification fields leave no optional gaps in triage output. The Communication Principles are unambiguous about ordering.
