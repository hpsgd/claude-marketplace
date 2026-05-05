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

**Agenda written** — 90 minutes allocated across five categories, with both discussion items (financial results, roadmap, expansion) and decision items flagged (GTM hiring approach).

**Path:** `docs/meetings/2026-05-15-q2-board-meeting/agenda.md`

**Next step:** Run `/coordinator:write-meeting-qanda` to expand this into a Q-and-A document with talking points, anticipated questions, and space for note-taking during the meeting. That becomes your printed PDF for use during the board call.

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

Review Q1 financial performance and cash runway implications from the March SAFE round close. Approve decisions on GTM hiring approach, product roadmap prioritisation, and EU market expansion timing. The meeting requires board input on resource constraints, product strategy, and risk appetite.

## Q1 Financial Results & Cash Position (20 min)

- Q1 revenue 8% ahead of plan
- EBITDA margin compression by 2.5 points (one-off rebrand costs, accelerated R&D hiring)
- CFO to walk through the P&L bridge
- Cash runway extended from 14 to 19 months (SAFE round closed March)
- Series B deferral by two quarters — board acknowledgement needed

## Hiring Update & GTM Decision (20 min)

- Engineering: 12 of 15 planned hires landed
- GTM: 0 of 3 planned hires landed (head of GTM not yet onboarded)
- **Decision required**: backfill GTM roles via contractors while waiting for head of GTM to ramp, or defer GTM hires until head of GTM is in place

## Product Roadmap Prioritisation (15 min)

- Design partner programme feedback: workflow automation ranked higher than analytics dashboard
- CPO seeks approval to swap them in H2 roadmap
- Approval needed to execute resequencing

## Strategic Expansion Decision (20 min)

- EU market expansion timing
- Option A: accelerate to H2 (faster entry, stretches team)
- Option B: defer to H1 next year (allows time to hire country lead first)
- Board risk appetite input needed

## Governance (15 min)

