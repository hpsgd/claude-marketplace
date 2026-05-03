# Ticket Handling

Scenario: A support agent receives a ticket about a data export timing out, and needs to classify, investigate, and respond appropriately.

## Prompt

> Triage and respond to this support ticket. Do not ask for clarification — the ticket contains enough information to classify it, form a root-cause hypothesis, draft a customer-facing reply, and specify internal escalation steps. Complete all of those steps now.
> 
> New ticket just came in:
> 
> **From:** marcus.chen@acme-corp.com
> **Subject:** URGENT: Data export keeps failing — board meeting tomorrow at 9am
> 
> Hi,
> 
> Our bulk customer record export has been timing out since this morning and I'm running out of time. We have about 180,000 records and every time I start the export it runs for a minute or two then fails with "Export failed. Please try again." No error code, nothing useful.
> 
> I've tried four times now with the same result.
> 
> Why this is urgent: I'm presenting our quarterly customer growth data to the board tomorrow at 9am. This export is the centrepiece of the whole presentation. Without it I'm standing up there with nothing.
> 
> Is there anything I can do right now to get this data, or a workaround while you fix the root cause? I genuinely don't know what else to try.
> 
> Marcus Chen
> Head of Operations, Acme Corp — Account #ACM-7842

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

## Ticket Triage

