# Test: Persona definition

Scenario: Testing whether the persona-definition skill requires evidence-based personas with validated segments, and explicitly prohibits demographic stereotyping.

## Prompt


/ux-researcher:persona-definition for the primary users of our project management tool — we think we have 3-4 distinct user types based on how they use the product differently.

## Criteria


- [ ] PASS: Skill requires an evidence inventory step before writing personas — existing research, analytics, interviews, or support data must be catalogued first
- [ ] PASS: Skill explicitly prohibits basing personas on demographic stereotypes — age, gender, and background are not valid differentiators unless backed by evidence
- [ ] PASS: Skill requires segment validation — each persona must be supported by a meaningful cluster of real user behaviour, not just intuition
- [ ] PASS: Skill requires each persona to describe goals, pain points, and behaviours — not just a demographic profile with a stock photo description
- [ ] PASS: Skill includes a validation checklist to verify personas are grounded in evidence, not assumptions
- [ ] PARTIAL: Skill requires a jobs-to-be-done or goals section per persona that is solution-agnostic — partial credit if goals are required but they could be solution-specific
- [ ] PASS: Skill warns against creating too many personas — and provides guidance on when sub-segments should be merged vs kept separate
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's evidence inventory step is shown — what existing data sources are available (interviews, analytics, support tickets, churn data, onboarding surveys) — and what data is MISSING for confident segmentation
- [ ] PASS: Output's segmentation is grounded in observed BEHAVIOUR — how users actually use the product, what they accomplish, what they avoid — NOT demographics (age / gender / job title alone)
- [ ] PASS: Output produces 2-4 personas — the team's hypothesis is "3-4 distinct user types" but the skill validates this; might consolidate to 2 if the data shows two clusters with genuine differentiation, or fan out to 4 if more are evidence-backed
- [ ] PASS: Output's personas each have goals (what they're trying to achieve), pain points (current frustrations), and behaviours (what they do in the product) — not stock photos with demographic profiles
- [ ] PASS: Output explicitly prohibits stereotyping — does not use age, gender, or background as differentiators unless behaviour patterns demonstrably correlate with them in the data
- [ ] PASS: Output's jobs-to-be-done per persona are solution-agnostic — describe what the user is trying to accomplish (e.g. "report status to my exec team weekly") not "use the dashboard"
- [ ] PASS: Output's validation checklist includes evidence trail per persona — for each persona attribute, what's the evidence (interview quote, analytics segment, support pattern), and what would falsify the persona
- [ ] PASS: Output flags any persona attribute that's currently an assumption rather than evidence-backed — clearly marked, with the recommendation to validate before relying on it for product decisions
- [ ] PASS: Output's persona names are descriptive of the role + behaviour, not stereotyped first names — e.g. "The Reporting-Heavy Operations Director" rather than "Sarah, 38, mum of two from Leeds"
- [ ] PARTIAL: Output addresses anti-personas or non-target users — who the product is explicitly NOT for (e.g. "freelancers using project management for personal task tracking") so product decisions don't try to please everyone
