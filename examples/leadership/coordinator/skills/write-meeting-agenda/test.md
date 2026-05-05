# Test: write-meeting-agenda

Scenario: A user has just had a session-long discussion preparing for a quarterly board meeting and invokes the skill to capture an agenda. The skill must synthesise the discussion into a structured agenda (summary + categorised topics + items), confirm metadata (or infer it from the prompt), derive a slug from the title, and write the file under `docs/meetings/<YYYY-MM-DD>-<slug>/agenda.md`.

## Prompt

I've just had a long discussion with you about the upcoming quarterly board meeting for Acme Robotics. Here's a recap of what we covered so you can write the agenda:

**Context:** Quarterly board meeting on 2026-05-15. 90 minutes scheduled. Attendees: CEO (Sam Patel), CFO (Rita Cho), Chair (Jordan Liu), two non-exec directors (Casey Morgan, Devi Iyer). Meeting type: board.

**What we discussed and want to cover:**

- Q1 financial results came in 8% ahead of plan on revenue but EBITDA margin compressed by 2.5 points due to one-off rebrand costs and accelerated R&D hiring. The CFO will walk through the bridge.
- Cash runway extended from 14 to 19 months because of the SAFE round closing in March. Need board acknowledgement of the new runway and the decision to defer the Series B by two quarters.
- Hiring: 12 of 15 planned engineering hires landed, 0 of 3 GTM hires landed because the head of GTM hasn't started yet. Need a board view on whether to delay the GTM hires until the head of GTM is onboarded or backfill via contractors.
- Product roadmap shift: customer feedback from the design partner programme has surfaced that the workflow automation feature ranks higher than the analytics dashboard we had prioritised. The CPO wants approval to swap them in the H2 roadmap.
- A strategic decision to discuss: whether to expand into the EU market in H2 (faster, but stretches the team) or wait until H1 next year (slower, but lets us hire a country lead first). Risk appetite question — board input needed.
- Standard governance: minutes from last meeting, conflicts of interest, AOB.

**Open question we landed on:** the GTM hiring decision needs a board steer, not just a recommendation — flag it as a decision item, not a discussion item.

Please now run:

/coordinator:write-meeting-agenda "Q2 Board Meeting" --dir docs/meetings

## Criteria

- [ ] PASS: Skill writes the agenda to a file at `docs/meetings/2026-05-15-q2-board-meeting/agenda.md` (or a path with the same date prefix and a slug derived from "Q2 Board Meeting"). Confirms the absolute path in chat output.
- [ ] PASS: Agenda frontmatter includes `title`, `date` (2026-05-15), `duration_minutes` (90), `type` (board), and an `attendees` list with all five named attendees.
- [ ] PASS: Agenda has a `## Summary` section of 2-3 sentences describing the meeting purpose. Summary references the actual content of the discussion (Q1 results, runway, GTM steer, EU expansion) — not generic board-meeting language.
- [ ] PASS: Topics are categorised into 2-5 logical groupings using `##` headings — not a flat list of every item.
- [ ] PASS: Items under topics are concrete and traceable to the discussion (Q1 8% revenue beat, EBITDA margin compression, runway 14→19 months, 12/15 engineering hires, GTM hiring decision, roadmap swap, EU expansion, governance items).
- [ ] PASS: The GTM hiring item is framed as a decision needing board steer, not as a generic discussion item — reflecting the explicit instruction in the prompt.
- [ ] PASS: No fabricated content — does not invent attendees, financial figures, or items not present in the discussion.
- [ ] PARTIAL: Output suggests `/coordinator:write-meeting-qa` as the next step.
- [ ] PASS: Slug in folder name matches the rule (lowercase, dashes, no special chars) — e.g. `q2-board-meeting`.

## Output expectations

- [ ] PASS: Output file's frontmatter has `duration_minutes: 90` and `type: board` exactly — not 60 (default) and not "Discussion".
- [ ] PASS: Output file's `attendees:` list contains all five named individuals from the prompt — Sam Patel (CEO), Rita Cho (CFO), Jordan Liu (Chair), Casey Morgan, Devi Iyer. Roles preserved where given.
- [ ] PASS: Output file has at least one category covering Financials/Performance (Q1 results, EBITDA, runway), one covering People (hiring), one covering Product/Strategy (roadmap swap, EU expansion), and a Governance category. Categories may be named differently but must cover these themes.
- [ ] PASS: Output file's items reproduce the specific facts — 8% revenue beat, 2.5 point EBITDA compression, 14→19 month runway, 12/15 vs 0/3 hires, swap of analytics dashboard with workflow automation, EU H2 vs H1-next-year choice — not abstracted into generic phrasing like "review financial performance".
- [ ] PASS: Output file flags the GTM hiring item with language indicating a decision/steer is required (e.g. "Decision:", "Board steer needed:", "DECIDE:") rather than just listing it as a topic.
- [ ] PASS: Output file does NOT include a Q&A section, talking points, or response capture areas — those belong to the sibling skill, not this one.
- [ ] PARTIAL: Output file's summary mentions success criteria for the meeting (e.g. board acknowledgement of runway, agreement on GTM approach, roadmap swap approval, EU direction).
