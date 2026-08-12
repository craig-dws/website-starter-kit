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

## Content handoff back to ZilvaEdge (PM, before Gate 8)
- [ ] **`CONTENT_CHANGELOG.md` complete.** Every copy change made during the build has a line,
  including microcopy written straight into Breakdance. Check it against what `final-check.md`
  found on the live site, not from memory.
- [ ] **`content/_live/` exported and committed**, so reconciliation runs on what the site actually
  says rather than on what the repo claims. A missing export does not block the launch, but it
  makes the reconciliation self-reported, and that has to be stated rather than glossed over.
- [ ] **ZilvaEdge content reconciliation run**, so the client's Google Docs match the launched
  site. This is a Gate 8 precondition, not a nicety.

## Verified done (record what was checked, so it is not re-raised)
- [ ] ...
