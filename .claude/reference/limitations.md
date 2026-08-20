# Known limitations

Things the tools **cannot** do, proven on a real build, each with its workaround. The flip side of
`build-standards.md` (what we do) and `breakdance-limits` (how Breakdance works). Add a limitation
here the moment it is proven, with the evidence, so it is never rediscovered. Items marked *(beta)*
are Breakdance/Agent-Connector beta constraints, revisit them when the tool updates.

**Which Breakdance version each entry was proven on.** Entries dated **2026-08-17** or
**2026-08-18** come from the Skills Beyond build on **Breakdance 3.0.0-beta.3**. Undated entries
were proven earlier, on **3.0.0-beta.1**. This matters: these are bugs in a beta, and some of them
will be fixed. **Pin the version in `.claude/CLAUDE.md` at the start of every build, and re-test any
*(beta)* entry that blocks you rather than trusting it.** A limitation that no longer reproduces
gets its entry struck through with the version it was fixed in, not deleted, so the trail survives.

**Class names in the examples are unprefixed** (`.hero__cta`, `--space-sm`) for readability. A real
build prefixes them with the site's own `css_prefix`.

## Breakdance native MCP (beta)

- **Cannot bind an image to the media library.** *(beta)* `from: media_library` with the only
  permitted shape `{id, url, alt}` renders the grey "no image" placeholder; the hydrated shape the
  renderer needs is rejected by the schema. **→** Reference images by the uploaded file's URL (WebP
  is served, alt kept, no native `srcset`); a human binds them in the builder for `srcset`.
- **Cannot upload to the media library over MCP.** The media abilities are in the locked Universal
  Abilities pack. **→** Upload with `.claude/tools/optimize-and-upload.py` (WP media REST API, scoped).
- **Cannot delete media.** The upload tool only posts. **→** Remove stale attachments in wp-admin;
  check for an existing same-named attachment before uploading, or WordPress suffixes `-1`.
- **`design-system-init` does not exist** as a registered ability. *(beta)* **→** Use
  `insert-css-variables` (global variables) and `insert-stylesheet` (global classes).
- **`html-to-page` drops alt on URL-sourced images** and force-lazy-loads them. *(beta)* **→** Set
  alt (and disable lazy loading above the fold) with the element mechanism that carries width/height,
  and verify the rendered HTML.
- **A URL-sourced image needs BOTH alt property pairs, or it renders no `alt` at all.** *(beta,
  found 2026-08-17 on the About build.)* The FImage schema names `alt_when_from_url` and
  `custom_alt_when_from_url` for URL images, `html-to-page` stores them from the markup's `alt`
  attribute, and `get-post-tree` shows them stored correctly — but the renderer emits no `alt`
  attribute from those alone. **→** With `edit-post`, also set `content.image.alt: "custom"` and
  `content.image.custom_alt` to the same text. Always confirm in the rendered DOM; the stored
  properties look right either way.
- **Width and height are not emitted on URL-sourced images**, because Breakdance cannot read the
  file's dimensions. *(beta)* **→** Add them as custom attributes under
  `settings.advanced.attributes` so the image reserves its space and does not shift the layout.
- **`html-to-page` silently drops any class with no CSS rule of its own** (including hook/wrapper
  classes). *(beta)* **→** Give every class at least one rule, or do not rely on it existing.
- **Wrapping an `<svg>` in a `<div>` that carries the class LOSES the class entirely.** *(beta,
  proven 2026-08-18 on the Contact build, cost a rebuild of two sections)* Authoring
  `<div class="quotes__car"><svg>...</svg></div>` collapses the wrapper and emits an **unclassed**
  SVG Icon element, which then renders at its 1em default instead of its designed size. The call
  returns `success: true` with no warning, and `get-post-tree` shows an element that simply has no
  classes. **→ Put the class on the `<svg>` itself** (`<svg class="quotes__car">`); `html-to-page`
  moves it onto the generated wrapper div, which is what the CSS is written against. A real
  container with the class is fine when it has other children too (a chip wrapping a glyph works:
  `<span class="chip"><svg class="glyph">`); the failure is a wrapper whose only child is the svg.
  Verify by rendering the element and checking the class is on the `bde-f-svg-icon2` div, not by
  trusting the write.
