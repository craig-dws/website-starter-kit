---
name: breakdance-limits
description: The Breakdance builder's constraints as an instruction, so a design or build stays within what Breakdance can build editably. Use when designing layout for Target A (WordPress plus Breakdance), when planning a build, or when deciding how an agent may safely touch Breakdance. Covers the element vocabulary, the layout engine, Client Mode limits, the absence of a layout API, and the ranked, safe ways to write. Facts come from docs/08 and docs/24; do not invent Breakdance internals.
---

# Breakdance limits

This is the single highest-value build skill on Target A. It keeps a design
buildable and keeps an agent inside the safe envelope. Everything here is
sourced from docs/08 and docs/24. Where a fact is not confirmed, it says so.

## How Breakdance stores content

- Layouts are structured JSON in the `_breakdance_data` postmeta on each post or
  page. It is data, not hand-written PHP. Never write raw PHP layout files;
  Breakdance ignores them and it is a security risk.
- The main content types are Templates, Headers, Footers, and Global Blocks.
  Global Blocks are reusable regions edited once and reflected everywhere.
- **Never hardcode custom post type slugs.** They vary between sites. Confirm
  them on the real install with `wp post-type list` before relying on any slug.

## Element vocabulary and layout engine

Design to what Breakdance builds natively, so the client can still edit it.

- The container element is **Div**, not "Container".
- The layout mechanism is the **Layout Engine** with Vertical, Horizontal, and
  Grid modes. It is not a branded "Auto Layout".
- Use **Section** and **Div** for structure; the **Columns** element for column
  arrangements; the **Post Loop Builder** for repeating content.
- In Figma terms: Auto Layout maps to Section and Div; column arrangements map
  to Columns; repeating content maps to the Post Loop Builder.

## Design tokens on Breakdance

- Breakdance Global Settings hold the token layer: Global Colours and Global
  Typography Presets. These are the semantic tier (docs/22).
- The honest mapping (docs/22): colour and typography map well at the semantic
  tier; spacing maps partially; there is no clean component-token home. Do not
  promise component-tier parity on Target A.
- Move tokens with the token-sync skill (differential merge), never a blind
  import.

## Client Mode limits

Client Mode lets a client edit text, images, and links, but not alter layout,
structure, or global design. Design so every routine client edit falls within
text, images, and links and never needs a structural change. The vendor warns
Client Mode "does not restrict privileges", so treat it as a UX guardrail, not a
security control.

## The layout-write path

**Breakdance 3.0 (beta, July 2026) ships a native, first-party MCP that writes
layouts.** This is the preferred path and it may resolve what used to be Target
A's central risk. It is Beta 1 and unproven, so it is tested before it touches
client work (see docs/27, the write test). If it passes, no third party is
needed.

**On Breakdance 2.x, or if the native MCP fails the write test,** there is no
sanctioned layout API, and any agent that builds a page is reverse-engineering an
undocumented internal format through a third party (Novamira, Respira). That is
managed risk, not removed. (docs/24 Section C, docs/26.)

Consequences that shape every build, on either path:

- **Snapshot before every agent write** that can affect the database or a live
  file. Our backup is the safety net, not the vendor's rollback. This matters as
  much on the native path, which uses admin-equivalent access.
- **Pin the Breakdance version** on client staging. A point release has already
  broken a third-party write path (2.8.0, June 2026), and a beta feature can
  change under you. A Breakdance update requires re-testing the write path before
  it touches client work.
- **Staging only.** The agent never writes layout on production.
- **Keep the layout-write step a capability**, never a hardcoded vendor tool, so
  the binding (native 3.0 MCP first, Novamira or Respira as fallback, or a manual
  build) is swappable (CLAUDE.md principle 5). See the builder-builder subagent.

## Building with the Breakdance 3.0 native MCP (observed on a live 3.0.0-beta.1 install)

Confirmed on a real install via `get-instructions`, which **must be called before any
build or edit tool, every session**. It is the vendor's authoritative guidance and can
change between versions, so read it live rather than trusting this summary. For the native
MCP path, the convention below overrides the element-by-element assumption elsewhere in
this skill.

**Authoring method:**

