# AI Web Design System v0.1: Implementation Runbook (WordPress plus Breakdance)

Document 19 of the AI Web Design System v0.1 series. This is the runbook for **Target A: WordPress plus Breakdance**. For **Target B: Astro plus Payload**, use [19b_astro_payload_implementation_runbook.md](19b_astro_payload_implementation_runbook.md) instead. The shared front-half (Steps up to token extraction) is common to both.
Audience: Dev Lead and operator (technical). PMs and Designer for context.
Status: Internal working document.

## Purpose

This runbook stands up the whole pipeline once, end to end, on a staging environment. Follow the steps in order. Each step has a verification and, where the step is risky, a rollback note. Do not run any part of this against production. Novamira is dev and staging only as a matter of policy, and its sandbox is not a security boundary.

## Layout-write path: native Breakdance 3.0 MCP first

The layout-write path for the write test and the initial builds is the **native Breakdance 3.0 MCP** (Settings then Agents and MCP). It is the preferred path and is tested first. See the write-test procedure in [27_breakdance_write_test.md](27_breakdance_write_test.md). The Novamira steps in this runbook are the **fallback**, used only if the native path fails the write test. Do not buy Novamira Pro before the test. Buy no third-party bridge until the native path has been proven to fail.

## Environment facts to keep in mind

- WordPress 7.0 "Armstrong", PHP 8.3.
- **Breakdance Pro has no REST API for layouts**. Never write raw PHP layout files. Layout changes go through the builder or through controlled DB writes with backups.
- Always back up `_breakdance_data` postmeta before any DB write, and run `wp breakdance clear_cache` after any DB write.
- `import_settings` and `export_settings` are Breakdance Pro only. `total_reset` is destructive; never run it on a populated site.
- Figma `get_design_context` can exceed token limits on large pages. Always scope it to individual frames.
- Application Passwords require HTTPS, or `define('WP_ENVIRONMENT_TYPE','local')` for a local build.
- Novamira supports domain locking and has a URL safe-mode kill switch. It is very young (about 3 to 4 months old); treat it as early stage. **Do not rely on the widely-cited 30 second PHP execution limit.** It appears only in third-party summaries, not in Novamira's own docs or changelog, and doc 01 records it as unverified. Assume no execution ceiling until we have measured one ourselves. Our real controls are backups, staging-only, and disposable environments, not a vendor limit that may not exist.

## Pre flight checklist

Confirm all of the following before Step 1.

- [ ] Node.js LTS installed (`node -v`, `npm -v` return versions).
- [ ] Staging host available with HTTPS, PHP 8.3, WP CLI and MySQL access.
- [ ] Breakdance Pro licence key to hand.
- [ ] Novamira is **not needed unless the native Breakdance 3.0 MCP fails the write test**. Buy no Novamira licence before the test. If the native path fails and you fall back to Novamira, you will need the Pro key then (not free core: free core cannot test the Pro Breakdance specialization). See 24 and 27.
- [ ] Figma account with a Professional Dev seat (about US$12 per operator per month) and the pilot Figma file created with named frames.
- [ ] Anthropic account and Claude Code access.
- [ ] Baseline captured (document 20) and scorecard prepared (document 11).
- [ ] Pilot artefacts to hand: `docs/pilot-artefacts/` (in this repository).
- [ ] A full backup of the staging site taken (database and files).

## Step 1: Provision WordPress staging

Provision a staging site over HTTPS with PHP 8.3 and WordPress 7.0, then install Breakdance Pro. InstaWP is a fast option for a disposable staging instance; a managed host staging environment is equally fine.

```bash
# Example with WP CLI on the staging host
wp core version                       # expect 7.0.x
php -v                                # expect 8.3.x
wp plugin install <breakdance-pro-zip> --activate
wp plugin list --status=active
```

Activate the Breakdance Pro licence in the WordPress admin (Breakdance > Settings > License).

Verification: `wp plugin list` shows Breakdance active; the site loads over HTTPS with a valid certificate.

Rollback: this is a fresh staging instance, so on failure destroy and recreate it. No production impact.

## Step 2: Install Claude Code