- **A comma-separated selector list is SPLIT into one custom selector per member, it is not stored
  verbatim.** *(proven 2026-08-18)* `insert-stylesheet` with `.h1, .h2, .h3 { ... }` created three
  separate `custom`-type selectors named `.h1`, `.h2`, `.h3`, each sitting alongside the existing
  `class`-type selector of the same name. It works and the CSS is correct, but the builder then
  lists the same name twice. **→** Expect one selector per member. Use it deliberately (it is the
  safe way to add ONE property to several existing classes without restating their whole
  definitions, which is what the token bindings and per-breakpoint sizes make risky), and put the
  result in a clearly named collection so the duplicate names read as intentional. The tool
  description's "comma lists become a verbatim custom selector" does not hold.
- **`insert-stylesheet` maps raw CSS back onto the native properties AND re-links `var()` to the
  registered variable.** *(capability, proven 2026-08-18)* Restating a selector as plain CSS with
  `var(--space-sm)` stores it as `{var-<uuid>}`, the same binding the original had, and
  `background-image: url(...)` becomes a native `backgrounds` array entry of type `external_image`.
  So a full restatement does NOT downgrade a selector to literals, which is what makes the
  restate-everything rule below safe to follow.
- **`insert-stylesheet` replaces, it does not merge.** *(beta)* **→** Restate every rule and every
  breakpoint each time, or earlier ones are lost.
- **That replacement is TOTAL, across every breakpoint, even when your call only mentions one.**
  *(proven 2026-08-17, cost a broken section)* Sending
  `@media (max-width: 767px) { .areas__map { ... } }` with no base rule in the same call wiped the
  selector's base and tablet-landscape properties entirely, leaving only the phone values. The call
  returns `success: true` with no warning. **→** Treat every `insert-stylesheet` as writing the
  selector's complete definition: include the base rule and every breakpoint override in one
  stylesheet, every time you touch it. Verify afterwards with `get-css-selectors
  include_properties: true`, which shows exactly which breakpoints survived.
- **An `@media` query that is not a registered breakpoint is skipped, and it DOES warn.** *(probed
  2026-08-17)* `@media (max-width: 1300px)` returned
  `Skipped @media block ... (no registered breakpoint matches this query)`. So the warning is
  reliable for arbitrary queries; the silent failure is the one above. There is no way to add an
  intermediate stack point in CSS, so a layout that must change between two registered breakpoints
  has to be solved fluidly (`min()`, `clamp()`, `vw`) or by a person registering a new breakpoint in
  Breakdance settings. **There is no create-breakpoints ability**; `get-breakpoints` is read-only and
  breakpoints are not in the global-settings tree, so no agent can add one.
- **No automated cache clear from the connection** (the `wp-cli` ability is denied with the Universal
  pack). **→** `html-to-page` self-regenerates CSS on page creation; for edits to an existing page,
  clear the cache in wp-admin if it does not self-regenerate (unproven on edit, verify on the first).

- **Element names (the structure-tree labels) cannot be set over MCP.** *(beta)* The AI cannot name
  elements, so navigability comes from descriptive CSS class names plus Breakdance's content preview
  in the tree. **→** Keep classes meaningful; a human names structural groups in the builder if
  wanted; a rebuild through `html-to-page` discards manual names.
- **`insert-stylesheet` mangles some CSS values silently.** *(beta)* `opacity:1` stores as `0.01` (a
  bare `1` is read as a percentage), `background-image:none` is dropped, and the `border-*-color`
  longhands are dropped. **→** Never send `opacity`; write every hover fill as an explicit
  single-colour `linear-gradient`; write borders as the four-side `border: 1px solid ...` shorthand. A
  modifier that overrides only one longhand, or clears a `background-image` with `background-color`,
  fails silently, so test each variant on its first real use.
- **A lone `outline-color` longhand is dropped, the same way `border-*-color` is.** *(beta, proven
  2026-08-18)* A `:focus-visible` child storing only `effects.outline_color` emitted just the text
  colour, so a button meant to have a white ring inherited the base navy one. On a dark band that is
  an invisible focus ring, a real WCAG failure that looks fine in the stored properties. **→** Write
  the full `outline: 3px solid <colour>` plus `outline-offset` in any state rule that changes the ring,
  and check the ring's colour against what is actually behind it, not just that a ring exists.
