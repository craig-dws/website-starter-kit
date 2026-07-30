# Blog (archive + single-post template)

Paste this into Claude Code (in the client folder) to build a **blog / resources / news** section. A
blog is **templates, not pages**: you build a **single-post template** and an **archive listing** once,
as Breakdance Templates applied by conditions, and every post inherits them. **Never build blog posts as
individual pages, and never duplicate a layout per post** — one template serves them all and changes in
one place. For a normal one-off page, use `new-page.md` instead.

---

You are building the blog templates. Work to `.claude/reference/build-standards.md`, `limitations.md`,
and the **Template and Post Loop** notes in the `breakdance-limits` skill. Staging only, human-approved.

## Start
0. **Pull the latest** (`git pull`).
1. Read `.claude/CLAUDE.md`, `design/sitemap.md`, `build-standards.md`, `limitations.md`, the
   `breakdance-limits` skill, and check `build-log/ACTIVE.md`.
2. Get these from me (ask for any I have not given):
   - The **post type**: standard WordPress posts, or a custom post type. **Confirm the real slug with
     `wp post-type list`, never hardcode it** (limits/skill rule).
   - The **reference to match**: a Figma blog design if one exists (single and archive), otherwise the
     already-built page patterns to reuse (the card and grid for the archive, the prose pattern for the
     single post).
   - The **archive slug** and the **single-post URL pattern**, from the sitemap.
   - The **posts**: which already have content (in `site-content.md`), and whether the rest come later.
3. **Claim it** in `build-log/ACTIVE.md`.

## Build (two templates, once)
- **Single-post template.** A Breakdance **Template** bound to the post type with
  `set-template-conditions`. Lay the post out with **dynamic data** (title, content, featured image,
  date, category as the design shows) via `get-dynamic-fields`, not hardcoded text, so every post
  inherits it. Reuse the type's prose and heading components. One template serves all posts.
- **Archive / listing.** A Breakdance Template for the blog index (or the post type's archive), using a
  **Post Loop Builder** to list posts: featured image, title, excerpt, date, link. Reuse the existing
  card and grid components. This is the `/resources` or `/blog` index in the sitemap.
- **Do not lay out individual posts.** Once the single template exists, a post is just its title,
  content and featured image as a WordPress post, with no layout work. If the posts already have content
  in `site-content.md`, create them as posts (they inherit the template); otherwise note they come later.
- Apply the standards: reuse global classes, dynamic body as one Rich Text field, images via the
  pipeline (featured images are set per post, not in the template), hover and focus states, responsive
  from `get-breakpoints`, correct slugs and SEO.
- **Verify** (chrome-devtools, headless): the single template against one real post (create or pick a
  test post), and the archive listing renders and links correctly. Diff against the design if one
  exists, else confirm structure and the build checklist.

## Finish
- **Record** in `build-log/pages/` (name it for the templates, e.g. `blog-templates.md`): the two
  templates, their conditions, the post type and slug, and the Deferred passes (per-post featured images
  and SEO). Release your claim in `build-log/ACTIVE.md`.
- **Commit and push** (see `git-workflow.md`).
- **Send me the report** in the same shape `new-page.md` defines (Status, What I built, Needs you,
  Routine one line, Next). For a blog, "Needs you" usually means "add each post's featured image and its
  SEO in wp-admin / the later passes"; the templates themselves are done once. Then stop for my review.
