# Test: Write KB article

Scenario: Testing whether the write-kb-article skill requires a question-format title, short answer first, prerequisites, and a troubleshooting section.

## Prompt


/user-docs-writer:write-kb-article explaining how to connect a custom domain to a Clearpath workspace — users need to use their company's domain instead of the default clearpath.app subdomain.

A few specifics for the response:

- **Plain-language gloss for any acronym on first use**: when CNAME first appears, add `(a CNAME record is a type of DNS record that points your domain to another domain)`. Same treatment for DNS, TTL, SSL on first use.
- **Prerequisites section** (its own heading) must list all four: admin/Owner role in Clearpath, admin access to the customer's DNS provider, the custom domain already registered (purchased), awareness that DNS changes can take up to 24 hours to propagate.
- **Troubleshooting section** must cover all four cases: (1) verification fails — DNS propagation delay, (2) verification fails — CNAME pointing wrong, (3) verification fails — conflicting existing A/AAAA record on the same hostname, (4) HTTPS/SSL not working — certificate provisioning takes 5-10 min after verification, (5) "domain mismatch" error and what causes it.
- **Post-setup verification** must include testing in incognito / private browsing to bypass cache, AND guidance for the case where some users still see the old URL because of their browser cache (hard refresh + incognito).

## Criteria


- [ ] PASS: Skill requires the article title to be a question the user would actually ask — not a feature description
- [ ] PASS: Skill requires a short answer or summary at the top before the step-by-step instructions
- [ ] PASS: Skill requires a prerequisites section listing what the user needs before they start
- [ ] PASS: Skill requires a troubleshooting section covering common problems users encounter with this task
- [ ] PASS: Skill requires each step to describe both the action and what the user should see after — not just the action
- [ ] PASS: Skill uses only product terminology — no technical jargon without plain-language explanation
- [ ] PARTIAL: Skill requires metadata (category, tags, related articles) — partial credit if related articles are required but category/tag metadata is not
- [ ] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields

## Output expectations

- [ ] PASS: Output's title is phrased as a user question — "How do I use my own domain instead of clearpath.app?" or "Can I connect a custom domain to my workspace?" — not "Custom Domain Configuration" or "Domain Mapping"
- [ ] PASS: Output's short answer at the top resolves the high-level question in 1-3 sentences — "Yes, you can connect a custom domain. You'll need to add a CNAME record at your DNS provider and verify ownership in Clearpath. Setup takes 5-30 minutes depending on DNS propagation."
- [ ] PASS: Output's prerequisites section names what's needed — admin access to Clearpath, admin access to the customer's DNS provider, the custom domain registered, awareness that DNS changes can take up to 24 hours
- [ ] PASS: Output's steps cover both sides — Clearpath side (enable custom domain in workspace settings, copy verification token) AND DNS provider side (add CNAME record pointing to clearpath app) — clearly labelled with provider-agnostic instructions
- [ ] PASS: Output's steps include expected results after each — e.g. "Step 4: Add the CNAME record. After saving, your DNS provider should show the record as 'pending' or 'active'" — not just the action
- [ ] PASS: Output's troubleshooting section covers — verification fails (DNS propagation delay, CNAME pointing wrong, conflicting record), HTTPS / SSL not working (certificate provisioning takes 5-10 minutes after verification), domain mismatch error
- [ ] PASS: Output uses product terminology only — "custom domain", "subdomain", "DNS record" — and explains "CNAME" briefly the first time as "a type of DNS record that points your domain to another domain"
- [ ] PASS: Output addresses the post-setup verification — how the user confirms their domain is now working, including testing in incognito to bypass cache, and what to do if some users still see the old URL (browser cache)
- [ ] PASS: Output's related articles link to adjacent topics — "Setting up SSO with a custom domain", "Email and notification settings under your domain", "Removing or changing your custom domain" — anticipating next steps
- [ ] PARTIAL: Output addresses metadata — category (e.g. "Workspace settings"), tags (e.g. "custom-domain", "DNS", "SSL"), and related articles in a structured frontmatter or footer block
