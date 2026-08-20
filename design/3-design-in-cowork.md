# 3. Design and systematise in Cowork (one tool, end to end)

Paste this into Claude Cowork, with the client folder (brief, brand assets, photos) attached and the
Figma plugin connected (a Full/edit Figma seat). This is the alternative to prompts 1 and 2: Cowork
designs **and** builds the system in Figma. It works through the process with you and stops at the
natural gates. Use it to compare against the Claude Design to Claude Code path.

---

Design this client's site in Figma from the brief and build a build-ready design system. **Work
through it with me, stopping where I need to decide or approve.** Load the Figma skills first. The
brief carries the strategy, so design to it rather than re-doing it.

## Start
- Read the brief and the brand assets (logo files, photos).
- **Confirm what you need and ask me for anything missing or ambiguous** before designing: any open
  scope question in the brief, any brand colour that fails WCAG AA. One question at a time; default
  sensibly from the brief where you can.
- **Do not wait on the logo.** If the master files are not there, design with a placeholder at the
  right size and record it as outstanding. It is swapped in when it arrives. On a page for a site
  that is already live, do not ask for it at all: the logo is on the site and in the client's media
  library. Never redraw the mark from a screenshot.

## Design the homepage, then stop
- Design the **homepage (desktop)** to the brand palette and fonts exactly, the signature accent
  dominant; match the voice to the visual; follow the homepage notes; primary call to action in the
  header, body and foot with tap-to-call. Avoid the AI look and honour the brief's "what to avoid".
- **Show me the homepage and stop for review** before you build the system or the other breakpoints.

## Build the system (after I approve the homepage)
- **Base kit first.** Check `reference/base-kit.md`. If the agency base kit **exists** (filled with a
  library URL), build this file as a Figma **Extended Collection** that inherits it and **overrides only
  colour, typography family and radius** (plus brand-only components), do NOT rebuild the shared tokens
  or components. If it does **not** exist yet, build fresh as below and **flag the base-kit candidates**
  (`design/0-build-agency-base-kit.md`).
- **Tablet and mobile** frames.
- **Three-tier tokens** named to the token model (no duplicated raw values, every variable scoped with
  `var(--...)`), **components with hover variants** and text as properties, and the **Breakdance
  structure** (each band a full-bleed frame around a fixed container; Header and Footer as Global
  Blocks).
- **Apply the agency defaults, do not ask** (report each at the gate): **spacing** snaps to the 4pt grid
  (a many-valued source is a dump, not a scale, drop the odd one-offs); the **type ramp** collapses
  near-identical heading sizes into a minimal ramp (two or three roles below H2, drop sizes the design
  never uses); **contrast** failures are fixed at the token level to pass WCAG 2.2 AA while keeping the
  look, with any accent that only clears 3:1 confined to icons, rules and large text; **hover and focus
  states** are always kept. Only stop for a genuinely novel or ambiguous call.

## Finish, and stop
- **QA:** zero unbound fills or strokes, zero unstyled text, zero default names, contrast to AA. Check
  against `design-for-build-checklist.md`.
- Give me a **short report** and **stop for my review.** On my go-ahead, **produce the Breakdance token
  export** (variables to Global Settings), the bridge to the build.

British and Australian English, no em dashes, no emojis unless the brand calls for them.
