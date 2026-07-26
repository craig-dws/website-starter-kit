---
name: token-to-code
description: Sync Figma design tokens into the Astro code token layer (Tailwind config and CSS custom properties) using the shared semantic token names. Use when the design system tokens have changed and need to be reflected in the Astro build (Target B), or when the operator runs token-to-code. Reads Figma variables, updates the token files, and shows the diff for review. This is the Target B counterpart to token-sync.
---

# Token to code

Sync the Figma design tokens into the Astro code token layer without breaking
the naming bridge. This is Target B (Astro plus Payload). For Target A
(Breakdance) use the token-sync skill instead.

On this target the token layer is code, version-controlled in the Astro
repository. There is no CMS "global settings" equivalent and Payload never holds
a design token (docs/08b). All three token tiers map cleanly here (primitive,
semantic, component), unlike Breakdance (docs/22).

## Steps

1. Read the current design tokens from Figma with the variable-definitions
   capability (get_variable_defs). Scope reads to the collection, not whole
   files.
2. Map each token to its semantic name, identical across Figma, the Tailwind
   config, the CSS custom properties, and any Payload block field name. The
   naming bridge is the whole game (docs/08b, docs/22).
3. Update the Tailwind config and the CSS custom properties with the resolved
   values. Change values only; do not rename tokens unless a new token was
   agreed at handoff.
4. Show the diff for review. Pause for human approval before committing.

## Rules

- Preserve the semantic token names exactly. A rename breaks every component and
  every client theme that references the name.
- Never hardcode a value in a component when a token exists. A hardcoded hex or
  off-scale spacing value is a defect.
- Tokens live in code, never in Payload. Brand and theme tokens never pass
  through the CMS.
- Reference the client theme through the base kit plus Extended Collection model
  (docs/22): a retheme changes semantic and primitive values, not component
  structure.
- British and Australian English. No em dashes, no en dashes, no emojis.

## TODO (per project)

- Confirm the exact location of the Tailwind config and the CSS custom-property
  file in the client's Astro repository, and record them in the project
  CLAUDE.md. This system does not assume a fixed path.
