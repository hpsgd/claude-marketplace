# Write Kb Article

Scenario: Testing whether the write-kb-article skill requires a question-format title, short answer first, prerequisites, and a troubleshooting section.

## Prompt

> /user-docs-writer:write-kb-article explaining how to connect a custom domain to a Clearpath workspace — users need to use their company's domain instead of the default clearpath.app subdomain.

## Output

Captured from a real headless invocation of the skill/agent.

### Chat response

KB article written to `docs/kb/how-to-connect-custom-domain.md`.

A few things worth flagging given the empty codebase: I had no source code to verify exact UI label names, plan tier names, or the specific CNAME target value (`custom.clearpath.app` is a placeholder). Before publishing, someone with product access should confirm:

- The exact CNAME target Clearpath generates
- Whether the settings path is **Settings > Domains** or something else
- The exact plan names that include custom domains (Pro/Enterprise is a reasonable assumption but needs verification)
- Whether the Owner-only restriction is accurate or if Admins can also do this

The article covers the full flow: enter domain, get CNAME values, add at registrar, verify, SSL auto-provisions. Troubleshooting covers the five most common failure modes including DNS propagation delay, wrong plan tier, SSL provisioning failure, and corporate IT environments.

### Artifacts written

#### `work/docs/kb/how-to-connect-custom-domain.md`

```
# How do I use my own domain instead of the default clearpath.app address?

You can replace your default `yourworkspace.clearpath.app` address with a domain you own — for example, `work.yourcompany.com`. The process takes about 5 minutes, then DNS propagation can add up to 48 hours before the domain is fully live.

## Prerequisites

- You must have the **Owner** role on the workspace. Admins cannot access this setting.
- Custom domains are available on the **Pro and Enterprise plans** only. If you're on the Free or Starter plan, you'll see the setting but won't be able to save changes.
- You need access to your domain's DNS settings. This is usually through your domain registrar (Namecheap, GoDaddy, Cloudflare, etc.) or your IT team.

## Steps

1. **Open your workspace settings**

   Click your workspace name in the top-left corner, then select **Settings** from the dropdown.

   Expected result: The Settings page opens, with a sidebar showing sections including **General**, **Members**, and **Domains**.

2. **Navigate to the Domains section**

   In the left sidebar, click **Domains**.

   Expected result: You see your current workspace URL (`yourworkspace.clearpath.app`) and a section labelled **Custom domain**.

3. **Enter your custom domain**

   In the **Custom domain** field, type the domain or subdomain you want to use. For example: `work.yourcompany.com`.

   Don't include `https://` or a trailing slash. Just the hostname.

   Expected result: A DNS record appears below the field. It will look something like this:

   | Type | Name | Value |
   |------|------|-------|
   | CNAME | `work` | `custom.clearpath.app` |

   Keep this page open. You'll need these values in the next step.

4. **Add the CNAME record at your DNS provider**

   Log in to wherever you manage DNS for your domain and create a new CNAME record using the values from step 3.

   The exact steps vary by provider. In most cases, you're looking for a section called **DNS Management**, **DNS Records**, or **Zone Editor**.

   - **Name/Host**: the value in the Name column (e.g. `work`)
   - **Value/Points to**: `custom.clearpath.app`
   - **TTL**: leave as the default, or set to 300 seconds if you want faster propagation

   Expected result: The record appears in your DNS provider's record list. Changes may take a few minutes to save on their end.

5. **Click Verify domain**

   Back in Clearpath, click the **Verify domain** button below the DNS record table.

   If your DNS change has propagated, the domain status changes to **Verified** and Clearpath begins provisioning an SSL certificate.

   If you see an error, see the Troubleshooting section below. DNS propagation can take up to 48 hours — if you just added the record, wait a few hours and try again.

6. **Confirm SSL is active**

   Once verified, a status indicator will show **SSL active** next to your domain. This can take up to 10 minutes after verification completes.

   Expected result: Your workspace is now accessible at your custom domain with a valid HTTPS certificate. The old `clearpath.app` address continues to work and redirects to your new domain automatically.

## Troubleshooting

**Problem**: Clicking **Verify domain** returns "DNS record not found."
**Cause**: The CNAME record hasn't propagated yet, or was entered incorrectly.
**Solution**: Double-check the Name and Value fields match exactly what Clearpath showed in step 3. Then use a DNS lookup tool (search "DNS lookup" in your browser) to check whether the record is visible publicly. If it's not there, confirm the record was saved at your DNS provider. If the record exists but verification still fails, wait a few hours and try again.

**Problem**: The **Verify domain** button doesn't appear after entering the domain.
**Cause**: Your account is on a plan that doesn't include custom domains.
**Solution**: Go to **Settings > Billing** and check your current plan. Upgrade to Pro to unlock this feature.

