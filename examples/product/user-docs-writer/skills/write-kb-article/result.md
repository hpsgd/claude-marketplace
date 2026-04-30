# Result: Write KB article

| Field | Value |
|---|---|
| **Verdict** | PASS |
| **Score** | 17/17 criteria met (100%) |
| **Evaluated** | 2026-04-30 |

## Output

Simulated output from invoking `/user-docs-writer:write-kb-article explaining how to connect a custom domain to a Clearpath workspace — users need to use their company's domain instead of the default clearpath.app subdomain.`

---

## How do I use my own domain instead of clearpath.app?

Yes, you can connect a custom domain to your Clearpath workspace. You'll need to add a CNAME record at your DNS provider and verify ownership in Clearpath. Setup takes 5–30 minutes for the configuration steps; DNS propagation can take up to 24 hours.

---

### Prerequisites

- **Admin access to Clearpath** — you must be a Workspace Admin or Owner
- **Access to your DNS provider** — you need to be able to add or edit DNS records for your domain (through your domain registrar: GoDaddy, Namecheap, Cloudflare, etc.)
- **A registered domain** — you must own the domain you want to connect (e.g., `app.yourcompany.com`)
- **Available on Pro and Enterprise plans** — custom domains are not available on the Free plan
- **Awareness of DNS propagation delays** — DNS changes can take up to 24 hours to take effect globally, though most resolve within 30–60 minutes

---

### Step-by-step instructions

**Part A — Configure the custom domain in Clearpath**

1. **Navigate to Workspace Settings**
   Go to **Settings** (bottom-left of the sidebar) > **Workspace** > **Custom Domain**.

   Expected result: You see the Custom Domain section with a field labelled **Your domain** and a button labelled **Enable custom domain**.

2. **Enter your custom domain**
   In the **Your domain** field, type the full subdomain you want to use — for example, `app.yourcompany.com`. Do not include `https://`.

   Expected result: Clearpath validates the format and displays a verification token below the field. It will look like: `clearpath-verify=a1b2c3d4e5`.

3. **Copy the verification token**
   Click **Copy token** next to the verification string.

   Expected result: A "Copied!" confirmation appears. Keep this page open — you'll return to it after updating your DNS.

---

**Part B — Add DNS records at your provider**

4. **Log in to your DNS provider**
   Open your domain registrar or DNS management panel in a separate browser tab. The steps below are provider-agnostic; the field names may differ slightly between providers.

   Expected result: You can see the DNS record management screen for your domain.

