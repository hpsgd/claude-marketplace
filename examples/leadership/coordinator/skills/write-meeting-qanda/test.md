# Test: write-meeting-qanda

Scenario: A user has had a session-long discussion preparing for a quarterly board meeting and runs both meeting skills in sequence — the agenda skill to capture the agenda, then the Q-and-A skill to produce a structured Q-and-A document supporting it. The qanda.md must mirror the agenda's structure exactly (including per-topic time allocations), expand each item into talking points + questions + a Notes capture area, and live alongside the agenda.

## Prompt

End-state task: produce both `agenda.md` and `qanda.md` in `docs/meetings/2026-05-15-q2-board-meeting/`. **Both files must exist when you finish — do not stop after the agenda is written.**

Run two skills in sequence. The first writes the agenda; the second expands it into the Q-and-A document. Carry the absolute path of the agenda from the first skill's output to the second.

Discussion context for the agenda:

I've just had a long discussion with you about the upcoming quarterly board meeting for Acme Robotics. Here's a recap of what we covered so you can write the agenda and Q-and-A:

- **Meeting metadata:** Quarterly board meeting on 2026-05-15. 90 minutes scheduled. Attendees: CEO (Sam Patel), CFO (Rita Cho), Chair (Jordan Liu), two non-exec directors (Casey Morgan, Devi Iyer). Meeting type: board.
- Q1 financial results came in 8% ahead of plan on revenue but EBITDA margin compressed by 2.5 points due to one-off rebrand costs and accelerated R&D hiring. The CFO will walk through the bridge.
- Cash runway extended from 14 to 19 months because of the SAFE round closing in March. Need board acknowledgement of the new runway and the decision to defer the Series B by two quarters.
- Hiring: 12 of 15 planned engineering hires landed, 0 of 3 GTM hires landed because the head of GTM hasn't started yet. Need a board view on whether to delay the GTM hires until the head of GTM is onboarded or backfill via contractors.
- Product roadmap shift: customer feedback from the design partner programme has surfaced that the workflow automation feature ranks higher than the analytics dashboard we had prioritised. The CPO wants approval to swap them in the H2 roadmap.
- A strategic decision to discuss: whether to expand into the EU market in H2 (faster, but stretches the team) or wait until H1 next year (slower, but lets us hire a country lead first). Risk appetite question — board input needed.
- Standard governance: minutes from last meeting, conflicts of interest, AOB.
- The GTM hiring decision needs a board steer, not just a recommendation — flag it as a decision item, not a discussion item.

Now run, in order:

1. `/coordinator:write-meeting-agenda "Q2 Board Meeting" --dir docs/meetings`
2. `/coordinator:write-meeting-qanda <absolute path to the agenda file from step 1>`

You are only finished when `qanda.md` exists alongside `agenda.md`. Confirm both absolute paths in your final message.

## Criteria

- [ ] PASS: Skill writes `qanda.md` to the same folder as the agenda (`docs/meetings/2026-05-15-q2-board-meeting/qanda.md` or equivalent absolute path). Confirms the absolute path in chat output.
- [ ] PASS: `qanda.md` frontmatter includes `agenda: ./agenda.md`, `title: "Q2 Board Meeting"` (or equivalent matching the agenda), and `date: 2026-05-15`.
- [ ] PASS: `qanda.md` mirrors the agenda's category structure — same `##` headings in the same order. (Agenda will have categories covering Financial/Performance, People, Product/Strategy, and Governance themes.)
- [ ] PASS: Category headings in `qanda.md` preserve the per-topic time allocation suffix `(N min)` from the agenda — character-for-character with what the agenda emitted.
- [ ] PASS: Each agenda item appears in `qanda.md` as a `###` sub-heading under the correct category — order matches the agenda. None merged, none reordered, none dropped.
- [ ] PASS: Each item has three labelled sections: `**Talking points:**`, `**Questions:**`, and `**Notes:**` — in that order.
- [ ] PASS: Each item is followed by a horizontal rule (`---`) as a section boundary for the downstream PDF generator.
- [ ] PASS: Talking points and questions are specific to each item — anchored in the agenda content (revenue beat, EBITDA compression, GTM decision, EU timing) rather than generic phrasing.
- [ ] PASS: The `**Notes:**` section is empty (or contains only a placeholder comment like `<!-- response capture area -->`) — does not pre-fill answers.
- [ ] PASS: Skill does NOT modify `agenda.md` — only writes the new `qanda.md`.
- [ ] PARTIAL: The GTM hiring decision item generates questions framed as decision-elicitation questions for the board (e.g. "Which option does the board prefer?"), reflecting the agenda's explicit decision framing.

## Output expectations

- [ ] PASS: `qanda.md` has `# Q-and-A: Q2 Board Meeting` (or equivalent matching the agenda title) as the top-level heading.
- [ ] PASS: `qanda.md` category headings exactly match the agenda's category headings — same names, same order, same `(N min)` time allocation suffix. No category renamed, split, or merged. No time allocation dropped.
- [ ] PASS: `qanda.md` has at least eight `###` item-level sub-headings — covering Q1 revenue, EBITDA, runway, Series B deferral, engineering hires, GTM hires, GTM decision, roadmap swap, EU expansion, and the governance items. (Items may be combined where the agenda lists them as one bullet.)
- [ ] PASS: Talking points for the EBITDA item reference the actual cause noted in the discussion (rebrand costs + accelerated R&D hiring) — not abstracted to "operating costs increased".
- [ ] PASS: Questions for the EU expansion item include at least one question that asks for a board view on the H2-vs-H1-next-year tradeoff — not a generic "what do you think?".
- [ ] PASS: The Notes section under each item is structurally present and visually separable — uses an HTML comment placeholder or visible blank space, never pre-filled with fabricated meeting responses.
- [ ] PASS: `qanda.md` uses `---` horizontal rules between items (not just between categories) — so each item gets its own clean PDF section boundary.
- [ ] PASS: `qanda.md` preserves the GTM decision framing from the agenda — retains the "DECIDE:" prefix or equivalent decision marker on that item.
- [ ] PARTIAL: Output marks any item with `<!-- TODO: insufficient context, expand manually -->` only when the agenda content genuinely lacks substance for talking points/questions — not used as a substitute for thinking.
