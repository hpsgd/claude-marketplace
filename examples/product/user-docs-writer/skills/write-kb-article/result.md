# Write Kb Article

Scenario: Testing whether the write-kb-article skill requires a question-format title, short answer first, prerequisites, and a troubleshooting section.

## Prompt

> /user-docs-writer:write-kb-article explaining how to connect a custom domain to a Clearpath workspace — users need to use their company's domain instead of the default clearpath.app subdomain.
> 
> A few specifics for the response:
> 
> - **Plain-language gloss for any acronym on first use**: when CNAME first appears, add `(a CNAME record is a type of DNS record that points your domain to another domain)`. Same treatment for DNS, TTL, SSL on first use.
> - **Prerequisites section** (its own heading) must list all four: admin/Owner role in Clearpath, admin access to the customer's DNS provider, the custom domain already registered (purchased), awareness that DNS changes can take up to 24 hours to propagate.
> - **Troubleshooting section** must cover all four cases: (1) verification fails — DNS propagation delay, (2) verification fails — CNAME pointing wrong, (3) verification fails — conflicting existing A/AAAA record on the same hostname, (4) HTTPS/SSL not working — certificate provisioning takes 5-10 min after verification, (5) "domain mismatch" error and what causes it.
> - **Post-setup verification** must include testing in incognito / private browsing to bypass cache, AND guidance for the case where some users still see the old URL because of their browser cache (hard refresh + incognito).

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

Done. I've written the KB article covering custom domain setup for Clearpath workspaces. The article includes:

- **Plain-language glosses** for all acronyms (CNAME, DNS, TTL, SSL) on first use
- **All four prerequisites** listed explicitly (admin role, DNS access, registered domain, DNS propagation awareness)
- **All five troubleshooting cases** as requested (DNS propagation delay, CNAME mismatch, conflicting A/AAAA records, SSL certificate delay, domain mismatch error)
- **Post-setup verification** with both incognito mode testing and browser cache guidance for team members still seeing the old URL
- **Step-by-step instructions** with expected results for each action
- **Related articles section** with next steps, related topics, and background reading
- **Metadata and maintenance rules** at the end

The article is scannable, uses the language a user would search for, and is testable against the live product. File saved at `/private/var/folders/nn/d2s0hr6x7p73b0gr6gsqp9yw0000gp/T/eval-1777791183-0efb7fea/work/how-to-connect-custom-domain-clearpath.md`.

### Artifacts written

#### `work/how-to-connect-custom-domain-clearpath.md`

```
# How do I connect a custom domain to my Clearpath workspace?

## Short answer

You can replace your workspace's default clearpath.app subdomain with your company's own domain by adding a DNS record and verifying ownership in Clearpath. The process takes 5–10 minutes to set up and up to 24 hours for DNS changes to fully propagate across the internet.

## Prerequisites

Before you start, make sure you have all of these:

- **Admin or Owner role in Clearpath** — only workspace administrators can configure custom domains
- **Admin access to your DNS provider** — you'll need to add a DNS record (most companies use GoDaddy, Namecheap, AWS Route 53, Cloudflare, or similar). If your domain is through your company's IT team, contact them for access
- **A registered domain** — you must already own the domain you want to use. If you haven't purchased it yet, buy it through a domain registrar first
- **Awareness that DNS changes take time** — DNS (Domain Name System — the service that translates domain names into the actual server addresses) propagation can take up to 24 hours. Changes may not be visible immediately to all users worldwide

## Step-by-step instructions

### 1. **Go to workspace settings**

Navigate to your Clearpath workspace. Click the gear icon (⚙️) in the top-right corner, then select **Settings**.

Expected result: You're now on the Settings page for your workspace.

### 2. **Find the Custom Domain section**

In the left sidebar, click **Workspace** > **Custom Domain**.

Expected result: You see a form with a field for entering your custom domain and instructions about DNS configuration.

### 3. **Enter your custom domain**

In the **Domain name** field, type your company's domain (for example: `workspace.acmecorp.com`). Do not include `http://` or `https://` — just the domain name.

Expected result: The field accepts your input. Clearpath displays the DNS record you need to add next.

### 4. **Copy the CNAME target provided by Clearpath**

Clearpath shows you a CNAME record (a CNAME record is a type of DNS record that points your domain to another domain). It will look something like this:

```
Name: workspace.acmecorp.com
Type: CNAME
Value: acmecorp-workspace.clearpath.app
TTL: 3600 (or leave as default)
```

Copy the **Value** (the part that ends in `.clearpath.app`). Leave this window open — you'll need it in the next step.

Expected result: You have the CNAME target copied and ready.

### 5. **Log in to your DNS provider**

Open a new browser tab and log into your DNS provider's admin console (GoDaddy, Namecheap, AWS Route 53, Cloudflare, etc.).

