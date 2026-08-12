# Triage a final check into a fix plan and tracker

Paste this into Claude Code after `final-check.md` has produced a report. It turns the report into three
things: an **AI change-plan**, a **tab-per-fix-type tracker** (a Google Sheet you drag in), and, inside
the tracker, the **human actionable list**. Read-only: it triages, it does not fix. The fixes then go
through `review-and-changes.md` / the compliance pass (AI items) and to the humans (their items).

---

You are triaging the latest final-check report into an actionable plan and tracker. Change nothing on
the site.

## Preflight, stop if the build is not ready
This runs at the **end of a build**, after `final-check.md`. Before anything else, confirm these exist:
- a final-check report in `build-log/`,
- `design/sitemap.md`,
- a staging URL for the built site.

If any are missing, **stop and say so plainly**, for example: "Triage runs after the site is built and
`final-check.md` has run. This site is not there yet (missing: the final-check report, the sitemap). There
is nothing to triage." Do **not** ask what I meant, do **not** scaffold the missing files, and do **not**
invent findings. A site still in design has nothing to triage; that is expected, not an error.

## Read
- The final-check report in `build-log/` (ask me which file if there is more than one).
- `design/sitemap.md` (to turn each page into its URL) and `.claude/reference/deferred-passes.md`.

## Turn every finding into a row
For each finding, produce: **Page, URL** (base staging URL + the sitemap slug), **Section, Issue** (what
is wrong), **Fix** (the *actual* fix, not a restatement of the issue), **Owner** (AI or Human), and
**Severity** (must-fix / should-fix / minor). Sort each into a **fix-type tab**:

- **Content** — grammar, consistency, terminology, register. Owner AI.
- **Compliance** — regulated-copy claims (see the client's `content-compliance.md` if it exists). Owner
  AI for recasts; **Owner Human for anything needing professional sign-off** (e.g. a missing risks
  section a clinician must write).
- **Images** — placeholders to source, portraits, `srcset` binding. Owner Human (or AI for the
  library-fillable ones).
- **Links** — broken or malformed links. Owner AI.
- **SEO & Schema (later)** — structured data, Open Graph, breadcrumbs, landmarks. These are the **later
  SEO pass**, not now; mark them so.
- **Performance (production)** — TTFB, caching, fonts. **Production-migration work.** Note the client's
  server location (ask me if unknown) and "re-measure on the production host".
- **wp-admin & Cleanup** — stale media, breakpoints, Gate approvals. Owner Human.

## Scope rules (do not miscategorise)
- **Page titles and meta descriptions are out of scope** — the deferred `seo-meta` pass. Do not list them.
- **Schema / structured data / og:image go in "SEO & Schema (later)"**, not the AI plan.
- **Core Web Vitals / performance is production work**; do not put it in the AI plan, and record the
  server-location note.
- **AI-fixable** = copy (into `content/{slug}.md` then surgical `edit-post`) and links
  (`review-and-changes`).
  **Human** = clinical sign-off, image commissioning, wp-admin, production, Gate approvals.
- **Content reconciliation gaps are launch blockers**, so they go in the fix plan, never the
  deferred list. A page whose live copy differs from `content/` with nothing in
  `CONTENT_CHANGELOG.md` explaining it means the site says something nobody recorded deciding.
  Gate 8 cannot be signed until it is resolved, and resolving it is the PM's with ZilvaEdge, not
  an AI fix. List each one with its page and the unexplained difference.

## Produce
1. **`build-log/prelaunch-fix-plan.md`** — the AI-doable half only, ordered (compliance recasts first,
   then the content pass, then links), stating the method: surgical `edit-post`, mirror to
   `site-content.md` and the client Doc, never a rebuild; and an explicit "not in this plan" list
   (risks sections, images, schema/SEO, titles/meta, performance).
2. **The tracker.** Write the findings to a temp `fixes.json` in the shape
   `{"title": "...", "overview": [context lines incl. the scope rules and the server-location note],
   "tabs": {"Content": [[page,url,section,issue,fix,owner,severity], ...], ...}}`, then run:
   `python .claude/tools/build-fix-tracker.py fixes.json build-log/<client>-prelaunch-fixes.xlsx`

## Report
- A short summary: counts per tab, the **launch blockers** (especially the human ones), and the line
  "to share as a Google Sheet, drag the .xlsx into Google Drive". Then stop; nothing is applied here.