- `insert-stylesheet` for the design system (global classes and selectors).
- `html-to-page` per section: author semantic HTML with a `<style>` block and pass it in;
  Breakdance converts it to native, editable elements. Do **not** assemble static layouts
  element by element.
- Reserve `edit-post` and the `set-element-*` tools for loops, forms and dynamic widgets,
  and for what `html-to-page` cannot express.
- **Populate the native Global Settings, not only CSS variables.** `insert-css-variables` and
  `insert-stylesheet` build the CSS-variable and class layer the pages reference, but they do
  NOT fill Breakdance's native Global Settings: the Colours (Brand, Text, Headings, Links,
  Background), the Palette, the Typography (heading font, body font, base size, ratio) and the
  Typography Presets. Populate those from the design tokens with `set-global-settings`, so the
  brand palette is pickable in the builder and elements inherit globally instead of being styled
  one by one. `set-global-settings` overwrites the whole blob, so do it as a differential: call
  `get-global-settings` first, merge the colours and typography into the existing settings, then
  set. Never blind-set. A design system with empty native Global Settings is only half done.

**Gotchas that fail silently, so fix them at design time:**

- **The theme is replaced entirely** (Breakdance Zero Theme). There are no prebuilt
  components; a card is a Container plus Image plus Text, built from scratch.
- **Only `@media` queries copied verbatim from `get-breakpoints` are imported.** A rounded
  or invented breakpoint is dropped silently, leaving a desktop-only page that looks fine
  until someone opens it on a phone. Use the exact breakpoints `get-breakpoints` returns.
- **Headings on a coloured background render near-black.** `h1`-`h6` and `a` get bare-tag
  rules from global settings, and a direct tag match beats inheritance, so set `color` on
  the heading's own class.
- **Loop items ship a hidden `padding: 20px`.** Designed cards need `design.post.padding`
  zeroed or the spacing is wrong.
- **Google Fonts load just by being named first in a `font-family`.** No `@font-face` and
  no `@import` needed.
- **`html-to-page` `<style>` blocks are global and outlive the page.** Every `<style>`
  block passed to `html-to-page` becomes a permanent selector in the site stylesheet;
  deleting the page does **not** remove it. Name selectors deliberately, and remove
  throwaway or superseded selectors with `delete-css-selectors`, or they silently
  accumulate and pollute the design system.
- **`html-to-page` drops alt text and force-lazy-loads URL-sourced images.** An image referenced
  by URL renders with no `alt` attribute even when alt was passed (leaving a linked logo with no
  accessible name), and gets `loading=lazy`, which is wrong for above-the-fold images. A URL `<img>` also lacks native `srcset`
  (WebP is still served by WebP Express). Binding to the media id would fix that, but **the native
  MCP cannot bind media**: `from: media_library` with the only permitted shape `{id, url, alt}`
  renders the grey "no image" placeholder, and the hydrated shape the renderer needs is rejected by
  the schema (proven on 3.0.0-beta.1). So MCP images are referenced by URL and a **human binds them
  in the builder** for `srcset`. Never use an external (Figma) URL, always the uploaded image. Set alt
  (and disable lazy loading for above-the-fold images) with the same element mechanism that
  carries width and height, and verify the rendered HTML rather than trusting the write. Check
  every URL-sourced image.

- **`html-to-page` silently drops any class that has no CSS rule of its own**, including classes
  written purely as structural hooks or band wrappers. A hook class with no rule vanishes from the
  output. Give every class at least one rule, or do not rely on it existing.
- **`insert-stylesheet` replaces, it does not merge.** Re-inserting a stylesheet restates every
  rule; restate all breakpoints each time, or earlier ones are lost.

**Cache on the native MCP path:** `html-to-page` regenerates the compiled CSS itself on
page creation (proven), so no manual cache clear is needed there and the WP-CLI
`clear_cache` command is not required. Whether it self-regenerates when editing an existing
page's postmeta is **unproven, verify on the first such edit**; if it does not, clear the
cache from wp-admin, since the connection may have no WP-CLI available. This supersedes the
blanket "always run wp breakdance clear_cache" guidance below for the native MCP path.