```bash
npm i -g @anthropic-ai/claude-code
claude --version
```

Then authenticate Claude Code per the standard login flow.

Verification: `claude --version` returns a version; `claude` launches and reports an authenticated account.

## Step 3: Create the client Claude project and .claude structure

Create a project directory for the pilot client and initialise the `.claude` structure so prompts, settings and MCP config live with the project.

```bash
mkdir -p /path/to/clients/<pilot-slug>
cd /path/to/clients/<pilot-slug>
mkdir -p .claude
claude          # run /init inside to scaffold, or create .claude/settings.json manually
```

Keep the pilot prompts (design system scaffolding, token translation, Novamira setup) in the project so they are versioned and reusable.

Verification: `.claude/` exists with a `settings.json`; the project opens in Claude Code.

## Step 4: Install and OAuth the Figma plugin

```bash
claude plugin install figma@claude-plugins-official
```

Then inside Claude Code:

1. Run `/plugin`.
2. Open Installed.
3. Select the Figma plugin and complete the OAuth flow in the browser.

This connects the remote Figma MCP server at https://mcp.figma.com/mcp using your Professional Dev seat.

Verification: `/mcp` lists the Figma server as connected. A scoped `get_metadata` call against the pilot Figma file returns data.

Rollback: remove the plugin with the plugin manager if OAuth misbehaves, then reinstall.

## Step 5: Connect the layout-write path

**Primary path: the native Breakdance 3.0 MCP.** In WordPress, go to Breakdance then Settings then Agents and MCP, install the one-click Agent Connector, and generate the credential (Application Password auth). Paste the connection command into Claude Code so it registers the native MCP server. Run `/mcp` and confirm it connects. This is the path you test first (see 27) and build on if it passes. If it passes, skip the Novamira fallback below.

**Fallback path: Novamira (only if the native path fails the write test).** Use the steps below only after the native Breakdance 3.0 MCP has failed a write-test PASS check. Buy the Novamira Pro licence at that point, not before.

1. Install the Novamira plugin on the staging site and activate it.
2. In Novamira settings, enable AI Abilities.
3. In WordPress, create an Application Password for the operator user (Users > Profile > Application Passwords). This requires HTTPS, or `define('WP_ENVIRONMENT_TYPE','local')` in `wp-config.php` for a local build.
4. Confirm domain locking is set to the staging domain and the safe mode kill switch is understood.
5. Paste the Novamira setup prompt into Claude Code, supplying the staging URL, the WordPress username and the Application Password so Claude Code registers Novamira as an MCP server.

```php
// wp-config.php, only for a local (non HTTPS) build
define('WP_ENVIRONMENT_TYPE','local');
```

Verification: Novamira shows AI Abilities enabled; the Application Password is created; `/mcp` in Claude Code lists Novamira as connected.

Rollback: deactivate the Novamira plugin and revoke the Application Password. Because it is domain locked to staging, exposure is limited to staging.

## Step 6: Verify with /mcp and a read only test

Before any write, prove the connection with a read only operation.

1. Run `/mcp` and confirm both Figma and Novamira are connected.
2. Ask Claude Code to read the site title or list pages through Novamira (read only). Confirm it returns real staging data.
3. Ask Claude Code for a scoped `get_metadata` on one Figma frame.

Verification: both read operations succeed. Do not proceed to writes until this passes.

## Step 7: Run the Figma design system scaffolding prompt

Run the design system scaffolding prompt so Claude Code extracts the design system foundations (colours, type scale, spacing, radius, components) from Figma. Scope every `get_design_context` call to a single frame to avoid token overflow on large pages.

Verification: the extracted design system is written to `pilot-artefacts/design_tokens.md` and matches the agreed tokens. No token overflow errors occurred.

## Step 8: Run the token translation prompt

Translate the extracted tokens into Breakdance global settings using a safe, reversible sequence.

1. Back up first:

```bash
# Back up the Breakdance data postmeta and export current settings
wp db export pilot-artefacts/breakdance_global_settings_backup/db_before_tokens.sql
wp post meta list <template-or-global-id> --keys=_breakdance_data > pilot-artefacts/breakdance_global_settings_backup/breakdance_data_before.txt
```