- **A value of the form `calc(min(...) * 0.5)` is silently DROPPED, storing nothing at all.** *(proven
  2026-08-18.)* `width: min(732px, calc(100vw - 672px))` stores and renders correctly, but
  `width: calc(min(732px, calc(100vw - 672px)) * 0.4754)` and the matching `top`/`left`/`height` were
  all absent from the emitted CSS, leaving the element at its 18px default size with **no warning and
  `success: true`**. A bare `min()` is fine; multiplying one inside a `calc()` is not. **→** Do not
  scale a `min()` by a factor. Put the fluid `min()` on a wrapper with `aspect-ratio` and position the
  children inside it in **percentages**, which store correctly.
- **`transform: scaleX(-1)` is silently mangled to `matrix(-1, 0, 0, 0, 0, 0)`** *(proven 2026-08-17)*,
  i.e. the Y scale is zeroed, so the element computes a real height but renders 0px tall and is
  invisible. Single-argument `rotate()` is fine. **→** Write a mirror as the explicit
  `transform: matrix(-1, 0, 0, 1, 0, 0)`. Suspect this whenever an element has the right computed
  width/height but a zero bounding box.
- **The `html-to-page` `<style>` block imports only flat class selectors.** *(beta)* Attribute
  selectors, `:has()`, `:not()`, combinators, pseudo-elements and nested rules are dropped from a
  `<style>` block. **→** Put those in `insert-stylesheet`, which does store them (including counters,
  `z-index`, `order`, `grid-area`).
- **Rebuilding a section with `html-to-page` renumbers its element ids.** *(beta)* Every `edit-post`
  repair (alt text, lazy-load, attributes) must be re-applied to the new ids after a rebuild, or the
  fix is silently lost. **→** Re-verify alt in the rendered DOM after any section rebuild.
- **`create-post` has no slug field, and a page born as a draft gets an empty `post_name`.** So a
  child parented to a born-draft parent loses the parent path segment (`/glaucoma` instead of
  `/eye-conditions/glaucoma`). This has bitten twice. **→** To mint a nested slug, create the parent
  **published**, verify its slug, then revert it to draft.
- **`html-to-page` builds from the Fundamental `F*` primitives** (`FText`, `FTextLink`, `FImage`,
  `FSvgIcon`, `FRichText`, ...). *(beta)* There is **no `FContainer`**, and an empty `<div>` comes back
  as an `FText` that cannot take children. **→** Fetch the `F*` schema (not the plain element name)
  when editing; insert a real element rather than relying on an empty `<div>`.
- **`html-to-page` cannot build an HTML table. Every table tag becomes a plain Container.** *(beta,
  proven 2026-08-18 on the Pricing build)* A real `<table>` with `<thead>`/`<tbody>`/`<tr>`/`<th>`/`<td>`
  returned one warning per tag, all reading "Unsupported tag `<x>` rendered as a Container", so both
  the table semantics and any CSS relying on them (`table-layout`, `vertical-align`, `th:nth-child`)
  are lost. **→** Build tabular data as flex rows of Containers carrying the ARIA table roles
  (`role="table"` on the wrapper with an `aria-label`, `role="row"`, `role="columnheader"`,
  `role="cell"`), which DO survive, and give the cells percentage `flex-basis` widths. This keeps
  assistive-tech semantics and leaves every cell an individually editable element, which a real table
  inside a code block would not. Add `min-width: 0` to the cells: flex items otherwise refuse to
  shrink below min-content and push the row past 100% (cost a 6px clip at 1280).
- **Composite elements ship fixed sizes in the per-post CSS, and the controlling property is often
  NOT where you would look.** *(beta, proven 2026-08-18)* The **Frequently Asked Questions** element
  renders at `width: 600px` and the **Swiper** at `height: 400px`. Symptom is an element that
  ignores its column and a section that is mysteriously too tall. **→ Find the real property by
  reading the element's own CSS template with `get-element-css`**, which shows the Twig expression
  feeding each declaration, then fetch that path with `get-element-schemas`. Do not conclude a
  property does not exist from a handful of guesses.
  - Swiper height: `design.container.height: "fit-content"`.
  - **FAQ width: `design.wrapper.width`.** *(corrected 2026-08-18 on the FAQs build)* An earlier
    version of this entry said NO schema property exposed it and prescribed a CSS override. That was
    wrong. The template reads `width: {{ design.wrapper.width.style }}`, and the property is a real,
    settable, per-breakpoint control; setting it to `100%` emits `width:100%` and fixes it at
    source. The original probe missed it because it tried `design.size`, `settings.size`,
    `settings.advanced.size`, `design.layout` and `design.width`, none of which is the path.
  - Only if an element genuinely has no native control, beat the per-post rule with a two-class
    descendant selector (e.g. `.split--faqs .faq { width: 100% }`); per-post CSS loads after
    `selectors.css`, so `insert_after_id` reordering cannot win, only specificity can.
