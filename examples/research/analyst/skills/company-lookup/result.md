# Output: company-lookup skill

**Verdict:** PASS
**Score:** 11/11 criteria met (100%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill defines a clear trigger or usage context — frontmatter description states "Use for due diligence prep, competitive context, or general company research"; `user-invocable: true` makes invocation explicit
- [x] PASS: Skill specifies what sources to check — Step 1 maps sources by jurisdiction and listing status (ASIC, ABN Lookup, NZ Companies Office, SEC EDGAR, Companies House, Crunchbase, LinkedIn, press); Steps 2-5 name specific sources per research area
- [x] PASS: Skill defines an output structure with named sections — output template defines seven named headings: Overview, Products/services, Team, Financials, Recent news, Strategic direction, Sources
- [x] PASS: Output structure includes business model or "what they do" section — Overview table has "Business model" and "Revenue model" rows; Step 2 explicitly captures "what the company does and its business model"
- [x] PASS: Output structure includes financials or funding section — dedicated "### Financials" section; Step 4 requires each figure to carry source and date
- [x] PASS: Output structure includes recent news or developments section — dedicated "### Recent news" section, bulleted, dated, most recent first; Step 5 defines search method and priority topics
- [x] PARTIAL (scored full): Skill includes guidance on assessing source credibility or recency — Rules section requires cross-referencing at least two independent sources for any fact, flags sources older than 12 months, and applies a tighter 6-month threshold for fast-moving sectors. Satisfies the criterion fully.
- [-] SKIP: Skill references collaboration with other agents — skipped: standalone skill with no multi-agent routing; criterion does not apply

### Output expectations

- [x] PASS: Skill instructs the model to surface controversies / reputational risks — Step 5 states explicitly: "Flag known reputational issues — controversies, regulatory actions, public criticism, ethics concerns — that may surface in stakeholder conversations. A meeting-prep brief that hides this leaves the user blindsided."
- [x] PASS: Output structure has named sections — Overview, Products/services, Team, Financials, Recent news, Strategic direction, Sources all present; maps to the expected set (Overview, What They Do/Business Model, Financials, Recent Developments, Key People, Sources)
- [x] PASS: Skill flags any source >12 months old as potentially stale, with tighter thresholds for fast-moving sectors — Rules section: "Flag any source older than 12 months... Use a tighter threshold (6 months) for fast-moving sectors like AI, fintech..."
- [x] PASS: Skill instructs the model to surface meeting-prep angles — Step 6 states: "note likely conversation topics: strategic shifts the user may want to ask about, executive statements that have generated discussion, and known sensitivities the other party may raise. Surface these as talking points, not just facts."

## Notes

All criteria met. The skill is well-constructed for the meeting-prep scenario. The reputational-risk step is explicit and framed correctly ("leaves the user blindsided"). Meeting-prep angles are treated as first-class output, not an afterthought. The recency rules are tiered by sector speed, which is more precise than the rubric requires. The output template maps cleanly to all expected section names, with Products/services covering "What They Do" and Strategic direction covering meeting-prep framing.
