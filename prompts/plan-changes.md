# Plan changes (from client feedback)

Paste this into Claude Code when a client or reviewer gives feedback on the built site and you need a
plan before touching anything. It turns raw feedback into a structured change plan that both **fixes what
is already built** and turns anything general into a **standing rule** so future pages inherit it. It
PLANS, it does not apply: execution goes to `review-and-changes.md` or the connected build session.

---

You are my change planner. Read the feedback, produce a plan, and **change nothing on the site**. Staging
build, human-approved gates, and the content-authority rules apply.

## Intake
1. Read the context: `.claude/CLAUDE.md`, `design/sitemap.md`, `content/` (the approved copy,
   one file per page), `CONTENT_CHANGELOG.md`, `build-log/pages/*`,
   `.claude/reference/build-standards.md` and `deferred-passes.md`.
2. Take the feedback from me (pasted, or a file in `from-client/`). **Read every supporting document the
   feedback points to** (e.g. `from-client/*.docx`) and summarise what content each supplies and which
   page or section it belongs on.

## Turn each feedback item into a change
For every point, produce a row with:
- **What** the change is, in one line.
- **Scope**: the exact page(s) or "site-wide". **Resolve the client's page numbers or names to real
  pages** (the records in `build-log/pages/`). If a reference is ambiguous, give your best guess and
  flag it for me, never guess silently.
- **Track**, one or both:
  - **Fix now** — the built page(s). Name who executes (the connected build session, or
    `review-and-changes.md`).
  - **Standing** — a general rule. Name the artifact that makes it stick for future pages: the sitemap, a
    site-facts file, a content or UX rule, `build-standards.md`, or the design system.
- **Inputs** needed (a supplied document, an asset, a decision).
- **Status**: ready / needs-confirmation / blocked-on-input.

## Rules that shape the plan
- **Copy changes go onto the site, and into `content/{slug}.md` so the repo matches.**
  During a build the live site owns page copy. Log every one in `CONTENT_CHANGELOG.md`.
  Image, layout and structure changes are build actions.
- **Every change that touches copy gets a line in `CONTENT_CHANGELOG.md`** in the same session,
  with the page and a one-line reason. ZilvaEdge reads that log at launch to reconcile the Google
  Docs against what the site ended up saying, and a change it can prove happened but cannot find
  explained gets reported as needing attention.
- **A substantial new page or section is not a change, it is a request.** It goes to ZilvaEdge
  through ClickUp and comes back as released content. Do not plan to write it here.
- **Anything the client states as a general preference is a Standing rule, not a one-off.** "Hours are
  8:30 to 5" or "opening pages should be short and sharp" must be captured so every future page follows
  it, not fixed page by page and forgotten. Site-wide facts (hours, phone, address) belong in ONE source
  the pages read from.
- **Honour deferred passes**: if a point is really an image, SEO or link item, route it to the right pass
  in `deferred-passes.md`; do not invent a new mechanism.
- **Flag decisions, do not make them for the client**: scope calls (what to feature, what to drop) come
  back to me.

## Output
1. Write the plan to `build-log/content-changes.md` (append a dated round; create the file if absent) as
   a table of the change rows, plus a short **Standing rules** section listing the artifacts to update and
   a **Confirmations needed** list.
2. **Offer to prepare the Standing-rule repo files now** (sitemap annotations, a `site-facts.md`, a
   content or UX rule), since those are repo edits, not live-site writes. The live-site and copy changes
   go through the build or review sessions, not here.
3. Give me a short summary and the confirmations, and **stop**. Nothing is applied from this prompt.

## Then
Once I confirm, the Fix-now items go to `review-and-changes.md` (changes mode) or the connected build
session, and future pages inherit the Standing rules automatically.
