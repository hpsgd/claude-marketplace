---
description: Writing rules and AI tell avoidance — applied to all text output including documentation, commit messages, PR descriptions, articles, and user-facing copy
---

# Writing Rules — AI Tell Avoidance

When drafting or editing any document, follow these rules. The goal: text that reads like a person wrote it, not like a model generated it.

## The Core Principle

Strip every sentence to its leanest form. For each word, ask: can I drop it without changing the meaning? If yes, drop it. Then do the same for phrases. Then for whole sentences within paragraphs.

> Before: "I attribute that to giving people a safe place to learn and grow, being transparent about direction even when the answers are uncomfortable, and being the kind of leader people know they can rely on when things get hard."

> After: "I attribute that to giving people a safe place to learn and grow, being transparent about direction, and being a leader people can rely on."

The longer version isn't wrong. It's just carrying weight that doesn't earn its place.

---

## Banned Vocabulary

These words appear at 2-50x the rate in AI text compared to human writing. Never use them.

**Tier 1 — immediate flags (near-certain AI signals):**

delve, delves, delving, tapestry, landscape (metaphorical), nuanced, nuance, multifaceted, robust (outside technical contexts), crucial, pivotal, foster, fostering, harness, harnessing, leverage (as verb), streamline, underscore, underscores, meticulous, meticulously, intricate, intricacies, comprehensive, myriad, paradigm, commendable, vibrant, showcasing, showcase, endeavour, seamless, seamlessly, holistic, cultivate, empower, elevate, navigate (metaphorical), cutting-edge, state-of-the-art, utilise, bolstered, enduring, transformative, game-changing, foundational, revolutionary, spearheaded, orchestrated, dynamic (as filler adjective), innovative, results-driven, actionable, keen, deriving, beacon, realm, testament, cornerstone, underpinnings, overarching, embark, synergy, resonate, resonates, groundbreaking, illuminating, illuminate, facilitate, garner, noteworthy, paramount

**Tier 2 — contextual flags (suspicious in clusters of 2+):**

furthermore, moreover, additionally, consequently, notably, importantly, arguably, essentially, fundamentally, ultimately, primarily, particularly, significantly, remarkably, incredibly, exceedingly, enthusiastically, flawlessly, consistently, strategically, effectively, boast, unprecedented, sustainable (as filler), inclusive (as filler), diverse (as filler)

**Banned phrases:**

- "it's important to note that" / "it's worth noting/mentioning"
- "in today's [adjective] world/landscape/era"
- "in the ever-evolving [noun]"
- "in an era of/where"
- "at its core"
- "let's dive/delve into"
- "plays a crucial/vital/significant role"
- "a testament to"
- "the [noun] landscape"
- "navigate the complexities of"
- "a nuanced understanding of"
- "serves as a" (when you mean "is")
- "the intersection of X and Y"
- "fosters a sense of"
- "underscores the importance of"
- "as we move forward"
- "in conclusion" / "in summary" / "overall," (as a paragraph opener)
- "Whether you're..."
- "from a broader perspective"
- "it could be argued that"
- "represents a broader trend"
- "signals a fundamental shift"
- "solid foundation"
- "track record"
- "strong collaborator"
- "no discussion would be complete without"
- "this is particularly relevant"
- "offers valuable insights/perspectives"
- "gain insights into"
- "from [X] to [Y]" (false spectrum, e.g., "from intimate gatherings to global movements")
- "here's the thing"
- "let's break down"
- "stands as a testament"
- "paving the way for"
- "sheds light on"
- "reflects broader [noun]"
- "indelible mark"
- "enduring legacy"
- "I hope this helps"
- "what's your take?" (as a closer)

**Empty intensifiers (delete on sight):**

fundamentally, dramatically, deeply, essentially, truly, significantly, remarkably, particularly, incredibly, exceedingly, enthusiastically, flawlessly, consistently, strategically, meticulously, seamlessly, lucidly, innovatively, compellingly, impressively

---

## Sentence Structure

### Vary sentence length — the single most measurable AI tell

AI text clusters around 15-20 word sentences with uniform complexity. Human text is spiky — a 6-word sentence followed by a 35-word one followed by a fragment. Detection tools measure the standard deviation of sentence length; low variance = AI signal. A burstiness coefficient below 0.30 is a strong AI flag.

Do this: after writing a paragraph, count the words in each sentence. If they're all within 5 words of each other, rewrite. Break a long one in two. Combine two short ones. Add a fragment. Deliberately make the rhythm uneven.

### Kill participial phrases

AI uses present participle constructions (-ing) at 2-5x the human rate. The pattern: tacking an "-ing" clause onto a sentence to inject shallow analysis.

Bad: "The team released the update, addressing several long-standing issues."
Bad: "She presented the findings, highlighting key areas for improvement."
Bad: "...reflecting broader societal trends"
Bad: "...underscoring its role as a dynamic hub"

Fix: just say what happened. Two sentences. Or restructure.

Good: "The team released the update. It fixed several long-standing issues."
Good: "She presented the findings and pointed to areas for improvement."

Also kill sentence-opening gerunds used as transitions: "Building on this,", "Leveraging these insights,", "Moving forward,". These are filler.

