# 2. Build the Figma design system in Claude Code

After Claude Design's **"transfer to Claude Code"**, paste its transfer prompt into Claude Code, then
add the block below. Claude Code needs the Figma MCP connected (a Full/edit Figma seat). It works in
phases and stops to flag decisions, the same way the build prompts do.

---

Also build this to the agency design-system standard, and **work through it with me in phases.** Load
the Figma workflow skill first (it runs discovery, foundations, components, assembly and QA).

## Start (discovery, no writes yet)
- **Base kit first.** Check `reference/base-kit.md`. If the agency base kit **exists** (filled with a
  library URL), build this client file as a Figma **Extended Collection** that inherits it and
  **overrides only colour, typography family and radius** (plus any brand-only components), do NOT
  rebuild the shared tokens or components. If it does **not** exist yet (early clients), build fresh as
  below, but **flag which tokens and components are base-kit candidates** for later extraction
  (`design/0-build-agency-base-kit.md`).
- Read the transferred design and `reference/design-for-build-checklist.md`. Extract the tokens and
  component inventory, inspect the Figma file, confirm the fonts are available.
- The transferred design is **one breakpoint (desktop)**. Systematise that; the responsive layer is a
  **separate later pass**, not decided here, so do not ask about responsive scope.

## Apply the agency defaults (do this, do not ask; report each at the gate)
These recurring decisions have a standard answer, so **apply them and report what you did** rather than
stopping to ask each time. Only stop for a genuinely novel or ambiguous call (a new shared component, a
real departure from the brand).
- **Spacing: snap to the agency 4pt grid.** A source with many one-off values is a dump, not a scale.
  Snap each to the nearest 4pt step and drop the odd one-offs (7, 11, 13, 19 and the like), so there are
  no off-scale spacing tokens.
- **Type ramp: collapse near-identical sizes.** Fold near-duplicate heading sizes into a minimal ramp
  (usually two or three roles below H2), and drop any size the design never uses. Never ship five
  near-identical heading tokens.
- **Contrast: fix AA failures at the token level.** Where a pair fails WCAG 2.2 AA, adjust the token to
  pass while keeping the look (darken a hover, lift a legal grey, raise an accent-on-dark). Confine a
  bright accent that only clears 3:1 to icons, rules and text at 24px or larger. Never ship a known failure.
- **Hover and focus states: always keep them**, even if the variant matrix widens (Breakdance needs them).

## Build (to standard)
- **Three-tier tokens** named to the token model: semantic aliases primitive, component aliases
  semantic, no duplicated raw values, no raw value above the primitive tier. Derive from the brief
  palette plus the transferred page. Every variable scoped, with `var(--...)` web code syntax.
- **Components with variants including hover**, text exposed as component properties.
- **Structured for Breakdance:** each band a full-bleed frame around a fixed container (Section then
  Div); Header and Footer single components (they become Global Blocks). Substitute a non-webfont per
  the standard if needed, and record it.

## Finish, and stop
- **QA:** zero unbound fills or strokes, zero unstyled text, zero default layer names, contrast checked
  to WCAG 2.2 AA on the tight pairs. Check the result against `design-for-build-checklist.md`.
- Give me a **short report** (what was built, the counts, any gap) and **stop for my review.**
- On my go-ahead, **produce the Breakdance token export** from the Figma variables (the values that
  populate Global Settings: Colours, Palette, Typography, Containers) and say where it is. This is the
  bridge to the build.
