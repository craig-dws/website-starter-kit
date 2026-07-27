# Cleanup punch-list

Standing housekeeping that needs **wp-admin or the connected build session** and cannot be done by the
build itself (deleting media, editing the live global CSS, wp-admin-only settings). These are **not
per-page defects** and should not be logged as follow-ups on individual page records: collect them here
and clear them before launch. This is the log-side companion to `.claude/reference/deferred-passes.md`.

Add a row the moment something is found that only a human or the connected session can finish. Tick and
date each as it is done.

## wp-admin (human, no MCP route)
- [ ] **Stale / duplicate media** — the build cannot delete media, only post it, so a name clash leaves
  a `-1` suffix. List the ids to delete and any file to re-upload for a clean slug.
- [ ] **Favicon / Site Icon and site-wide SEO config** — deferred pass 4 (`prompts/seo-meta.md`): the
  Site Icon, the site title template, the site description.
- [ ] **Unused breakpoints** registered but never authored into — delete unless deliberate.
- [ ] **`srcset` media binding** — a human binds URL-referenced images to the media library in the
  builder for responsive `srcset` (the MCP cannot bind media).

## Connected build session (live CSS / layout)
- [ ] **Any global-CSS reconciliation** where two rules fight for one role (e.g. two `a:hover` sources).
  Inspect the live cascade, pick one authority, remove the other.

## Verified done (record what was checked, so it is not re-raised)
- [ ] ...
