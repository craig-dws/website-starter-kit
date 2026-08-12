# Export what the site actually says

Paste this into Claude Code in this folder, with the Breakdance MCP connected.

---

You are exporting the live text of every page into `content/_live/`, so that what the site says
becomes a thing in git rather than a thing in a database.

## Why this exists, so you make the right trade-offs

This is WordPress plus Breakdance. The copy that is live sits in the `_breakdance_data` postmeta
field, not in a file. A developer who edits a heading in the Breakdance UI leaves **no git evidence
at all**. So a diff of `content/` shows what ZilvaEdge released, which is a different question from
what the site says, and reconciling from it alone would quietly miss exactly the changes
reconciliation exists to catch.

`content/` is the approved copy. `content/_live/` is the truth. `CONTENT_CHANGELOG.md` is the
explanation. Where the export and the changelog disagree, the export wins on fact.

The output is read by two audiences, a human scanning a diff and ZilvaEdge reconciling a Google
Doc. Neither wants fidelity to Breakdance's internals. **A stable, boring, predictable shape matters
far more than completeness.**

## The rule that governs everything else

**The same unchanged page must produce a byte-identical file on every run.**

If the export reorders anything between runs, or stamps a timestamp that moves on its own, every
diff fills with noise and the whole mechanism is worthless inside a fortnight. Nobody reads a diff
that is wrong 90 percent of the time.

That has one consequence worth stating plainly, because it contradicts the obvious approach:
**do not write an export timestamp that changes on every run.** Instead:

1. Build the new body for the page.
2. If a file already exists and its body is identical, **leave the file completely alone**. Do not
   rewrite it, do not touch its header.
3. Only when the body has genuinely changed do you write the file, with today's date in the header.

So the date in a file answers "when did this page last change", which is a useful question, rather
than "when did the export last run", which is not.

## What to export

For each page in `design/sitemap.md`, read the live page through the Breakdance MCP tools already
connected for this build, and write its visible text to `content/_live/{slug}.md`.

**Include, in the order they appear on the page:**

- Headings, with their level
- Paragraphs
- List items
- Button labels and link text

**Exclude, without exception:**

- Layout JSON, styling, classes, element ids, any Breakdance structure
- Anything invisible to a visitor: hidden responsive variants, `display:none` blocks, aria-only text
- Image files, though keep alt text if a page carries meaningful alt copy

Text only. If you find yourself preserving something because it might be useful later, it does not
belong here.

## File shape

```markdown
---
slug: web-hosting
page_id: 412
source: breakdance
last_changed: 2026-08-12
---

# Australian web hosting that stays fast

Some paragraph text exactly as it reads on the page.

## Why our hosting is different

- A list item
- Another list item

[Button] Get started
```

`slug`, `page_id` and `source` are stable identity and do not change between runs. `last_changed`
moves only when the body moves, per the rule above.

Mark button and link labels with a `[Button]` or `[Link]` prefix so a reader can tell a call to
action from a sentence. Keep that convention exactly; changing it later rewrites every file and
buries a real change in a thousand-line diff.

## Blog posts are different, do not treat them as pages

Blog and resource posts are ordinary WordPress posts. Their copy is in `post_content`, rendered
through **one shared Breakdance template**, not a per-post layout. **Export those from
`post_content` directly.** Reading them the way you read a Breakdance page will return the
template's chrome rather than the post, and you will not notice, because it will look plausible.

Confirm the post type with `wp post-type list` rather than assuming, per the breakdance-limits
skill.

## Then commit

Commit the export with a plain message naming how many pages changed. **The commit is the
evidence.** An export sitting uncommitted in a working tree proves nothing to anybody.

If nothing changed, say so and commit nothing. An empty commit is noise in the same way a moving
timestamp is.

## When to run this

- **After any session that changed page copy**, including microcopy typed straight into Breakdance.
- **Always as part of `final-check.md`**, before launch. Gate 8 needs content reconciliation
  complete, and reconciliation without this export is self-reported rather than verified.

## Report back

- How many pages were exported, and how many actually changed.
- Any sitemap page you could not read, and why. Do not guess at its content and do not silently
  skip it: a page missing from `content/_live/` reads downstream as a page that has not changed,
  which is the most dangerous wrong answer available here.
- Any page whose live text differs from `content/{slug}.md` with nothing in `CONTENT_CHANGELOG.md`
  explaining it. Report it; do not fix it, and do not guess at the reason.