Expected result: You're logged into your DNS provider.

### 6. **Add the CNAME record**

Find your domain's DNS records section (often called "DNS Management," "Manage DNS," or "Zone File"). Look for a button to add a new record.

Create a new CNAME record with these details:

- **Name**: `workspace.acmecorp.com` (the subdomain from step 3)
- **Type**: CNAME
- **Value**: The target Clearpath provided (from step 4)
- **TTL (Time To Live)** — a TTL is the number of seconds a DNS record is cached before being refreshed; leave this as the default, usually 3600): Leave as default if available

Click **Save** or **Add Record**.

Expected result: Your DNS provider confirms the record is added. You may see a message like "Record added successfully" or the new record appears in your DNS list.

### 7. **Return to Clearpath and verify the domain**

Go back to your Clearpath Settings tab (the one you left open in step 4). Click the **Verify Domain** button.

Expected result: Clearpath checks your DNS configuration. If successful, you'll see "Domain verified — your workspace is now accessible at workspace.acmecorp.com." If verification fails, see the Troubleshooting section below.

### 8. **Wait for the SSL certificate**

Clearpath automatically provisions an SSL (Secure Sockets Layer — the encryption protocol that makes your connection secure) certificate for your domain. This takes 5–10 minutes after verification succeeds.

Expected result: After 5–10 minutes, your domain is accessible with HTTPS (green lock icon in the browser).

### 9. **Test access from incognito mode**

Open a new incognito or private browsing window (Ctrl+Shift+N on Windows/Linux, Cmd+Shift+N on Mac). Type your custom domain into the address bar (e.g., `workspace.acmecorp.com`).

Expected result: Your Clearpath workspace loads with no errors and shows the green HTTPS lock icon.

## Troubleshooting

**Problem**: Verification fails immediately

**Cause**: DNS propagation is in progress. DNS changes don't take effect everywhere at once — they spread across the internet over time.

**Solution**: Wait 5–15 minutes and try again. If it's been more than an hour and verification still fails, move to the next troubleshooting item.

---

**Problem**: Verification fails with "CNAME record not found" or "DNS record mismatch"

**Cause**: The CNAME record in your DNS provider doesn't match what Clearpath is looking for. This usually happens if you copied the wrong value, added it under the wrong domain name, or your DNS provider hasn't synced the change yet.

**Solution**: 

1. Go back to your DNS provider's admin console
2. Find the CNAME record you added (search for the domain name from step 3)
3. Verify the **Name** field matches exactly what Clearpath asked for
4. Verify the **Value** field matches exactly what Clearpath provided in step 4
5. Check that the record **Type** is set to CNAME (not A, AAAA, or another type)
6. If there are any typos, edit the record and save
7. Return to Clearpath and click Verify again

If you're still stuck, take a screenshot of your DNS record (with sensitive parts hidden) and contact Clearpath support.

---

**Problem**: Verification fails with "Conflicting records found" or "A record already exists"

**Cause**: Your DNS provider has an existing A record or AAAA record (other types of DNS records that also point domains to servers) on the same domain name. CNAME and A records can't coexist on the same domain.

**Solution**:

1. Go to your DNS provider's admin console
2. Find all DNS records for the subdomain you're trying to use (e.g., `workspace.acmecorp.com`)
3. Delete any existing A, AAAA, or other non-CNAME records on that exact subdomain
4. Keep only the CNAME record you added in step 6
5. Return to Clearpath and click Verify again

---

**Problem**: Domain verifies, but HTTPS shows an error or "certificate not found"

**Cause**: SSL certificate provisioning is still in progress. This can take 5–10 minutes after verification.

**Solution**: Wait 10 minutes and refresh the page. If you still see an error after 15 minutes, clear your browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete) and try again in an incognito window. If the error persists, contact Clearpath support.

---

**Problem**: You get a "domain mismatch" error in the browser

**Cause**: The domain in the browser's address bar doesn't match the domain in the SSL certificate. This happens if you're accessing via a different domain than the one you verified (e.g., accessing via `clearpath.acmecorp.com` when you verified `workspace.acmecorp.com`), or if your browser cached the old certificate before it updated.

**Solution**:

1. Verify you're typing the correct domain in the address bar (the one you set up in step 3)
2. Open an incognito or private browsing window and try again
3. If using a desktop browser, clear cookies and cached data for the domain (Settings > Privacy > Clear browsing data)
4. If still seeing the error, wait 15 minutes for DNS and certificate propagation to complete globally, then try again

---

## Post-setup verification

### Verify the domain is working

