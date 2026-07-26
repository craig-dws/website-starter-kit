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

## Claude Code sessions

- **No automatic lock between chats.** Two sessions on one build can clobber shared writes. **→** Use
  the `build-log/ACTIVE.md` claim board and `parallel-builds.md`.

## DPI (not a limitation, a non-issue, recorded so it is not raised again)

- DPI is irrelevant for web, browsers render by pixel dimensions. There is nothing to set; only pixel
  dimensions and compression matter.
