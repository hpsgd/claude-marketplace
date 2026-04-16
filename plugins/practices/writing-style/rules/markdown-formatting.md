---
description: Markdown formatting conventions — whitespace, line length, GFM compliance, and structural rules. Applied to all generated markdown files.
---

# Markdown Formatting

All markdown output must render correctly on GitHub (GitHub Flavoured Markdown). These rules prevent rendering bugs, diff noise, and readability issues.

## Whitespace

- **Blank line before and after every block element.** Headings, lists, tables, code fences, blockquotes, and horizontal rules all need a blank line above AND below. Without both, GitHub may not render the element correctly.
- **Blank line between list items with multi-line content.** If a list item contains a paragraph, code block, or sub-list, separate items with a blank line.
- **No trailing whitespace.** Do not rely on trailing spaces for line breaks. Use a blank line for paragraph breaks instead.
- **Single blank line only.** Never use two or more consecutive blank lines. One is sufficient.
- **End every file with a single newline.** No trailing blank lines, but the file must end with `\n`.

## Headings

- **ATX style only** (`# Heading`, not `Heading\n===`).
- **Blank line before and after every heading.** No exceptions.
- **No skipped levels.** `##` then `###`, never `##` then `####`.
- **No duplicate headings** at the same level within a document.
- **Sentence case** for headings ("Step 1: Define the scope", not "Step 1: Define The Scope").

## Line length

- **Soft wrap at 120 characters** for prose paragraphs. Do not hard-wrap prose mid-sentence — let the editor wrap.
- **Tables and code blocks are exempt** from line length limits.
- **URLs are exempt.** Never break a URL across lines.

## Lists

- **Unordered lists use `-`**, not `*` or `+`. Consistent across the project.
- **Ordered lists use `1.`** for every item (markdown auto-numbers). This prevents diff noise when reordering.
- **Indent nested lists by 2 spaces** (not 4).
- **No blank line between simple list items** (single-line items). Blank lines between complex items (multi-line content).

## Tables

- **Use tables for key-value and tabular data.** When you have two or more `**Label:** value` items that form a set (metadata, properties, summaries), put them in a table. Consecutive bold-label lines without blank lines between them render as a single paragraph in GitHub. Tables avoid this and are easier to scan.
- **Always include the header separator row** (`|---|---|`).
- **Align pipes** for readability in source, but this is a preference not a requirement.
- **No empty cells.** Use `—` or `N/A` explicitly.
- **Keep tables under 6 columns** where possible. Wider tables are hard to read in source and may not render well.

## Code blocks

- **Always specify the language** after the opening fence: ` ```python `, ` ```json `, ` ```bash `, etc.
- **Never use indented code blocks** (4-space indent). Always use fenced blocks (triple backtick).
- **Inline code** for short references: `function_name`, `file.txt`, `--flag`. Not for emphasis.
- **No syntax errors in code blocks.** If showing a template with placeholders, use `[placeholder]` or `{{placeholder}}` syntax, not broken code.

## Links

- **Descriptive link text.** "See the [deployment guide](url)" not "click [here](url)".
- **Reference links for repeated URLs.** If the same URL appears 3+ times, use `[text][ref]` with `[ref]: url` at the bottom.
- **Relative paths for in-repo links.** `[ADRs](../architecture/adr/)` not `https://github.com/org/repo/tree/main/docs/architecture/adr/`.

## Frontmatter

- **YAML frontmatter** uses `---` delimiters (not `+++`).
- **Blank line after closing `---`** before document content.
- **Quote string values** that contain colons, special characters, or could be misinterpreted as YAML types.

## GitHub-specific

- **Task lists** use `- [ ]` and `- [x]` (with a space inside brackets).
- **Alerts/callouts** use the `> [!NOTE]`, `> [!WARNING]`, `> [!IMPORTANT]` syntax.
- **Mermaid diagrams** in fenced blocks: ` ```mermaid `.
- **Emoji shortcodes** (``:warning:``) are acceptable but not required. Plain text is always fine.