- **The FAQ element's typography is at `design.typography.title` / `.content`, not `design.item`.**
  *(beta, 2026-08-18)* `design.item` holds only padding, icon, backgrounds and gaps. Left at its
  defaults the question renders in the global heading font at a ratio-derived size (22.5px weight
  400), not the designed size. **→** Set `design.typography.title` and `.content` with
  `custom.customTypography`; `title_tag` there also gives the question a real heading level.
- **The Frequently Asked Questions element exposes no focus-state property.** *(2026-08-18)* Its
  questions render as real `<button>`s with `aria-expanded`/`aria-controls`, but the focus ring is
  the browser default. **→** Same contained exception as the header's MenuBuilder: add one
  token-based rule for `.bde-faq__question:focus-visible`, scoped under a class applied to the
  element via `meta.classes`.
- **The Swiper element has almost no design surface** *(2026-08-18)* — `design.container` exposes
  only width and height; there is no pagination, navigation or slide styling. **→** Theme it through
  Swiper's own custom properties (`--swiper-pagination-color`,
  `--swiper-pagination-bullet-inactive-color`, `--swiper-pagination-bullet-inactive-opacity`,
  `--swiper-pagination-bullet-size`, `--swiper-pagination-bottom`) set on a wrapper class you own.
  That is the library's supported theming API, not styling internal markup, so it does not fight the
  element's generated CSS. Note the `...-inactive-opacity: 1` custom property is NOT hit by the
  `opacity` mangling bug.
- **A composite element's native icon property DOES accept a multi-colour SVG with `var()` fills.**
  *(capability, proven 2026-08-18 on the FAQ accordion)* Passing `svgCode` containing
  `<rect fill="var(--color-brand-yellow)"/>` plus a glyph path in a second token colour renders
  both colours intact; the element's own `icon.color` does not flatten them. So a two-tone control
  (a coloured tile with a contrasting glyph) can be built without abandoning the token rule.
- **`html-to-page` emits one Fundamental Text (`FText`) element per `<p>` by default.** *(observed on a
  real build)* A multi-paragraph passage then becomes several separate elements, which is hard to edit
  and breaks the one-element-per-block editability standard. **→ Proven fix:** author the block as **one
  Fundamental Text with `tag=div`, the real `<p>` tags inside, and the site's prose/body class** (the
  class that styles the `<p>` children); it renders identically and stays a single editable element.
  Confirm in `get-post-tree` that it came out as one element. (FRichText was considered and rejected:
  unproven on this beta, and it would split the site across two body-text methods.)
- **The number in a rendered `bde-*` class is the element id** (e.g. `bde-f-text-link-340-152` is
  element 152), usable directly, **but the rendered HTML can lag the post data.** **→** Re-fetch or
  check `get-post-tree` before trusting an id from a cached render, and never conclude another session
  has finished from rendered HTML. `edit-post` `meta.classes` takes **selector ids from
  `get-css-selectors`**, not class-name strings, and the class must exist before the element uses it.
- **Inlined SVGs render with both fill and stroke set to `currentColor`,** and that CSS beats the
  SVG's own `fill="none"`, so a stroke-drawn icon fills into a solid blob (the footer clock became a
  solid disc). **→** Set fill and stroke explicitly in CSS, keyed off the paths' own
  `[stroke-width]`/`[fill]` attributes. An icon inside a button must inherit `currentColor`, never a
  fixed fill (a fixed colour fails contrast the moment the button inverts on hover). Strip `id`
  attributes before duplicating an inlined glyph.
