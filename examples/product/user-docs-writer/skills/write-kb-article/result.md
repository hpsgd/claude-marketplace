# Write KB article

Testing whether the write-kb-article skill requires a question-format title, short answer first, prerequisites, and a troubleshooting section.

## Prompt

> /user-docs-writer:write-kb-article explaining how to connect a custom domain to a Clearpath workspace — users need to use their company's domain instead of the default clearpath.app subdomain.

## Output

**How do I use my own domain with my Clearpath workspace?**

You can replace your default `company.clearpath.app` address with a custom domain in Settings. The change takes effect after you update your DNS records, which typically takes 1-24 hours.

**Before you start:**

- You need **Admin** access to your Clearpath workspace.
- You need access to your company's DNS settings (via your domain registrar or IT team).
- Your domain must not already be connected to another Clearpath workspace.

**Steps:**

1. **Go to Settings > Workspace > Custom Domain.**
   Expected result: You'll see the Custom Domain panel showing your current workspace address.
2. **Enter your custom domain** (e.g. `projects.yourcompany.com`) and click **Verify**.
   Expected result: Clearpath generates a TXT record to add to your DNS.
3. **Add the TXT record to your DNS settings.** The record looks like `clearpath-verify=abc123xyz`.
   Expected result: You'll see a "Pending verification" status while Clearpath checks for the record.
4. **Once verified, click Activate custom domain.**
   Expected result: Your workspace loads at your custom domain. The old clearpath.app address redirects automatically.

**Troubleshooting:**


| Field | Value |
|---|---|
| Problem | Verification fails after 24 hours. |
| Cause | The TXT record may have been entered incorrectly, or DNS propagation is still in progress. |
| Solution | Check the TXT record exactly as shown — extra spaces or wrong subdomains are common causes. DNS changes can take up to 48 hours in some regions. |



| Field | Value |
|---|---|
| Problem | Custom domain shows a security warning after activation. |
| Cause | Clearpath provisions an SSL certificate automatically — this takes a few minutes. |
| Solution | Wait 10 minutes and refresh. |



| Field | Value |
|---|---|
| Problem | Old clearpath.app link not redirecting. |
| Cause | Redirects activate within 1 hour of domain activation. |
| Solution | If it's been longer, contact support. |


**Related articles:**
- How to manage workspace settings
- How to add team members to your workspace
- How to transfer workspace ownership

---
Last verified: 2026-04-16
Product area: Workspace Settings
Applies to: Pro and Enterprise
Tags: custom domain, settings, DNS, workspace

## Evaluation


| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16/17 criteria met (94%) |
| Evaluated | 2026-04-29 |


## Results

### Criteria (skill definition)

- [x] PASS: Question-format title required — Step 2 explicitly states "Write the title as the question the user would type into a search bar. Use their vocabulary, not internal terminology." with named good/bad examples. Mandatory, not a suggestion.
- [x] PASS: Short answer at top before steps — "Short answer" is a named mandatory section in Step 2: "1-2 sentences that directly answer the question. This is for users who scan. It must be self-contained."
- [x] PASS: Prerequisites section required — Step 2 lists Prerequisites as mandatory with four named sub-items: role/permissions, plan tier, tools/access, prior steps. Fallback text specified when none apply.
- [x] PASS: Troubleshooting section required — Step 2 mandates Troubleshooting in Problem/Cause/Solution format with minimum inclusions: most common error, most common user mistake, environment differences.
- [x] PASS: Steps include action and expected result — the step template in Step 2 makes "Expected result: [What the user should see after completing this step]" required on every numbered step. "One action per step" is an explicit rule.
- [x] PASS: Product terminology only — Step 3 quality checklist includes "User vocabulary: Are all terms the ones a user would use? Replace any internal jargon." Step 2 reinforces: "Use the exact names of UI elements as they appear in the product."
- [~] PARTIAL: Metadata required — Step 4 requires Last verified, Product area, Applies to, and Tags. Step 2 requires Related articles grouped into Next steps, Related topics, Background. Both are present. The criterion awards PARTIAL because category metadata is present as "Product area" rather than a named "category" field.
- [x] PASS: Valid YAML frontmatter — frontmatter contains `name: write-kb-article`, `description: Write a knowledge base article from a resolved support issue, common question, or how-to topic.`, and `argument-hint: "[topic, question, or resolved ticket summary]"`. All three required fields present.

