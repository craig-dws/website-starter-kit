# What earlier builds learnt

**Read the section for the job before starting it.** Each item was found the hard way on a DWS
build and costs nothing to avoid once known. Gathered 17 November 2026 from the build logs of Ende
Urology (Breakdance 3.0.1 on the DWS staging host, finished 11 November 2026), Halo Care Services
(Breakdance, October to November 2026) and Family Focus Legal (block editor with ACF, November
2026). Earlier builds' lessons are already folded into the other reference files.

The proven Breakdance 3.0.1 behaviours are in `.claude/reference/limitations.md`. **When a build
finds something new that any later build would hit, add it here and to the kit**, not only to the
build's own log.

## Connecting a machine

- **Register the connection under both spellings of the folder's drive letter** (`C:/...` and
  `c:/...`). Claude Code on Windows can open the folder as either, and a local registration under
  the other spelling does not load. Ende lost three connection attempts to this.
- **"Connection Failed" at start-up with the health check later showing Connected** means the
  connection was slow to start, not that the password is wrong. Reconnect with `/mcp`; if the
  tools still do not reach the chat, restart Claude Code fully and open a new chat.
- **Keep the server name the deny rules name**, not the longer name the Connect screen suggests. A
  different name silently switches the deny rules off.
- **Each developer generates their own Application Password.** Never share one: removing a person
  then cuts off only their machine.
- **Record what the staging starter holds**, read only, in the build log: the home, header and
  footer post ids, the site title and tagline (the DWS starter ships "Start Website Breakdance"),
  the SEO plugin installed against the one `SITE-SETTINGS.md` plans, and every other active plugin.
  Ende's staging came with Rank Math where Yoast was planned, plus All-in-One WP Migration,
  FluentSMTP, Gravity Forms, WP Crontrol, Wordfence Login Security, ASE, WPCode Lite and WebP
  Express. Anything that differs from the plan goes to a person, not into the build.
- **Times in the log come from each machine's own clock**, which can sit behind another machine's.
  Say so in the row when it matters.

## Token sync

- **A person takes a full backup with All-in-One WP Migration before the first global write**, and
  the chat exports the Breakdance settings before it writes. Those two are the restore points. The
  host's own backups were never confirmed over the connection, so they are not relied on.
- **Strip the licence key from the settings export before committing it.** The export includes
  `license_key_validity_info` even though the tool says keys are left out. Keep the full copy
  outside the repo.
- **Remove the starter template's leftovers** from global settings with the person's approval: on
  Ende, a Purple palette colour and the Amaranth Typography Preset 1. The page kept requesting
  Amaranth from Google Fonts afterwards until **a person opened Breakdance Global Styles and saved
  once**. Ask for that click and recheck.
- **Switch Modern Normalize on before any page exists.** It is Breakdance's only supported margin
  reset, and nothing moves when nothing is built yet.
- **Use the agency class prefixes, never the site's `css_prefix`.** Breakdance makes `css_prefix`
  from the site title (Ende's changed from `sb-` to `endeurolog-` when the title was set), and
  `.claude/reference/class-naming.md` replaces it. The heading classes are `sw-h1` and so on.
- **Check once that none of the five prefixes (`sw-`, `gb-`, `wg-`, `pg-`, `sc-`) collide with a
  class the theme or plugins ship**, and record the result in `build-log/DECISIONS.md`.
- **Breakpoints are set by a person** in Breakdance, then read back with `get-breakpoints`. There is
  no ability to create them.

## Content types and menus

- **The connection could not create or fill a WordPress menu on Ende** (checked against its list
  of abilities). Ende typed the menu links once into the header instead, which meant the client
  edits menu links in the Breakdance header rather than under Appearance, Menus. Ende did create
  post categories through the WordPress REST route with the login the upload script uses, with
  the developer's approval. So try the REST menu routes with that login; if they refuse, stop and
  ask whether a person builds the menus in wp-admin from your click steps, or the links are typed
  into the header.
- **Whether the connection can create custom content types is unproven.** Check its list of
  abilities first. If it cannot, write numbered click steps for a person and stop. Never install a
  plugin without asking.
- **A misspelt custom field name draws nothing and warns nowhere** (Family Focus Legal, ACF). Read
  every field back on a sample entry, logged out, before any template uses it.
- **The DWS starter publishes dummy posts.** Ende's had 11 lorem-ipsum posts dated 2022 and "Hello
  world", which would have filled every post listing ahead of the real entries. Set them to draft
  (reversible, nothing deleted) before any listing is built, and log the ids.
- **The connection's `create-post` has no date option.** Set a dated entry's date another way (the
  REST route with the upload script's login) and read it back.

## Global parts

- **Reuse the starter's existing header, footer and home page posts** rather than creating new
  ones. Delete their demo sections, keep the post ids, and set the template conditions. WordPress
  already serves the starter's home post at `/`.
- **Breakdance's Header element applies its scrolled style at the first pixel** and has no distance
  setting (its Offset setting moves the header down the page instead). If the design changes the
  header after a set scroll distance, a short script in a Breakdance JavaScript Code element inside
  the header adds `is-stuck`, labelled so a person can find it in the builder.
- **Make an on-dark button modifier in the design system from the start**, `sw-btn--on-dark`, if
  any button sits on a dark band. The standard focus ring is invisible there, and Ende had to
  retrofit it page by page.
- **Link the header logo to `/`**, not the full live address, or it sends people from staging to
  the live site.

## Building pages

- **Images bind to the media library in Breakdance 3.0.1**, which gives `srcset`, width, height and
  alt. Keep the width and height attributes when switching an image to the library, turn lazy
  loading off for images above the fold, and check the rendered tag.
- **A listing's excerpt is set per entry**, in the excerpt field. Breakdance's truncate counts
  characters and adds an ellipsis, so it cannot match a word count.
- **A news or blog listing is a normal page with a Post Loop**, not WordPress's posts archive, which
  leaves the reading settings alone and keeps the listing editable in the builder.
- **An accordion is Breakdance's native FAQ element** with its own schema switch off, since schema
  is not part of a build.
- **A video or other embed goes in as its `<iframe>`**, which `html-to-page` keeps word for word.
- **`insert-stylesheet` mangles `opacity`**; write a hover as an explicit colour instead
  (`color-mix` of the token works).

## Finishing a page

- **The builder check needs a person.** Claude's browser is logged out of WordPress, so before a
  page is called finished the developer opens it in the builder in their own logged-in browser,
  confirms it opens with no error, and saves nothing. On Halo Care the check stalled until the
  developer did it in their own browser.
- **When two chats on one machine both want the browser,** the second checks the page in headless
  Chrome with its own profile rather than waiting.
- **A developer's change to a design decision is a decision, not a fix.** Ende's header was changed
  and reversed twice in one afternoon on preference. A change to the design source is logged in
  `build-log/DECISIONS.md` and goes to the person who owns the design, not straight into the page.

## Forms and files

- **The connection has no Gravity Forms ability.** On Ende a person built the form in wp-admin from
  Claude's click steps, then Claude placed and styled it. The staging recipient is a team address,
  never the client's, and reCAPTCHA stays off until its keys arrive, because a reCAPTCHA field
  with no keys blocks every submission.
- **The upload script cannot take a PDF, and WordPress files a new upload under the current month**,
  so a re-uploaded PDF changes address. Settle where the site's PDFs live before the image pass, so
  the redirect map at launch knows the new addresses.
