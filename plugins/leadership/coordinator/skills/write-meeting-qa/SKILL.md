---
name: write-meeting-qa
description: "Expand a meeting agenda into a structured Q&A document — talking points, questions, and capture space for responses per item. The output mirrors the agenda structure and is the foundation for a printable note-taking PDF (e.g. for Remarkable Paper Pro). Defaults to the most recent agenda under `docs/meetings/`."
argument-hint: "[path to agenda.md] [--dir <path>]"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Write Meeting Q&A

Take an existing meeting agenda and expand each item into a Q&A structure: talking points to anchor on, specific questions to ask, and a labelled capture area for the response. The output is a single file mirroring the agenda's structure, intended as the source for a printable PDF used during the meeting itself.

## Step 1: Resolve agenda path to absolute

Parse `$ARGUMENTS`:

- If a path ending in `.md` is provided, use it as the agenda path.
- Otherwise:
  - If `--dir <path>` provided, resolve under that root; else `docs/meetings/`.
  - Find the most recently modified `agenda.md` under that root and use it.

**Resolve the agenda path to an absolute path before reading or writing.** The `Read` and `Write` tools require absolute paths; relative paths can resolve against the wrong base. Use `Bash`:

```bash
ARG="<input path or directory>"
case "$ARG" in
  /*) ABS="$ARG" ;;
  *) ABS="$(pwd)/$ARG" ;;
esac
# If ABS is a directory, find the latest agenda.md under it:
[ -d "$ABS" ] && ABS=$(find "$ABS" -name 'agenda.md' -type f -print0 | xargs -0 ls -t 2>/dev/null | head -1)
echo "$ABS"
```

If no agenda is found, stop and report. If multiple recent agendas exist and the latest is ambiguous, list candidates and ask which to use.

## Step 2: Read the agenda

Read the resolved agenda. Extract:

- Frontmatter (`title`, `date`, `attendees`, `duration_minutes`, `type`)
- Summary
- Categories (top-level `##` headings after Summary) and the items beneath each

The Q&A document must mirror this structure exactly — same categories, same items, same order. Don't reorder, merge, or split.

## Step 3: Expand each item

For every item in the agenda, generate three sections:

1. **Talking points** — 2-4 bullets. The substance the user wants to communicate or anchor on for this item.
2. **Questions** — 1-3 specific questions to ask the other attendees. Open questions, not yes/no fishing.
3. **Notes** — labelled empty section for handwritten capture during the meeting. The PDF generator turns this into the writable area.

Source talking points and questions from the session discussion that produced the agenda. If a particular item is too thin to expand meaningfully, mark it with `<!-- TODO: insufficient context, expand manually -->` rather than padding with generic filler.

## Step 4: Write the Q&A document

**Use the `Write` tool to create `qa.md` at the absolute path of the agenda's folder** (replace `agenda.md` with `qa.md` in the resolved absolute path from Step 1). Do not claim the file was written without calling `Write`. In a non-interactive session, do not stop to ask for confirmation — write the file and report the path.

Content template:

```markdown
---
agenda: ./agenda.md
title: "<title>"
date: <YYYY-MM-DD>
---

# Q&A: <title>

> Foundation document for meeting note-taking. The printable PDF is generated from this file.

## <Category 1>

### <Item 1.1>

**Talking points:**

- <point>
- <point>

**Questions:**

- <question>
- <question>

**Notes:**

<!-- response capture area -->

---

### <Item 1.2>

**Talking points:**

- <point>

**Questions:**

- <question>

**Notes:**

<!-- response capture area -->

---

## <Category 2>

...
```

Use a horizontal rule (`---`) between items so the downstream PDF generator has a clean section boundary. Preserve the agenda's exact category and item titles — character-for-character.

## Step 5: Confirm path

Output the absolute path to the Q&A document.

## Rules

- **Mirror the agenda.** Categories, items, order — all match. Don't reorder, merge, or split.
- **Don't invent content.** If the discussion didn't surface a question or talking point for an item, mark a TODO. Generic filler is worse than an acknowledged gap.
- **One file, mirroring the agenda.** Don't split into per-category files. The PDF generator expects one source.
- **Preserve frontmatter linkage.** The `agenda: ./agenda.md` reference ties the Q&A to its agenda for downstream tooling.
- **Read-only on the agenda.** Never edit the agenda from this skill. If the agenda has gaps, surface them; don't fix them silently.

## Related Skills

- `/coordinator:write-meeting-agenda` — produces the agenda this skill expands. Run that first.
