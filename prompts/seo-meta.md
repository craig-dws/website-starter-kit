# SEO meta (deferred pass)

Paste this into Claude Code (in the client folder) to finish the **SEO titles and meta descriptions**,
once pages are built. The Breakdance MCP cannot write post meta, so these are set in wp-admin via the
SEO plugin (The SEO Framework). The build has already drafted them per page; this pass gathers the
drafts so a human pastes them in one sitting. See `.claude/reference/deferred-passes.md`.

---

You are running the SEO meta pass. Staging only, human-applied in wp-admin.

## Start
1. Read `.claude/CLAUDE.md`, `.claude/reference/build-standards.md` (SEO basics) and
   `deferred-passes.md`.
2. **Gather the drafts.** Read every `build-log/pages/*.md` and collect the **SEO meta** drafts (title
   and meta description) into one table: page, slug, title, meta description, character counts.
3. **Fill any gaps.** For any built page with no draft, write one now from the page's content and
   sitemap slug: a unique, specific title (`Primary Topic Location | Business Name`, roughly 50 to 60
   characters) and a meta description (roughly 140 to 160 characters, active, no filler, no keyword
   stuffing). About and Contact titles carry the business name per the slug rule.
4. **Check the site-wide config too**, since it is the same wp-admin sitting (deferred pass 4 in
   `deferred-passes.md`): the **favicon / Site Icon** (a fresh install has none), the **site title
   template** (a fresh install emits a duplicated `Business - Business` title), and the **missing site
   description**. List these as a short site-level block above the per-page table.

## Apply
- **Confirm the route.** Default is a **human paste** into The SEO Framework in wp-admin, one page at a
  time, because the MCP has no post-meta ability. Only if a safe post-meta route is confirmed (a REST
  endpoint the SEO plugin exposes, scoped like the media endpoint) may you apply directly, and only
  after showing me the route and one test write read back.
- Present the full table for me to paste, grouped by page, titles and descriptions ready to copy. Flag
  any that exceed the length guides.

## Finish
- Note in each page record that the SEO meta is applied (or handed to me to paste), and clear the SEO
  meta line from its **Deferred passes** section.
- Record the pass in `build-log/BUILD-LOG.md`.