**Severity:** 🔴 **CRITICAL** — Business-impacting, time-bounded deadline (12 hours)  
**Category:** Data export / bulk operations  
**Customer Value:** High (Account #ACM-7842, Head of Operations)  
**Root Cause Hypothesis:** Database or export service query timeout (1-2min failure pattern) triggered by 180k record volume  

---

## Root-Cause Analysis

The consistent 1-2 minute failure window across 4 attempts suggests:
1. **Primary:** Export query exceeding database timeout (most likely)
2. **Secondary:** Resource contention (memory/CPU spike) in export service
3. **Tertiary:** Network timeout during streaming response

Generic error message indicates failure is caught at application layer, not data validation.

---

## Customer-Facing Response

**Subject:** RE: URGENT: Data export — immediate workarounds + active investigation

Hi Marcus,

I understand the pressure — board meetings wait for no one. Here's what we can do right now:

**Immediate workarounds (try these in order):**

1. **Export in batches** — Export 50k records at a time (by date range or customer segment) and combine the CSVs offline. This bypasses the timeout by reducing per-request load.

2. **Filtered export** — If you don't need all columns, disable optional fields (metadata, audit logs, etc.) to reduce payload size.

3. **Direct access** — If your team has database credentials, we can provide a SQL query to extract the data directly from the warehouse — this often completes in seconds.

4. **Staged delivery** — Export to S3/cloud storage in smaller chunks and download the files individually (faster than the UI).

**What we're doing right now:**
- I've escalated this to our platform team as P1 (priority tier 1)
- They're investigating your account's export logs and database performance
- We'll have a root cause identified within the next 2 hours
- If the above workarounds don't work, we'll have a permanent fix ready before your 9am meeting

**Next step from you:** Try the batch export approach while we investigate. If that works, you have your data for tomorrow. If it doesn't, reply immediately with which method you attempted — that data helps us debug faster.

You've got this. I'll follow up within 2 hours with either a fix or confirmation that the workaround is stable for your meeting.

—  
Claude Code Support

---

## Internal Escalation

**To:** Platform/Backend Team Lead  
**Priority:** P1 — Revenue-impacting, board-level deadline  
**SLA:** Root cause + fix within 4 hours (9am customer deadline)

**Investigation checklist:**
- [ ] Export service logs (past 4 hours) — search for timeout errors on Account #ACM-7842
- [ ] Database query performance for 180k-record export — check query plan, execution time
- [ ] Resource monitoring — CPU/memory/disk during export windows; check if spike occurred ~morning
- [ ] Timeout configuration — verify export/database timeouts haven't been reduced in recent deploy
- [ ] Data anomaly — scan customer's 180k records for corrupted/oversized rows that could trigger early failure
- [ ] Version/deploy correlation — any service deployments in the last 24 hours?

**Possible fixes (in order of likelihood):**
1. Increase export query timeout (temporary + permanent config fix)
2. Optimize export query (pagination, indexing, column selection)
3. Add memory/resource pooling to export service
4. Batch processing on backend (stream results in chunks instead of all-at-once)

**Customer escalation path:** If root cause isn't found in 2 hours, assign on-call engineer to call Marcus directly at time of next attempt.

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 14.5/16.0 (91%) |
| Evaluated | 2026-05-02 |
| Target duration | 17775 ms |
| Target cost | $0.0212 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Leads with empathy and acknowledgment of urgency before any technical content — the board report deadline is recognised, not ignored | PASS | Customer reply opens with 'I understand the pressure — board meetings wait for no one.' The board meeting is explicitly named in the immediate response section, and the reply prioritises workarounds before any technical explanation. |
| c2 | Classifies the ticket across all dimensions: category (bug/data/performance), severity (high — time-sensitive business impact), and routing (likely escalation to engineering given dataset size) | PASS | Triage section labels Category: 'Data export / bulk operations', Severity: 'CRITICAL — Business-impacting, time-bounded deadline (12 hours)', and routing is covered by 'I've escalated this to our platform team as P1' and Internal Escalation to 'Platform/Backend Team Lead'. |
| c3 | Identifies the likely root cause (180,000 records likely exceeding export timeout threshold) as a hypothesis, not a definitive answer | PASS | Root-Cause Analysis section states 'The consistent 1-2 minute failure window across 4 attempts suggests:' (hypothesis framing), with Primary: 'Export query exceeding database timeout (most likely)' — framed as likelihood, not certainty. 180k record volume is cited in the triage header. |
| c4 | Provides an immediate workaround or interim path — e.g. date range slicing, filtered export, async export if available — so Marcus can get data before the board meeting | PASS | Four immediate workarounds listed: batch export by 50k records (date range or customer segment), filtered export (disable optional columns), direct database access via SQL query, and staged delivery to S3/cloud storage in smaller chunks. |
| c5 | Drafts a customer-facing response that is empathetic, concrete, and does not expose internal technical uncertainty | PASS | Customer reply is empathetic ('board meetings wait for no one'), concrete (numbered steps with specific record counts), and uses confident language: 'I've escalated this to our platform team as P1' and 'They're investigating' — no technical-debt admissions or internal uncertainty exposed. |
| c6 | Flags this ticket for pattern detection — if other customers have hit export timeouts with large datasets, this warrants a bug report or known issue — partial credit if escalation is recommended but pattern check is not mentioned | PARTIAL | Escalation IS recommended (P1 to Platform/Backend Team Lead with full checklist) but the output contains no mention of searching for similar tickets from other customers or checking for a broader pattern of export timeouts. The escalation checklist does not include 'review ticket history for similar issues'. |
| c7 | Specifies next internal steps with owners — who investigates, what they check, by when given the urgency | PASS | Internal Escalation section names 'Platform/Backend Team Lead' as owner, lists a 6-item investigation checklist (export logs, DB query performance, resource monitoring, timeout config, data anomaly scan, recent deploys), and sets SLA: 'Root cause + fix within 4 hours (9am customer deadline)'. |
| c8 | Output's customer-facing reply opens with empathy and explicit acknowledgment of the urgency — naming the board meeting deadline, not generic 'we understand this is important' | PASS | 'I understand the pressure — board meetings wait for no one.' directly names the board meeting, not a generic acknowledgment. The urgency is also reinforced by 'we'll have a permanent fix ready before your 9am meeting'. |
| c9 | Output's reply provides at least one immediate workaround — date-range slicing the export, filtered subset export, async/queued export if available — so Marcus has a path to get the data BEFORE the board meeting | PASS | Four workarounds provided, including 'Export in batches — Export 50k records at a time (by date range or customer segment)' and 'Filtered export — If you don't need all columns, disable optional fields.' Both directly address getting data before the meeting. |
| c10 | Output's classification labels the ticket consistently — category (data export / performance issue), severity (high — time-bound business impact), routing (engineering escalation given dataset size of 180K records) | PASS | Triage: Category 'Data export / bulk operations', Severity 'CRITICAL — Business-impacting, time-bounded deadline (12 hours)', routing via Internal Escalation to Platform/Backend Team Lead with '180k record volume' referenced in root-cause analysis. Consistent throughout. |
| c11 | Output's root-cause hypothesis names the specific suspected cause (180,000 records exceeds export timeout window, likely 30-60s) but frames it as a hypothesis to verify, not a definitive answer | PASS | 'Primary: Export query exceeding database timeout (most likely)' with 'consistent 1-2 minute failure window across 4 attempts suggests' framing. 180k records cited in Triage. Framed as hypothesis with 'suggests' and 'most likely' language rather than definitive diagnosis. |
| c12 | Output's reply does NOT expose internal uncertainty or technical-debt admissions — keeps the language confident and customer-facing while acknowledging the issue is real | PASS | Customer reply uses: 'I've escalated this to our platform team as P1', 'They're investigating', 'We'll have a root cause identified within the next 2 hours', 'we'll have a permanent fix ready before your 9am meeting' — confident throughout with no technical-debt admissions or hedging about internal systems. |
| c13 | Output's internal escalation note (separate from the customer reply) names the engineering owner, the specific investigation steps (check export timeout config, recent error logs for this user_id, query the export job table for failed runs), and a target response time given the urgency | PASS | Separate Internal Escalation section names 'Platform/Backend Team Lead', lists 6 specific steps including export service logs (search for timeout errors on Account #ACM-7842), timeout configuration check, version/deploy correlation, and sets SLA: '4 hours (9am customer deadline)'. Customer escalation path also specified. |
| c14 | Output flags this for pattern detection — recommends searching the ticket queue for 'export timeout' or 'export failed' tickets in the last 30-60 days to see if Marcus is the canary or the latest of many | FAIL | No mention anywhere in the output of checking the ticket queue or support history for similar export timeout issues from other customers. The investigation checklist covers technical server-side checks only; no ticket pattern search is recommended. |
| c15 | Output's customer reply includes a commitment with a time anchor — 'we'll have an update for you within 2 hours' or 'the workaround above should unblock you immediately; we're investigating the root cause' — not vague 'we'll get back to you' | PASS | 'We'll have a root cause identified within the next 2 hours' and 'we'll have a permanent fix ready before your 9am meeting' — two concrete time anchors. Final line: 'I'll follow up within 2 hours with either a fix or confirmation that the workaround is stable for your meeting.' |
| c16 | Output addresses follow-up communication — proactive update once root cause is identified, even if Marcus doesn't ask, given the high-stakes context | PASS | 'I'll follow up within 2 hours with either a fix or confirmation that the workaround is stable for your meeting.' Also: 'Customer escalation path: If root cause isn't found in 2 hours, assign on-call engineer to call Marcus directly at time of next attempt.' — proactive outreach explicitly planned. |
| c17 | Output recommends creating a KB article on 'exporting large datasets' if pattern detection confirms repeat occurrence — feeding back into self-service deflection | FAIL | No mention of a KB article, documentation, or self-service deflection anywhere in the output. The output does not recommend any knowledge-base or help-centre follow-up action. |

### Notes

The output is high quality overall, achieving PASS on 14 of 17 criteria. It excels at empathy (c1, c8), completeness of triage (c2, c10), workaround specificity (c4, c9), confident customer-facing language (c5, c12), and internal escalation structure (c7, c13). Two criteria are missed entirely: pattern detection across the ticket queue (c14) and KB article creation as self-service deflection (c17). C6 earns partial credit because escalation is present but the pattern-check angle is absent. These omissions are thematically related — the output is strong on immediate incident response but does not think beyond the current ticket to systemic prevention or knowledge management.
