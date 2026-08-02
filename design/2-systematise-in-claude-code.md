# 2. Build the Figma design system in Claude Code

After Claude Design's **"transfer to Claude Code"**, paste its transfer prompt into Claude Code, then
add the block below. Claude Code needs the Figma MCP connected (a Full/edit Figma seat). It works in
phases and stops to flag decisions, the same way the build prompts do.

---

Also build this to the agency design-system standard, and **work through it with me in phases.** Load
the Figma workflow skill first (it runs discovery, foundations, components, assembly and QA).

## Start (discovery, no writes yet)
- Read the transferred design and `reference/design-for-build-checklist.md`. Extract the tokens and
  component inventory, inspect the Figma file, confirm the fonts are available.
- **Flag the decisions and ask me before writing:** whether to tokenise or keep the source's one-off
  spacing values (a dump is not a scale), and any variant matrix that runs over the guideline (keep
  hover states regardless, Breakdance needs them). Lock the token set and component list with me, then
  build.

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