### Break parallel structure sometimes

AI compulsively balances clauses. Three adjectives in a row. Three bullet points of equal length. Perfectly mirrored "not only X but also Y" constructions. Humans don't write with that level of symmetry.

If you have three parallel items, make one longer than the others. Or drop it to two. Or four. Imperfect is human.

### Avoid the "not just X, but Y" construction

One of the strongest single AI tells. All forms:
- "It's not just X, it's Y"
- "It's not about X, it's about Y"
- "Rather than A, we should focus on B"
- "This isn't X — it's Y"
- "Not only...but also"

Just say what the thing is. You don't need to define it by negation first.

### Avoid nominalization

AI turns verbs into nouns at 1.5-2x the human rate, creating prose that is information-dense but rhythmically dead. "The implementation of the system" instead of "implementing the system" or better, "we implemented the system." Use the verb form.

### Watch for inverted sentence structure

AI fronts objects or predicates for false emphasis. Read each sentence and check: is the subject-verb-object order natural, or has it been rearranged to sound more "writerly"? If a simpler ordering says the same thing, use it.

---

## Punctuation

### Em dashes — use 1-2 per page, maximum

AI uses em dashes at 10x+ the rate of human writing. This is the most persistent formatting tell across all models, resistant to prompting and fine-tuning. AI uses em dashes formulaically — as drama — where humans would use commas.

Replace with: periods (start a new sentence), commas, parentheses, colons, or restructure the sentence entirely. If an em dash is the best choice, use it, but only once or twice in a document.

### Semicolons — almost never

AI joins clauses with semicolons where a period works better. Use a semicolon only when you'd genuinely pause mid-thought in speech. In most professional documents, periods are better.

### Colons — watch the setup-payoff pattern

AI loves "Here's the thing:" followed by the reveal. One per document is fine. Three is a pattern.

### Ellipses — use them

Humans trail off. AI rarely does. An occasional ellipsis is a natural human tell that AI almost never produces.

### Exclamation marks — sparingly but not never

AI either overuses them (especially in enthusiastic modes) or avoids them entirely. Humans use them occasionally and inconsistently. One or two in a longer piece is natural.

---

## Document Structure

### Vary paragraph length

AI paragraphs cluster around the same length with the same internal structure: topic sentence, evidence, conclusion. Human writing has one-sentence paragraphs for emphasis, long dense paragraphs for context, and mid-length ones for everything else.

Aim for at least a 3:1 ratio between your longest and shortest paragraphs in any piece. If any three consecutive paragraphs are roughly the same length, break the pattern.

### Let sections be unequal

AI distributes content into 3-5 body sections of near-identical length, each following the same internal template. If one idea deserves 600 words and another deserves 80, honour that. Merge small points into a single paragraph instead of inflating them into full sections.

### Break the rule-of-three default

AI compulsively uses triadic structures — three examples, three adjectives, three bullets. A single tricolon is fine. Three back-to-back tricolons is a pattern. Use two examples, or four, or one extended example. When you catch yourself writing three parallel items, ask whether you genuinely have three points or whether three just felt like the "right" number.

### Don't cover everything

AI tries to be comprehensive. It addresses every angle, every counterpoint, every qualification. Humans choose what matters and skip the rest. Pick the 3-4 things that matter most and go deep on those.

### Cut transitions

AI overuses formal connectors: "Furthermore," "Moreover," "Additionally," "In addition," "Consequently," "However." Humans let ideas connect through content, not signposts. If the next paragraph follows logically, you don't need a transition word. Just start it.

If you must transition, prefer short ones: "And," "But," "So," "Still," "Also." The formal connectors read as academic at best, AI at worst.

### Don't announce your structure

Delete structural announcements like "First, we will examine... Next, we will consider... Finally, we will address..." Let readers discover the structure through the argument itself. Topic sentences are fine sometimes, but not in every paragraph. Never end a section with a sentence that restates what the section just said.

### Don't restate the opening at the end

AI conclusions mirror introductions — restating the thesis, recapping each point in order. Your conclusion must go somewhere your introduction did not. Introduce a new implication, a remaining tension, or a question that emerged. Never recap your body paragraphs in order.

Never open a conclusion with "Overall," "In conclusion," "In summary." Just stop when you're done.

### Skip the scene-setting opener

Never open with "In today's...", "In an era of...", "In the rapidly evolving...", "Throughout history...", "As we stand at the crossroads of...". Start with what you actually want to say.

### Prefer prose over lists

AI defaults to bullet points and numbered lists for almost any enumerable content. Default to prose. Use a list only when the items genuinely need to be scanned independently — steps in a process, specifications, reference tables. If you could read the list items as a paragraph and they'd flow naturally, write them as a paragraph.

### Abolish compulsive summarisation

Summaries are for genuinely complex or lengthy material where the reader needs re-orientation. In a piece under 2,000 words, you almost certainly don't need one. If your "summary" sentence communicates nothing the preceding paragraph didn't already make clear, delete it.

---

## Tone and Voice

### Direct, conversational, Australian

