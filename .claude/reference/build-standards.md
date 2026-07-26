# Website build standards

The single source for how we build. **Change a standard here and every future build follows.**
The build checklist (`build-checklist.md`) is the per-page tick-list of these standards; keep it
aligned with this file. Deep-dives are in the linked docs. Design-side standards (token naming,
base kit, anti-AI-look, house style) live in the `discoverweb-design-standard` skill.

## Images
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

## Accessibility (WCAG 2.2 AA, human-certified)
- Sane heading order, contrast meets AA, visible focus states, correct alt text.

## SEO basics
- SEO-friendly filenames and slugs, descriptive alt, sensible heading hierarchy, unique title and
  meta per page.

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
- `alt-text-guidelines.md`, `parallel-builds.md`, `connect.md`
- the `breakdance-limits` skill — Breakdance constraints and the native-MCP build method
