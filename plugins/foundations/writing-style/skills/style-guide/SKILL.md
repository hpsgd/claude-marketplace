---
name: style-guide
description: Apply writing style and tone guidelines when creating documentation, commit messages, PR descriptions, or user-facing text
allowed-tools: Read, Grep, Glob
---

Apply these writing standards to all text output: documentation, commit messages, PR descriptions, comments, UI copy, error messages, and any user-facing text. When reviewing existing text, check against every rule and suggest specific rewrites.

## Core Principles

1. **Say it directly.** Lead with the point. No preamble, no throat-clearing.
2. **Say it once.** If you have made the point, move on.
3. **Say it concretely.** Examples beat abstractions. Specific beats general.
4. **Say it actively.** The subject does the action. Not "the file was deleted" but "the script deletes the file."
5. **Say it plainly.** If a simpler word works, use it.

## Quick Reference — Word Substitutions

Replace the left column with the right:

| Do not write | Write instead |
|-------------|---------------|
| utilize | use |
| implement | build |
| facilitate | help, enable |
| leverage | use |
| comprehensive | complete, thorough, full |
| robust | strong, reliable, solid |
| streamline | simplify |
| empower | let, enable |
| foster | encourage, support |
| paradigm | model, approach |
| synergy | (cut the word entirely) |
| ecosystem | system, platform |
| cutting-edge | modern, current |
| game-changing | (describe the actual change) |
| best practices | (say what the practice is) |
| deep dive | look at, examine, review |
| at the end of the day | (cut the phrase) |
| in order to | to |
| it should be noted | (cut — just state the thing) |
| going forward | from now on, next |
| a myriad of | many |
| a plethora of | many |
| utilize | use |
| optimal | best |
| prior to | before |
| subsequent to | after |
| in the event that | if |
| due to the fact that | because |
| at this point in time | now |

## Banned Words — Hard Stops

Flag every occurrence. These are AI tells and corporate filler:

`delve`, `tapestry`, `landscape`, `nuanced`, `realm`, `multifaceted`, `holistic`,
`pivotal`, `cornerstone`, `underpinning`, `intricate`, `noteworthy`, `commendable`,
`meticulous`, `elevate`, `testament`, `embark`, `encompass`, `spearhead`

No exceptions. If you find one, rewrite the sentence.

## Banned Phrases — Hard Stops

Flag every occurrence:

- "It's important to note" / "It's worth mentioning" — just state the fact
- "In today's world" / "In the modern era" / "In this day and age" — cut
- "At its core" / "At the heart of" — state what it is directly
- "This allows us to" / "This enables us to" — state what it does
- "When it comes to" — cut and restructure
- "As mentioned earlier/above" — if the reader needs the info, repeat it briefly
- "Without further ado" — cut
- "Let's take a look at" — just present it
- "It goes without saying" — then do not say it
- "Needless to say" — then do not say it

## Sentence Structure Rules

1. **Active voice** — the subject performs the action:
   - Wrong: "The configuration is loaded by the service on startup"
   - Right: "The service loads the configuration on startup"

2. **No participial phrase openers** — do not start sentences with -ing constructions:
   - Wrong: "Leveraging the new API, the client fetches data faster"
   - Right: "The client fetches data faster with the new API"
   - Wrong: "Running the migration script, the database schema updates"
   - Right: "The migration script updates the database schema"

3. **Vary sentence length** — mix short and medium sentences. Three consecutive sentences of the same length feel monotonous. A short sentence after a long one adds punch.

4. **One idea per sentence** — if a sentence has "and" connecting two independent clauses, split it into two sentences. Compound sentences that span three lines are not sentences; they are paragraphs pretending.

5. **Front-load the important word** — put the subject or key term early:
   - Wrong: "For the purpose of improving reliability, we added retry logic"
   - Right: "Retry logic improves reliability"

6. **Parallel structure** — list items use the same grammatical form:
   - Wrong: "The system handles authentication, is logging requests, and data validation"
   - Right: "The system handles authentication, logs requests, and validates data"

## Punctuation Rules

1. **Em dashes** — maximum 2 per document. More than that means you are using them as a crutch. Replace extras with periods, commas, or parentheses.

2. **Semicolons** — use sparingly. Most semicolon usage should be two separate sentences instead. Acceptable in lists where items contain commas.

3. **Exclamation marks** — maximum 1 per document. Zero is better. They do not make text more exciting; they make it less credible.

4. **Oxford comma** — always use it. "Red, white, and blue" not "Red, white and blue."

5. **Quotation marks** — use double quotes for direct quotes, single quotes for terms used in a special sense or code references in prose (not in code blocks).

## Paragraph Structure

1. **Lead with the point** — the first sentence of a paragraph states its purpose. Supporting detail follows. Do not build up to the point.

2. **Short paragraphs** — 1-4 sentences. A paragraph that fills a full screen is not a paragraph.

3. **No transition padding** — do not start paragraphs with "Additionally", "Furthermore", "Moreover", "In addition", "That being said". Just state the next point.

4. **Headings over transitions** — if you need to signal a topic change, use a heading, not a transitional sentence.

## Formatting for Technical Writing

1. **Code references** — use backticks for inline code, function names, file names, commands, and variable names. Do not use backticks for emphasis.

2. **Lists** — use bullet points for unordered items, numbered lists for sequential steps. Do not use numbered lists for non-sequential items.

3. **Headings** — use heading levels correctly. `##` for sections, `###` for subsections. Do not skip levels.

4. **Links** — descriptive link text. "See the [deployment guide](url)" not "Click [here](url)".

5. **Tables** — use tables for structured comparison. Do not use tables for single-column lists.

## Reviewing Text — Checklist

When asked to review documentation, copy, or any prose, check in this order:

1. [ ] **Banned words scan** — grep or search for every word in the banned list
2. [ ] **Banned phrases scan** — search for every phrase in the banned list
3. [ ] **Passive voice** — read each sentence and check whether the subject acts or is acted upon
4. [ ] **Participial openers** — check first word of each sentence for -ing forms
5. [ ] **Sentence length** — flag sentences over 30 words
6. [ ] **Paragraph length** — flag paragraphs over 5 sentences
7. [ ] **Em dash count** — count total, flag if more than 2
8. [ ] **Filler phrases** — "in order to", "it should be noted", etc.
9. [ ] **Accuracy** — do code references match the actual codebase? Do links work?
10. [ ] **Clarity** — could a new team member understand this on first read?
11. [ ] **Conciseness** — can anything be cut without losing meaning?
12. [ ] **Parallel structure** — are list items grammatically consistent?

For each finding, provide:
- The exact text that violates the rule
- Which rule it violates
- A specific rewrite

Do not give abstract feedback ("make it more concise"). Rewrite the specific sentence.

## Context-Specific Guidance

### Commit messages
- Imperative mood: "Add feature" not "Added feature"
- First line under 70 characters
- Body explains WHY, not WHAT

### PR descriptions
- Lead with the problem being solved
- Bullet points, not prose paragraphs
- Test plan is concrete and actionable

### Error messages
- State what went wrong, what the user can do, and where to find help
- No jargon the user would not understand
- No stack traces in user-facing errors

### API documentation
- Start with what the endpoint does (one sentence)
- Parameters: name, type, required/optional, constraints
- Response: shape, status codes, error format
- Example request and response

### README files
- First paragraph: what it is and why you would use it
- Quick start: fewest steps to working code
- No badges wall — one line of badges maximum