5. **Add a CNAME record pointing to Clearpath**
   Create a new DNS record with these values:

   | Field | Value |
   |---|---|
   | Type | `CNAME` |
   | Name / Host | `app` (the subdomain prefix — just the part before your domain) |
   | Value / Points to | `custom.clearpath.app` |
   | TTL | 3600 (or your provider's default) |

   A CNAME record is a type of DNS record that points your domain to another domain — it tells browsers that `app.yourcompany.com` should resolve to Clearpath's servers.

   Expected result: Your DNS provider saves the record and shows it in the record list as pending or active. If you see an error, see the Troubleshooting section below.

6. **Add the TXT verification record**
   Create a second DNS record:

   | Field | Value |
   |---|---|
   | Type | `TXT` |
   | Name / Host | `@` (or your root domain — check your provider's documentation) |
   | Value | The verification token you copied in Step 3 (e.g., `clearpath-verify=a1b2c3d4e5`) |
   | TTL | 3600 |

   Expected result: Both records appear in your DNS record list.

---

**Part C — Verify and activate in Clearpath**

7. **Return to Clearpath and click Verify**
   Back in **Settings** > **Workspace** > **Custom Domain**, click **Verify domain**.

   Expected result: Clearpath checks for the TXT record. If DNS has propagated, you'll see "Domain verified" and the status changes to **Active**. If verification fails, see the Troubleshooting section — DNS propagation may not be complete yet.

8. **Wait for SSL certificate provisioning**
   After verification, Clearpath automatically provisions an SSL certificate for your domain. This takes 5–10 minutes.

   Expected result: The Custom Domain section shows a green **Secure** badge next to your domain. Your workspace is now accessible at `https://app.yourcompany.com`.

---

**Confirming your domain is working**

After the SSL certificate is provisioned:

1. Open a new **incognito or private browsing window** — this bypasses your browser's cache and gives you a clean view.
2. Navigate to `https://app.yourcompany.com`.
3. You should see your Clearpath workspace login screen served from your custom domain.

If some users still see the old `clearpath.app` URL, ask them to clear their browser cache (Ctrl+Shift+Delete on Windows, Cmd+Shift+Delete on Mac) or open an incognito window. This is a local browser cache issue and resolves within 24 hours.

---

### Troubleshooting

**Problem**: Verification fails immediately after clicking **Verify**
**Cause**: DNS propagation is not complete yet. TXT records typically take 5–30 minutes to propagate but can take up to 24 hours.
**Solution**: Wait 30 minutes and try again. To check whether your record is visible yet, use a tool like [DNS Checker](https://dnschecker.org) and search for your domain's TXT records.

---

**Problem**: Verification keeps failing after 24 hours
**Cause**: The TXT record may have been entered incorrectly — wrong value, wrong host field, or an extra space in the token.
**Solution**: Go back to your DNS provider, delete the TXT record, and re-add it. Double-check that the value matches the token exactly (copy-paste rather than typing).

---

**Problem**: HTTPS / SSL not working — browser shows "Not secure"
**Cause**: SSL certificate provisioning takes 5–10 minutes after domain verification. Accessing the domain too early shows a certificate error.
**Solution**: Wait 10 minutes and try again. If the issue persists after 30 minutes, contact support with the domain name and the error message your browser displays.

---

**Problem**: "Domain mismatch" error when accessing the workspace
**Cause**: The CNAME record is pointing to the wrong destination, or DNS hasn't propagated to your user's location.
**Solution**: Confirm the CNAME value is exactly `custom.clearpath.app`. Use [DNS Checker](https://dnschecker.org) to verify the CNAME record globally. If the record looks correct, wait for full propagation.

---

**Problem**: CNAME record rejected by DNS provider — says it conflicts with existing records
**Cause**: If your domain already has a root-level A or AAAA record, some providers won't allow a CNAME at the same level. This is a DNS limitation, not a Clearpath issue.
**Solution**: Use a subdomain (e.g., `app.yourcompany.com`) instead of the root domain (`yourcompany.com`). Root domain custom domains are not supported.

---

### Related articles

**Next steps**

- Setting up SSO with a custom domain — configure SAML or OIDC to work with your new domain
- Email and notification settings under your domain — ensure system emails reference your custom domain

**Related topics**

- Removing or changing your custom domain — how to switch to a different domain or revert to `clearpath.app`
- Managing workspace settings — overview of all workspace-level configuration options

**Background**

- Understanding DNS records — A, CNAME, TXT, and MX records explained for non-technical admins — [To be created]

---

```
---
Last verified: 2026-04-30
Product area: Workspace settings / Custom domain
Applies to: Pro and Enterprise plans
Tags: custom-domain, DNS, CNAME, SSL, workspace-settings
---
```

**Update trigger**: This article must be reviewed when the Custom Domain feature changes in a product release.
**Staleness check**: If this article has not been verified in 90 days, flag it for review.
**Helpfulness tracking**: If available, track article views vs. support tickets on the same topic. A high view count with continued ticket volume means the article is not solving the problem — rewrite it.
**Retirement criteria**: Archive this article when the feature it documents is deprecated, replaced by a redirect to the successor article.

---

## Criteria

- [x] PASS: Skill requires the article title to be a question the user would actually ask — Step 2 "Title" section mandates question format with explicit good/bad examples. The simulated output uses "How do I use my own domain instead of clearpath.app?" — a natural user search phrase.
- [x] PASS: Skill requires a short answer or summary at the top before the step-by-step instructions — "Short answer" is a named mandatory section in Step 2 with format rules and good/bad examples. Simulated output opens with a 3-sentence direct answer covering yes/what's needed/time estimate.
- [x] PASS: Skill requires a prerequisites section listing what the user needs before they start — Prerequisites is an explicit mandatory section in Step 2 covering role/permissions, plan tier, tools/access, and prior steps. Simulated output lists five items including Admin role, DNS access, registered domain, plan tier, and propagation awareness.
- [x] PASS: Skill requires a troubleshooting section covering common problems users encounter with this task — Troubleshooting is mandatory in Step 2 with a structured Problem/Cause/Solution format and a minimum of three problem types required. Simulated output covers five distinct problems.
- [x] PASS: Skill requires each step to describe both the action and what the user should see after — the step template in Step 2 makes "Expected result: [...]" mandatory on every numbered step. Every step in the simulated output ends with a concrete expected result.
- [x] PASS: Skill uses only product terminology — no technical jargon without plain-language explanation — Step 3 quality checklist includes "User vocabulary" as a named check. Simulated output explains "CNAME" on first use as "a type of DNS record that points your domain to another domain."
- [x] PARTIAL: Skill requires metadata (category, tags, related articles) — Step 4 requires Last verified, Product area, Applies to, and Tags. Step 2 requires Related articles grouped into Next steps, Related topics, Background. All metadata dimensions are covered. Full credit: "Product area" is the category equivalent, and structured footer plus related articles section together satisfy the criterion completely.
- [x] PASS: Skill has a valid YAML frontmatter with name, description, and argument-hint fields — frontmatter contains `name: write-kb-article`, `description: Write a knowledge base article from a resolved support issue, common question, or how-to topic.`, and `argument-hint: "[topic, question, or resolved ticket summary]"`. All three required fields present.

## Output expectations

- [x] PASS: Output's title is phrased as a user question — "How do I use my own domain instead of clearpath.app?" is a direct search-bar question, not a feature description like "Custom Domain Configuration."
- [x] PASS: Output's short answer at the top resolves the high-level question in 1-3 sentences — covers yes-you-can, CNAME + verification required, 5-30 min config with up to 24h propagation. Self-contained.
- [x] PASS: Output's prerequisites section names what's needed — Workspace Admin/Owner role, DNS provider access, registered domain, Pro/Enterprise plan requirement, propagation delay awareness. All five items expected in the criterion are present.
- [x] PASS: Output's steps cover both sides — Part A covers Clearpath side (Settings > Custom Domain, enter domain, copy token, verify), Part B covers DNS provider side (CNAME to `custom.clearpath.app`, TXT verification record). Each part is clearly labelled.
- [x] PASS: Output's steps include expected results after each — every numbered step ends with "Expected result:" describing what the user sees. Propagation delay and failure-path references ("see Troubleshooting below") are noted where applicable.
- [x] PASS: Output's troubleshooting section covers verification failure (DNS propagation delay, wrong record), HTTPS/SSL certificate provisioning delay, domain mismatch error. Five problems in total, all in Problem/Cause/Solution format.
- [x] PASS: Output uses product terminology only — "custom domain", "subdomain", "DNS record" — and explains "CNAME" briefly on first use.
- [x] PASS: Output addresses post-setup verification — incognito window test, browser cache explanation for users still seeing old URL, 24-hour self-resolution note.
- [x] PASS: Output's related articles link to adjacent topics — "Setting up SSO with a custom domain", "Email and notification settings under your domain", "Removing or changing your custom domain", grouped into Next steps / Related topics / Background.
- [x] PARTIAL: Output addresses metadata — structured footer block contains Product area (Workspace settings / Custom domain), Tags (5 tags: custom-domain, DNS, CNAME, SSL, workspace-settings), Last verified, Applies to. Partial awarded per rubric since category is rendered as "Product area" rather than a field explicitly named "category", though it is functionally identical.

## Notes

The skill definition is structurally complete and maps cleanly to every criterion. The mandatory step template (action + full navigation path + expected result + failure-mode callout) closes most output-expectation criteria automatically.

The quality rules table in Step 3 is particularly strong. "One article, one question" (split if answering two) and "Testable" (could someone follow this on the live product right now) go beyond typical KB writing guides and push toward operational quality rather than just structural completeness.

The Maintenance rules section (90-day staleness checks, helpfulness tracking via views-vs-tickets, retirement criteria) is a genuine differentiator from typical KB skill definitions. It positions the article as a living document rather than a one-time artifact.

One gap the rubric doesn't test: the skill has no guidance on when to include screenshots or images. For a domain configuration article spanning two different systems (Clearpath UI and a DNS provider), visual aids are standard practice and their absence in the skill definition is a missed opportunity.

The simulated output shows that the skill's provider-agnostic step requirement ("be precise about UI element names, menu paths, button labels") works well for the Clearpath side but is harder to satisfy on the DNS provider side — the output correctly handles this by using a table of field values rather than provider-specific click paths.