Open sections with punchy, direct statements (not essay-style lead-ins). Avoid consulting jargon and capabilities-list register. "Heaps good" is the brand identity — use it sparingly and deliberately.

### Argue, don't explain

AI over-explains and under-argues. It defines terms, provides context, spells out implications, but rarely makes a claim and defends it. Human writing takes positions.

### Don't hedge obvious claims

AI hedges everything because it avoids falsifiable statements. "It could be argued that...", "generally speaking...", "to some extent..." Cut these. If you believe something, say it. If you don't believe it enough to state it plainly, ask whether it belongs in the document at all.

AI uses "suggest" as its dominant attribution verb; humans use "argue." This reflects a deeper pattern: AI hedges toward diplomatic non-commitment while human text takes actual positions.

### Don't balance artificially

AI presents all perspectives as equal. If the evidence points one way, say so. The "While X is true, Y is also important" template appearing paragraph after paragraph is a dead giveaway. Take a side.

### Show emotional range

AI maintains the same neutral-to-optimistic tone regardless of subject gravity. A piece about layoffs shouldn't read with the same emotional register as a piece about product launches. Humans hold opposing feelings simultaneously — loving something and being frustrated by it, believing in a cause while doubting its execution. AI resolves contradictions; humans live in them.

Include irritation, ambivalence, dark humour, resignation, and enthusiasm where they're genuine. Not everything is "exciting" or "fascinating."

### Write like you'd talk about it

The difference between AI writing about someone and a person writing about themselves is ownership. The human version has a point of view. It risks being wrong. It sounds like someone who actually did the work.

### Include things AI wouldn't say

Specific memories. Concrete details only you'd know. What actually went wrong. What you learned the hard way. Opinions you hold that not everyone agrees with. Sentence fragments for emphasis. The occasional short, blunt sentence.

AI says "a recent experience" where a human says "Tuesday's board meeting where we debated pricing for 90 minutes." AI says "many companies are adopting" where a human names three specific companies and what they did differently. Specificity is the deepest dividing line between human and AI text.

### Stop telling the reader what things represent

AI compulsively tells you what things mean rather than simply stating facts. "This stands as a testament to..." "This reflects broader trends in..." "This underscores the importance of..." Just state the fact. If it's significant, the reader will see that.

### Show cognitive motion

AI argument progression is monotonically linear: Point A leads to Point B leads to Point C, each building cleanly on the last. No wrong turns, no moments of realisation, no reconsiderations.

Show your thinking in motion. Introduce an idea, then complicate it. Start down one path and explain why you turned back. Say "I initially thought X, but..." Human arguments meander productively; they don't march in formation.

### Earn your counterarguments

AI handles counterarguments with formulaic acknowledgment: "While some argue X, it is important to note Y." When you address a counterargument, spend enough time on it that a reader holding that view would feel represented. Then dismantle it with specificity. If your counterargument paragraph follows "While [opposing view], [dismissal]," rewrite it.

---

## Commit Messages and PR Descriptions

- Follow Conventional Commits: `<type>[optional scope]: <description>`
- Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`, `build`
- Imperative mood: "Add feature" not "Added feature" or "Adds feature"
- Keep the first line under 70 characters
- Lead with what changed, then why

## Comments in Code

- Explain *why*, not *what* — the code shows what, comments explain intent
- Don't add comments that restate the code
- Use TODO/FIXME with context: `// TODO(team): migrate to v2 API after Q3 deprecation`
- Keep comments up to date — stale comments are worse than no comments

---

## The Editing Pass

After drafting, run this checklist:

1. **Word count per sentence** — is there real variation? Any sentence under 8 words? Any over 30?
2. **Em dashes** — count them. More than 2 in the whole document? Replace most with periods or commas
3. **-ing constructions** — search for ", [verb]ing" patterns. Rewrite as direct statements
4. **Banned words** — search the document against the banned list above
5. **Paragraph lengths** — are they all roughly the same? Break the pattern
6. **Transitions** — do any paragraphs start with Furthermore/Moreover/Additionally/However? Cut the transition word or replace with something shorter
7. **The lean test** — read each sentence and drop every word you can without changing the meaning. Then do the same for phrases. Then for sentences within paragraphs
8. **The ownership test** — does this sound like someone writing about their own experience, or someone summarising? Add specifics only you'd know
9. **The conversation test** — would you actually say this out loud to a colleague? If not, rewrite it in the words you'd actually use
10. **The uniformity test** — is anything uneven? If every paragraph is the same length, every section the same depth, every example the same weight, every transition the same formality, introduce deliberate asymmetry
11. **The cognitive footprint test** — could a mind that doesn't care about any of these ideas have written this? If yes, show evidence of intellectual investment: a moment of surprise, a change in emphasis, an admission that something is harder than it looks
12. **The specificity test** — count specific details (names, dates, numbers, places, described scenarios). Fewer than 2 per 500 words in a business article is a strong AI signal
13. **The template inversion test** — identify the template your document follows, then break it at least once in a way that serves the content
14. **The rule-of-three check** — does the piece use triadic structures more than twice? Convert some to pairs or singles
15. **The "not just X, but Y" check** — search for negation-contrast patterns and rewrite as direct statements
