# Build checklist

Apply this to **every page and every component** (header, footer, menus, sections). This is
the plan, not a nice-to-have. A page or component is not done until every item is met or
consciously waived with a recorded reason. Work through it, do not wait to be asked.

These items enforce the standards in `build-standards.md` — **that file is the single source**;
change a standard there, this is the per-page tick-list.

## Layout and design
- Matches the design frame (screenshot diff via the chrome-devtools MCP, headless).
- Sections sit in the container/grid from the tokens (no edge-to-edge unless the design says so).
- Responsive at every breakpoint from `get-breakpoints` (no invented `@media` queries).
- **The header is sticky, responsive and short on mobile.** Sticky: fixed to the top on scroll,
  above content (z-index), with content offset so nothing is hidden; on mobile follow the design
  for what stays sticky, commonly the main bar sticks and the utility bar scrolls away. Compact
  on mobile, keep the header **as short as possible**: the **main bar is one row** (logo, an
  icon-only CTA shown only on mobile, and the hamburger), and a **top/utility bar, if used, is
  also one row** trimmed to only what fits (phone and hours, drop the address if needed). Neither
  bar may wrap, so the whole header is at most two single rows on mobile.

## Tokens
- Every colour, type and spacing value references a token (`var(--...)`), never a hardcoded value.
- The rendered CSS shows `var(--...)` references, verified, not baked-in numbers.

## Interactive states (menus, buttons, links, dropdowns)
- Menu items change colour on hover.
- Buttons change background or text colour on hover, per the button's styling.
- Dropdown items have a hover treatment, and an arrow or icon in front where the design shows it.
- Links have a distinct hover **and** a visible keyboard focus state (WCAG 2.2 AA).
- Every state comes from a token, and **link hover is distinct from the brand colour**
  (Breakdance derives it from brand otherwise and it loses its distinction).
- **Reveals and toggles work on touch.** Any hover/focus-driven reveal (dropdowns, expanding panels)
  also keys off `:focus`, because a tap fires neither `:hover` nor `:focus-visible`. Keep the
  `:focus-visible` ring separate for keyboard-only.

## Images
- Optimised before upload (sized to display width, compressed); full-width heroes only at ~2500px.
  **Every image, whatever its source** (client gallery, stock, AI-generated), goes through the pipeline.
- **Images not yet worked out use a placeholder block** at the correct display size (`image-placeholder.md`),
  never an invented image or a collapsed slot; each placeholder logged under **Outstanding images** in
  the page record. Sourcing the real image is a post-build pass (`prompts/source-images.md`).
- Descriptive alt on content images, empty alt on decorative; alt verified in the rendered HTML
  (`html-to-page` silently drops alt on URL-sourced images). See `alt-text-guidelines.md`.
- **Alt re-verified after any section rebuild** — re-running `html-to-page` renumbers element ids and
  re-drops alt, so the `edit-post` repair must be re-applied to the new ids (see `limitations.md`).
- SVGs inlined as SVG Icon elements, not uploaded. **Inlined SVGs set fill and stroke explicitly in
  CSS** (Breakdance forces `currentColor` on both and overrides the SVG's own `fill="none"`, so
  stroke-drawn icons otherwise render as solid blobs); an icon inside a button inherits `currentColor`.
- **Images reference the uploaded file** (WebP served, alt set). On the Breakdance beta the MCP
  cannot bind media, so images are URL-referenced; a human binds them in the builder for `srcset` as
  a batch pass. Never an external (Figma) URL.

## Accessibility
- Heading order is sane; colour contrast meets WCAG 2.2 AA.
- Focus states are visible; images carry the correct alt.

## Editability (a human logs in and edits this)
- **Descriptive, consistent CSS class names** (element names cannot be set over MCP, see
  limitations.md; classes plus Breakdance's content preview carry navigability). Human element names
  are an optional structural-only manual pass.
- **Each body block is ONE element** (a Rich Text element) holding all its paragraphs, not one element
  per paragraph. Verify in `get-post-tree` that a multi-paragraph passage came out as a single element,
  since `html-to-page` tends to split `<p>` tags into separate Fundamental Text elements (see
  limitations.md). Consolidate if it split.
- Structure is shallow and sensibly grouped, scannable by a person.

## Record
- Page or component recorded in `build-log/`; database writes and uploads logged.
- **Deferred passes recorded, not failed** (`deferred-passes.md`): placeholder images, internal links
  to real-but-unbuilt sitemap slugs, and drafted SEO title/meta go once in the page record's Deferred
  passes section. These do not fail the checklist. A link to an off-sitemap slug or an un-placeholdered
  empty image slot does fail it.
