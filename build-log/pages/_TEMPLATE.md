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

## Status
[In progress | Built, awaiting review | Approved]

## Notes
[anything unusual: Breakdance limits hit, deviations from Figma and why, follow-ups]
