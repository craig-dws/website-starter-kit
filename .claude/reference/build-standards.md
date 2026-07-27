# Website build standards

The single source for how we build. **Change a standard here and every future build follows.**
The build checklist (`build-checklist.md`) is the per-page tick-list of these standards; keep it
aligned with this file. Deep-dives are in the linked docs. Design-side standards (token naming,
base kit, anti-AI-look, house style) live in the `discoverweb-design-standard` skill.

## Images
- **Every image is optimised before upload, whatever its source.** Client-gallery, stock, or
  AI-generated images go through the same pipeline as design assets, no exceptions. There is no such
  thing as an image the AI drops in un-optimised.
- **Optimise before upload:** resize to roughly 2x display width, contained/section images
  ~1600px, full-width heroes ~2500px; compress (JPEG quality ~82). WebP Express serves WebP on
  the site, so do not pre-convert; just size and compress.
- **DPI is irrelevant for web.** Browsers render by pixel dimensions, not DPI, so "72dpi" changes
  nothing for display or file size. Only pixel dimensions and compression matter.
- **Rename** to descriptive, SEO-friendly, kebab-case filenames from the design; placeholders keep
  placeholder names.
- **Alt text** per `alt-text-guidelines.md`: descriptive for content images, empty for decorative.
- **SVGs inlined** as SVG Icon elements, not uploaded.
- Upload with `.claude/tools/optimize-and-upload.py` (scoped media REST API, no dangerous abilities).
- **Media library binding vs URL is tool-dependent.** Binding an image to the media library (media
  id) is best, it gives responsive `srcset`, WebP, alt and migration. **But the Breakdance
  3.0.0-beta.1 native MCP cannot bind media** (the schema forbids the only shape that renders,
  proven), so MCP-written images are referenced **by URL**. A URL image still serves WebP (WebP
  Express rewrites uploads-folder URLs) and keeps alt; it only lacks native `srcset`. To restore
  `srcset`, a human binds the images in the builder (pick from the library, ~30s each) as a batch
  pass, a responsive-images improvement, not a defect. Never use an external (Figma) URL, always the
  uploaded image. Revisit when the MCP supports binding.
- **No worked-out image? Build a placeholder, do not invent one.** For any page built without its
  imagery decided (any page with no design, or a design whose images are not final), put a
  **placeholder block** in the slot at the correct display size, per `image-placeholder.md`. Do not
  AI-generate or guess an image at build time, and do not leave the slot empty and let the layout
  collapse. Log every placeholder in the page record under **Outstanding images**.

## Image sourcing (a pass after the build, not during it)
Finding or creating the real images is its own pass once the layout is built, driven by the
**Outstanding images** lists in the page records. See `prompts/source-images.md`. For each
placeholder, in order:
1. **Client gallery first.** If the client supplied a gallery, search it for an image that fits the
   slot's subject and orientation, and use it if there is a genuine match.
2. **Else stock or AI.** If there is no gallery match, source a stock image or generate one, fit for
   purpose and licensed.
3. **Always optimise and upload** with the tool, set alt, then **swap the placeholder for the image**
   and clear the Outstanding-images row. Never bypass optimisation because an image "came from AI".
This pass is deliberately after the build so the layout is settled first; pouring images into a
still-moving layout wastes work.

## Typography
- Heading and body fonts from the design; substitute a non-webfont (e.g. Segoe UI) for the closest
  licensed webfont and record the decision.
- Sizes, line-heights and scale come from tokens; set the native Typography + Presets, not only CSS.

## Colour and tokens
- Every colour, type and spacing value references a token (`var(--...)`), never a hardcoded value.
- Populate the **native Global Settings** (Colours, Palette, Typography, Containers), not only CSS
  variables, so the palette is pickable and elements inherit. Differential writes only.

## Header and navigation
- **Sticky** (fixed on scroll, above content, content offset so nothing is hidden). On mobile,
  follow the design for what stays sticky, often the main bar sticks and the utility bar scrolls away.
- **Short on mobile:** main bar one row (logo, an icon-only CTA shown only on mobile, hamburger); a
  top/utility bar, if used, one row trimmed to what fits (phone and hours, drop the address if
  needed); at most two single rows, neither wraps.
- Built from `design/sitemap.md`, correct labels and slugs.

## Interactive states
- Menu items change colour on hover; buttons change background or text; dropdown items get a hover
  treatment and an arrow/icon; links have a distinct hover and a visible focus state.
- All states from tokens; **link hover distinct from the brand colour**.

## Responsive
- Breakpoints from `get-breakpoints`; no invented `@media` queries.
- Where the design is desktop-only, derive the responsive layer with standard collapse patterns and
  record every derived value for design review at the gate.

## Editability and structure (humans log in and edit, not only AI)
The output must be navigable and editable by a person in the builder, not just correct on screen.
- **Descriptive CSS class names carry the meaning.** Element *names* (the structure-tree labels)
  cannot be set over the Breakdance MCP (see `limitations.md`), so navigability comes from meaningful
  BEM class names (`ees-hero__copy`, `ees-approach__intro`) plus Breakdance's own content preview in
  the tree. Keep classes descriptive and consistent, this the build CAN control.
- **Human element names are an optional manual pass, structural only.** If a person wants extra
  clarity they name the sections and major groups in the builder, not every leaf. A rebuild through
  `html-to-page` discards manual names, so do not invest heavily.
- **Body copy is one Text element with its paragraphs inside it**, not a container or a separate
  Text element per paragraph. Over-structured text is harder to edit and bloats the DOM. Reserve
  separate elements for genuinely distinct blocks (a callout, a multi-column layout, a card). This
  the build CAN control, via the html-to-page markup.
- **Keep the structure shallow and sensibly grouped** (Section > Container > named groups) so a
  human can scan it. Do not nest for the sake of it.

## Accessibility (WCAG 2.2 AA, human-certified)
- Sane heading order, contrast meets AA, visible focus states, correct alt text.

## SEO basics
- SEO-friendly filenames and slugs, descriptive alt, sensible heading hierarchy, unique title and
  meta per page.
- **About and Contact page slugs carry the business name:** `about-<business-name>` and
  `contact-<business-name>` (e.g. `about-eastwood-eye-surgery`, `contact-eastwood-eye-surgery`).
  Agency default, it helps branded-intent searches. (Mildly redundant where the production domain
  already contains the business name, but keep it as the default for consistency.)

## Recovery before risky writes
- A recovery path must exist before a write that would lose real work: a manual snapshot, or
  existing coverage (daily backup, Breakdance revisions). For global-settings writes rely on the
  daily/full backup.

## Parallel work
- See `parallel-builds.md`: safe for independent page objects once the design system is locked;
  serialise global-style writes; claim work in `build-log/ACTIVE.md`.

## See also
- `design-for-build-checklist.md` — the designer-facing side: how to set up the Figma design so the
  build goes cleanly. Give it to the designer, and check the design against it at handoff.
- `limitations.md` — what the tools **cannot** do, and the workaround for each. Consult it before
  attempting something that may not be supported; do not retry a proven limitation.
- `build-checklist.md` — per-page enforcement of these standards
- `image-placeholder.md` — the placeholder block for images not yet worked out, and the sourcing pass
- `deferred-passes.md` — what is finished after the build, not during it (images, internal links, SEO
  meta), and the rule that these are recorded once as expected, never re-flagged as defects
- `alt-text-guidelines.md`, `parallel-builds.md`, `connect.md`
- the `breakdance-limits` skill — Breakdance constraints and the native-MCP build method
