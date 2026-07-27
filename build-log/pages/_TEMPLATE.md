# Page record — [PAGE NAME]

Copy this file to `pages/<page-slug>.md` for each page built. One record per page.

## Source
- **Figma frame:** [frame name / node link]
- **Slug / URL:** [/path]
- **Build target:** [A / B]

## Build
- **Built on:** [YYYY-MM-DD] by [name / agent]
- **Snapshot before first write:** [yes/no, location]
- **Staging preview URL:** [url]
- **Tokens referenced:** [list the token names used, or "all from global variables"]

## Verification (one page at a time, verified)
- [ ] Matches the Figma frame (screenshot diff attached / linked)
- [ ] Token names only, no hardcoded colour / type / spacing values
- [ ] Responsive at the required breakpoints
- [ ] Interactive states: hovers on menus / buttons / links / dropdowns, visible focus states
- [ ] Accessibility pass (contrast, headings, alt text, focus)
- [ ] Full build checklist applied (`.claude/reference/build-checklist.md`)
- [ ] No console errors on the rendered page
- [ ] Cache cleared after the last DB write

## Deferred passes (expected, resolved in a later pass — NOT defects)
What is deliberately left for a dedicated pass. See `.claude/reference/deferred-passes.md`. Record
once here; do not repeat these as follow-ups or defects. Omit any line that does not apply.

**Outstanding images** — placeholders to source later (`prompts/source-images.md`):
| What it is | Slot / section | Display size | Supply size (2x) | Requested | Status |
|------------|----------------|--------------|------------------|-----------|--------|
| [e.g. Glaucoma anatomy diagram] | [hero / body] | [980 x 468] | [1960 x 936] | [YYYY-MM-DD] | placeholder |

**Deferred links** — internal links to pages not built yet (real sitemap slugs, 404 until built;
resolved by building those pages, then the link check). All must exist in `design/sitemap.md`; a link
to a slug not in the sitemap is a defect, not a deferred item.
- [/target-slug, /another-slug ...] — N links

**SEO meta** — drafted here, pasted into The SEO Framework later (`prompts/seo-meta.md`):
- Title: [drafted title]
- Meta description: [drafted meta description]

## Status
[In progress | Built, awaiting review | Approved]

## Notes
[anything unusual: Breakdance limits hit, deviations from Figma and why, follow-ups]
