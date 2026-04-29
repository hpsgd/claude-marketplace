# Output: content-analyst — content evaluation

**Verdict:** PASS
**Score:** 17.5/18 criteria met (97%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Agent routes to `/analyst:content-analysis` skill for a single article URL — workflow routing table maps "Analyse this article / document / transcript" → `/analyst:content-analysis`. Single URL input is unambiguous.
- [x] PASS: Agent distinguishes analysis from summarisation — first paragraph states "You don't summarise; you analyse." `What you don't do` explicitly includes "Summarise without analysing."
- [x] PASS: Framing observations are stated as interpretive judgements, not facts — Principles state "don't hide interpretive judgements behind passive voice"; content-analysis skill Step 4 rules say "State your framing observations as interpretive judgements, not facts: 'The piece frames X as...' not 'The piece proves X is...'"
- [x] PASS: Sentiment is assessed at the author's tone level, not the subject's actual situation — content-analysis skill Step 3: "Do not conflate the author's sentiment with the subject's actual situation." Agent Principles: "Sentiment applies to the author's tone, not the subject's character."
- [x] PASS: Source structure section identifies how claims are attributed — Step 6 defines the four-row source structure table (named primary, named secondary, anonymous, unattributed). Agent Principles devote a full paragraph to source attribution structure.
- [~] PARTIAL: Agent notes what the article omits or backgrounds, with a caveat if topic knowledge is insufficient — Step 4 Omissions field is required; Rules state "If you don't know enough to identify what's missing, say so." Omissions are structurally required and the caveat instruction exists, but the agent relies on the skill for this rather than reinforcing it in agent-level Principles. Partially met: 0.5.
- [x] PASS: Agent does not produce a literature review or academic-style output — `What you don't do`: "Produce academic-style literature reviews — that's research, not content analysis."
- [x] PASS: Agent does not assess whether the article's conclusions are correct — `What you don't do`: "Assess whether a source's conclusions are correct — only whether it's credible."

### Output expectations

- [x] PASS: Output is structured per the content-analysis format — the skill's output format template defines sections for Entities, Key Claims, Sentiment, Framing, Narrative, and Source Structure. The agent routes to this skill for single-URL requests, so the structured format would be produced rather than a plain summary.
- [x] PASS: Output's Entities section extracts people (by role: source / subject / authority), organisations, key statistics and dates — Step 1 of the skill explicitly requires people with roles (source/subject/authority), organisations, and "Key figures cited" covering statistics and dates. The skill fetches the URL before analysis if a URL is provided.
- [x] PASS: Output's Key Claims section distinguishes primary, supporting, and implicit claims with attribution per claim — Step 2 defines exactly these three claim types and requires attribution type (named source, anonymous, author assertion, or presented as fact) for each.
- [x] PASS: Output's framing observations are stated as interpretive — Step 4 Rules: "State your framing observations as interpretive judgements, not facts: 'The piece frames X as...'" This is both stated in the agent Principles and enforced by the skill's explicit rule.
- [x] PASS: Output's sentiment assessment evaluates the author's tone and targets — Step 3 assesses overall tone, targets of sentiment, and notable language signals, with explicit instruction not to conflate author sentiment with subject's reality.
- [x] PASS: Output's source structure analyses claim attribution — Step 6 produces the four-row table (named primary, named secondary, anonymous, unattributed) with count and claim type columns.
- [x] PASS: Output identifies the dominant narrative structure and what audience response it activates — Step 5 lists named narrative structures (hero/villain, crisis/urgency, progress/innovation, conflict/battle, revelation/exposure, human cost) and says "Identifying the dominant narrative helps explain why a piece feels the way it does." The output format includes a Narrative section requiring what story is told and what audience response it activates.
- [x] PASS: Output flags omissions with a caveat if topic knowledge insufficient — Step 4 Framing requires an Omissions field; the output format template shows `[what's absent — or "insufficient topic knowledge to assess"]`; Rules state "If you don't know enough to identify what's missing, say so."
- [x] PASS: Output is analytical not encyclopedic — the skill's six-step structure keeps output focused on this article's argument, and the agent explicitly excludes literature reviews.
- [~] PARTIAL: Output flags the competitive context — Atlassian is a competitor, so framing may serve commercial interest in collaboration tooling. The skill's Implicit claims step (Step 2) and Framing step (Step 4) would surface commercial interest as an implicit claim and a backgrounded element. The agent's collaboration table includes business-analyst for competitive research inputs. However, neither the agent nor the skill has an explicit instruction to flag commercial/competitive alignment of the source's findings when the requester names a competitive context. This would likely surface through the analysis but is not structurally guaranteed. Partially met: 0.5.

## Notes

The definition is strong. The skill's output format template is precise enough that an agent following it could not produce a plain summary — the structure forces analytical output. The main gap is the competitive context flag: when a user explicitly states "we compete with [vendor]," there is no agent-level instruction to treat this as a relevance signal for implicit claims or framing. The implicit claims step would likely catch the commercial alignment, but the competitive intel angle (Atlassian's commercial interest in positive remote-work-productivity findings) is not structurally guaranteed. The rest of the rubric is met by explicit rules in either the agent definition or the skill.
