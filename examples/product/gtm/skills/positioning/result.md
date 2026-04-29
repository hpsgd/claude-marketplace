# Output: Positioning

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17.5/18 criteria met (97.2%) |
| **Evaluated** | 2026-04-29 |

## Results

### Criteria

- [x] PASS: April Dunford framework — Steps 1-5 map exactly to Dunford's sequence: competitive alternatives → unique attributes → value mapping → target customer → market category. The skill states "Follow the five steps below in exact order — the sequence matters" and provides a rationale for the ordering.
- [x] PASS: Competitive alternatives as anchor — Step 1 is mandatory first. The "Why this order matters" section explicitly states "Most positioning exercises start with the market category... This is wrong" and enforces alternatives-first.
- [x] PASS: Unique attributes relative to alternatives — Step 2 requires attributes be "Unique — the alternative genuinely lacks this, not 'we do it slightly better'." Rules require specificity over general claims ("3-step setup vs. 12-step wizard" not "better UX") and mapping to named alternatives from Step 1.
- [x] PASS: Attributes mapped to specific value — Step 3 uses a four-column table (unique attribute → capability → outcome → business impact). Rules require customer-language framing and quantification: "Save 10 hours per week beats Save time."
- [x] PASS: Complete canvas before messaging — Step 6 assembles the positioning canvas as the first element, before the positioning statement, tagline, and sales narrative are written.
- [x] PASS: Validation questions — Step 7 is a dedicated required section with a structured table that tests each positioning step and includes "If 'no'" remediation guidance per question.
- [~] PARTIAL: Sales narrative — Step 6 includes a required "Sales narrative" section with an explicit 3-sentence template (problem → outcome → unique attribute). Fully present as a required structured output. Scoring at 0.5 per PARTIAL convention.
- [x] PASS: All output labelled DRAFT — Rules section states: "All output is DRAFT until human-reviewed. Label every output with 'DRAFT — requires human review' at the top and bottom." Explicit and required.
- [x] PASS: Valid YAML frontmatter — frontmatter contains `name: positioning`, `description`, and `argument-hint: "[product or feature to position]"` fields.

### Output expectations

- [x] PASS: Competitive alternatives listed first — Step 1 is mandatory before any other step. The skill requires listing direct competitors, adjacent competitors, manual processes, status quo, and in-house solutions with a minimum of five alternatives.
- [x] PASS: Unique attributes are differentiating relative to alternatives, concrete and verifiable — Step 2 requires attributes be "Factually true," "Verifiable," and "Unique." Rules explicitly discard table stakes and vague claims, and require specificity tied to named alternatives from Step 1.
- [x] PASS: Each unique attribute maps to specific customer value — Step 3 four-column table (attribute → capability → outcome → business impact) with quantifiable outcomes required.
- [x] PASS: Target customer is precise — Step 4 requires company characteristics, buyer role, trigger, current behaviour, must-haves, and deal-breakers. The example "Mid-market SaaS companies with 50-200 employees who have outgrown spreadsheet-based customer tracking" demonstrates the expected specificity level.
- [x] PASS: Market category named explicitly — Step 5 requires naming a category using one of three explicit strategies, with a rule against categories that require explanation and a "Google test" for whether the target customer would search for the term.
- [x] PASS: Positioning canvas covers all five Dunford elements in a structured layout — Step 6 assembles a structured canvas with labelled sections for all five elements before any copy is written.
- [x] PASS: Validation questions test whether real customers will recognise the positioning — Step 7 questions include "Would your best customers agree with the competitive alternatives list?" with the remediation "Talk to customers," indicating the test is customer-grounded, not internal.
- [x] PASS: Sales narrative follows the canvas — the 3-sentence template in Step 6 follows: problem in customer words → outcome not feature → unique attribute alternatives lack. This sequence matches the requirement.
- [x] PASS: Every customer-facing tagline / message draft labelled DRAFT — the blanket rule "Label every output with 'DRAFT — requires human review' at the top and bottom" covers all output including the tagline in Step 6.
- [~] PARTIAL: Output addresses where the canvas may shift on pricing — partially met: business model (pricing, packaging, terms) is listed as a category of unique attributes in Step 2, which means a per-seat add-on price could surface as an attribute. However, there is no explicit prompt to reason about what pricing signals to the market or how the pricing tier interacts with the market category choice. An operations director evaluating a $15/seat add-on versus bundled platform reporting would weigh this differently, and the skill does not surface that interaction.

## Notes

The Dunford framework is implemented faithfully. The "Why this order matters" intro is a genuine quality signal — it pre-empts the most common positioning mistake rather than just listing steps.

Step 3's four-column value chain (attribute → capability → outcome → business impact) is more rigorous than frameworks that stop at "benefit." The distinction forces specificity that prevents generic claims from passing unchallenged.

The only substantive gap is the pricing-canvas interaction. For an add-on product positioned against bundled platform reporting, the price tier communicates something about the buyer's perceived value and affects which market category lands credibly. The skill touches business model as an attribute category but does not prompt the practitioner to reason about what their pricing signals to the market.