- **Flex alignment is silently dropped on any breakpoint where `display` is not a flex value.**
  *(proven 2026-08-14 on the header icon buttons)* Writing `display: none; align-items: center;
  justify-content: center;` at base and then only `display: inline-flex` inside a media query stores
  the alignment as `layout.flex_align` on the **base** breakpoint, where `display: none` means
  Breakdance never emits it. The element then renders with `align-items: normal` and the contents sit
  top-left, with no error and nothing obviously wrong in the stored properties. **→** Repeat
  `align-items` and `justify-content` **inside the same breakpoint block that turns the flex display
  on**. Verify with computed style, not with `get-css-selectors`, because the properties look correct
  in storage.
- **A responsive `display` override loses to a later base rule of equal specificity.** *(proven
  2026-08-14 on the header)* `.header__cta { display: none }` inside `@media (max-width: 1023px)` had
  no effect because `.btn { display: inline-flex }` was registered later in `selectors.css`; media
  queries do not add specificity, so source order decided it. This bites whenever a utility class (a
  button, a layout helper) is applied to the same element as the class carrying the responsive
  override, and it gets worse because a later `html-to-page` call re-registering the shared class
  moves it further down the cascade. **→** Do not reach for `!important` or a compound selector.
  Re-import the overriding class with `insert-stylesheet` using `insert_after_id` pointing at the
  shared class and `move_existing: true`, so it lands after it. Restate the whole rule (base plus
  every breakpoint), since that tool replaces rather than merges.
- **The NATIVE alt control does nothing on a URL-sourced image.** *(beta, proven 2026-08-17)*
  `content.image.alt_when_from_url: "custom"` plus `custom_alt_when_from_url`, with or without
  `from: "url"`, stores without error and renders **no `alt` attribute at all**. **→** Do not reach
  for the native control; go straight to `settings.advanced.attributes` (below). Verify with
  `preview-element`, which bypasses page cache.
  *Update 2026-08-18:* setting **both** alt pairs (`alt` + `custom_alt` AND
  `alt_when_from_url` + `custom_alt_when_from_url`) alongside an `alt` entry in
  `settings.advanced.attributes` renders the alt correctly, and in the same call
  **`content.image.lazy_load: false` DID work** — the rendered `<img>` came back with no `loading`
  attribute at all, which is what an above-the-fold hero needs. So `lazy_load` is not reliably
  ignored; set it and verify in the rendered DOM rather than assuming either way.
- **Setting an image's `alt` through `settings.advanced.attributes` works, and is the fix for the
  dropped-alt limitation above.** *(proven on the header and footer logos)* Send `attributes` as the
  full array including the existing `width`/`height` entries plus `{"name": "alt", "value": "..."}`;
  it renders as a real `alt` on the `<img>`. Verify with `preview-element`, and re-apply after any
  section rebuild because ids renumber.
- **Native design properties DO accept `var()` tokens** (this is a capability, not a limitation, but
  it is routinely assumed otherwise). Passing a unit object as
  `{"number": 18, "unit": "px", "style": "var(--type-size-h6)"}`, or a colour field as
  `"var(--color-navy)"`, stores and emits the reference intact. So composite elements can be
  restyled through their native properties without breaking the token rule.
- **`global-settings.css` is a defaults `:root` block followed by an override block,** so the same
  custom property appears twice and the later one wins. **→** Read the whole file, not the first
  match, or you report a phantom failure. Check the compiled per-post CSS (`post-<id>.css`), not only
  rendered HTML, before deleting a global palette colour or preset.
- **`set-global-settings` deep-merges but replaces ARRAYS wholesale.** *(2026-08-14)* Removing one
  typography preset or one palette colour therefore means reading and restating the whole settings
  tree, which is a large read to do mid-build. **→** Treat a global-settings cleanup as its own short
  standalone job, not something tacked onto a page build, and check the compiled per-post CSS before
  removing anything a live page may still use.

## Figma (MCP)

- **A Mesh Gradient (and other editor-only pattern fills) is invisible to every extraction route.** It
  exports as the flat solid beneath it via the CSS export, `get_design_context`, and Figma's own image
  render alike. Cost one build about two days. **→** A band the designer expects tinted but that reads
  plain white/solid is a likely mesh fill: ask the designer to flag mesh layers at handoff (see
  `design-for-build-checklist.md`), and reproduce the wash as a CSS-gradient token sampled from a
  supplied PNG (never upload the PNG).
