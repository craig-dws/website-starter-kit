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

## Images
- Optimised before upload (sized to display width, compressed); full-width heroes only at ~2500px.
- Descriptive alt on content images, empty alt on decorative; alt verified in the rendered HTML
  (`html-to-page` silently drops alt on URL-sourced images). See `alt-text-guidelines.md`.
- SVGs inlined as SVG Icon elements, not uploaded.
- **Images reference the uploaded file** (WebP served, alt set). On the Breakdance beta the MCP
  cannot bind media, so images are URL-referenced; a human binds them in the builder for `srcset` as
  a batch pass. Never an external (Figma) URL.

## Accessibility
- Heading order is sane; colour contrast meets WCAG 2.2 AA.
- Focus states are visible; images carry the correct alt.

## Editability (a human logs in and edits this)
- Every element has a **human-readable name** in the structure tree, no Breakdance defaults
  ("Div", "Text", "Fundamental Text"). CSS classes stay as the separate BEM styling layer.
- **Body copy is one Text element** with its paragraphs inside, not a container/element per paragraph.
- Structure is shallow and sensibly grouped, scannable by a person.

## Record
- Page or component recorded in `build-log/`; database writes and uploads logged.
