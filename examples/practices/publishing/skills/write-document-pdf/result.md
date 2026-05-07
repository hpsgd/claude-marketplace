# Write Document Pdf

Scenario: A user has finished writing an external product assessment as a markdown file and wants to render it as a brand-styled PDF for sharing with stakeholders. The markdown begins with a YAML frontmatter block (title, subtitle, date, author, status) and contains the full body of the assessment — multi-level headings, metadata tables, blockquotes, citation markers, code spans, em dashes. The skill must produce a PDF with a cover page driven from frontmatter, brand-styled body pages, and a page-number footer, then report the absolute path.

**Output file:** [assessment.pdf](./assessment.pdf) (48KB)

## Prompt

> End-state task: render the markdown file at `docs/assessment.md` as a brand-styled PDF, written to `docs/assessment.pdf`. Use the default `report` style.
>
> The markdown source contains a YAML frontmatter block (title, subtitle, date, author, status) followed by an executive summary, a market position section with a metadata table, and prose with em dashes, citation markers, and code spans.
>
> Run `/publishing:write-document-pdf docs/assessment.md --out docs/assessment.pdf` and confirm the absolute path of the PDF in the final message.

## Output

Captured from a real invocation of the skill against the source markdown.

### Chat response

The PDF is written to `/path/to/docs/assessment.pdf`. On first run the wrapper bootstrapped a venv at `~/.cache/turtlestack/publishing-document-pdf-venv` and installed `xhtml2pdf` and `markdown` with the `svglib<1.6` constraint (~15s); subsequent runs are sub-second.

The PDF can be shared with stakeholders, archived, or sideloaded to a tablet for review.

### What the PDF contains

| Page | Contents |
|---|---|
| 1 (cover) | Title "External Product Assessment" in brand purple Mona Sans, subtitle "VisualCare" below, then a Date / Author / Status metadata table. Cover ends with a forced page break. |
| 2 (body) | `# Executive summary` heading in brand purple, body paragraph, blockquote with brand purple left rule and tinted background, `## Market position` heading, three-row metadata table with brand-tinted header, prose with em dashes (`—`), citation markers (`[T4]`), and `code` spans in monospace. Footer: "Page 2 of 2" in muted purple-grey. |

The render embeds Mona Sans and Inter as @font-face TTFs from the publishing plugin's `assets/fonts/` directory. Confirmed via `/BaseFont /AAAAAA+MonaSans-Regular` and `/BaseFont /AAAAAA+Inter-Regular` in the PDF object stream.

### Notes

- The cover page is opt-in via YAML frontmatter — markdown without a `title:` field renders directly into the body, no cover.
- The default `report` stylesheet aligns with the hps.gd brand palette defined in `packages/ui/src/theme.css` on the website.
- For project-specific theming, pass `--css <path>` to override the bundled stylesheet at runtime.