- **A PATTERN fill is invisible to `get_design_context` but DOES show in `get_screenshot`.** *(proven
  2026-08-18)* Every full-width band on one frame carried a faint road-network pattern; the code
  export reported the rectangles as flat hex colours. **→ This is the cheap way to catch the whole
  family of pattern and mesh fills:** screenshot the background rectangle **on its own** with
  `contentsOnly: true` and compare it against the flat colour the code export claims. Do it once per
  band on any new frame; it takes one call. Reproducing a pattern is a designer hand-off (ask for the
  tile as an SVG), never a trace from the screenshot.
- **Figma exports a pattern fill as an embedded RASTER inside an SVG wrapper, not as vector.**
  *(proven 2026-08-18)* The `.svg` looks promising but contains a band-colour `<rect>` plus one
  base64 PNG referenced through an SVG `<pattern>`. **→ This is good news, not bad:** the wrapper
  states the exact tiling recipe, so read it rather than measuring. `patternTransform="matrix(S 0 0 S
  x y)"` gives the tile size S and the offset, and the outer `<rect>` carries the band colour, the
  `fill-opacity` and any `mix-blend-mode`. Extract the base64 image, and **pre-composite** the
  pattern over the band colour at that opacity and blend mode rather than reproducing them in CSS:
  Breakdance mangles `opacity`, and a pre-composited tile needs only `background-image`,
  `background-repeat` and `background-size`. Watch for an off-by-one source: a 1401px-wide image for
  a 1400px tile carries a 1px overlap column, so crop `[1:width]` or the tile seams. Give the tile an
  opaque alpha channel so `optimize-and-upload.py` keeps it as PNG; it turns anything without alpha
  into JPEG, which does not preserve edge pixels and therefore seams.
- **Judge a low-contrast raster by MEAN error, never by max error.** *(cost two false alarms on the
  same asset, 2026-08-18)* A band pattern whose contrast is 12-17 greyscale levels was twice declared
  unusable, first as JPEG then as WebP, because the maximum single-pixel error reached 54. Measured
  properly the served WebP had **mean error 1.4 and a 95th percentile of 2**, and it looked clean.
  **→** Use mean and 95th-percentile error, and look at the rendered result, before rejecting a
  format. Also beware measuring "signal" as the gap between the two most common colours: on that
  pattern it captured the road surface and missed the dashed centre lines, which carry most of the
  contrast, and made a visible pattern look invisible.
- **Figma flattens a dashed stroke into an outlined path on export, producing multi-MB SVGs.** A
  winding road exported at **1.34 MB** and a straight dashed divider at **2.8 MB**, each a single
  `<path>` tracing every dash. **→** Do not inline or upload these. Take the underlying geometry
  (a companion un-dashed layer often carries the same `d`) and redraw the dashes as
  `stroke-dasharray` over it. 4.15 MB became 1.3 KB with no visible difference.
  *Worst case so far, 2026-08-18:* one winding road exported at **1.34 MB as a single `<path>` with
  34,218 commands**; rounding every coordinate to whole numbers still left 749 KB, so optimisation is
  not the answer. **→ Recovery method when there is no companion un-dashed layer:** each dash is its
  own closed subpath, so split the `d` on `M`, take each subpath's bounding-box centre to recover the
  centreline exactly, collapse collinear runs, and re-emit one smooth path. The dash length, gap and
  stroke width all fall out of the same measurements (there, 20 / 11 / 3). **1.34 MB became 1,011
  bytes.** Verify by overlaying the rebuild on the original in two colours.
- **The local Dev Mode MCP is not always enabled; the remote official Figma MCP is the reliable
  route.** *(proven 2026-08-17)* The local server returns an "enable Dev Mode MCP Server" message and
  needs the desktop app configured. The remote server reads the same file by `fileKey` plus node id
  with no desktop dependency. **→** Prefer the remote server; it also takes `maxDimension` on
  screenshots and returns a short-lived URL instead of inlining the image.
- **`get_design_context` on a whole page frame exceeds the context limit but SAVES TO FILE.** The
  error names the path. **→** Do not retry or narrow blindly; mine the saved JSON with python. A
  1920 x 7143 frame came back as about 68k characters holding every coordinate, colour and string.
