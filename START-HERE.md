# Start Here

Read this first. It is the front door to a client's website, **design through build**. Everything is
here: the design workflow and the build workflow. This touches **staging only**, never production.

## What this repo is

The agency's starter kit for one client's website, on **WordPress plus Breakdance**. Clone it per
client. It covers two phases:
- **Design** (Phase 1), in Claude Design / Cowork / Figma, and
- **Build** (Phase 2), in Claude Code on the Breakdance staging site.

---

## Phase 1: Design

Turn the brief into a homepage and a **build-ready Figma design system**. The brief (from ZilvaEdge)
already carries the strategy, audience, voice and page notes, so the design step designs *to* it, it
does not re-do strategy. Full detail in **`design/README.md`**.

Two paths, run either, or both to compare:
- **Claude Design, then Claude Code** (best for a build-ready system). Paste
  `design/1-design-in-claude-design.md` into Claude Design; when it offers "transfer to Claude Code",
  paste `design/2-systematise-in-claude-code.md` into Claude Code (with the Figma MCP connected).
- **Cowork** (one tool, end to end, gives responsive frames). Paste `design/3-design-in-cowork.md`.

Then **polish in Figma, approve, and export the tokens to Breakdance Global Settings** (the bridge to
the build). You design to the standards in **`design/reference/`** (the design-for-build checklist, the
design-system rules, the quality standard) and the `discoverweb-design-standard` audit.

**Last, once the design is final: `design/5-export-design-pack.md`.** It pulls everything the build
needs out of Figma into `design-pack/`, so whoever builds the site can clone the repo and work without
a Figma dev seat. Run it on the machine that has the Figma connection, commit it, and re-run it after
any later design change. See `design-pack/README.md`.

---

## Phase 2: Build

You run a build by pasting one prompt into Claude Code, in this folder. Pick one (see `prompts/README.md`
for which, when):

- **Guided** (new to this). `prompts/guided-build.md`. Connects the site, walks every step, asks before risk.
- **Advanced** (once fluent). `prompts/advanced-build.md`. Whole stages, little narration.
- **New machine or joining.** `prompts/connect-mcps.md`. Connects the MCPs, prompting you for the manual bits.
- **New page.** `prompts/new-page.md`. One internal page from its reference and content. Run several in parallel.
- **Blog.** `prompts/blog.md`. The single-post template and archive, as Breakdance Templates, not one page per post.
- **Source images.** `prompts/source-images.md`. Fill the image placeholders (a post-build pass).
- **SEO meta.** `prompts/seo-meta.md`. The per-page title and meta drafts to paste into the SEO plugin.
- **Plan changes.** `prompts/plan-changes.md`. Turn client feedback into a fix-now plus standing-rule plan.
- **Status.** `prompts/status.md`. Where the build is, plus the outstanding lists.
- **Review and changes.** `prompts/review-and-changes.md`. Review the site, or apply a punch-list, one at a time.
- **Final check.** `prompts/final-check.md`. Pre-launch sweep: links, spelling, grammar, consistency, technical SEO.
- **Triage final check.** `prompts/triage-final-check.md`. Turns the report into an AI fix-plan plus a tab-per-fix-type tracker (a Google Sheet you drag in).

To paste a prompt: open this folder in Claude Code, copy the file's contents into the chat, and send it.

## Where the words come from

`content/` holds the approved page copy, one markdown file per page. ZilvaEdge puts it there once the
editor has signed off the Google Doc. Build from those files, not from a Doc somebody sent you.

**The ownership rule.** During the build this repo owns page copy. ZilvaEdge does not edit released
pages while the build is live. The Google Doc will go stale during the build; that is expected, and
it is refreshed at launch when the PM runs ZilvaEdge's content reconciliation.

That gives you three cases:

- **Microcopy**, meaning CTAs, button labels and short connective copy: write it here and log it in
  `CONTENT_CHANGELOG.md`. Two lines of copy do not go through the full ZilvaEdge pipeline.
- **A full new page or a substantial section:** request it from ZilvaEdge through ClickUp. It comes
  back as released content in `content/`. Do not improvise a page.
- **A factual error or a compliance problem:** raise it. Do not quietly correct it, because the Doc
  is what the client approved.

`content/_live/` is a different thing again: the export of what the site **actually says**, pulled
out of WordPress and committed. Breakdance keeps live copy in the database rather than in a file, so
without the export there is no git evidence of a heading someone changed in the Breakdance UI.
`content/` is the approved copy, `content/_live/` is the truth, `CONTENT_CHANGELOG.md` is the
explanation.

**A build folder arrives with all of this already populated.** If a piece is missing, that is a
handover problem to raise with the PM, not something to improvise around. Improvised copy is the
single most expensive thing that can happen in a build: it looks finished, it passes a visual review,
and nobody finds out it was invented until the client reads it.

`content/README.md` has the detail.

## Before you start (build phase)

- **Claude Code** installed, and this folder open in it.
- The **design done** (Phase 1), with its tokens ready to load into Breakdance.
- **Either** the **design pack** in `design-pack/`, **or** the Figma connection and a dev seat. The
  pack is the usual case: it means the build needs no Figma access at all. If `design-pack/` is
  populated, that is the design source and you can skip Figma entirely.
- The client's **approved page copy** in `content/`.
- The client's **sitemap** (page list and menu structure) before you build navigation.
- A **WordPress staging site** with the **Agent Connector** plugin, and wp-admin access.
- **Node.js**, and **Python** with `pillow` and `requests` (the image and post tools).
- The **chrome-devtools MCP** connected, for visual diffs and the QA auditors. See CONNECT.md.

## What the build looks like

