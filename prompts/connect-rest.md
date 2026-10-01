# Connect through the WordPress REST API (block theme and WPBakery sites)

> **If you are Claude and this file was attached or referenced rather than pasted, these are your
> instructions. Follow them from "Start" below.** Do not ask what to do with the file.

Paste this into Claude Code, in the client folder, to connect Claude to a **WordPress block theme**
or **WPBakery** site through WordPress's own built-in REST API. It is the setup for
`.claude/connections/wordpress-rest.md`.

**No plugin is installed**, not the Agent Connector and not a bridge. The site already has
everything needed. The only thing you make is an Application Password: a site login for Claude,
one per person, that you can revoke in wp-admin at any time.

## Before you paste

- **The staging or local copy's address**, never the live site's.
- **A wp-admin login on that copy**, as a user who can edit pages.
- The project's `.claude/CLAUDE.md` loads `connections/wordpress-rest.md`, and `builders/block-theme.md`
  or `builders/wpbakery.md`. If it does not, the setup is wrong for this prompt; `START-HERE.md` explains the choices.

---

You are connecting this project to a block theme or WPBakery site through the WordPress REST API. You are not
connecting to the live site.

Read `.claude/CLAUDE.md`, `.claude/connections/wordpress-rest.md`, the builder file it loads
(`.claude/builders/block-theme.md` or `.claude/builders/wpbakery.md`) and `.claude/settings.json`
before you start.

I am a project manager, not a developer. I never run commands and I never edit code. You run
everything you can. When a step genuinely needs me, which means a wp-admin login or a click in the
browser, **stop, give me numbered instructions, and wait.**

## Start

1. **Get the site's address from me** and show it back. **If it is the live site's address** (the
   production address in `.claude/CLAUDE.md`, or a public domain I have not told you is staging),
   **stop and say so.** Nothing below may proceed against the live site.
2. **Check the builder matches the builder file**, from the public home page's source. A block theme
   shows `wp-block-` classes, `wp-block-template-part` wrappers and `--wp--preset--` custom
   properties. WPBakery shows `vc_row` and `wpb_` classes and a "Powered by WPBakery Page Builder"
   generator tag. If it does not match, stop: the wrong builder is set up for this project.
   On WPBakery, also note whether `<site>/wp-json/wp/v2/pages` refuses a logged-out request. That is
   usually a security plugin, and the same plugin may switch off Application Passwords, so say so
   before the next step.
3. **Check the tooling** and report anything missing with its fix: `python --version`, and
   `python -c "import requests"`.

## The Application Password (my hands, your instructions)

Give me these as numbered steps and wait.

1. Log in to wp-admin on the **copy**. Check the address bar shows the copy's address before
   anything else.
2. Go to **Users, then Profile**, and scroll to **Application Passwords**.
3. Name it for the person and the job, for example "Claude - <your name>", and click **Add New
   Application Password**.
4. **Copy it straight away.** WordPress shows it once and keeps only a scrambled copy.
5. Paste it back here with the username it belongs to.

If there is no Application Passwords section, or it says Application Passwords need HTTPS, a
security plugin is usually switching them off. The troubleshooting order is in `START-HERE.md`.
Read it and hand me the fix as clicks.

## Store it, outside git

1. **Confirm `.claude/settings.local.json` is excluded from git** with `git check-ignore -v
   .claude/settings.local.json`. If it is not excluded, **stop**: the password would be committed.
2. Write the three values into the `env` block of `.claude/settings.local.json`, keeping anything
   already in that file:
   ```json
   { "env": { "WP_SITE_URL": "https://<the copy>", "WP_API_USERNAME": "<username>",
              "WP_API_PASSWORD": "<the application password>" } }
   ```
3. Never write the password anywhere else: not in a committed file, not in the build log, not in a
   commit message. Do not repeat it back to me.

## Verify, and be strict about it

Report a short green or red checklist:

- `python .claude/tools/create-post.py --whoami` returns **the copy's own address**, and the user is
  logged in. Show me what came back. Not "it connected", but what it said its site is.
- `python .claude/tools/create-post.py --rest-base pages --read <any page id>` returns the raw
  layout: on a block theme, block markup starting with `<!-- wp:`; on WPBakery, shortcodes starting
  with `[vc_row`. Plain HTML with neither means the read is not authenticated.
- `<site>/wp-json/wp/v2/types` lists the kinds of content, and the REST base of every custom post
  type this project will touch is recorded.
- Logged out, `<site>/wp-json/wp/v2/templates` refuses. If it serves templates to a logged-out
  request, report it as a site misconfiguration.
- No write of any kind has been attempted.

If any line is red, say so and stop.

## Finish

1. **Record it in `build-log/DECISIONS.md`**: the connection (WordPress REST API), the copy's address,
   the user, the REST bases found, and the date. Not the password.
2. **Fill in the builder file's bracketed values** you can now read: the WordPress version, the theme
   and child theme, the block-providing plugins (on WPBakery, the WPBakery version and every plugin
   that adds WPBakery elements) and the caching plugin. Leave any you could not read
   in brackets and say which.
3. **Send me the report below.** Then stop. Building is a separate prompt.

### The report to send me

```
## Site connected

Status: <Connected and verified on the copy  |  Not connected, see below>

What it is pointed at: <the address the site reported back, in its own words>

Kinds of content found: <pages, and each custom post type with its REST base>

Needs you:
- <plain actions only I can do, or "Nothing.">
```

Rules for the report:

- **Never report connected without having seen the copy's address come back from the site itself.**
- **The first write on this site is a throwaway test page**, created as a draft, opened in the editor
  by a person to confirm it is editable, then deleted by a person. Say so as the next step.

## When the job is done

Revoke the Application Password in wp-admin (Users, then Profile) and remove the three values from
`.claude/settings.local.json` once the work on this copy is finished.

British and Australian English. No em dashes, no en dashes, no double hyphens in prose. No emojis.