- **`get_metadata` truncates on large frames** with a truncated SSE payload ("EOF while parsing a
  string"), deterministically at the same byte on retry. **→** Scope `get_design_context` to a frame
  instead. `get_metadata` with **no nodeId** returns the current Figma selection, which identifies a
  layer when copy-link-to-selection is not available.
- **Layer names go stale and can be actively wrong.** *(2026-08-17)* On one frame several card bodies
  were named after text no longer in them, and two option cards had swapped names: the layer named
  "Card / Automatic" held the heading "Manual". **→** Build from the rendered text content that
  `get_design_context` returns, never from `data-name`. Tell the designer; a future reader could
  easily build the swapped version.
- **A frame that is not in the register may be a wrapper, not a new design.** *(2026-08-17)* An
  operator's selection link looked like an unknown frame; `get_metadata` showed it was a review
  section whose only page child was a frame already in the register. **→** Run `get_metadata` on an
  unfamiliar node before assuming a redesign, and before discarding work already done.
- **A frame may be absolutely positioned rather than auto layout**, in which case there is no spacing
  rhythm to extract and the spacing scale is **derived and reviewable**, not measured. *(2026-08-14)*
  **→** Say so explicitly in the design-system proposal, record every derived value, and put it to
  the designer at the gate rather than presenting it as measured fact.

## Hosting firewall (LiteSpeed / mod_security on the DWS staging host)

- **Any API write whose payload injects a `<script>` tag is rejected with 403 Forbidden.** *(proven
  2026-08-18 wiring a booking widget)* Writing a JavaScript Code element containing
  `document.createElement('script') ... appendChild` returned a LiteSpeed 403 page, not a Breakdance
  error. A `console.log('probe')` payload into the same element wrote fine, so the element and the
  write path are healthy — it is the content that trips the rule, which is a standard cross-site
  scripting signature. Adding `document.getElementById` plus `addEventListener` to a second attempt
  tripped it too. **→ Do not tune the payload to get past it; that is evasion, not a fix.** A
  site-wide third-party loader belongs in WPCode Lite or the theme header anyway, so treat "load this
  vendor script" as a human step, like media deletion and breakpoint registration. The page-level
  code that *uses* the loaded global writes fine.

## Third-party embeds

- **Read a vendor loader before embedding it.** *(proven 2026-08-18)* One booking vendor's
  `widget.js` calls `document.write()` when no `container_id` is given. `document.write` after the
  document has finished parsing **replaces the entire document**, so the vendor's own copy-paste
  snippet will wipe a page whenever it runs late (async, deferred, or injected). **→** Always pass a
  `container_id` pointing at a real element, and put a fallback message inside that element: such a
  widget only overwrites the container's `innerHTML` on success, so the fallback survives if the
  script is blocked or slow. The failure is invisible until it fires.

## Gravity Forms (third-party, proven 2026-08-18)

- **An import file with no `markupVersion` falls back to LEGACY markup.** The form then renders
  `gform_legacy_markup_wrapper` / `gform-theme--no-framework`, and legacy CSS overrides the site's own
  form rules: two-column field grids collapse to one column and control sizing is ignored. Gravity
  Forms' own settings screen warns that legacy markup is incompatible with the Orbital theme and is
  removed in 3.1.0. **→** Put `"markupVersion": 2` in the import JSON. On a form already imported, a
  human unticks **Form Settings > Form Layout > Enable legacy markup**; there is no MCP route to it.
- **A form's `cssClass` is rendered with `_wrapper` appended.** Setting `cssClass: "gform-x"` puts
  `gform-x_wrapper` on the wrapper, NOT `gform-x`. **→** Do not rely on it. Put your own class on the
  container you control (the Breakdance Shortcode element via `meta.classes`) and write descendant
  rules from there.
- **The Orbital theme beats site CSS on control sizing and colour, and even beats inline styles**, so
  it is using `!important` somewhere the CSSOM does not expose (walking every readable stylesheet finds
  no matching rule). Symptoms: the submit button renders Gravity Forms blue at 38px however you style
  it, and a textarea keeps its `rows`-derived height. **→ `!important` DOES survive `insert-stylesheet`**
  and is the working fix; it is a justified exception against third-party plugin CSS, not a licence to
  use it against Breakdance's own defaults. Setting Gravity Forms' custom properties
  (`--gf-ctrl-btn-size`, `--gf-ctrl-size`, `--gf-icon-ctrl-select`, ...) on an **ancestor** does NOT work,
  because Gravity Forms sets them on the wrapper itself with an id selector; only setting them on the
  element itself, or a plain `!important` declaration, wins.
- **Turning legacy markup off adds a `"*" indicates required fields` legend** above the form that no
  design will show. Keep it: it is what explains the asterisks on required fields. Record it as a
  deliberate deviation rather than hiding it.

## WordPress

- **SVG uploads are blocked by default.** **→** Inline SVGs as Breakdance SVG Icon elements, or add
  a Safe SVG plugin to upload deliberately.
- **WordPress does NOT create an automatic redirect when a page's slug changes** in the cases that
  matter here. *(proven 2026-08-18)* The old URL returned a hard 404. **→** A slug change needs a
  real 301 rule in the SEO plugin, created by a human in wp-admin (every MCP ability is
  `breakdance/*`, and redirects live in a plugin table). **It must be recreated on production at
  migration**, because the domain changes and staging redirects do not travel with a fresh install.

## Agent Connector (beta)

- **Universal Abilities cannot be disabled** (no toggle on this beta). The dangerous pack (shell-exec,
  php-eval, file-write, wp-cli, etc.) stays registered. **→** Deny `mcp-adapter-execute-ability` in
  `settings.json` (blocks the MCP route for this project) and remove the connector at migration.
  Residual risk accepted, see the client DECISIONS log. Revisit if a toggle ships.
- **Some sites expose only `breakdance/*` abilities**, with no shell-exec, php-eval, wp-cli or
  filesystem tools at all. *(verified 2026-08-14)* That is a better posture than assumed. **→** Run
  `discover-abilities` and record what is actually exposed, rather than assuming the worst or the
  best. Deny the ability-executor meta-tools anyway, as defence in depth if the pack is ever enabled.

## Browser / QA

- **The pane-based browser tool needs a visible window** and cannot screenshot headless. **→** Use
  the chrome-devtools MCP (headless) for visual diffs and QA.
- **The chrome-devtools MCP can leave an orphaned Chrome holding its profile lock**
  (`~/.cache/chrome-devtools-mcp/chrome-profile`), which blocks the next launch. Hit repeatedly. **→**
  Kill only processes whose command line matches `chrome-devtools-mcp`, never `chrome.exe` broadly;
  check ownership before killing.
- **Lazy-loaded images never fetch in the Claude browser pane or a full-page capture,** so
  below-the-fold images read as broken and screenshot diffs come back with empty boxes. **→** Do not
  diagnose a missing image from the pane; force `loading="eager"` and scroll to the foot before
  capturing.
- **`resize_page` clamps at about 512px** (it reports 512 when asked for less). **→** Use `emulate`
  (e.g. `375x812x3, mobile, touch`) for true phone widths.
- **A programmatic `.focus()` reports `outline: 0px` even when the focus rule is applying.** *(cost a
  wrongly-declared accessibility defect, 2026-08-18)* `el.focus()` followed by
  `getComputedStyle(el).outlineWidth` returns `0px`, and `el.matches(':focus-visible')` returns **true**
  at the same time, so the reading looks trustworthy. A real `press_key: Tab` on the same control shows
  the correct `3px solid` ring. The headless window does not have true focus, so focus-visible styles
  are not painted. **→ Never judge a focus ring from `.focus()`. Tab to the control and read it, or
  screenshot it.** Check the emitted `selectors.css` too: if the rule is there with the right values and
  nothing competes with it, suspect the measurement before rewriting the CSS.
- **A collision detector needs its known exceptions excluded, not the layout changed.** *(2026-08-18)*
  A text-over-media check flagged seven chips that are *designed* to sit on a map graphic, every run.
  **→** Measure the real clearance before calling a collision a defect, and exclude a deliberate
  overlay by name in the check rather than "fixing" the design.

## Claude Code sessions

- **No automatic lock between chats.** Two sessions on one build can clobber shared writes. **→** Use
  the `build-log/ACTIVE.md` claim board and `parallel-builds.md`.

## DPI (not a limitation, a non-issue, recorded so it is not raised again)

- DPI is irrelevant for web, browsers render by pixel dimensions. There is nothing to set; only pixel
  dimensions and compression matter.