2. Export current Breakdance settings (Breakdance > Settings > Export, Pro only) and save the file into the backup folder.
3. Have Claude Code produce a differential merge of the new tokens against the current settings (change only what must change; do not overwrite unrelated settings).
4. Import the merged settings (Breakdance > Settings > Import, Pro only).
5. Clear the cache and check status:

```bash
wp breakdance clear_cache
wp breakdance --help          # confirm the command set is available
```

Verification: global settings reflect the new tokens; unrelated settings are unchanged; cache cleared without error; a spot check page renders with the new tokens.

Rollback: re import the exported settings file from the backup folder, or restore `_breakdance_data` from the backup, then run `wp breakdance clear_cache`.

## Step 9: Generate the homepage, then human review

Generate the homepage in Breakdance via the project's bound layout-write capability (the native Breakdance 3.0 MCP first, Novamira only as fallback), mapped to the approved Figma frame and content outline. Then stop for full human review (Phase 3 gate in document 10).

Verification: the homepage renders on staging; Dev Lead reviews the build line by line; Designer compares it to the Figma frame; PM confirms scope. Back up before accepting:

```bash
wp post meta get <homepage-id> _breakdance_data > pilot-artefacts/breakdance_global_settings_backup/homepage_data.txt
```

Rollback: delete or revert the homepage, restore `_breakdance_data` from backup if needed, run `wp breakdance clear_cache`, rebuild manually.

## Step 10: Generate subpages

Generate the remaining pages one at a time or in small batches. Back up before each batch. Review each page against its Figma frame and content outline before acceptance (Phase 4 in document 10).

Verification: each page renders and passes review; effort and rework recorded against the scorecard.

Rollback: restore the affected page or batch from backup, run `wp breakdance clear_cache`, rebuild manually.

## Step 11: QA and accessibility pass

Run the full QA and accessibility pass across all pages.

- Lighthouse performance on key pages (mobile and desktop); record Core Web Vitals.
- WCAG AA check per page (automated plus manual).
- Breakpoint review at each defined breakpoint.
- Token and component adherence audit on a page sample.
- Design versus build mismatch review per page.

Verification: results recorded in the scorecard (document 11). Blocking accessibility violations and breaking breakpoint errors are fixed before handoff.

## Step 12: Backup and handoff

1. Take a full site backup (database and files).
2. Export final Breakdance settings into the artefacts folder.
3. Confirm all `_breakdance_data` backups are saved.
4. Complete the scorecard and the decisions and failures log (document 21).
5. Hand off to the PM for the pilot review.

```bash
wp db export pilot-artefacts/breakdance_global_settings_backup/db_final.sql
```

Verification: backups present; scorecard and decisions log complete; review scheduled.

## Troubleshooting

### Application Password blocked by a security plugin

Some security plugins disable Application Passwords or the REST authentication path. Confirm the site is served over HTTPS (or `WP_ENVIRONMENT_TYPE` is `local`), then allow Application Passwords in the security plugin, or temporarily deactivate that plugin on staging to create the password. Re enable it and retest the Novamira read from Step 6.

### get_design_context token overflow

Large Figma pages exceed the token limit. Never call `get_design_context` on a whole page. Scope each call to one frame, extract in pieces, and assemble the design system from the per frame results. If a single frame is still too large, split it in Figma or extract by section.

### Breakdance cache not reflecting changes

After any DB write the front end can show stale output. Run `wp breakdance clear_cache`. If the change still does not appear, clear any hosting or CDN cache, confirm the write landed by inspecting `_breakdance_data`, and reload without the browser cache. Never edit raw PHP layout files to force a change.

### Novamira abilities dormant after a clone

Cloning or migrating a site can leave Novamira with AI Abilities disabled, domain locking pointing at the old domain, or safe mode engaged. Re open Novamira settings, re enable AI Abilities, update the domain lock to the current staging domain, confirm safe mode is off for the intended work, then regenerate or re register the Application Password and re run the Step 6 read only test before any write.
