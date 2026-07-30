# Status (build progress and outstanding work)

Paste this into Claude Code (in the client folder) any time you want a snapshot of where the build is:
page-by-page progress, plus consolidated lists of images to update, things that need you, and what has
not been done yet. It reads the durable records and **changes nothing**.

---

You are giving me a build status snapshot. **Read-only, change nothing.** Work from the records, not
memory.

## Read
- `design/sitemap.md` (the full list of pages the site needs)
- every `build-log/pages/*.md` (a record means that page is built; read its Status and Deferred passes)
- `build-log/ACTIVE.md` (pages claimed or in progress right now)
- `build-log/CLEANUP.md` (the wp-admin / live-session punch-list)
- `build-log/content-changes.md` (the client-feedback plan and its open items), if present
- `.claude/reference/deferred-passes.md` (so you classify deferred items correctly)

## Give me this report. Plain language, scannable, no element ids or class names.

### 1. Pages
A table of every page in the sitemap, grouped by section, each with a status:
- **Not started** (no record, not claimed)
- **In progress** (claimed in `ACTIVE.md`)
- **Built, awaiting review** (a record exists, not yet approved)
- **Approved**

Finish with a one-line count: "X of Y pages built, Z awaiting review, W not started."

### 2. Images that need updating
Every placeholder across all page records (from their Outstanding images lists): page, what the image
is, display size. This is the list the `source-images.md` pass works from. If none, say "None."

### 3. Needs you (a person)
Everything only a human can do, gathered from each page's "Needs you" items, from `CLEANUP.md` (the
wp-admin and live-session jobs), and from any open decision in `content-changes.md`. Plain actions, most
important first. If none, say "None."

### 4. Not done yet (in the build)
The outstanding deferred work: SEO titles and meta not applied, internal links still pointing at pages
not built yet, images not yet bound in the builder for `srcset`, and any unresolved page follow-ups.
One line each. These are expected and scheduled, not defects; they are simply what remains.

Keep it plain. Do not change anything. If I ask, drill into any one page.
