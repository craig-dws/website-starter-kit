# content/

**Approved page copy, as markdown. One file per page.**

This is where the words for the site live. It is populated from ZilvaEdge, not written here.

## Where these files come from

A page is written by ZilvaEdge, reviewed, published to a Google Doc, and approved by the editor.
Once it is approved, ZilvaEdge's `/content-release` pulls the Doc back to markdown and commits the
file into this folder, with a commit message naming the client, the page and the Doc it came from.

So the answer to "is this the approved copy" is always in `git log`.

## The rule while a build is live

**During a build, this repo owns the page copy.** ZilvaEdge does not edit released pages while you
are building, and the Google Doc is expected to go stale. It is brought back into line at launch by
ZilvaEdge's `/content-reconcile`.

That gives you three cases:

| You need to | Do this |
|---|---|
| Change a heading, a CTA, a button label, short connective copy | Edit it here and log it in `CONTENT_CHANGELOG.md` |
| Add a new page or a substantial new section | Request it from ZilvaEdge through ClickUp. It arrives here through `/content-release` |
| Fix a factual error or a compliance problem | Raise it. Do not quietly correct it here, because the Doc is what the client approved |

Microcopy is the only direct-write exception. Routing two lines of button text through the full
content pipeline helps nobody.

## Log what you change

Anything you edit here goes in `CONTENT_CHANGELOG.md` at the repo root, with the page and a one-line
reason. That log is what ZilvaEdge reads at launch to work out what changed and why, and an
unexplained change is reported as needing attention rather than being quietly accepted.

## Naming

Lower-case, hyphenated, matching the page slug. `home.md`, `contact.md`,
`why-choose-us.md`, `resources-what-is-a-cdn.md`.

The folder name itself is lower-case `content` and must stay that way. Git is case-sensitive and
Windows is not, so a repo that ends up with both `Content` and `content` behaves differently
depending on who is looking at it.

## `_live/`

`content/_live/` is the export of what the site **actually says**, dumped out of WordPress and
committed. It exists because Breakdance keeps live copy in the database, not in a file, so a
developer editing a heading in the Breakdance UI leaves no evidence in git at all.

`content/` is the approved copy, `content/_live/` is the truth, and `CONTENT_CHANGELOG.md` is the
explanation. Where the export and the changelog disagree, the export wins on fact.

The export step is not built yet. Until it is, reconciliation falls back to this folder plus the
changelog, and the result is self-reported rather than verified.
