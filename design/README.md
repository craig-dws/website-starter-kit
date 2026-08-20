# Design workflow

The design half of a build, kept lean. The **brief** (from ZilvaEdge) already carries the strategy,
audience, voice, page notes, brand colours, fonts and constraints, so the design step turns the brief
into a homepage and a build-ready Figma **design system**, it does not re-do strategy.

There are **two paths to the same result**. Run both on the same brief to see which you prefer, then
standardise on the winner.

## First, the reuse model (read `reference/base-kit.md`)
Do **not** build a bespoke design system per client. The agency keeps **one shared base kit** (the
spacing scale, type ramp, component structure, naming, states — the plumbing) and each client **swaps
only the brand layer** (colour, fonts, radius, logo, brand-only components). Sharing the base does not
make sites look alike: the look comes from the theme and composition.
- **Once, for the agency:** build the base kit with **`0-build-agency-base-kit.md`**, then record it in
  `reference/base-kit.md`. Best done after two or three clients exist so you extract what is common.
- **Per client, once the base kit is recorded:** the client Figma file **extends** the base (overriding
  only colour, type, radius). Prompts 2 and 3 do this automatically when `reference/base-kit.md` is filled.
- **Until the base kit exists (early clients):** build fresh, and the prompts flag the shared tokens and
  components as base-kit candidates for later extraction.

## Path A — Claude Design, then Claude Code (best for a build-ready system)
1. **`1-design-in-claude-design.md`** — Claude Design designs the homepage from the brief.
2. **`2-systematise-in-claude-code.md`** — its "transfer to Claude Code" prompt, plus our standard, has
   Claude Code build the Figma design system (three-tier tokens, components with hover, Breakdance
   structure, QA) and produce the Breakdance token export.

## Path B — Cowork (one tool, end to end, gives responsive frames)
- **`3-design-in-cowork.md`** — Cowork designs the homepage plus tablet and mobile, and builds the
  design system, in Figma, in one place.

## Then, either path
3. **Polish in Figma** and approve (one design gate).
4. **Internal pages** — feed the polished homepage and system back to Design or Cowork.
5. **Token export to Breakdance Global Settings** hands over to the build side (`new-page`, etc.).
6. **`5-export-design-pack.md`** pulls everything the build needs out of Figma into `design-pack/`,
   so the developer can build the whole site from the repo with no Figma seat. Run it **once the
   design is final**, on the machine that has the Figma connection, and re-run it after any later
   design change. Optional, but it is what lets a developer with only a view seat build the site.

## Later, any time — one more page on a built site
- **`4-design-an-extra-page.md`** — design a **single** page (a landing page, or an extra service page)
  against the **existing** system, reusing its tokens and components. This is the design-side twin of
  `prompts/new-page.md`: it does not rebuild the system, it composes one page from it, and only adds a
  new component if the page genuinely needs one. Run it whenever a site needs another page.

## The checks (guardrails, not stages)
All three prompts point at the same standards in `reference/`:
- `design-for-build-checklist.md` — is the Figma build-ready.
- the design-system rules, quality standard and anti-AI-look / house-style audit
  (`discoverweb-design-standard` skill).
- WCAG 2.2 AA contrast (the brief flags where a bright accent fails on white).

That is the whole design process: **brief in, homepage and a tokenised Figma design system out, checked
against the standards, exported to Breakdance.**