**Problem**: You see "SSL provisioning failed" after verification succeeds.
**Cause**: SSL certificate generation failed, usually because the CNAME was removed or changed before the certificate was issued.
**Solution**: Confirm the CNAME record still exists at your DNS provider, then contact Clearpath support. Include your workspace name and the domain you're trying to connect.

**Problem**: The domain shows as verified, but visiting it shows a browser security warning.
**Cause**: The SSL certificate is still being provisioned. This takes up to 10 minutes after verification.
**Solution**: Wait 10 minutes and hard-refresh your browser (`Cmd+Shift+R` on Mac, `Ctrl+Shift+R` on Windows).

**Problem**: You manage DNS through your company's IT team and they need more information.
**Cause**: Some corporate DNS environments require explicit approval or have longer propagation times.
**Solution**: Send your IT team the CNAME record details from step 3. Let them know propagation from their internal DNS may take longer than usual. The Clearpath verification step works as soon as the record is publicly visible.

## Related articles

**Next steps**

- How do I set a custom login page for my workspace? [To be created]
- How do I require SSO login for my domain? [To be created]

**Related topics**

- How do I change my workspace name and URL?  [To be created]
- How do I invite team members to my workspace? [To be created]

**Background**

- What's the difference between Owner and Admin roles? [To be created]

---

| Field          | Value                                |
|----------------|--------------------------------------|
| Last verified  | 2026-05-01                           |
| Product area   | Workspace settings / Domains         |
| Applies to     | Pro and Enterprise plans             |
| Tags           | custom domain, DNS, CNAME, workspace settings, domain verification |

---

- **Update trigger**: Review this article when domain configuration or SSL provisioning behaviour changes in a product release.
- **Staleness check**: Flag for review if not verified within 90 days of the last verified date above.
- **Helpfulness tracking**: If article views are high but support tickets on custom domain setup continue at volume, the DNS steps in particular may need more provider-specific examples.
- **Retirement criteria**: Archive if the custom domain feature is replaced or the domain settings UI is substantially redesigned — replace with a redirect to the new article.

