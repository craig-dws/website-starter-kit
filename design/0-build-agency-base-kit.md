# 0. Build the agency base kit (once, not per client)

Do this **once for the agency**, not for each site. It builds the shared foundation every client site
then extends: the three-tier tokens and the component structure, with **no client brand baked in**. Best
done after two or three client systems exist (DWH, Eastwood) so you extract what is genuinely common
rather than guessing. Paste into Claude Code with the Figma MCP connected (a Full/edit Figma seat).

---

You are building the **agency base kit** in Figma: the shared foundation all client sites extend. **Work
through it with me and stop where I need to decide.** Load the Figma skills first.

## Start
- Read `design/reference/base-kit.md` and `design/reference/design-system-rules.md`.
- Read the existing client Figma systems (I will give you the file links, e.g. DWH and Eastwood) and
  find what they share: the same Button, Card, Nav, Footer, Step, List, Trust and Icon structure, the
  scales and the naming.
- **Bring me the shared component list and the scales to confirm** before building. Anything genuinely
  client-specific stays out of the base.

## Build (brand-neutral)
- **Three-tier tokens:** primitives (neutral placeholder values), semantic (roles, no client colour),
  component (structure). The spacing scale, the type ramp and roles, the radius scale. Named to the
  token model, scoped, with `var(--...)` syntax.
- **The shared components with states:** Button, Card (pillar / resource), Nav/Link, Footer/Link,
  Step/Item, List/Reason, Trust/Item, form fields, icons. Include hover and focus.
- **Structured for Breakdance:** each band a full-bleed frame around a fixed container; header and
  footer as single components (Global Blocks).
- **No client colour, font family or logo** — those are the per-client override.

## Publish and record (this is what makes it referenceable)
- **Publish** the base as a Figma library.
- **Fill in `design/reference/base-kit.md`:** the library URL / file key, the collection names, the
  semantic token names and the component list.
- Paste the semantic token names into the token-model section of `design/discoverweb-design-standard.md`,
  which switches on the base-kit-adherence checks.

From then on a new client **extends** this (via `design/2-...` or `design/3-...`) instead of building a
system from scratch.
