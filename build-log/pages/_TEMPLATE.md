# Page record — [PAGE NAME]

Copy this file to `pages/<page-slug>.md` for each page built. One record per page.

## Source
- **Figma frame:** [frame name / node link, or "none: patterned from <sibling page>" on an existing site]
- **Slug / URL:** [/path]
- **Build target:** [A / B]
- **Builder / connection:** [e.g. breakdance / breakdance-native-mcp, block-theme / wordpress-rest]
- **Snapshot before overwrite:** [snapshot file, on any page that existed before this work; "n/a, new page" otherwise]

## Build
- **Built on:** [YYYY-MM-DD] by [name / agent]
- **Snapshot before first write:** [yes/no, location]
- **Staging preview URL:** [url]
- **Tokens referenced:** [list the token names used, or "all from global variables"]

## Verification (one page at a time, verified)
- [ ] Matches the Figma frame (screenshot diff attached / linked)
- [ ] Token names only, no hardcoded colour / type / spacing values
- [ ] Responsive at the required breakpoints
- [ ] **Measured, not eyeballed:** image crop loss 0% on every image, no text over a graphic at any
      breakpoint, no button breaking its container
- [ ] Interactive states: hovers on menus / buttons / links / dropdowns, visible focus states
      (focus rings checked by pressing Tab, never by a script)
- [ ] External links open in a new tab with `rel="noopener noreferrer"`; internal links do not
- [ ] Accessibility pass (contrast, headings, alt text, focus)
- [ ] Full build checklist applied (`.claude/reference/build-checklist.md`)
- [ ] No console errors on the rendered page
- [ ] Cache cleared after the last DB write
- [ ] Public page shows the new copy, checked logged out
- [ ] Opens cleanly in the builder's editor, per the builder file (block theme: no invalid-content
      warning, every ACF field renders). Checked by: [person / logged-in browser]
- [ ] Rebuild only: slug, status and parent unchanged; every link kept or its removal noted;
      every conversion button's address identical, query string included

## Composed image crops (judgement calls a rebuild would lose)
Only where a source was cropped to fit its box. Record what was kept and why, so a later rebuild or
a re-export does not blindly centre-crop it again. Omit if no image needed a crop.

| Image / class | Box (w x h) | Source | Crop taken (source px) | What the crop keeps |
|---|---|---|---|---|
| [e.g. hero photo, `x-hero__img`] | [663 x 769] | [file.jpg, 2048 wide] | [x 418-1742, full height] | [driver, roof sign, P plate; loses the rear of the car] |

Note where one source is used at two different box ratios: that is **two files under two names**,
not one. Note any image left below 2x for its box, with the reason (do not upscale).

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
