# Build checklist

Apply this to **every page and every component** (header, footer, menus, sections). This is
the plan, not a nice-to-have. A page or component is not done until every item is met or
consciously waived with a recorded reason. Work through it, do not wait to be asked.

## Layout and design
- Matches the design frame (screenshot diff via the chrome-devtools MCP, headless).
- Sections sit in the container/grid from the tokens (no edge-to-edge unless the design says so).
- Responsive at every breakpoint from `get-breakpoints` (no invented `@media` queries).

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

## Accessibility
- Heading order is sane; colour contrast meets WCAG 2.2 AA.
- Focus states are visible; images carry the correct alt.

## Record
- Page or component recorded in `build-log/`; database writes and uploads logged.
