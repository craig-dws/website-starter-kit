# [CLIENT] Site Build

## Project overview
Design-to-WordPress build for [CLIENT]. The design source is a Figma file
([FIGMA FILE - the source design file. Build each page from a Copy link to selection for its
frame, never by reading the whole file, which overflows on large multi-page files. Needed at
build time, not to connect; Figma is reached via its MCP]). Build target is the
Breakdance staging site at [STAGING_URL]. Production is
[PRODUCTION_URL - recorded for migration and launch only, never touched; fill at migration].

Build target: WordPress + Breakdance.

Starting condition: [ blank staging | DWS starter template | existing site with content ].
If a starter template or existing site, its current header, footer, home and demo content
are template defaults to be replaced, not client work, so Stage 4 is a replacement job, not
a blank canvas. This also underpins any snapshot waiver: a regenerable starter has nothing
to restore.

## Stack
- WordPress on [HOST - where it runs, e.g. hosting provider or server; informational, fill
  when known]
- Breakdance (version [read from wp-admin > Plugins once connected, then pin it here]) as
  the page builder
- Figma as the design source of truth (reached via the Figma MCP, not a URL)
- Claude Code with the Figma MCP and the WordPress MCP (see CONNECT.md)

## Staging operating model
- Agents touch the staging site only. Safety is by process, not the connector's env
  guards, so it does not matter what environment the site reports.
- At migration, move to the client domain and **remove the Agent Connector plugin and
  the MCP connection** before it goes live. This is the step safety depends on.
- Agent Connector settings: **Universal Abilities OFF, Log MCP events OFF**, everything
  else left as shipped. Exact toggle table in CONNECT.md.

## Breakdance conventions
- Auto Layout maps to Section and Div; column arrangements map to Columns.
- Repeating content uses the Post Loop Builder.
- Never write raw PHP layout files. Build through Breakdance elements only.
- Never blind-import settings. Always export first, then differential merge.
- Always run wp breakdance clear_cache after any DB-affecting operation.
- Content lives in the _breakdance_data postmeta. Back it up before writes.
- Pin the Breakdance version on staging. Re-test the write path after any update.

## Token source of truth
- Figma Local Variables are the source of truth for design tokens.
- Breakdance global variables mirror the Figma tokens.
- Reference variables, never hardcoded hex or off-scale spacing.

## Images and SVGs
For every raster image the build runs one process in order: **pull from Figma, rename from the
design, resize to display size, optimise for web, then upload and reference it.** SVGs are
inlined, not uploaded. WebP Express converts format server-side but does not resize, so images
must be sized down before upload, not left massive.

- **Upload path.** The build cannot upload through MCP (the media abilities are in the locked
  Universal pack). It uploads with `.claude/tools/optimize-and-upload.py`, which resizes,
  compresses and posts to the WordPress media REST API (`/wp/v2/media`) with the Application
  Password, scoped to media, no dangerous abilities. It reads the credentials from
  ~/.claude.json automatically (where claude mcp add stored them), so there is nothing to set.
  The build runs this script itself via Bash; the human never runs Python or commands.
- **The build can upload but not DELETE media.** The tool only posts. Before uploading, check
  for an existing attachment of the same name (breakdance-search-posts with
  post_type: attachment), or WordPress silently suffixes the new one `-1` and leaves the old
  one in place. Removing a stale attachment is a human action in wp-admin. The build extracts the assets it needs from the Figma
  frame, **renames each to a descriptive, SEO-friendly, kebab-case filename** based on what it
  shows and its role (for example `cataract-surgery-hero.jpg`, never the Figma layer name or a
  hash), and proposes alt text. You upload those named files; the build references them **by the
  uploaded file's URL** (the Breakdance beta MCP cannot bind media, proven), which still serves WebP
  and keeps alt but lacks `srcset`; a human binds them in the builder afterwards for `srcset`. Never
  use an external (Figma) URL; do not inline large data URIs.
- **Optimise before upload.** Images often export oversized (Figma exports at 2500px).
  Resize each to roughly 2x its display width, cap contained/section images at ~1600px and
  only full-width heroes at ~2500px, then compress (JPEG quality ~82). Pillow is available for
  this. WebP Express converts format server-side but does not resize, so dimensions must be
  right before upload.
- **Name and alt-text from the design, not by asking.** Read the names, section labels and
  content in the Figma frame to derive each filename and alt text (a surgeon's name, the
  section it sits in); do not ask the human for what the design already says. Name by section
  where it helps (for example practice-apart-*, surgeons-*).
