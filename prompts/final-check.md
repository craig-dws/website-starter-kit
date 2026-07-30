# Final check (pre-launch QA)

Paste this into Claude Code (in the client folder) for a thorough pre-launch sweep of the built site:
broken links, spelling, grammar, consistency and house style, across every page. **Read-only** — it
reports, it does not fix. Copy fixes go into the content source, build fixes go through
`review-and-changes.md`. Run it when the pages are built and before launch.

---

You are doing the pre-launch final check on the built **staging** site. **Read-only, change nothing.**

## Read and set up
- `design/sitemap.md` (all pages and slugs), `design/content/site-facts.md` (the facts that must match
  everywhere), `design/content/site-content.md` (the approved copy), and the `STAGING_URL`.
- `.claude/reference/deferred-passes.md`, so you separate expected-deferred work from real problems.
- Crawl every built page with the chrome-devtools MCP (headless).

## Check, and report findings grouped by these headings

1. **Broken links.** Every internal and external link on every page. An internal link that 404s to a
   **real-but-unbuilt** sitemap slug is expected-deferred, report it separately, not as broken. A link
   to a slug **not** in the sitemap, a typo'd URL, or a dead external link IS broken. List each: page,
   link text, target, verdict.
2. **Spelling.** British and Australian English. Flag misspellings and US spellings (color, center,
   and -ize where -ise is house style). Give the page and the word.
3. **Grammar.** Obvious errors, sentence fragments, doubled words, wrong homophones. Page and sentence.
4. **Consistency.** The site facts must be identical everywhere: opening hours (per `site-facts.md`),
   phone, address, business name. Also terminology (one name per thing), button labels, heading
   capitalisation, and date formats. Flag every mismatch with both variants and where each appears.
5. **House style.** No em dashes, en dashes, double hyphens or emojis in visible copy.
6. **Accessibility and SEO sanity** (light pass). One H1 per page, sensible heading order, alt text on
   content images, a unique title and meta per page (or note SEO is still deferred). For the deep
   audits, hand off to the auditor agents (`accessibility-auditor`, `seo-optimizer`,
   `performance-tuner`) rather than duplicating them here.

## Report
- Grouped by the six headings. For each finding: page, what is wrong, the fix. Mark severity:
  **must-fix before launch**, **should-fix**, or **minor**.
- Keep **expected-deferred** items (links to unbuilt pages, un-applied SEO) in their own short list, so
  the scheduled passes are not counted as failures.
- End with a plain verdict: **is the site launch-ready**, and the short list of must-fix items.
- **Change nothing.** Copy fixes go into `design/content/site-content.md` then to staging (the Gate 7
  content rule); build fixes go through `review-and-changes.md`.
