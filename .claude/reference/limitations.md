# Known limitations

Things the tools **cannot** do, proven on a real build, each with its workaround. The flip side of
`build-standards.md` (what we do) and `breakdance-limits` (how Breakdance works). Add a limitation
here the moment it is proven, with the evidence, so it is never rediscovered. Items marked *(beta)*
are Breakdance/Agent-Connector beta constraints, revisit them when the tool updates.

## Breakdance 3.0.0-beta.1 native MCP

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
- **`html-to-page` silently drops any class with no CSS rule of its own** (including hook/wrapper
  classes). *(beta)* **→** Give every class at least one rule, or do not rely on it existing.
- **`insert-stylesheet` replaces, it does not merge.** *(beta)* **→** Restate every rule and every
  breakpoint each time, or earlier ones are lost.
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
- **`global-settings.css` is a defaults `:root` block followed by an override block,** so the same
  custom property appears twice and the later one wins. **→** Read the whole file, not the first
  match, or you report a phantom failure. Check the compiled per-post CSS (`post-<id>.css`), not only
  rendered HTML, before deleting a global palette colour or preset.

## Figma (MCP)

- **A Mesh Gradient (and other editor-only pattern fills) is invisible to every extraction route.** It
  exports as the flat solid beneath it via the CSS export, `get_design_context`, and Figma's own image
  render alike. Cost this build about two days. **→** A band the designer expects tinted but that reads
  plain white/solid is a likely mesh fill: ask the designer to flag mesh layers at handoff (see
  `design-for-build-checklist.md`), and reproduce the wash as a CSS-gradient token sampled from a
  supplied PNG (never upload the PNG).
- **`get_metadata` truncates on large frames** with a truncated SSE payload ("EOF while parsing a
  string"), deterministically at the same byte on retry. **→** Scope `get_design_context` to a frame
  instead. `get_metadata` with **no nodeId** returns the current Figma selection, which identifies a
  layer when copy-link-to-selection is not available.

## WordPress

- **SVG uploads are blocked by default.** **→** Inline SVGs as Breakdance SVG Icon elements, or add
  a Safe SVG plugin to upload deliberately.

## Agent Connector (beta)

- **Universal Abilities cannot be disabled** (no toggle on this beta). The dangerous pack (shell-exec,
  php-eval, file-write, wp-cli, etc.) stays registered. **→** Deny `mcp-adapter-execute-ability` in
  `settings.json` (blocks the MCP route for this project) and remove the connector at migration.
  Residual risk accepted, see the client DECISIONS log. Revisit if a toggle ships.

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

## Claude Code sessions

- **No automatic lock between chats.** Two sessions on one build can clobber shared writes. **→** Use
  the `build-log/ACTIVE.md` claim board and `parallel-builds.md`.

## DPI (not a limitation, a non-issue, recorded so it is not raised again)

- DPI is irrelevant for web, browsers render by pixel dimensions. There is nothing to set; only pixel
  dimensions and compression matter.