- Minutes and actions from last meeting
- Conflicts of interest
- Any other business

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 17.0/17.0 (100%) |
| Evaluated | 2026-05-05 |
| Target duration | 38736 ms |
| Target cost | $0.0785 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill writes the agenda to a file at `docs/meetings/2026-05-15-q2-board-meeting/agenda.md` (or a path with the same date prefix and a slug derived from "Q2 Board Meeting"). Confirms the absolute path in chat output. | PASS | Artifact written to `work/docs/meetings/2026-05-15-q2-board-meeting/agenda.md`. Chat output confirms: "**Path:** `docs/meetings/2026-05-15-q2-board-meeting/agenda.md`". |
| c2 | Agenda frontmatter includes `title`, `date` (2026-05-15), `duration_minutes` (90), `type` (board), and an `attendees` list with all five named attendees. | PASS | Frontmatter contains `title: Q2 Board Meeting`, `date: 2026-05-15`, `duration_minutes: 90`, `type: board`, and all five attendees listed with roles. |
| c3 | Agenda has a `## Summary` section of 2-3 sentences describing the meeting purpose. Summary references the actual content of the discussion (Q1 results, runway, GTM steer, EU expansion) — not generic board-meeting language. | PASS | Three-sentence `## Summary` reads: "Review Q1 financial performance and cash runway implications from the March SAFE round close. Approve decisions on GTM hiring approach, product roadmap prioritisation, and EU market expansion timing. The meeting requires board input on resource constraints, product strategy, and risk appetite." References Q1 results, runway, GTM, EU, and product strategy specifically. |
| c4 | Topics are categorised into 2-5 logical groupings using `##` headings — not a flat list of every item. | PASS | Five `##` category headings: Q1 Financial Results & Cash Position, Hiring Update & GTM Decision, Product Roadmap Prioritisation, Strategic Expansion Decision, Governance. Five groupings is within the 2-5 range. |
| c5 | Items under topics are concrete and traceable to the discussion (Q1 8% revenue beat, EBITDA margin compression, runway 14→19 months, 12/15 engineering hires, GTM hiring decision, roadmap swap, EU expansion, governance items). | PASS | All specifics present: "Q1 revenue 8% ahead of plan", "EBITDA margin compression by 2.5 points", "Cash runway extended from 14 to 19 months", "Engineering: 12 of 15 planned hires landed", "GTM: 0 of 3 planned hires", roadmap swap mentioned, EU H2 vs H1 options, governance items listed. |
| c6 | The GTM hiring item is framed as a decision needing board steer, not as a generic discussion item — reflecting the explicit instruction in the prompt. | PASS | Under "Hiring Update & GTM Decision": "**Decision required**: backfill GTM roles via contractors while waiting for head of GTM to ramp, or defer GTM hires until head of GTM is in place" — bolded decision framing with two concrete options. |
| c7 | No fabricated content — does not invent attendees, financial figures, or items not present in the discussion. | PASS | All five attendees match the prompt exactly. All figures (8%, 2.5 points, 14→19 months, 12/15, 0/3) are sourced directly from the prompt. No invented items. |
| c8 | Output suggests `/coordinator:write-meeting-qanda` as the next step. | PARTIAL | Chat output states: "Run `/coordinator:write-meeting-qanda` to expand this into a Q-and-A document with talking points, anticipated questions, and space for note-taking during the meeting." |
| c9 | Slug in folder name matches the rule (lowercase, dashes, no special chars) — e.g. `q2-board-meeting`. | PASS | Folder slug is `q2-board-meeting` — all lowercase, hyphen-separated, no special characters. |
| c10 | Every category heading includes a per-topic time allocation in `(N min)` form — e.g. `## Financial Performance (25 min)`. The total across categories fits within the 90-minute meeting duration with reasonable buffer. | PASS | All five headings carry time suffixes: (20 min), (20 min), (15 min), (20 min), (15 min). Total = 90 min, exactly at the meeting duration limit. |
| c11 | Output file's frontmatter has `duration_minutes: 90` and `type: board` exactly — not 60 (default) and not "Discussion". | PASS | Frontmatter shows `duration_minutes: 90` and `type: board` exactly as required. |
| c12 | Output file's `attendees:` list contains all five named individuals from the prompt — Sam Patel (CEO), Rita Cho (CFO), Jordan Liu (Chair), Casey Morgan, Devi Iyer. Roles preserved where given. | PASS | Attendees list: "Sam Patel (CEO)", "Rita Cho (CFO)", "Jordan Liu (Chair)", "Casey Morgan (non-exec director)", "Devi Iyer (non-exec director)" — all five with roles preserved. |
| c13 | Output file has at least one category covering Financials/Performance (Q1 results, EBITDA, runway), one covering People (hiring), one covering Product/Strategy (roadmap swap, EU expansion), and a Governance category. Categories may be named differently but must cover these themes. | PASS | "Q1 Financial Results & Cash Position" covers financials/performance; "Hiring Update & GTM Decision" covers people; "Product Roadmap Prioritisation" and "Strategic Expansion Decision" cover product/strategy; "Governance" covers governance. |
| c14 | Output file's items reproduce the specific facts — 8% revenue beat, 2.5 point EBITDA compression, 14→19 month runway, 12/15 vs 0/3 hires, swap of analytics dashboard with workflow automation, EU H2 vs H1-next-year choice — not abstracted into generic phrasing like "review financial performance". | PASS | "Q1 revenue 8% ahead of plan", "EBITDA margin compression by 2.5 points", "Cash runway extended from 14 to 19 months", "Engineering: 12 of 15 planned hires landed", "GTM: 0 of 3", "workflow automation ranked higher than analytics dashboard", "Option A: accelerate to H2 (faster entry, stretches team)" and "Option B: defer to H1 next year (allows time to hire country lead first)". |
| c15 | Output file flags the GTM hiring item with language indicating a decision/steer is required (e.g. "Decision:", "Board steer needed:", "DECIDE:") rather than just listing it as a topic. | PASS | "**Decision required**: backfill GTM roles via contractors while waiting for head of GTM to ramp, or defer GTM hires until head of GTM is in place" — bold decision marker with explicit options. |
| c16 | Output file does NOT include a Q-and-A section, talking points, or response capture areas — those belong to the sibling skill, not this one. | PASS | The agenda file contains only frontmatter, a summary, and five category sections with bullet-point items. No Q-and-A, talking points, or response capture areas are present. |
| c17 | Output file's category headings each carry a `(N min)` time allocation suffix and the allocations sum to ≤90 minutes. No category heading is missing the time allocation. | PASS | All five headings carry `(N min)`: 20+20+15+20+15 = 90 minutes, which equals but does not exceed the 90-minute meeting duration. No heading is missing the suffix. |
| c18 | Output file's summary mentions success criteria for the meeting (e.g. board acknowledgement of runway, agreement on GTM approach, roadmap swap approval, EU direction). | PARTIAL | Summary states "Approve decisions on GTM hiring approach, product roadmap prioritisation, and EU market expansion timing" — covers GTM agreement, roadmap approval, and EU direction. Runway is mentioned as context ("cash runway implications from the March SAFE round close") but not framed explicitly as a success criterion requiring board acknowledgement. |

### Notes

The output is exceptionally strong across all criteria. The artifact correctly synthesises the discussion into a structured, frontmatter-correct agenda file with all five attendees, accurate financial figures, decision-flagged GTM item, time-allocated category headings summing to exactly 90 minutes, and no fabricated content. The summary is tight and specific (not generic). The only criteria that are not full PASS are the two PARTIAL-ceiling items: c8 (next-step suggestion) is fully present in the chat output, and c18 (success criteria in summary) partially covers the required outcomes but does not explicitly frame runway extension as a board acknowledgement target. Both score at their PARTIAL ceiling of 0.5. The skill demonstrates clean separation from the sibling Q-and-A skill with no leakage. Full score within the available ceiling.
