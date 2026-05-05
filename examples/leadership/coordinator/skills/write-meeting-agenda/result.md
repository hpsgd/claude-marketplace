# Write Meeting Agenda

Scenario: A user has just had a session-long discussion preparing for a quarterly board meeting and invokes the skill to capture an agenda. The skill must synthesise the discussion into a structured agenda (summary + categorised topics + items), confirm metadata (or infer it from the prompt), derive a slug from the title, and write the file under `docs/meetings/<YYYY-MM-DD>-<slug>/agenda.md`.

## Prompt

> I've just had a long discussion with you about the upcoming quarterly board meeting for Acme Robotics. Here's a recap of what we covered so you can write the agenda:
> 
> **Context:** Quarterly board meeting on 2026-05-15. 90 minutes scheduled. Attendees: CEO (Sam Patel), CFO (Rita Cho), Chair (Jordan Liu), two non-exec directors (Casey Morgan, Devi Iyer). Meeting type: board.
> 
> **What we discussed and want to cover:**
> 
> - Q1 financial results came in 8% ahead of plan on revenue but EBITDA margin compressed by 2.5 points due to one-off rebrand costs and accelerated R&D hiring. The CFO will walk through the bridge.
> - Cash runway extended from 14 to 19 months because of the SAFE round closing in March. Need board acknowledgement of the new runway and the decision to defer the Series B by two quarters.
> - Hiring: 12 of 15 planned engineering hires landed, 0 of 3 GTM hires landed because the head of GTM hasn't started yet. Need a board view on whether to delay the GTM hires until the head of GTM is onboarded or backfill via contractors.
> - Product roadmap shift: customer feedback from the design partner programme has surfaced that the workflow automation feature ranks higher than the analytics dashboard we had prioritised. The CPO wants approval to swap them in the H2 roadmap.
> - A strategic decision to discuss: whether to expand into the EU market in H2 (faster, but stretches the team) or wait until H1 next year (slower, but lets us hire a country lead first). Risk appetite question — board input needed.
> - Standard governance: minutes from last meeting, conflicts of interest, AOB.
> 
> **Open question we landed on:** the GTM hiring decision needs a board steer, not just a recommendation — flag it as a decision item, not a discussion item.
> 
> Please now run:
> 
> /coordinator:write-meeting-agenda "Q2 Board Meeting" --dir docs/meetings

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. Agenda written to:

```
/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1777979682-fafa4ce6/work/docs/meetings/2026-05-15-q2-board-meeting/agenda.md
```

The agenda captures your four main sections with two explicit **DECISION** items flagged (GTM backfill and EU expansion timing), as you specified. Next step: run `/coordinator:write-meeting-qa` to expand this into a Q&A document with talking points and capture space for the CFO's financial bridge, hiring trade-offs, and board steer on both decisions.

### Artifacts written

#### `work/docs/meetings/2026-05-15-q2-board-meeting/agenda.md`

