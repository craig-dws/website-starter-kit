# AI Web Design System v0.1: Implementation Runbook (Astro plus Payload)

Document 19b of the AI Web Design System v0.1 series. This is the Astro plus Payload counterpart to 19 (the WordPress and Breakdance runbook).
Audience: Dev Lead and operator (technical). PMs and Designer for context.
Status: Internal working document.

## Purpose

This runbook stands up the Astro plus Payload pipeline once, end to end. Follow the steps in order. Each step has a verification and, where the step is risky, a rollback note. The shared front-half (brief, research, design system, Figma high-fidelity, token extraction) is identical to the WordPress path; see 03, 04 (steps 1 to 4), and 05 stages 1 to 4. This runbook covers the target-specific back-half.

The key difference from the WordPress runbook: there is no Novamira and no raw-PHP execution surface. The agent works on version-controlled code and a governed Payload API, so the whole pipeline is inherently safer. The risk shifts from "an agent writing to a live database" to ordinary code review and deployment discipline.

## Environment facts to keep in mind

- **Astro ships zero JavaScript by default** and bakes content to HTML at build time, which is good for Core Web Vitals and AI-crawler fidelity.
- **Tokens live in code**, not in a CMS: the Tailwind config plus CSS custom properties. Payload never holds a design token.
- **Payload 3.x installs into a Next.js app** and needs Node 20.9 or later plus a database (MongoDB, PostgreSQL, or SQLite). It pins to specific Next.js version ranges, so it is not "any" Next.js version.
- **This is a split deployment.** The Astro front-end is static and served from a CDN or host; the Payload backend is a persistent Node service plus a database. They deploy separately.
- **Payload Cloud is not a safe managed option** after the Figma acquisition (new sign-ups paused). Self-host the Payload backend.
- **Default dev ports do not collide.** Astro defaults to 4321 and Payload (Next.js) to 3000. Only reassign if you changed a default or something else uses those ports.
- **Static content is frozen at build time.** A client edit in Payload must trigger a rebuild and redeploy (a publish webhook), or specific sections must use Astro on-demand rendering.
- **There is no first-party Astro package for Payload.** Integration is generic REST or GraphQL fetch, or a community Local-API plugin. Treat community plugins as convenience, not a supported dependency.

## Pre-flight checklist

Confirm all of the following before Step 1.

- [ ] **Node.js 20.9 or later** installed (`node -v`).
- [ ] **A Git repository** for the client project (monorepo or two packages: Astro app and Payload app).
- [ ] **A database available**: MongoDB or PostgreSQL for staging and production, or SQLite for a quick local build.
- [ ] **A Node host** identified for the Payload backend (your own VPS, Railway, Render, Fly.io, or similar) and a static host or CDN for the Astro front-end.
- [ ] **Figma account** with a Professional Dev seat (about US$12 per operator per month) and the pilot Figma file created with named frames.
- [ ] **Anthropic account** and Claude Code access.
- [ ] **Baseline captured** (document 20) and scorecard prepared (document 11).
- [ ] **Pilot artefacts folder** created.

## Step 1: Provision the project repository

Create the project repository with an Astro app and a Payload app. Keep them as separate packages if in one monorepo, so Vite does not try to parse Payload's server code.

```bash
# Astro app
npm create astro@latest -- --template minimal
# Payload app (Next.js based), in its own package or folder
npx create-payload-app@latest
```

Verification: both apps install and their dev servers start (`astro dev` on 4321, Payload on 3000). Rollback: this is a fresh repository, so on failure delete and recreate. No production impact.

## Step 2: Install Claude Code

```bash
npm i -g @anthropic-ai/claude-code
claude --version
```

Verification: `claude --version` returns a version and `claude` reports an authenticated account.

## Step 3: Create the client Claude project and .claude structure

Initialise the `.claude` structure so prompts, settings, and MCP config live with the project and are version-controlled.

```bash
cd /path/to/clients/<pilot-slug>
mkdir -p .claude
claude          # run /init to scaffold, or create .claude/settings.json manually
```

Verification: `.claude/` exists with a `settings.json`; the project opens in Claude Code. Keep the design-system and page-generation prompts in the project.

## Step 4: Install and OAuth the Figma plugin

```bash
claude plugin install figma@claude-plugins-official
```

Then inside Claude Code run `/plugin`, open Installed, select the Figma plugin, and complete OAuth in the browser. This connects the remote Figma MCP server at https://mcp.figma.com/mcp.

Verification: `/mcp` lists the Figma server as connected; a scoped `get_metadata` call on the pilot Figma file returns data. Rollback: remove and reinstall the plugin if OAuth misbehaves.

## Step 5: Configure Payload (schema and database)

Configure the Payload database adapter and define the initial content model in code.