- **Alt text is accessibility, not just SEO, and there is a right strategy.** Content images
  (photos, meaningful graphics) get descriptive alt written from what the design shows.
  Decorative icons get empty alt or aria-hidden, they add no information. Set the media fields
  at upload with the script (`--alt`, and `--title`, `--caption`, `--description` where useful),
  AND set the alt on the rendered image element in the layout. Accessibility is a certified
  gate, so get this right rather than putting generic text on everything. Follow the rules in
  `.claude/reference/alt-text-guidelines.md`.
- **Keep placeholder images as placeholders.** A dummy or grey-silhouette image is not renamed
  after a real person; give it a placeholder name and flag it so the human supplies the real
  asset later.
- **SVGs (icons, logos): inline them, do not upload.** WordPress blocks SVG uploads by default
  and you do not need it: the build pulls the SVG from Figma and places the markup directly in
  the layout as a Breakdance SVG Icon element. That is best practice for icons and logos
  anyway, crisp at any size, styleable with the colour tokens, no HTTP request. For a large
  SVG illustration where inlining would bloat the page, rasterise it to WebP (WebP Express is
  available) and treat it as a normal image, or add a Safe SVG plugin and upload it deliberately.
- If a plugin exposes a media-only upload ability outside the Universal pack, that one can be
  allowed so the build uploads safely. Check discover-abilities before assuming.

## Page copy: this repo owns it during the build

During the build this repo owns page copy. ZilvaEdge does not edit released pages while the
build is live. The Google Doc will go stale during the build; that is expected, and it is
refreshed at launch when the PM runs ZilvaEdge's content reconciliation.

- `content/` holds the approved copy, one markdown file per page. Build pages from those
  files. **Refuse to build a page whose released content is missing**, and tell the operator
  to request it, rather than improvising copy. Improvised copy looks finished, passes a
  visual review, and is not found out until the client reads it.
- **Microcopy is the only direct-write exception**: CTAs, button labels, short connective
  copy. Two lines of copy do not go through the full ZilvaEdge pipeline.
- **Full new pages or sections are requested from ZilvaEdge through ClickUp** and arrive as
  released content in `content/`. Do not improvise a page.
- **Any edit to a file under `content/`, and any copy written directly into a page including
  microcopy, gets a line in `CONTENT_CHANGELOG.md` in the same session.** That log is what
  ZilvaEdge reads at launch to work out what changed and why. An unexplained change gets
  reported as needing attention later, so logging it now costs ten seconds and saves a
  conversation.
- `content/_live/` is the export of what the site actually says, and it is evidence rather
  than input. Breakdance keeps live copy in the database, so without it there is no git trace
  of a heading changed in the Breakdance UI.

## Protected paths (do not edit)
- wp-config.php, wp-settings.php
- Anything under the production environment.
- .env and any secret-bearing file.

## Dos
- Scope every Figma read to one selected frame via its Copy-link-to-selection node id; the
  whole file overflows. On an overflow or a truncated metadata read, ask for the frame's
  selection link rather than retrying the same call.
- Work one page at a time and return a staging preview URL.
- Verify every built page against Figma with a screenshot diff.
- Before a write that would lose real work, make sure a **recovery path** exists: a manual DB
  snapshot, or existing coverage (a daily automatic backup, Breakdance revision history). A
  manual export is not mandatory if adequate coverage is in place. On a fresh, disposable site
  it can be waived (recorded). Caveat: Breakdance per-post revisions may not cover the global
  design-system layer and direct MCP writes may not create a revision, so for global-settings
  writes rely on the daily/full backup.

## Don'ts
- Do not run wp breakdance total_reset.
- Do not run wp breakdance import_settings blind.
- Do not run destructive shell commands (rm -rf, sudo).
- Do not commit secrets. The site connection and its Application Password live in your
  local Claude config via claude mcp add, never in the repo. See CONNECT.md.

## Build log
- Keep an audit trail in build-log/. The build-log.sh hook auto-records
  database-affecting commands; you record snapshots, gate approvals and milestones.
- Every gate in build-log/GATES.md needs a person's approval, never the AI's. Mark it
  Approved when approved; no need to record an owner name.
- Before a write that would lose real work, snapshot and log it. On a disposable empty
  site this may be waived by a recorded decision; reinstate before real work exists.

## House style
- British and Australian English. No em dashes, no en dashes, no double hyphens in
  prose (CLI flags in code are fine). No emojis.

## Reference
- Build runbooks and best practices are in docs/ (19 for the build runbook, 23 best practices).
- The full agency system, its complete docs and the front-half creative skills live
  in the AI Web Design System repo, not here. Consult it for anything not covered by
  this project. This repo is one client build and stays lean by design.