## Internal pages: content-first, from a page-type design plus the style guide

Pages of the same type share a design language, but they are not identical, content differs, so
**let the content drive the layout, not the other way around.**

**First, establish the mode at the design-to-build handoff.** Some projects hand over a design
for **every** page; others hand over a **few reference designs plus a style guide**. Decide which
at the handoff and record it: with a design per page, build each page from its own design; with
references plus a style guide, use the content-first approach below. Do not assume, it changes
what gets built.

- **The design system, one reference design per page type, and a style guide** define the visual
  language (tokens, components, spacing, the page-type layout). That is enough to build from.
- **Build each page from its type's reference as a starting point, then adapt it to that page's
  content.** A condition page with three sections and one with seven both start from the
  condition design; each is then adjusted to its own content. Do not force content into a rigid
  mould.
- **Claude can design pages that have no explicit frame** (a page type without a design) from the
  reference designs, the style guide and the content, staying within the design system. That is
  AI proposing a design for a human to approve, never AI approving its own design.
- **Genuinely uniform, content-light pages** (blog posts) can use a Breakdance **Template**
  applied with `set-template-conditions`, so one layout serves many and changes once. Do not
  duplicate a page N times, that creates copies that drift.
- **Shared sections** (a CTA band, a contact block, related links) go in a
  `create-reusable-global-block` Global Block, edited once, reused everywhere.

## Interactive states: build every interactive element with its states

Menu items, buttons, links and dropdown items need visible states, not just a default:
- **Menu items:** hover changes the colour.
- **Buttons:** hover changes the background or the text colour, per the button's styling.
- **Dropdown items:** a hover treatment, and consider an arrow or icon in front of the item.
- **Links:** a distinct hover, and keep a distinct focus state for keyboard users (WCAG 2.2 AA).

Drive these from design tokens (a hover-colour token), never a hardcoded value. Breakdance
derives some hover states from the brand colour, so confirm the design's intended hover exists
as its own token, especially **link hover**, which otherwise collapses into the brand colour
and loses its distinction.

The invariant is the design **system**, not the page layout: every page references the same
tokens, components and style guide, while its layout follows its content.

## The five ways to target Breakdance, ranked safest first

Prefer the highest-ranked method that can do the job (docs/08).

1. **WP-CLI settings and cache.** `wp breakdance status`, `wp breakdance
   clear_cache`, and Pro settings export and import applied as a differential
   merge. Supported and predictable.
2. **Global Settings JSON import and export.** Move the token layer via exported
   and imported Global Settings JSON, differential merge only.
3. **Constrained JSON-patch on known-good Global Blocks or templates.** Patch
   only values inside a structure that already works. Never restructure.
   Validate before and after, back up `_breakdance_data` first, human-reviewed.
4. **Builder-UI browser automation.** Drive the builder through the supported UI
   so it respects the builder's own validation. Slower and more fragile; back up
   first, human-reviewed.
5. **Raw `_breakdance_data` writes (last resort).** Highest risk. A malformed
   write destroys the layout. Only when nothing above can do the job, always
   after backing up the postmeta, always human-reviewed, always followed by
   `wp breakdance clear_cache`.

## Command safety

- Always run `wp breakdance clear_cache` after any database write. Postmeta
  writes do not fire `save_post`, so a cache purge must be explicit.
- Never run `wp breakdance import_settings` blind. It overwrites the whole
  config. Differential merge only, with the diff reviewed.
- Never run `wp breakdance total_reset` from any automated path. It is
  destructive and human-gated.
- Settings export and import are Pro only. Confirm the licence before relying on
  them.

## TODO (confirm on a real install before hardcoding anything)

- The exact custom post type slugs (for example the template, header, and footer
  types). Confirm with `wp post-type list`.
- The full native element vocabulary beyond Div, Section, Columns, and Post Loop
  Builder. docs/01 confirms these; the complete set should be captured from a
  live Breakdance install and added here.
- The layout-write capability binding for the project (native Breakdance 3.0 MCP
  first; Novamira or Respira only as fallback if the native path fails the write
  test in docs/27). Record which binding is in use and the pinned Breakdance
  version in the project CLAUDE.md.