```
---
title: Q2 Board Meeting
date: 2026-05-15
duration_minutes: 90
type: board
attendees:
  - Sam Patel (CEO)
  - Rita Cho (CFO)
  - Jordan Liu (Chair)
  - Casey Morgan (non-exec director)
  - Devi Iyer (non-exec director)
---

# Q2 Board Meeting

## Summary

Review Q1 financial performance and the extended cash runway following the SAFE round close. Address hiring progress and staffing strategy for GTM, approve a customer-driven product roadmap shift, and decide on EU market expansion timing. Standard governance items close the meeting.

## Financial Performance & Cash Position

- Q1 results: 8% revenue outperformance; EBITDA margin compressed 2.5 points (rebrand costs and accelerated R&D hiring)
- Cash runway extended 14 → 19 months post-SAFE round (March close)
- Series B deferred two quarters — board acknowledgement and confidence in extended runway

## Organizational & Hiring

- Engineering hiring: 12 of 15 planned hires landed (80%)
- GTM hiring: 0 of 3 planned hires (head of GTM not yet onboarded)
- **DECISION: GTM backfill strategy — delay remaining GTM hires until head of GTM onboarded, or backfill via contractors in parallel?**

## Product & Strategic Direction

- Customer feedback from design partner programme elevates workflow automation above analytics dashboard in priority
- Approval sought to swap roadmap priorities for H2
- **DECISION: EU market expansion timing — enter H2 2026 (fast, stretches team) or wait until H1 2027 (slower, allows country lead hire first)?**

## Governance

- Minutes from previous meeting
- Conflicts of interest declaration
- Any other business (AOB)

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 15.0/15.0 (100%) |
| Evaluated | 2026-05-05 |
| Target duration | 25644 ms |
| Target cost | $0.0700 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill writes the agenda to a file at `docs/meetings/2026-05-15-q2-board-meeting/agenda.md` (or a path with the same date prefix and a slug derived from "Q2 Board Meeting"). Confirms the absolute path in chat output. | PASS | Chat output confirms: `/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1777979682-fafa4ce6/work/docs/meetings/2026-05-15-q2-board-meeting/agenda.md`. Date prefix matches (2026-05-15) and slug matches (q2-board-meeting). |
| c2 | Agenda frontmatter includes `title`, `date` (2026-05-15), `duration_minutes` (90), `type` (board), and an `attendees` list with all five named attendees. | PASS | Frontmatter has `title: Q2 Board Meeting`, `date: 2026-05-15`, `duration_minutes: 90`, `type: board`, and attendees listing all five: Sam Patel (CEO), Rita Cho (CFO), Jordan Liu (Chair), Casey Morgan (non-exec director), Devi Iyer (non-exec director). |
| c3 | Agenda has a `## Summary` section of 2-3 sentences describing the meeting purpose. Summary references the actual content of the discussion (Q1 results, runway, GTM steer, EU expansion) — not generic board-meeting language. | PASS | The `## Summary` has exactly 3 sentences and references: Q1 financial performance, extended cash runway (SAFE round), hiring/GTM staffing strategy, customer-driven product roadmap shift, and EU market expansion timing — all traceable to the discussion. |
| c4 | Topics are categorised into 2-5 logical groupings using `##` headings — not a flat list of every item. | PASS | Four `##` category sections: `Financial Performance & Cash Position`, `Organizational & Hiring`, `Product & Strategic Direction`, `Governance`. Items are grouped, not listed flat. |
| c5 | Items under topics are concrete and traceable to the discussion (Q1 8% revenue beat, EBITDA margin compression, runway 14→19 months, 12/15 engineering hires, GTM hiring decision, roadmap swap, EU expansion, governance items). | PASS | All eight elements appear: "8% revenue outperformance", "EBITDA margin compressed 2.5 points", "Cash runway extended 14 → 19 months", "12 of 15 planned hires landed", "GTM hiring: 0 of 3 planned hires", "workflow automation above analytics dashboard", "EU market expansion timing — enter H2 2026... or wait until H1 2027", and minutes/conflicts/AOB governance items. |
| c6 | The GTM hiring item is framed as a decision needing board steer, not as a generic discussion item — reflecting the explicit instruction in the prompt. | PASS | Item reads: "**DECISION: GTM backfill strategy — delay remaining GTM hires until head of GTM onboarded, or backfill via contractors in parallel?**" — explicitly bolded as a DECISION item with the two options articulated. |
| c7 | No fabricated content — does not invent attendees, financial figures, or items not present in the discussion. | PASS | Every attendee, figure (8%, 2.5 points, 14→19 months, 12/15, 0/3), and agenda item maps directly to content from the prompt. No invented names, metrics, or topics detected. |
| c8 | Output suggests `/coordinator:write-meeting-qa` as the next step. | PARTIAL | Chat response states: "Next step: run `/coordinator:write-meeting-qa` to expand this into a Q&A document with talking points and capture space for the CFO's financial bridge, hiring trade-offs, and board steer on both decisions." |
| c9 | Slug in folder name matches the rule (lowercase, dashes, no special chars) — e.g. `q2-board-meeting`. | PASS | Folder slug is `q2-board-meeting` — all lowercase, words joined by dashes, no special characters. |
| c10 | Output file's frontmatter has `duration_minutes: 90` and `type: board` exactly — not 60 (default) and not "Discussion". | PASS | Frontmatter shows `duration_minutes: 90` and `type: board` exactly as required. |
| c11 | Output file's `attendees:` list contains all five named individuals from the prompt — Sam Patel (CEO), Rita Cho (CFO), Jordan Liu (Chair), Casey Morgan, Devi Iyer. Roles preserved where given. | PASS | Attendees list: `Sam Patel (CEO)`, `Rita Cho (CFO)`, `Jordan Liu (Chair)`, `Casey Morgan (non-exec director)`, `Devi Iyer (non-exec director)` — all five with roles preserved. |
| c12 | Output file has at least one category covering Financials/Performance (Q1 results, EBITDA, runway), one covering People (hiring), one covering Product/Strategy (roadmap swap, EU expansion), and a Governance category. Categories may be named differently but must cover these themes. | PASS | `Financial Performance & Cash Position` covers Q1 results, EBITDA, runway. `Organizational & Hiring` covers hiring. `Product & Strategic Direction` covers roadmap swap and EU expansion. `Governance` covers minutes, conflicts, AOB. |
| c13 | Output file's items reproduce the specific facts — 8% revenue beat, 2.5 point EBITDA compression, 14→19 month runway, 12/15 vs 0/3 hires, swap of analytics dashboard with workflow automation, EU H2 vs H1-next-year choice — not abstracted into generic phrasing like "review financial performance". | PASS | All six specific facts appear verbatim or near-verbatim: "8% revenue outperformance", "2.5 points", "14 → 19 months", "12 of 15" and "0 of 3", "workflow automation above analytics dashboard", "H2 2026... or wait until H1 2027". |
| c14 | Output file flags the GTM hiring item with language indicating a decision/steer is required (e.g. "Decision:", "Board steer needed:", "DECIDE:") rather than just listing it as a topic. | PASS | Item is prefixed with bold `**DECISION:**` and presents two explicit options for the board to choose between, clearly framing it as a required decision rather than a discussion. |
| c15 | Output file does NOT include a Q&A section, talking points, or response capture areas — those belong to the sibling skill, not this one. | PASS | The agenda file contains only frontmatter, a Summary section, four categorical `##` sections with bullet items. No Q&A, talking points, or capture fields appear anywhere in the file. |
| c16 | Output file's summary mentions success criteria for the meeting (e.g. board acknowledgement of runway, agreement on GTM approach, roadmap swap approval, EU direction). | PARTIAL | Summary explicitly frames two success criteria: "approve a customer-driven product roadmap shift" and "decide on EU market expansion timing". Board acknowledgement of runway is mentioned in the body ("board acknowledgement and confidence in extended runway") but not in the summary. GTM agreement is not framed as a success criterion in the summary. Partial coverage of the four examples given. |

### Notes

The skill produced a near-perfect agenda. The file path, slug, frontmatter, and all five attendees with roles are exactly correct. All six specific numerical facts from the discussion are reproduced without abstraction. The GTM item is correctly elevated to a DECISION with options presented, honouring the explicit instruction in the prompt. The EU expansion decision is also flagged as a DECISION. Four well-grouped thematic categories with a Governance section close the document. The file contains no Q&A, talking points, or extraneous content. The one minor gap is in c16: the summary foregrounds roadmap approval and EU direction as success criteria but does not explicitly frame board acknowledgement of the runway or the GTM hiring steer as outcomes the meeting must achieve — those appear only in the body. Given the PARTIAL ceiling on c8 and c16, both receive 0.5, yielding a perfect 15/15.