- **Set the database adapter** (MongoDB, PostgreSQL, or SQLite) in the Payload config.
- **Define Collections** (Pages, Posts, Services, Team) and **Globals** (header, footer, navigation, contact details).
- **Define the Blocks field** (Hero, CTA, Feature grid, Gallery) as the composable page sections.
- **Run the Payload admin** and create the first admin user.

Verification: the Payload admin loads, the schema matches the sitemap, and a test document can be created and read back through the REST or GraphQL API. Rollback: schema is code, so revert the commit; run a migration down if a database change was applied.

## Step 6: Verify Figma read and Payload read

Before generating anything, prove both ends work.

- **Run `/mcp`** and confirm the Figma server is connected.
- **Ask Claude Code for a scoped `get_metadata`** on one Figma frame.
- **Read a Payload document** through the API (or the Local API) to confirm content access.

Verification: both read operations succeed. Do not proceed to generation until this passes.

## Step 7: Run the Figma design-system scaffolding prompt

Run the design-system scaffolding prompt so Claude Code extracts the foundations (colours, type scale, spacing, radius, components) from Figma. Scope every `get_design_context` call to a single frame to avoid token overflow.

Verification: the extracted design system is recorded and matches the agreed tokens; no token-overflow errors occurred.

## Step 8: Sync tokens into code and model content

- **Write the resolved token values** into the Tailwind config and CSS custom properties, using the same semantic token names agreed at handoff.
- **Confirm the Payload content model** matches the sitemap and the design (one Block type per reusable design section).
- **Human review gate**: the Dev Lead reviews the token layer for completeness and the content model against the sitemap before any page is built.

Verification: token names are identical across Figma, the Tailwind or CSS layer, and Payload block field names; the content model is reviewed and committed. Rollback: revert the commit.

## Step 9: Build components and the homepage, then human review

- **Build one Astro component per Payload block type** and per layout region (header, footer), referencing token names for all colour, type, and spacing. A hardcoded value is a defect.
- **Use `get_design_context` and `get_screenshot` scoped to one frame**, and `get_code_connect_map` where components are mapped.
- **Wire the homepage** to fetch content from Payload and render the Blocks array to the matching components.
- **Stop for full human review** (the Phase 3 gate in document 10).

Verification: the homepage renders locally, the screenshot diff against Figma is clean, and the Dev Lead and Designer sign off. Rollback: revert the commit; the previous build is intact in Git.

## Step 10: Generate subpages

Generate the remaining pages one at a time. Each is an Astro component composition wired to Payload content. Review each page against its Figma frame before acceptance (Phase 4 in document 10).

Verification: each page renders and passes review; effort and rework recorded against the scorecard. Rollback: revert the per-page commit.

## Step 11: QA, accessibility, and the publish path

- **Run Lighthouse** on key pages (mobile and desktop) and record Core Web Vitals.
- **Run the WCAG 2.2 AA check** per page (automated plus manual).
- **Review each breakpoint** and audit token and component adherence on a page sample.
- **Configure the publish path**: wire a rebuild-and-redeploy webhook so a Payload publish triggers an Astro rebuild, or set on-demand rendering for dynamic sections.

Verification: results recorded in the scorecard (document 11); blocking accessibility and breakpoint errors fixed; a test content edit in Payload triggers a rebuild.

## Step 12: Deploy and handoff

- **Deploy the Astro front-end** as static output to the CDN or host.
- **Deploy the Payload backend** to the Node host with its database, file storage, and email provider.
- **Take a database snapshot** and confirm the repository is tagged.
- **Complete the scorecard** and the decisions and failures log (document 21), then hand off to the PM for the pilot review.

Verification: the live front-end serves correctly, the Payload admin is reachable, a publish triggers a rebuild, backups exist, and the review is scheduled.

## Troubleshooting

### Vite tries to parse Payload server code

In a shared monorepo, Vite may attempt to parse Payload's server code and break on path aliases. Keep Astro and Payload in separate packages, or exclude Payload from Vite dependency optimisation and use relative imports.

### Node version too low

Payload 3.x requires Node 20.9 or later. If install or build fails with engine errors, upgrade Node and reinstall dependencies.

### A published edit does not appear on the site

A static Astro build freezes content at build time. Confirm the publish webhook fired and the rebuild and redeploy completed. For sections that must be always-current, use Astro on-demand rendering instead of static generation.

### Payload Cloud sign-up is unavailable

New Payload Cloud sign-ups are paused after the Figma acquisition. Self-host the Payload backend on a Node host with a database; do not architect around Payload Cloud.

### get_design_context token overflow

Large Figma pages exceed the token limit. Never call `get_design_context` on a whole page. Scope each call to one frame and assemble the design system from the per-frame results.