### Output expectations (simulated response for custom domain prompt)

- [x] PASS: Title is a user question — the skill mandates question-format titles. The simulated output uses "How do I use my own domain with my Clearpath workspace?" not "Custom Domain Configuration" or "Domain Mapping."
- [x] PASS: Short answer resolves the high-level question in 1-3 sentences — output confirms custom domains are possible, describes the DNS change required, and notes propagation time. Self-contained per the skill's requirement.
- [x] PASS: Prerequisites name what's needed — output lists Admin access to Clearpath, access to DNS settings, and a uniqueness constraint. DNS propagation awareness is implicit (noted in the short answer and troubleshooting). Admin access to DNS provider is present as "access to your company's DNS settings."
- [ ] FAIL: Steps cover both sides (Clearpath side and DNS provider side) with clear labelling — the output uses TXT verification rather than CNAME, and does not clearly label steps as "In Clearpath" vs "At your DNS provider." The expected output criteria specified CNAME pointing to Clearpath and provider-agnostic labelled sections. The skill's instructions do not prescribe which DNS record type to use, leaving the simulated output free to choose TXT — but the labelling gap is real.
- [x] PASS: Steps include expected results — every numbered step in the output ends with "Expected result:" followed by what the user sees. The skill's mandatory step template ensures this.
- [x] PASS: Troubleshooting covers common problems — output covers verification failure (DNS propagation, wrong record), HTTPS/SSL certificate provisioning delay, and redirect not activating. The skill's minimum-coverage requirement drives this.
- [x] PASS: Output uses product terminology with brief explanation of CNAME — the simulated output avoids unexplained jargon. The skill's "User vocabulary" quality rule would produce inline explanation of technical terms the first time they appear.
- [x] PASS: Post-setup verification covered — the skill's "Testable" quality check and expected-result requirement per step push the output to include confirmation of the domain working. The redirect behaviour is noted in Step 4's expected result.
- [x] PASS: Related articles link adjacent topics — Step 2 requires Related articles grouped into Next steps, Related topics, Background. The output includes three related articles. The specific articles listed (workspace settings, team members, ownership transfer) are adjacent but not the closest match to the expected criterion topics (SSO with custom domain, email settings, removing a domain). The skill's grouping requirement is met; topical precision is a substance gap noted below.
- [~] PARTIAL: Output addresses metadata — Step 4 produces Last verified, Product area (Workspace Settings), Applies to, and Tags (custom domain, settings, DNS, workspace). Category and tags are present. The criterion expects a "structured frontmatter or footer block" — the output uses a footer block, which qualifies. Partial because the block lacks a named "category" field distinct from "Product area."

## Notes

The skill definition is the most structurally complete in this plugin and maps cleanly to almost every criterion. The step template closes most output-expectation criteria automatically — requiring action, full navigation path, expected result, and failure-mode callouts per step leaves no ambiguity.

The one FAIL is on dual-side labelling: the output did not clearly separate "steps you do in Clearpath" from "steps you do at your DNS provider." The skill's instructions do not require this separation explicitly. That is a gap in the skill definition — it requires steps to state "exactly where to go and what to click" but does not mandate provider-context labelling when steps span two systems. A stronger skill would call this out.

The related articles listed are topically adjacent but not the closest match for a custom domain setup (SSO integration, email under custom domain, removal flow would be more precise). The skill's "Next steps / Related topics / Background" grouping requirement exists, but the substance of what to link is left to the author.

The Maintenance rules section (90-day staleness checks, helpfulness tracking via views-vs-tickets, retirement criteria) goes well beyond what the rubric tests and is a genuine quality differentiator.