```

## Evaluation

| Field | Value |
|---|---|
| Verdict | PARTIAL |
| Score | 13.0/17.0 (76%) |
| Evaluated | 2026-05-01 |
| Target duration | 114813 ms |
| Target cost | $0.2657 |
| Permission denials | 0 |

### Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| c1 | Skill requires the article title to be a question the user would actually ask — not a feature description | PASS | Title is 'How do I use my own domain instead of the default clearpath.app address?' — phrased as a direct user question, not a feature description like 'Custom Domain Configuration'. |
| c2 | Skill requires a short answer or summary at the top before the step-by-step instructions | PASS | Opening paragraph before Prerequisites: 'You can replace your default `yourworkspace.clearpath.app` address with a domain you own — for example, `work.yourcompany.com`. The process takes about 5 minutes, then DNS propagation can add up to 48 hours before the domain is fully live.' |
| c3 | Skill requires a prerequisites section listing what the user needs before they start | PASS | '## Prerequisites' section exists with three bullet points covering role requirement, plan tier, and DNS access. |
| c4 | Skill requires a troubleshooting section covering common problems users encounter with this task | PASS | '## Troubleshooting' section present with five Problem/Cause/Solution blocks covering DNS not found, button absent, SSL failure, security warning, and corporate IT environments. |
| c5 | Skill requires each step to describe both the action and what the user should see after — not just the action | PASS | Every step (1–6) ends with an explicit 'Expected result:' sub-section, e.g., Step 4: 'Expected result: The record appears in your DNS provider's record list.' |
| c6 | Skill uses only product terminology — no technical jargon without plain-language explanation | PARTIAL | Most language is plain, but 'CNAME', 'DNS propagation', and 'TTL' appear without explanation. 'CNAME' first appears in a table in Step 3 with no gloss. 'TTL: leave as the default, or set to 300 seconds' is used without defining the acronym. |
| c7 | Skill requires metadata (category, tags, related articles) — partial credit if related articles are required but category/tag metadata is not | PARTIAL | Footer table includes 'Product area: Workspace settings / Domains' and 'Tags: custom domain, DNS, CNAME, workspace settings, domain verification'. Related articles section also present. Ceiling is PARTIAL so max 0.5. |
| c8 | Skill has a valid YAML frontmatter with name, description, and argument-hint fields | FAIL | The captured output contains no evidence of the skill definition's YAML frontmatter. The output article itself has no frontmatter block. Cannot verify the skill file has name, description, and argument-hint fields from the captured output alone. |
| c9 | Output's title is phrased as a user question — 'How do I use my own domain instead of clearpath.app?' or 'Can I connect a custom domain to my workspace?' — not 'Custom Domain Configuration' or 'Domain Mapping' | PASS | Title is 'How do I use my own domain instead of the default clearpath.app address?' — matches the user-question pattern exactly. |
| c10 | Output's short answer at the top resolves the high-level question in 1-3 sentences — 'Yes, you can connect a custom domain. You'll need to add a CNAME record at your DNS provider and verify ownership in Clearpath. Setup takes 5-30 minutes depending on DNS propagation.' | PASS | Opening paragraph: 'You can replace your default `yourworkspace.clearpath.app` address with a domain you own... The process takes about 5 minutes, then DNS propagation can add up to 48 hours before the domain is fully live.' — Two sentences resolving the question. |
| c11 | Output's prerequisites section names what's needed — admin access to Clearpath, admin access to the customer's DNS provider, the custom domain registered, awareness that DNS changes can take up to 24 hours | PARTIAL | Prerequisites covers Owner role (admin access to Clearpath) and DNS settings access, but does not explicitly state 'the custom domain must already be registered' and does not include DNS propagation time awareness in the prerequisites block itself (it appears in the intro paragraph instead). |
| c12 | Output's steps cover both sides — Clearpath side (enable custom domain in workspace settings, copy verification token) AND DNS provider side (add CNAME record pointing to clearpath app) — clearly labelled with provider-agnostic instructions | PASS | Steps 1–3 cover the Clearpath side (navigate Settings > Domains, enter domain, copy CNAME values). Step 4 explicitly covers the DNS provider side with provider-agnostic instructions: 'The exact steps vary by provider. In most cases, you're looking for a section called DNS Management, DNS Records, or Zone Editor.' |
| c13 | Output's steps include expected results after each — e.g. 'Step 4: Add the CNAME record. After saving, your DNS provider should show the record as 'pending' or 'active'' — not just the action | PASS | All six steps include 'Expected result:' sub-sections. Step 4 specifically: 'Expected result: The record appears in your DNS provider's record list. Changes may take a few minutes to save on their end.' |
| c14 | Output's troubleshooting section covers — verification fails (DNS propagation delay, CNAME pointing wrong, conflicting record), HTTPS / SSL not working (certificate provisioning takes 5-10 minutes after verification), domain mismatch error | PARTIAL | DNS propagation delay and CNAME entered incorrectly are covered in the first troubleshooting entry. SSL provisioning failure is covered. But 'conflicting record' (e.g., existing A record blocking the CNAME) and 'domain mismatch error' are not addressed anywhere in the troubleshooting section. |
| c15 | Output uses product terminology only — 'custom domain', 'subdomain', 'DNS record' — and explains 'CNAME' briefly the first time as 'a type of DNS record that points your domain to another domain' | FAIL | CNAME first appears in the table in Step 3 ('\| CNAME \| `work` \| `custom.clearpath.app` \|') with no accompanying explanation. The article proceeds to use 'CNAME record' throughout without ever providing the brief gloss required by this criterion. |
| c16 | Output addresses the post-setup verification — how the user confirms their domain is now working, including testing in incognito to bypass cache, and what to do if some users still see the old URL (browser cache) | PARTIAL | Step 6 confirms SSL active and notes the old clearpath.app address redirects. Troubleshooting mentions hard-refresh ('Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows'). However, incognito/private browsing to bypass cache is never mentioned, and there is no guidance for the scenario where some users still see the old URL due to their browser cache. |
| c17 | Output's related articles link to adjacent topics — 'Setting up SSO with a custom domain', 'Email and notification settings under your domain', 'Removing or changing your custom domain' — anticipating next steps | PASS | '## Related articles' section lists: 'How do I require SSO login for my domain?' (maps to SSO with custom domain), 'How do I change my workspace name and URL?' (maps to changing custom domain), plus custom login page, team invites, and Owner vs Admin roles — all adjacent next-step topics. |
| c18 | Output addresses metadata — category (e.g. 'Workspace settings'), tags (e.g. 'custom-domain', 'DNS', 'SSL'), and related articles in a structured frontmatter or footer block | PARTIAL | Footer table contains 'Product area: Workspace settings / Domains' (category), 'Tags: custom domain, DNS, CNAME, workspace settings, domain verification'. Related articles in a separate '## Related articles' section. No YAML frontmatter. Ceiling is PARTIAL so max 0.5. |

### Notes

The output is a well-structured KB article that satisfies most structural requirements: question-format title, short answer, prerequisites, numbered steps with expected results, troubleshooting, related articles, and footer metadata. The main gaps are: (1) CNAME is never explained despite being a core technical term (c15 fail, c6 partial); (2) the troubleshooting section misses 'conflicting DNS record' and 'domain mismatch error' scenarios; (3) post-setup verification lacks incognito testing guidance; (4) prerequisites don't explicitly mention the domain must be pre-registered or call out propagation time; (5) the skill's own YAML frontmatter cannot be verified from the output. The score of 76.5% puts it comfortably in PARTIAL territory — a high-quality draft that would need targeted revision on CNAME explanation, troubleshooting completeness, and cache/incognito guidance before publishing.
