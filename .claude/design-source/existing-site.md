# Design source: the existing site

There is no design file. **The site as it stands is the design.** Its own pages, sections,
reusable parts and tokens are the whole vocabulary, and the measure of success is that nobody,
visitor or client, can tell which page was built or rebuilt later.

Starting condition: an existing site with real content and real traffic. Nothing on it is a
template default. Every page, section and setting is there on purpose and stays, unless the
operator says otherwise.

## Where the design comes from
- **Tokens** are read from the site, where the builder file says they live. They are never
  changed. A change restyles every page.
- **The reference for a page is its sibling**: the existing page of the same type that is closest
  to it. Its structure is the pattern.
- **Take the inventory before building anything, and stop there.** Enumerate what the site already
  has, show it to the operator, and compose only from it. The procedure is the `existing-site-page`
  skill. **If the copy needs something the site has no pattern for, such as a table, numbered
  steps or a run of questions and answers, stop and ask.** Never improvise a section to fill the
  gap, and never add a token or a shared part to make one possible.
- **Where a drawing does exist**, such as a sketch or a frame for one section, it shows intent.
  The site's existing components still win over it.

## Images
- Reuse an image already on the site where it is genuinely the right one. Do not upload a second
  copy of it.
- Otherwise build a placeholder block at the right size, per
  `.claude/reference/image-placeholder.md`, and log it under Outstanding images. Never invent or
  generate an image at build time.
- A new image is still cropped, optimised, named and alt-texted to
  `.claude/reference/build-standards.md` and `alt-text-guidelines.md`. With no design to read
  them from, the name and alt text come from the page's approved copy and what the image shows.

## Verification
- There is no design to diff against. Compare the page with its siblings at each of the site's own
  breakpoints, and say honestly where it differs.
- The page is verified as editable the way the builder file says.
- **Never change an existing page's slug** (its address). It has history and inbound links.

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| inventory | the list of what the site already has, taken before anything is built |
| sibling page | an existing page of the same type, used as the pattern |
| slug | the last part of a page's web address |
