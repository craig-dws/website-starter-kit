# 4. Design an extra page or landing page (on an existing site)

Use this **after** the site's design system exists (homepage plus tokens plus components, built with
prompts 1 to 3). It designs **one more page** to a brief, a new content page, a service page, or a
standalone landing page, by **reusing the established system**. It does not rebuild the system.

This is the design-side counterpart to `prompts/new-page.md` on the build side: one page, reusing what
is already built.

Paste into **Claude Design** or **Claude Cowork**, with the client folder and the built Figma design
system (or the base-kit library) attached, and Figma connected.

---

Design one page for this site, reusing the existing design system. **Work through it with me and stop
where I need to decide.** Load the Figma skills first.

## Start
- Read the notes for **this page**: its goal, its audience, and the **single most important action** it
  drives. For a landing page, this is usually one focused conversion.
- Read the **existing design system**: the client's Figma file (or the base-kit library), its tokens and
  its components. This page is built from those, not from scratch.
- Confirm two things with me before designing: the page's job and primary call to action, and, for a
  landing page, whether it keeps the site header and nav or is a **focused standalone** (landing pages
  often strip the nav to hold attention on one action).

## Design, reusing the system
- Design the page to the brief using the **existing tokens and components**. Do not invent new colours,
  type sizes or spacings, reuse the established scale (the consistency rule from prompt 1 still applies).
- **Only add a new component if the page genuinely needs one** that does not already exist. If you do,
  name it to the system, keep it on-brand, and **flag it** as a candidate to add to the client system
  (and to the base kit if it is not client-specific).
- **Landing-page notes** (if this is one): one focused goal, the primary call to action strong and
  repeated, minimal competing links, trust signals near the action. Keep it unmistakably on-brand.
- Avoid the AI look, honour the brief's "what to avoid", keep **WCAG 2.2 AA** contrast.

## Finish, and stop
- Show me the page and **tell me the judgment calls**: any new component, and anywhere you departed from
  the brief or the system, and why. **Stop for my review.**
- On my approval, hand off to the build: this page goes through **`prompts/new-page.md`** (surgical, one
  page, reusing the built components). If you added a new component, it is added to the system first so
  the build has it.

Responsive is handled the same way as a system page: design the one breakpoint here, the build (Claude
Code) builds the mobile frame from it. In Cowork, design the mobile frame too.

British and Australian English, no em dashes, no emojis unless the brand calls for them.
