# Output: Persona definition

**Verdict:** PASS
**Score:** 17/18 criteria met (94%)
**Evaluated:** 2026-04-29

## Results

### Criteria

- [x] PASS: Skill requires an evidence inventory step before writing personas — Step 1 mandates cataloguing existing research, analytics, interviews, and support data before defining any attributes
- [x] PASS: Skill explicitly prohibits basing personas on demographic stereotypes — Rules section states "Age, gender, and job title do not predict product decisions" and "Never use a human name for a persona"
- [x] PASS: Skill requires segment validation — Step 2 requires both a decision test and assignment test; segments must be defined by behaviour and goals, not demographics
- [x] PASS: Skill requires each persona to describe goals, pain points, and behaviours — Step 3 template mandates Goals (ranked), Frustrations (ranked), and Behaviour Patterns sections
- [x] PASS: Skill includes a validation checklist — Step 4 is a mandatory five-item checklist with explicit pass/fail criteria including evidence threshold and no-stereotypes checks
- [~] PARTIAL: Skill requires a jobs-to-be-done or goals section that is solution-agnostic — Goals section requires "what success looks like in THEIR words" with evidence backing, which nudges toward outcome orientation. However, the skill does not explicitly prohibit solution-specific framing in goal statements; a compliant persona could still write "use the dashboard to check status" and satisfy the template. Goals are required and evidence-backed, but solution-agnostic framing is implied rather than enforced
- [x] PASS: Skill warns against creating too many personas and provides merge guidance — Rules section states "3–5 personas maximum" with explicit rule: "If two personas would make the same product decisions, merge them." Step 2 enforces the same merge decision at segment validation time
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — all three fields present and well-formed

### Output expectations

- [x] PASS: Output's evidence inventory step is shown with data sources and gaps — Step 1 produces a structured table with source, type, volume, and recency; rules require flagging thin evidence and prohibit inventing attributes to fill gaps
- [x] PASS: Output's segmentation is grounded in observed behaviour — Step 2 explicitly requires "distinguishing behaviours" as the differentiator; the Rules section reinforces that demographics don't predict product decisions
- [x] PASS: Output produces 2-4 personas — the 3–5 maximum rule validates the team's hypothesis of 3-4; the decision-test merge rule could consolidate to fewer if evidence clusters warrant it
- [x] PASS: Output's personas each have goals, pain points, and behaviours — Step 3 template mandates all three with evidence citations per attribute, explicitly not demographic profiles
- [x] PASS: Output explicitly prohibits stereotyping — Rules section and Step 4 checklist both enforce behaviour-over-demographics; Step 2 states demographics are not valid segment differentiators
- [x] PASS: Output's jobs-to-be-done per persona are solution-agnostic — Goals section specifies "what success looks like in THEIR words" with evidence backing, oriented toward the user's context
- [x] PASS: Output's validation checklist includes evidence trail per persona — Step 4 includes "Is every attribute backed by at least 3 data points?" and Step 3 template requires an evidence source on every attribute row
- [x] PASS: Output flags assumption-based attributes — rules flag personas with fewer than 3 data points as "hypothesis — needs validation" and prohibit inventing attributes to fill gaps
- [x] PASS: Output's persona names are descriptive of role and behaviour, not stereotyped first names — Step 3 template shows `[descriptive archetype name — e.g., "First-time evaluator" not "Sarah"]`; Rules state never use a human name
- [x] PASS: Output addresses anti-personas — Anti-Persona Signals is a mandatory section in Step 3 and the Rules state "Anti-persona signals are mandatory. Knowing who is NOT this persona is as valuable as knowing who is." The section captures disqualifying signals per persona

## Notes

The skill is well-structured and enforces its key principles mechanically rather than relying on the practitioner to remember them. The evidence-first sequencing (Step 1 before any attributes), the mandatory merge tests in Step 2, and the validation checklist in Step 4 create real process gates rather than just guidelines.

The one genuine gap is the solution-agnostic framing for goals. The "in THEIR words" instruction is doing meaningful work but without an explicit prohibition — something like "goals must describe what the user is trying to accomplish, not what they do in the product" — a compliant persona could slip into feature-referencing goal statements. This is the only reason the PARTIAL criterion applies.

Anti-Persona Signals are mandatory at the persona-segment level (who is not this persona) rather than at the product level (who the product is not for as a category). The test case example of "freelancers using project management for personal task tracking" is a product scope decision. The skill covers the narrower per-segment boundary, which partially addresses this intent; the product-level framing would require an additional step or output section.
