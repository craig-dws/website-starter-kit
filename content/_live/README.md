# content/_live/

**What the site actually says, exported from WordPress and committed.**

Empty until the export step is built. This folder exists now so the convention is fixed before
builds start diverging on it.

## Why it has to exist

This is WordPress plus Breakdance. The copy that is live sits in the `_breakdance_data` postmeta
field in the database, not in a file in this repo. A developer who edits a heading in the Breakdance
UI leaves no git evidence whatsoever.

That means a diff of `content/` alone cannot tell you what changed on the site. It tells you what
ZilvaEdge released, which is a different question, and reconciling from it would quietly miss exactly
the changes reconciliation exists to catch.

## How the three sources relate

| Source | Answers |
|---|---|
| `content/` | What was approved and released |
| `content/_live/` | What the site actually says now |
| `CONTENT_CHANGELOG.md` | Why it differs |

Where `_live/` and the changelog disagree, `_live/` wins on fact and the changelog gap is reported.

## Consumed by

ZilvaEdge's `/content-reconcile`, monthly across every registered build and again at launch. If this
folder is missing or stale, it still runs, but it says plainly in its output that the result is
self-reported and unverified rather than pretending otherwise.