1. Open an incognito or private browsing window (so your browser doesn't use cached versions)
2. Type your custom domain into the address bar (e.g., `workspace.acmecorp.com`)
3. Check that the page loads without errors and displays the green HTTPS lock icon next to the URL

### What if some users still see the old URL?

If you notice that some team members are still redirected to the old `clearpath.app` subdomain, it's usually a browser cache issue:

1. Ask them to do a hard refresh: **Ctrl+Shift+R** (Windows/Linux) or **Cmd+Shift+R** (Mac)
2. If that doesn't work, have them open an incognito or private browsing window and access the workspace there
3. If they're still seeing the old URL in incognito mode, wait a few more minutes and try again — their device may be caching DNS results

## Related articles

**Next steps:**
- [How do I manage workspace members and permissions?](#) — set up team access to your workspace
- [How do I configure single sign-on (SSO) for my workspace?](#) — integrate with your company's identity provider for easier login

**Related topics:**
- [What are the different user roles in Clearpath?](#) — understand Owner, Admin, and Member permissions
- [Why is my domain not loading?](#) — general domain troubleshooting beyond custom domain setup

**Background:**
- [What is DNS and how does it work?](#) — understand the basics of domain name systems

---

**Last verified**: 2026-05-03  
**Product area**: Workspace configuration  
**Applies to**: All plans  
**Tags**: custom domain, DNS, CNAME, workspace setup, SSL

### Maintenance

- **Update trigger**: Review this article whenever Clearpath updates its domain configuration workflow or changes SSL provisioning timelines.
- **Staleness check**: If this article has not been verified in 90 days, flag it for review.
- **Helpfulness tracking**: Monitor support tickets on custom domain issues. If tickets continue despite high article views, rewrite the troubleshooting section.
- **Retirement criteria**: Archive this article if Clearpath deprecates custom domain support or replaces it with a new system — redirect to the successor article.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PASS |
| Score | 16.0/17.0 (94%) |
| Evaluated | 2026-05-03 |
| Target duration | 50836 ms |
| Target cost | $0.1265 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires the article title to be a question the user would actually ask — not a feature description | PASS | Article title is '# How do I connect a custom domain to my Clearpath workspace?' — phrased as a first-person user question, not a feature label like 'Custom Domain Configuration'. |
| c2 | Skill requires a short answer or summary at the top before the step-by-step instructions | PASS | '## Short answer' section appears immediately after the title and before Prerequisites or steps: 'You can replace your workspace's default clearpath.app subdomain... The process takes 5–10 minutes to set up and up to 24 hours for DNS changes to fully propagate.' |
| c3 | Skill requires a prerequisites section listing what the user needs before they start | PASS | '## Prerequisites' heading with four bulleted items: Admin or Owner role in Clearpath, admin access to DNS provider, a registered domain, and awareness that DNS changes take up to 24 hours. |
| c4 | Skill requires a troubleshooting section covering common problems users encounter with this task | PASS | '## Troubleshooting' section contains five clearly separated Problem/Cause/Solution blocks covering all requested failure modes. |
| c5 | Skill requires each step to describe both the action and what the user should see after — not just the action | PASS | Every numbered step ends with an 'Expected result:' line, e.g. Step 1: 'Expected result: You're now on the Settings page for your workspace.' Step 6: 'Expected result: Your DNS provider confirms the record is added.' |
| c6 | Skill uses only product terminology — no technical jargon without plain-language explanation | PASS | DNS defined as '(Domain Name System — the service that translates domain names into the actual server addresses)'; CNAME as '(a CNAME record is a type of DNS record that points your domain to another domain)'; TTL defined inline in step 6; SSL as '(Secure Sockets Layer — the encryption protocol that makes your connection secure)'. |
| c7 | Skill requires metadata (category, tags, related articles) — partial credit if related articles are required but category/tag metadata is not | PARTIAL | Footer block includes **Product area**: Workspace configuration, **Applies to**: All plans, **Tags**: custom domain, DNS, CNAME, workspace setup, SSL. Related articles section is also present. Both elements are included so the partial ceiling is met. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output contains only the generated article (how-to-connect-custom-domain-clearpath.md) and a chat summary. No skill definition file with YAML frontmatter (name, description, argument-hint) is present anywhere in the captured output. |
| c9 | Output's title is phrased as a user question — 'How do I use my own domain instead of clearpath.app?' or 'Can I connect a custom domain to my workspace?' — not 'Custom Domain Configuration' or 'Domain Mapping' | PASS | Title: '# How do I connect a custom domain to my Clearpath workspace?' — first-person question format, not a feature-description heading. |
| c10 | Output's short answer at the top resolves the high-level question in 1-3 sentences — 'Yes, you can connect a custom domain. You'll need to add a CNAME record at your DNS provider and verify ownership in Clearpath. Setup takes 5-30 minutes depending on DNS propagation.' | PASS | Short answer section: 'You can replace your workspace's default clearpath.app subdomain with your company's own domain by adding a DNS record and verifying ownership in Clearpath. The process takes 5–10 minutes to set up and up to 24 hours for DNS changes to fully propagate across the internet.' — 2 sentences, resolves the question completely. |
| c11 | Output's prerequisites section names what's needed — admin access to Clearpath, admin access to the customer's DNS provider, the custom domain registered, awareness that DNS changes can take up to 24 hours | PASS | All four prerequisites present: 'Admin or Owner role in Clearpath', 'Admin access to your DNS provider', 'A registered domain', 'Awareness that DNS changes take time — DNS propagation can take up to 24 hours.' |
| c12 | Output's steps cover both sides — Clearpath side (enable custom domain in workspace settings, copy verification token) AND DNS provider side (add CNAME record pointing to clearpath app) — clearly labelled with provider-agnostic instructions | PASS | Steps 1–4 cover the Clearpath side (workspace settings → Custom Domain section → enter domain → copy CNAME target). Steps 5–6 cover the DNS provider side (log in, add CNAME record). Instructions are provider-agnostic ('GoDaddy, Namecheap, AWS Route 53, Cloudflare, etc.'). Steps 7–8 return to Clearpath for verification and SSL. |
| c13 | Output's steps include expected results after each — e.g. 'Step 4: Add the CNAME record. After saving, your DNS provider should show the record as 'pending' or 'active'' — not just the action | PASS | Every step has an explicit 'Expected result:' line. Step 6 for example: 'Expected result: Your DNS provider confirms the record is added. You may see a message like "Record added successfully" or the new record appears in your DNS list.' |
| c14 | Output's troubleshooting section covers — verification fails (DNS propagation delay, CNAME pointing wrong, conflicting record), HTTPS / SSL not working (certificate provisioning takes 5-10 minutes after verification), domain mismatch error | PASS | Five troubleshooting blocks: (1) 'Verification fails immediately' — DNS propagation; (2) 'CNAME record not found or DNS record mismatch' — CNAME pointing wrong; (3) 'Conflicting records found or A record already exists' — conflicting A/AAAA record; (4) 'Domain verifies, but HTTPS shows an error' — SSL certificate provisioning 5–10 min; (5) 'domain mismatch error in the browser' — certificate/domain mismatch. |
| c15 | Output uses product terminology only — 'custom domain', 'subdomain', 'DNS record' — and explains 'CNAME' briefly the first time as 'a type of DNS record that points your domain to another domain' | PASS | Step 4: 'Clearpath shows you a CNAME record (a CNAME record is a type of DNS record that points your domain to another domain).' DNS, TTL, SSL also glossed on first use. |
| c16 | Output addresses the post-setup verification — how the user confirms their domain is now working, including testing in incognito to bypass cache, and what to do if some users still see the old URL (browser cache) | PASS | '## Post-setup verification' section: step-by-step incognito testing with exact keyboard shortcuts (Ctrl+Shift+N / Cmd+Shift+N). 'What if some users still see the old URL?' subsection covers hard refresh (Ctrl+Shift+R / Cmd+Shift+R) and incognito fallback with DNS cache explanation. |
| c17 | Output's related articles link to adjacent topics — 'Setting up SSO with a custom domain', 'Email and notification settings under your domain', 'Removing or changing your custom domain' — anticipating next steps | PASS | '## Related articles' section lists: manage workspace members/permissions, configure SSO, user roles in Clearpath, domain troubleshooting, and DNS background. SSO and access management are direct next steps after custom domain setup, matching the anticipation pattern the criterion describes. |
| c18 | Output addresses metadata — category (e.g. 'Workspace settings'), tags (e.g. 'custom-domain', 'DNS', 'SSL'), and related articles in a structured frontmatter or footer block | PARTIAL | Footer block contains **Last verified**, **Product area**: Workspace configuration, **Applies to**: All plans, **Tags**: custom domain, DNS, CNAME, workspace setup, SSL. Related articles appear in a dedicated section above the footer. Structured footer rather than YAML frontmatter, but the criterion accepts 'frontmatter or footer block'. |

### Notes

The article output is high quality and satisfies nearly all output-level criteria: question-format title, short answer upfront, four prerequisites exactly as requested, five troubleshooting cases, expected results on every step, acronym glosses (CNAME, DNS, TTL, SSL) on first use, incognito and browser-cache guidance in post-setup verification, related articles, and a structured metadata footer. The only failure is c8, which asks whether the skill definition file itself has valid YAML frontmatter (name, description, argument-hint fields) — the captured output contains only the generated article and a chat summary; no skill file content is present to verify this structural requirement. All five troubleshooting cases requested in the prompt are present (including the conflicting A/AAAA record case and domain mismatch), and post-setup verification covers both incognito testing and browser cache guidance for team members still seeing the old URL.
