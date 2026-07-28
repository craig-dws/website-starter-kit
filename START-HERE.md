# Start Here

Read this first. It is the front door to this client's website build. From here you pick
how to run it, guided or advanced, and everything else follows.

## What this repo is

One client's website build, scaffolded from the agency's AI Web Design System. It is lean
on purpose: only the tools and records this build needs. The full system lives in a
separate repo. This build touches **staging only**, never production.

## Step 1: pick how you'll run the build

You run a build by pasting one prompt into Claude Code. The prompt sets how Claude works
with you for the session. Pick one:

- **Guided** (start here if you are new). Paste `prompts/guided-build.md`. Claude connects
  the site first, then walks you through every step one at a time, explains what each
  skill and hook does, and asks before anything risky.
- **Advanced** (once the flow is second nature). Paste `prompts/advanced-build.md`. Claude
  moves in whole stages with little narration, stopping only for real decisions and gates.
- **New page** (internal-pages phase, once the design system is locked). Paste `prompts/new-page.md`.
  Claude builds one internal page from its reference design and content, reusing the type's
  components. Run several in parallel, one page per chat.
- **Source images** (after pages are built). Paste `prompts/source-images.md`. Claude works through
  the placeholders left during the build, finds a match in the client gallery or sources stock/AI,
  optimises and uploads each, and swaps it in. Images are a deliberate post-build pass, not part of a
  page build.
- **SEO meta** (after pages are built). Paste `prompts/seo-meta.md`. Claude gathers the per-page SEO
  title and meta-description drafts for a human to paste into the SEO plugin (the MCP cannot write post
  meta). Another deliberate post-build pass. See `.claude/reference/deferred-passes.md` for why images,
  links and SEO meta are finished after the build, not during it.
- **Plan changes** (when a client or reviewer gives feedback). Paste `prompts/plan-changes.md`. Claude
  turns raw feedback into a structured change plan, splitting each item into "fix what is built" and
  "standing rule so future pages inherit it", and writes it to `build-log/content-changes.md`. It plans;
  it does not apply. Feeds review-and-changes.
- **Review and changes** (after a build or stage is done). Paste `prompts/review-and-changes.md`.
  Claude reviews the built site against the standards, or applies a punch-list of changes you give
  it, one at a time. Use it for sign-off, suggestions, or changes noticed later.

To paste a prompt: open this folder in Claude Code, copy the file's contents into the
chat, and send it. That is the whole "start". Claude takes it from there.

## Before you start (prerequisites)

- **Claude Code** installed, and this folder open in it.
- The client's **Figma file** link (needed once you build, not needed just to connect).
- The client's **sitemap** (page list and menu structure) before you build navigation.
- A **WordPress staging site** with the **Agent Connector** plugin, and wp-admin access.
- **Node.js** installed (the WordPress MCP server runs via npx).
- The **chrome-devtools MCP** connected, for Figma visual diffs and the QA auditors (it
  screenshots headless, no visible browser needed). See CONNECT.md.

## What the whole build looks like

Whichever prompt you use, the build follows the same path. Guided walks you through it;
advanced assumes you know it.

1. **Connect** the staging site to Claude Code. See `CONNECT.md`. This is a session on its
   own: do it first and confirm the Breakdance tools appear before anything else.
2. **Snapshot** the database before the first write, and log it.
3. **Smoke-test** the write path with one throwaway page, confirm it is editable, delete it.
4. **Build the home page** first, verify it against Figma, record it. Then the next page.
5. **Pass the gates.** Each lifecycle gate is approved by a named human, never the AI.

Sessions are resumable. The `build-log/` is the durable memory, so when a chat gets long you
can start a fresh Claude session and it re-reads the log to pick up where you left off.
Prefer starting fresh at a stage boundary, not mid-write.

### Resuming in a new session
1. Open this folder in Claude Code (new chat, or after reopening the app).
2. Run `/mcp` to confirm the site is still connected.
3. Paste this to continue:
   `Follow prompts/guided-build.md for this build, then do Stage 0 to reorient from the build
   log and continue.`
   (Or paste the full `prompts/guided-build.md`; both work. Its Stage 0 reads the build log
   and tells you where the build stands and the next step.)

Nothing is lost between sessions because the state lives in `build-log/`, not the chat. Just
make sure the previous session logged its work before you closed it (the guide does this at
each stage boundary).

## Connecting the site

The connection is one command from the Agent Connector plugin, run in this folder. The
full procedure, the settings to set, and the staging operating model are in `CONNECT.md`.
If the Application Password screen refuses to generate one, see Troubleshooting below.

**New machine, or someone joining the build?** Paste `prompts/connect-mcps.md`. Claude walks
through connecting every MCP this build uses (Breakdance, chrome-devtools, and Figma if you read
designs), does what it can itself, and stops to prompt you only for the manual bits (the wp-admin
login for the Application Password, and restarting the app). The only secret is that one WordPress
Application Password, and it never enters the repo.

## Troubleshooting: the site will not connect

The most common wall is the Application Password screen refusing to generate one. In order
of likelihood:

1. **An "Application passwords require HTTPS" error, but the site IS on https.** A security
   plugin is blocking it. Check **Admin and Site Enhancements (ASE)** → Security tab → turn
   **off** "Disable Application Passwords". This overrides everything else, so check first.
2. **A genuinely local dev site (LocalWP).** WordPress must know it is local. Confirm
   `define( 'WP_ENVIRONMENT_TYPE', 'local' );` is in `wp-config.php`, then **restart the
   site** in Local so PHP reloads the file.
3. **A staging site behind LiteSpeed / a proxy that terminates SSL.** WordPress cannot see
   the HTTPS. Add to `wp-config.php`, above the "stop editing" line:
   ```php
   if ( isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && stripos($_SERVER['HTTP_X_FORWARDED_PROTO'],'https') !== false ) {
       $_SERVER['HTTPS'] = 'on';
   }
   ```
   Then **restart lsphp** (`killall lsphp`) so OPcache reloads `wp-config.php`, and
   `wp litespeed-purge all`. On LiteSpeed, edits to `wp-config.php` often do nothing until
   the PHP process restarts.
4. **The connection registers but lists no Breakdance tools.** The adapter URL is wrong, or
   the Breakdance native MCP is not enabled. Copy the command exactly from the Agent
   Connector Connect screen, and check Breakdance > Settings > Agents & MCP.

## Where things live

| Need | Location |
|------|----------|
| How to run the build (this doc) | `START-HERE.md` |
| Which prompt to use, when | `prompts/README.md` |
| Guided / advanced prompts (paste into Claude) | `prompts/` |
| When to commit + two-machine sync | `.claude/reference/git-workflow.md` |
| Connecting the site + settings + operating model | `CONNECT.md` |
| This client's brief and rules (loaded every session) | `.claude/CLAUDE.md` |
| Skills, agents, commands, hooks | `.claude/` |
| Build runbooks + best practices | `docs/` |
| Audit trail (log, gates, decisions, pages) | `build-log/` |
| End-of-build wp-admin / live-session punch-list | `build-log/CLEANUP.md` |
| The full agency system | the AI Web Design System repo (separate) |
