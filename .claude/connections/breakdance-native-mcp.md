# Connection: the Breakdance native MCP, through the Agent Connector plugin

Breakdance 3.0's own first-party MCP (the connection that lets Claude drive the site), exposed by
the Agent Connector plugin on the staging site.

**Supports:** Breakdance 3.0 and later. Not Breakdance 2.x, which has no native MCP. Not
Elementor, not a block theme.

**Credential:** a WordPress Application Password, registered with `claude mcp add` at the
default local scope, so it lives in your local Claude config (`~/.claude.json`) and never in
the repo. Setup: `CONNECT.md`, or `prompts/connect-mcps.md` on a new machine.

**Status:** proven on client builds, on Breakdance 3.0.0-beta.1 and beta.3
(`.claude/reference/limitations.md`).

## How each capability is done

| Capability | On this connection |
|------------|--------------------|
| Confirm the environment | `breakdance/site-info`: show the site address it returns. Call `get-instructions` first, every session |
| Read a page's layout | `get-post-tree` |
| Snapshot a page | No per-page export over this connection. A person takes a database backup, or confirms existing coverage (the recovery path below) |
| Write a page's layout | `html-to-page` per section, `edit-post` for what it cannot express, per `breakdance-limits` |
| Upload media | Not over MCP. `.claude/tools/optimize-and-upload.py`, below |
| Clear the cache | `html-to-page` regenerates the CSS when it creates a page. After an edit, unproven: a person clears the Breakdance cache and any page cache in wp-admin |
| Read the design tokens | `get-global-settings`, `get-css-selectors`, `get-breakpoints` |
| Write the design tokens | `insert-css-variables`, `insert-stylesheet`, and `set-global-settings` as a differential, per `breakdance-limits` |

## Stack
- Claude Code with the Figma MCP and the WordPress MCP (see CONNECT.md)

## Staging operating model
- Agents touch the staging site only. Safety is by process, not the connector's env
  guards, so it does not matter what environment the site reports.
- At migration, move to the client domain and **remove the Agent Connector plugin and
  the MCP connection** before it goes live. This is the step safety depends on.
- Agent Connector settings: **Universal Abilities OFF, Log MCP events OFF**, everything
  else left as shipped. Exact toggle table in CONNECT.md.

## Media over this connection
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
- If a plugin exposes a media-only upload ability outside the Universal pack, that one can be
  allowed so the build uploads safely. Check discover-abilities before assuming.

## Recovery path
- Before a write that would lose real work, make sure a **recovery path** exists: a manual DB
  snapshot, or existing coverage (a daily automatic backup, Breakdance revision history). A
  manual export is not mandatory if adequate coverage is in place. On a fresh, disposable site
  it can be waived (recorded). Caveat: Breakdance per-post revisions may not cover the global
  design-system layer and direct MCP writes may not create a revision, so for global-settings
  writes rely on the daily/full backup.

## Don'ts
- Do not commit secrets. The site connection and its Application Password live in your
  local Claude config via claude mcp add, never in the repo. See CONNECT.md.

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| MCP | the connection that lets Claude drive Figma or the WordPress site |
| `srcset` | the setting that serves a smaller image to a phone, added by hand in the builder afterwards |
| Application Password | the site login the upload script uses |
| Universal Abilities | the locked group of risky site actions, kept switched off |
