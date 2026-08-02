# Agency base kit (design reuse model)

The **one shared foundation** every client site is built on. It holds what does **not** change per
client: the three-tier tokens (spacing scale, type ramp and roles, radius scale, naming), the component
**structure** with states, the accessibility patterns and the Breakdance band structure. Only the
**brand layer** (colour values, typography family, radius values, logo, brand-specific components) is
swapped per client. This is the agency Design-System Reuse Model: **do not build a bespoke system per
client**; theme a shared base.

## Status

**NOT BUILT YET.** Until it exists, client design systems are built fresh (see the design prompts), and
the shared parts are flagged as base-kit candidates so the base can be **extracted from the first few
clients** (for example DWH and Eastwood, which already share the same Button, Card, Nav, Footer, Step,
List, Trust and Icon component types). Build it once with `design/0-build-agency-base-kit.md`, then fill
this file in. That switches the workflow from "build fresh" to "extend the base".

## Where it lives (fill in when built) — this is how everything references it

- **Figma base library URL / file key:** `[not built yet]`
- **Published library name:** `[not built yet]`
- **Token collections:** Primitives `[name]`, Semantic `[name]`, Component `[name]`

Once these are filled, the design prompts and the designer reference the base kit **from this file**: a
client Figma file subscribes to the library above and extends it.

## The shared foundation (build once, in the base kit)

- Spacing scale, type ramp and roles, radius scale.
- Component **structure** with states: Button, Card (pillar / resource), Nav/Link, Footer/Link,
  Step/Item, List/Reason, Trust/Item, form fields, icons.
- The three-tier token **naming**, the accessibility patterns, and the Breakdance band structure
  (full-bleed band around a fixed container; header and footer as global blocks).

## The per-client brand theme (swapped each time — this is what keeps sites distinct)

- Colour values, with their roles.
- Typography family (headings, body).
- Radius values, the logo, and any brand-only components.
- The page compositions. Sharing the base does **not** make sites look alike: the look comes from the
  theme and the composition, not from rebuilding the plumbing.

## How a client extends it (once built)

- The client Figma file is a Figma **Extended Collection** that inherits the published base library and
  **overrides only colour, typography family and radius** (plus adds brand-only components).
- It does **not** fork the base and does **not** rename tokens. Token names are an API: once a name
  ships, changing it breaks every client.
- Also paste the base kit's **semantic token names** into the token-model section of
  `discoverweb-design-standard.md`, which switches on the base-kit-adherence checks.

## Base kit semantic token list (paste when built)

`[Not yet supplied. Run v1 checks only until this is filled.]`
