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
- **Crop each image to the ratio of the box it is displayed in, before upload.** A photograph is
  almost always 4:3 or 3:2 landscape and the slot it sits in often is not. `object-fit: cover` (the
  CSS rule that fills a box by cropping the image) then centre-crops it, and because
  `object-position` defaults to `50% 50%`, **nothing has chosen what to keep**. The result reads as
  wrong framing rather than as a deliberate crop. **→** Compose the crop by eye so the subject, the
  faces and any branding stay in frame, save it at the box's exact ratio, and reference that file.
  Two consequences worth planning for: the crop is a **judgement call worth recording** in the page
  record, because a rebuild loses it; and one source used at two different box ratios becomes **two
  files under two names**, not one.
  - Where a real crop is impossible (a shared image, a slot whose ratio changes responsively), set
    an explicit `object-position` instead. Never leave it at the default and hope.
  - **Do not upscale to reach 2x.** A 1024px source cropped for a 540px box lands at about 1.3x, and
    inventing pixels only softens it. Record the shortfall and ask the client for a
    higher-resolution original.
  - Proven on Skills Beyond 2026-08-18: nine images across four pages, worst case losing **37 per
    cent** of the picture. The operator spotted the 25 and 23 per cent cases by eye; the 37 and 35
    per cent cases were found only by measuring. **This is a measured check, not a visual review** —
    see `build-checklist.md` and `prompts/final-check.md`.
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
- **The heading scale is fixed site-wide and lives in `type-scale.md`.** Fill that file in once, at
  the design-system stage, then apply the shared classes it defines. Never invent a per-page heading
  size, never style a bare `<h1>`/`<h2>`, and never put a literal px size in a media query. Semantic
  tag and visual size are chosen separately: pick the tag for outline order, the class for size.

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

## Links
- **An external link opens in a new tab**, with `target="_blank"` and `rel="noopener noreferrer"`.
  An internal link never does. Set it on every external link as it is built, not as a later sweep:
  the miss is invisible in review because the link still works. (Added 2026-08-18. Found on Skills
  Beyond with six external links across two pages opening in the same tab while a seventh on a third
  page was correct, so it fails silently and inconsistently.)
- A link inside a composite element's rich-text field (a FAQ answer, for example) is easy to
  overlook because it is not a Text Link element. Check the rendered `<a>` tags, not the tree.

## Buttons
- **A button label never wraps.** `white-space: nowrap` belongs on the base button class, and
  nothing may override it back to `normal`. A label that will not fit gets **shortened**, or its
  container gets more room; it does not get to wrap.
- Check every button against its container at each breakpoint, not just against the viewport. A
  button that fits the page but breaks out of its card or its footer column still reads as broken.
- Where a button sits in a grid track, give the track a real minimum (`minmax(<min>, <fr>)`), not
  `minmax(0, <fr>)`. A zero minimum lets the track squeeze below the button and the button spills,
  which puts a horizontal scrollbar on every page carrying that component.

## Headings
- **No heading ends on a single word.** Apply `text-wrap: balance` to the heading classes so the
  browser evens out the lines. It costs one declaration and fixes every heading on every page at
  every width, which hand-tuning with non-breaking spaces does not.
- Headings inside a composite element (a FAQ accordion question) do not carry the heading classes,
  so they need the rule applying to the element's own title class as a scoped exception.
- **Pick one capitalisation convention for the whole site and record it**, at the design-system
  stage rather than at the final check. A Figma file will often carry both title case and sentence
  case within one page, so following the design is not an option once one convention has to win.
  Whichever is chosen, note the deliberate exceptions (FAQ accordion questions read wrong in title
  case, for instance) so a later reviewer does not "correct" them.

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
- **Each body block is ONE element holding all its paragraphs**, not one element per paragraph. A
  passage of two or three paragraphs under a heading is a single block, so it is **one Fundamental Text
  element with `tag=div`, the real `<p>` tags inside it, and the site's prose/body class applied** (the
  class that styles the `<p>` children), never a separate element per paragraph. This is the proven
  method: it renders identically and stays a single editable element where the copy lives in one place.
  Per-paragraph elements are hard to edit and bloat the DOM. Reserve separate elements for genuinely
  distinct blocks (a callout, a card, a multi-column layout).
  **Verify in `get-post-tree` that the block came out as one element**, since `html-to-page` otherwise
  emits one Fundamental Text element per `<p>`; consolidate if it split (see `limitations.md`).
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
  **`/contact-us/` and `/about-us/` are never acceptable**, on any build. They carry no brand or
  service term and win nothing in branded-intent search.
  **This rule outranks a sitemap that says otherwise.** A sitemap will often default these two
  slugs to the existing live URL to preserve ranking history. That is the wrong trade: take the
  business-name slug and carry a 301 (a permanent redirect) from the old URL, which preserves the
  history anyway. If a sitemap and this rule disagree, follow this rule and add the redirect.
  **Check the sitemap against this rule before any page is built** — it is a condition of the
  sitemap-approval gate, not a build-time check. (Proven on Skills Beyond 2026-08-18, where the
  sitemap had set `/contact-us/` and it had to be undone after the page was built, costing 42
  internal link repairs across the header, footer and five pages, plus a 301 that must now be
  recreated on production at migration.)

## Recovery before risky writes
- A recovery path must exist before a write that would lose real work: a manual snapshot, or
  existing coverage (daily backup, Breakdance revisions). For global-settings writes rely on the
  daily/full backup.

## Parallel work
- See `parallel-builds.md`: safe for independent page objects once the design system is locked;
  serialise global-style writes; claim work in `build-log/ACTIVE.md`.

## Content compliance (regulated niches)
Some clients are regulated (medical, dental, health, legal, finance). Where a client is regulated, keep
a **content-compliance reference** in the client's `.claude/reference/` (the niche's advertising rules,
for example AHPRA for medical practices) and **check every page's copy against it before it ships**, now
and in future. Treat a breach as a defect.

**The narrower carve-out on where copy is fixed.** For AHPRA-regulated clients the site still owns copy
during the build, as everywhere else, but only for changes that cannot alter a regulated claim.

- **On the site:** corrections, formatting, length fixes, headings, and non-clinical wording.
- **Back to ZilvaEdge:** any clinical claim, any outcome or benefit claim, any practitioner
  qualification, and any description of a treatment or service.

The reason is the order the checks run in. Those four categories are exactly what the AHPRA compliance
persona exists to check, and **it runs before the Doc, not after**. A change made on the site never
passes it. Editing one of them directly on the site does not just skip a review step, it puts a
regulated claim live that nothing has ever checked.

## See also
- `design/reference/design-for-build-checklist.md` — the designer-facing side: how to set up the Figma design so the
  build goes cleanly. Give it to the designer, and check the design against it at handoff.
- `limitations.md` — what the tools **cannot** do, and the workaround for each. Consult it before
  attempting something that may not be supported; do not retry a proven limitation.
- `build-checklist.md` — per-page enforcement of these standards
- `type-scale.md` — the site's single heading scale, filled in once at the design-system stage
- `image-placeholder.md` — the placeholder block for images not yet worked out, and the sourcing pass
- `deferred-passes.md` — what is finished after the build, not during it (images, internal links, SEO
  meta), and the rule that these are recorded once as expected, never re-flagged as defects
- `alt-text-guidelines.md`, `parallel-builds.md`, `connect.md`
- the `breakdance-limits` skill — Breakdance constraints and the native-MCP build method
