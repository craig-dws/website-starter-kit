# Connection: the WordPress REST API, with an Application Password

WordPress's own built-in REST API (the site's interface for reading and writing content),
authenticated with an Application Password (a revocable, per-person site login generated in
wp-admin). **No plugin is installed.** It works directly on a staging site over HTTPS.

**Supports:** a WordPress block theme and WPBakery, for layout. Both keep a page's layout in the
page's own content (block markup, or shortcodes), which is exactly what this API reads and writes.
Not Elementor or Breakdance for layout: they keep layout in fields this API does not write as
layout. (Their own connections already use this API for media, which is a different job.)

**Credential:** in `.claude/settings.local.json` in this project folder, as three values in its
`env` block: `WP_SITE_URL`, `WP_API_USERNAME` and `WP_API_PASSWORD`. That file is excluded from git
by this kit's `.gitignore`, so it stays on this one machine. Each person generates their own
password. Setup: `prompts/connect-rest.md`.

**Status:** the storage model and the endpoints were verified against a live block theme site on
16 September 2026 (AI Web Design System, docs/24 Section I). Writing through this kit's tools has
not yet been proven on a client site, so the first write on each site is a throwaway test page,
checked in the editor and then deleted by a person.

On WPBakery: the storage model and the site's element usage were read from a live WPBakery 8.7.1
site's 37 public pages on 1 October 2026 (AI Web Design System, docs/24 Section J). **Writing is
unproven**, and so is whether a save through this API rebuilds WPBakery's Design Options styling.
The first page settles both (`wpbakery-limits`).

## How each capability is done

All through `.claude/tools/create-post.py`, which the build runs itself. The operator never runs
it.

| Capability | On this connection |
|------------|--------------------|
| Confirm the environment | `--whoami`: prints the site name and address the site itself reports, and the user the password belongs to. Show it. Write nothing until the operator confirms it is staging |
| Read a page's layout | `--read <id> --rest-base <base>`: prints the raw block markup, or on WPBakery the raw shortcodes. This needs the password; a public page gives only the finished HTML, with the block settings stripped out or the shortcodes already expanded, which is not enough to learn the site's syntax |
| Snapshot a page | `--snapshot <id> --rest-base <base>`: saves the raw markup, title, slug, status and address to `build-log/snapshots/`. `--update` takes one itself before every overwrite, and `--restore <file>` puts a snapshot back |
| Write a page's layout | `--update <id> --rest-base <base> --content-file <file>` replaces the page's block markup or shortcodes. The slug, status and title are left exactly as they are unless passed. Without `--update` it creates a new page as a draft. On WPBakery a new page is instead a person's duplicate of its reference page, then updated, so it keeps WPBakery's page settings |
| Upload media | `.claude/tools/optimize-and-upload.py`, with the same credential |
| Clear the cache | Not over this API. A person purges the page cache in the site's caching plugin (named in the builder file), and any CDN in front of the site, then the public page check in the core instructions confirms it. Whether the plugin purges by itself after an API write is unconfirmed; the check makes the answer not matter. On WPBakery, a person may also need to click Update in the WPBakery editor to rebuild the page's Design Options styling (`wpbakery-limits`) |
| Read the design tokens | Block theme, no login needed: the `--wp--preset--*` custom properties in any public page's CSS. The theme's full settings need the password *(confirm the endpoint on the site)*. WPBakery has no token layer: the values are read from the sibling pages' raw shortcodes |
| Write the design tokens | Not through this kit. The API can change global styles, which restyles the whole site: that is a human-approved job of its own |

**The REST base** is the name the API uses for a kind of content: `pages` for pages, and a custom
post type has its own, listed at `<site>/wp-json/wp/v2/types`. Read it there; do not guess it from
the post type's name.

**Revisions.** WordPress may keep a revision when a page is updated through the API, if that kind
of content supports revisions. It is a second line of recovery, never a substitute for the
snapshot. *(Confirm per post type.)*

**Endpoints that should be locked.** Unauthenticated, `<site>/wp-json/wp/v2/templates` should
refuse. If it serves templates to a logged-out request, the site is misconfigured: report it.

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| REST API | WordPress's built-in way for another program to read and change the site |
| Application Password | a site login for Claude, one per person, revocable in wp-admin |
| REST base | the name the site uses for one kind of content, such as pages or services |
| snapshot | a saved copy of a page's layout, kept in the build log so it can be put back |
