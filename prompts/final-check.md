# Final check (pre-launch QA)

Paste this into Claude Code (in the client folder) for a thorough pre-launch sweep of the built site:
broken links, spelling, grammar, consistency, house style, and accessibility / technical-SEO /
performance sanity (headings, alt, canonical, image weight), across every page. It does **not** check
page titles or meta descriptions, which are the deferred `seo-meta` pass. **Read-only** — it reports,
it does not fix. Copy fixes go into the content source, build fixes go through
`review-and-changes.md`. Run it when the pages are built and before launch.

---

You are doing the pre-launch final check on the built **staging** site. **Read-only, change nothing.**

## Read and set up
- `design/sitemap.md` (all pages and slugs), `design/content/site-facts.md` (the facts that must match
  everywhere), `design/content/site-content.md` (the approved copy), and the `STAGING_URL`.
- `.claude/reference/deferred-passes.md`, so you separate expected-deferred work from real problems.
- Crawl every built page with the chrome-devtools MCP (headless). **Extract prose from the rendered
  `innerText`, not `textContent`** — `textContent` glues a label to its body across block boundaries
  (`display:block`) and includes hidden responsive labels (`display:none`), which produces false
  run-together findings like "Referral-Based CareA current referral...". Verify any run-together or
  doubled-word hit against the rendered DOM before reporting it.

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
6. **Accessibility, technical SEO and performance sanity** (light pass). Check the signals that are
   ready by build time: one H1 per page, sensible heading order, alt text on content images, `lang`
   set, a canonical per page, and images sized and optimised (flag obvious performance red flags like an
   oversized image). **Do NOT check or flag page titles or meta descriptions** — those are the deferred
   SEO pass (`seo-meta.md`), written after the build, so treat them as out of scope, never as gaps. For
   depth, hand off to the auditor agents: full WCAG (Gate 5) to `accessibility-auditor`, technical SEO
   to `seo-optimizer`, and Core Web Vitals and performance (Gate 6) to `performance-tuner`.

## Report
- Grouped by the six headings. For each finding: page, what is wrong, the fix. Mark severity:
  **must-fix before launch**, **should-fix**, or **minor**.
- Keep **expected-deferred** items (links to pages not built yet) in their own short list, so the
  scheduled passes are not counted as failures. **Page titles and meta descriptions are out of scope**
  (the deferred `seo-meta.md` pass), so do not flag them, but the technical SEO and performance signals
  above ARE in scope.
- End with a plain verdict: **is the site launch-ready**, and the short list of must-fix items.
- **Change nothing.** Copy fixes go into `design/content/site-content.md` then to staging (the Gate 7
  content rule); build fixes go through `review-and-changes.md`.
