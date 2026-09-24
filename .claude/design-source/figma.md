# Design source: Figma

The design is a Figma file, or the design pack extracted from it into `design-pack/`. New builds
from a design are proven on Breakdance only so far, and some lines below still say so.

## Project overview
Design-to-WordPress build for [CLIENT]. The design source is a Figma file
([FIGMA FILE - the source design file. Build each page from a Copy link to selection for its
frame, never by reading the whole file, which overflows on large multi-page files. Needed at
build time, not to connect; Figma is reached via its MCP]). Build target is the
Breakdance staging site at [STAGING_URL]. Production is
[PRODUCTION_URL - recorded for migration and launch only, never touched; fill at migration].

Starting condition: [ blank staging | DWS starter template | existing site with content ].
If a starter template or existing site, its current header, footer, home and demo content
are template defaults to be replaced, not client work, so Stage 4 is a replacement job, not
a blank canvas. This also underpins any snapshot waiver: a regenerable starter has nothing
to restore.

## Stack
- Figma as the design source of truth (reached via the Figma MCP, not a URL)

## Token source of truth
- Figma Local Variables are the source of truth for design tokens.
- Breakdance global variables mirror the Figma tokens.

## Images and SVGs
For every raster image the build runs one process in order: **pull from Figma, rename from the
design, resize to display size, optimise for web, then upload and reference it.** SVGs are
inlined, not uploaded. WebP Express converts format server-side but does not resize, so images
must be sized down before upload, not left massive.

- **Optimise before upload.** Images often export oversized (Figma exports at 2500px).
  Resize each to roughly 2x its display width, cap contained/section images at ~1600px and
  only full-width heroes at ~2500px, then compress (JPEG quality ~82). Pillow is available for
  this. WebP Express converts format server-side but does not resize, so dimensions must be
  right before upload.
- **Name and alt-text from the design, not by asking.** Read the names, section labels and
  content in the Figma frame to derive each filename and alt text (a surgeon's name, the
  section it sits in); do not ask the human for what the design already says. Name by section
  where it helps (for example practice-apart-*, surgeons-*).
- **SVGs (icons, logos): inline them, do not upload.** WordPress blocks SVG uploads by default
  and you do not need it: the build pulls the SVG from Figma and places the markup directly in
  the layout as a Breakdance SVG Icon element. That is best practice for icons and logos
  anyway, crisp at any size, styleable with the colour tokens, no HTTP request. For a large
  SVG illustration where inlining would bloat the page, rasterise it to WebP (WebP Express is
  available) and treat it as a normal image, or add a Safe SVG plugin and upload it deliberately.

## Dos
- Scope every Figma read to one selected frame via its Copy-link-to-selection node id; the
  whole file overflows. On an overflow or a truncated metadata read, ask for the frame's
  selection link rather than retrying the same call.
- Verify every built page against Figma with a screenshot diff.

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| node id, selection link | the link copied from a single Figma frame |
| WebP, WebP Express | the compressed image format, converted on the server |

Every page report says which page it covers, which staging URL to look at, and what needs
a human decision. Never ask the operator for something the Figma frame or `content/`
already says.