Whichever prompt you use, the build follows the same path. Guided walks you through it; advanced assumes
you know it.

1. **Connect** the staging site to Claude Code. See `CONNECT.md`. Do it first and confirm the Breakdance
   tools appear before anything else.
2. **Recovery path** in place before the first write (a snapshot, or the daily backup / Breakdance revisions).
3. **Smoke-test** the write path with one throwaway page, confirm it is editable, delete it.
4. **Build the home page** first, verify it, record it. Then the next page.
5. **Pass the gates.** Each lifecycle gate is approved by a human, never the AI.

Sessions are resumable: the `build-log/` is the durable memory, so a fresh Claude session re-reads the
log to pick up where you left off. Prefer starting fresh at a stage boundary, not mid-write.

### Resuming in a new session
1. Open this folder in Claude Code (new chat, or after reopening the app).
2. Run `/mcp` to confirm the site is still connected.
3. Paste: `Follow prompts/guided-build.md for this build, then do Stage 0 to reorient from the build log
   and continue.` Its Stage 0 reads the build log and tells you where the build stands.

## Connecting the site

One command from the Agent Connector plugin, run in this folder. The full procedure, settings and the
staging operating model are in `CONNECT.md`. **New machine or someone joining?** Paste
`prompts/connect-mcps.md` and Claude walks through connecting every MCP, prompting you only for the
manual bits (the wp-admin login for the Application Password, the restart). The only secret is that one
WordPress Application Password, and it never enters the repo.

## Troubleshooting: the site will not connect

The most common wall is the Application Password screen refusing to generate one. In order of likelihood:

1. **An "Application passwords require HTTPS" error, but the site IS on https.** A security plugin is
   blocking it. In **Admin and Site Enhancements (ASE)**, go to **Disable Components to Disable Smaller
   Components** and make sure **Application Passwords** is **not** disabled (on that tab the toggles turn
   features off, so leave it enabled). The exact location has moved between ASE versions, older builds
   put it on the Security tab, so if it is not there check the Security and "Log In/Out | Register" tabs.
   This overrides everything else, so check first.
2. **A genuinely local dev site (LocalWP).** Confirm `define( 'WP_ENVIRONMENT_TYPE', 'local' );` is in
   `wp-config.php`, then **restart the site** in Local so PHP reloads the file.
3. **A staging site behind LiteSpeed / a proxy that terminates SSL.** WordPress cannot see the HTTPS.
   Add to `wp-config.php`, above the "stop editing" line:
   ```php
   if ( isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && stripos($_SERVER['HTTP_X_FORWARDED_PROTO'],'https') !== false ) {
       $_SERVER['HTTPS'] = 'on';
   }
   ```
   Then **restart lsphp** (`killall lsphp`) so OPcache reloads `wp-config.php`, and `wp litespeed-purge
   all`. On LiteSpeed, edits to `wp-config.php` often do nothing until the PHP process restarts.
4. **The connection registers but lists no Breakdance tools.** The adapter URL is wrong, or the
   Breakdance native MCP is not enabled. Copy the command exactly from the Agent Connector Connect
   screen, and check Breakdance > Settings > Agents & MCP.

## Placeholders: what arrives filled and what does not

This kit is a template. Bracket placeholders such as `[CLIENT]` mark what has to be replaced per
build. **A remaining bracket is a signal, not an oversight**: it tells you the value is genuinely
not known yet.

| Placeholder | Where | Filled by |
|---|---|---|
| `[CLIENT]` | `.claude/CLAUDE.md`, `build-log/BUILD-LOG.md`, `DECISIONS.md`, `GATES.md`, `design/reference/design-system-checklist.md`, `handoff-checklist.md` | Scaffolding, automatically |
| `[STAGING_URL]` | `.claude/CLAUDE.md` | **You**, once the staging site exists |
| `[HOST]`, `[PRODUCTION_URL]` | Added per build where relevant | **You**, at launch planning |
| `[NAME]`, `[LINK]`, `[DESIGNER]`, `[ROLE]`, `[VALUE]`, `[VALUES]`, `[USAGE]`, `[EXCLUSION]`, `[RATIONALE]`, `[BEHAVIOUR]`, `[EVIDENCE]` | `design/reference/DESIGN.template.md`, the design checklists | **The designer**, as the design system is built |

**Nothing should ever guess a staging URL, a production URL or a host.** A plausible wrong URL is
worse than a visible gap, because somebody will try to connect to it and spend an hour working out
why it fails.

## Where things live

| Need | Location |
|------|----------|
| How to run it (this doc) | `START-HERE.md` |
| Released page content, the baseline for the build | `content/` |
| What the pages actually say now, exported from the site | `content/_live/` |
| Condensed strategy, audience, voice, page notes | `strategy-brief.md` |
| The design, extracted from Figma so the build needs no Figma seat | `design-pack/` and its README |
| Page list and menu structure | `design/sitemap.md` |
| Every content change made during the build | `CONTENT_CHANGELOG.md` |
| The design workflow (Phase 1) | `design/` and `design/README.md` |
| Design standards the design is held to | `design/reference/` |
| Which build prompt to use, when | `prompts/README.md` |
| Build prompts (paste into Claude) | `prompts/` |
| When to commit + two-machine sync | `.claude/reference/git-workflow.md` |
| Connecting the site + settings + operating model | `CONNECT.md` |
| This client's brief and rules (loaded every session) | `.claude/CLAUDE.md` |
| Skills, agents, hooks | `.claude/` |
| Build runbook + best practices | `docs/` |
| Audit trail (log, gates, decisions, pages) | `build-log/` |
| End-of-build wp-admin / live-session punch-list | `build-log/CLEANUP.md` |
