# New page

Paste this into Claude Code (in the client folder) to build **one internal page**. Use it during the
internal-pages phase, once the design system is locked and the shared chrome (header/footer) is
built. For the first build or setup, use the guided or advanced prompt instead.

---

You are building one internal page. Work to `.claude/reference/build-standards.md`, the limits in
`.claude/reference/limitations.md`, and `.claude/reference/parallel-builds.md`. Staging only,
human-approved gates.

## Start
1. Read `.claude/CLAUDE.md`, `design/sitemap.md`, `build-standards.md`, `build-checklist.md` and
   `limitations.md`, and check `build-log/ACTIVE.md` for other active sessions.
2. Get these from me for the page (ask for any I have not given):
   - **Which page** and its **type** (condition / treatment / surgeon / content / other).
   - The **reference design** node id for that type (identify by node id, never by frame name).
   - The **slug** (from the sitemap).
   - The **content** (I paste it or point to the source).
3. **Claim it** in `build-log/ACTIVE.md` (what, which slug, the time, status active), so a parallel
   session does not collide.

## Build
- **Content-first from the reference design**, adapted to this page's content. **Reuse the type's
  existing components and global classes, do not re-invent them.**
- **If this is the first page of its type**, it establishes the type's shared components: build it
  **solo** (not in parallel), so the pattern is set before the rest fan out.
- **Do not write global settings, they are locked.** If the page genuinely needs a new shared
  component, stop and tell me rather than adding global classes mid-parallel.
- Apply the standards: **descriptive CSS classes**, **one Text element per body block**, images via
  `.claude/tools/optimize-and-upload.py` (referenced by URL, media binding is a known limit), SVGs
  inlined, hover and focus states, responsive from `get-breakpoints`, correct slug and SEO.
- **Verify** against the reference with a screenshot diff (chrome-devtools MCP, headless).

## Finish
- Record the page in `build-log/pages/<slug>.md`, log the writes, and **release your claim** in
  `build-log/ACTIVE.md`.
- Stop for my review before the next page.
