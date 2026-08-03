# 4. Design an extra page or landing page (on an existing site)

Use this to design **one more page** for a site that is already built or part-built, so the new page
matches the rest: a landing page, a new service page, or an extra page. It reuses the site's **existing
look**, in whatever form that look already exists, and does not reinvent it.

This is the design-side counterpart to `prompts/new-page.md` on the build side: one page, matching what
is already there.

## The "system" is whatever already exists (read this first)
Most sites will **not** have a maintained Figma design system, and that is fine. The look still exists,
it just lives in the build. Use whichever of these the site actually has, in this order:

- **A Figma file / design system** (the hoped-for case, if prompts 1 to 3 built one): reuse its tokens
  and components directly.
- **A website as the example** (when there is no Figma file): work from a live site and its screenshots.
  That example is usually **this site's own built staging pages** (match the brand already built, the
  Breakdance Global Settings colours, fonts and spacing, and the existing header, footer, buttons, cards
  and bands). But it can also be an **example site you have been given**, a sister or parent site, or an
  approved reference, whose style this page should follow. Either way, match its brand, layout rhythm and
  components so the new page is consistent.
- **Nothing bespoke needed?** If it is a straightforward extra page rather than a distinct landing page,
  you may not need to design it at all. Build it directly with `prompts/new-page.md`, which reuses the
  built Breakdance components (its "reference a built sibling" mode).

Paste the block below into **Claude Design** or **Claude Cowork**, with the client folder attached, and
either the **Figma file** (if one exists) or a **website example** (this site's built pages, or an
example site) and its screenshots. Connect Figma if you will design in it.

---

Design one page for this site, matching its existing look. **Work through it with me and stop where I
need to decide.** Load the Figma skills first if we are designing in Figma.

## Start
- Read the notes for **this page**: its goal, its audience, and the **single most important action** it
  drives. For a landing page, this is usually one focused conversion.
- Read what the look already is (see "The system is whatever already exists" above): the **Figma file**
  if there is one, otherwise the **website example** you were given (this site's built pages, or a
  reference site). This page matches that, it does not start a new style.
- Confirm two things with me before designing: the page's job and primary call to action, and, for a
  landing page, whether it keeps the site header and nav or is a **focused standalone** (landing pages
  often strip the nav to hold attention on one action).

## Design, matching the existing look
- Design the page using the **existing brand and components**: the same colours, fonts and spacing, and
  the same buttons, cards and section bands the built pages already use. Do not invent new colours, type
  sizes or spacings, reuse the established ones (the consistency rule from prompt 1 still applies).
- **Only add a new component if the page genuinely needs one** that does not already exist on the site.
  If you do, keep it on-brand, and **flag it** so it is built once and reused (and added to the Figma
  system or base kit if one exists).
- **Landing-page notes** (if this is one): one focused goal, the primary call to action strong and
  repeated, minimal competing links, trust signals near the action. Keep it unmistakably on-brand.
- Avoid the AI look, honour the brief's "what to avoid", keep **WCAG 2.2 AA** contrast.

## Finish, and stop
- Show me the page and **tell me the judgment calls**: any new component, and anywhere you departed from
  the brief or the existing look, and why. **Stop for my review.**
- On my approval, hand off to the build: this page goes through **`prompts/new-page.md`** (surgical, one
  page, reusing the built components). If you added a new component, it is built once first so the rest
  of the site can reuse it.

Responsive is handled the same way as any page: design the one breakpoint here, the build (Claude Code)
builds the mobile frame from it. In Cowork, design the mobile frame too.

British and Australian English, no em dashes, no emojis unless the brand calls for them.
