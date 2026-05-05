---
name: write-meeting-agenda
description: "Synthesise the preceding session discussion into a structured meeting agenda — high-level summary, categorised topics, and specific items per topic. Defaults to writing under `docs/meetings/<YYYY-MM-DD>-<slug>/agenda.md`. Pair with `/coordinator:write-meeting-qa` to produce the supporting Q&A document used to generate a printable note-taking PDF."
argument-hint: "[meeting title hint] [--dir <path>]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Write Meeting Agenda

Generate a meeting agenda from the discussion that has happened in this session. The agenda captures what to cover at the meeting — a high-level summary, categorised topics, and specific items under each topic.

The agenda is the foundation document. The companion Q&A document (built by `/coordinator:write-meeting-qa`) expands each item into talking points, questions, and capture space for responses, which is then converted into a printable PDF for note-taking during the meeting.

## Step 1: Resolve target directory to an absolute path

Parse `$ARGUMENTS`:

- `--dir <path>` — meeting directory root. If absent, default to `docs/meetings/`.
- Remaining text — optional title hint.

**Resolve the directory to an absolute path before writing.** The `Write` tool requires absolute paths; relative paths can resolve against the wrong base. Use `Bash` to compute the absolute base:

```bash
DIR_ARG="<dir or default>"
case "$DIR_ARG" in
  /*) BASE="$DIR_ARG" ;;
  *) BASE="$(pwd)/$DIR_ARG" ;;
esac
echo "$BASE"
```

The agenda will be written to `<BASE>/<YYYY-MM-DD>-<slug>/agenda.md`. Carry the absolute `<BASE>` through to Step 5.

## Step 2: Identify the discussion thread

If the session has covered multiple unrelated topics, ask the user which discussion the meeting is for. Don't merge unrelated threads into one agenda. If the discussion is a single coherent thread, proceed without asking.

## Step 3: Resolve meeting metadata

Resolve the following fields from the available context. The title comes from the user's `$ARGUMENTS` if provided; everything else is inferred from the session discussion.

| Field | Source | Default if absent |
|---|---|---|
| Title | `$ARGUMENTS` (the title hint) | Inferred from the discussion |
| Date | Stated in the discussion | Today's date in YYYY-MM-DD |
| Attendees | Named in the discussion | Empty list — don't invent names |
| Duration | Stated in the discussion | 60 minutes |
| Meeting type | Stated in the discussion | "Discussion" |

If running in an interactive session and any field is genuinely ambiguous, ask the user before writing. In a non-interactive session, use the resolved values without prompting. Either way: never invent attendees, dates, or facts that weren't stated.

## Step 4: Synthesise the agenda

Read back over the relevant session discussion. Extract three things:

1. **High-level summary** — 2-3 sentences. What the meeting is for. What success looks like at the end.
2. **Categorised topics** — 2-5 logical groupings. Each becomes a top-level section heading.
3. **Items per topic** — concrete things to discuss within each. Specific, not abstract.

Source content from the session, not from training knowledge. If the discussion is too thin to support a real agenda, stop and tell the user — don't pad with generic prompts.

## Step 5: Write the agenda

The slug is derived **from the resolved title only** — not from the discussion content. Lower-case the title, replace whitespace with `-`, strip non-alphanumeric except `-`, collapse repeats, truncate to 50 chars. Examples:

- Title `Q2 Board Meeting` → slug `q2-board-meeting`
- Title `1:1 with Jane (May)` → slug `1-1-with-jane-may`
- Title `Acme — Onboarding Kickoff` → slug `acme-onboarding-kickoff`

If the discussion centred on different content (e.g. Q1 financial results) but the title is "Q2 Board Meeting", the slug is `q2-board-meeting`. The title wins.

**Use the `Write` tool to create the agenda file at the absolute path `<BASE>/<YYYY-MM-DD>-<slug>/agenda.md`** (where `<BASE>` is the resolved absolute directory from Step 1). Do not claim the file was written without calling `Write`. The `Write` tool creates parent folders automatically.

Agenda content:

```markdown
---
title: "<title>"
date: <YYYY-MM-DD>
duration_minutes: <duration>
type: <meeting type>
attendees:
  - <name or role>
---

# <title>

## Summary

<2-3 sentence summary>

## <Category 1>

- <item>
- <item>

## <Category 2>

- <item>
- <item>
```

## Step 6: Confirm path

Output the absolute path to the agenda. Suggest `/coordinator:write-meeting-qa` as the next step if the user wants the supporting Q&A document.

## Rules

- **Source content from the session, not from training knowledge.** If the agenda needs facts that weren't discussed, ask — don't fabricate.
- **Don't pad.** A short agenda with five real items beats a long agenda half-filled with generic prompts.
- **One agenda per meeting.** If two unrelated meetings surfaced in the discussion, write two agendas via separate invocations.
- **Preserve the user's framing.** If the discussion used specific terminology, carry it through. Don't translate into consulting-speak.
- **Don't invent attendees.** Empty list is better than wrong names.

## Related Skills

- `/coordinator:write-meeting-qa` — expand the agenda into a Q&A document with talking points, questions, and capture space for responses. Run this after the agenda exists.
