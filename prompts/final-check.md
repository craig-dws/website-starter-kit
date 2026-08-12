# Final check (pre-launch QA)

Paste this into Claude Code (in the client folder) for a thorough pre-launch sweep of the built site:
broken links, spelling, grammar, consistency, house style, and accessibility sanity (headings,
landmarks, alt, canonical, image weight), across every page. It does **not** check page titles, meta
descriptions, schema / structured data, or cache / performance, which are all done **after** the build
and are never launch blockers. **Read-only** — it reports, it does not fix. Copy fixes go into the
content source, build fixes go through `review-and-changes.md`. Run it when the pages are built and
before launch.

---

You are doing the pre-launch final check on the built **staging** site. **Read-only, change nothing.**

## Read and set up
- `design/sitemap.md` (all pages and slugs), `content/` (the approved copy, one file per page),
  `CONTENT_CHANGELOG.md` (every copy change made during the build), and the `STAGING_URL`.
  `content/_facts.md` is optional: where it exists it holds the facts that must match everywhere.
  Where it does not, check cross-page consistency against the approved copy and say the facts file
  was not supplied, rather than reporting nothing to check.
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
6. **Accessibility sanity** (light pass). Check only the signals that are ready by build time: one H1
   per page, sensible heading order, semantic landmarks, alt text on content images, `lang` set, a
   canonical per page, and images sized and optimised (flag an obviously oversized image).

   **Done after the build, never a launch blocker. Do NOT check these, do NOT attempt them, and do NOT
   flag their absence:**
   - **Page titles and meta descriptions** (the deferred `seo-meta.md` pass).
   - **Schema / structured data** of any kind: JSON-LD, breadcrumbs, MedicalClinic / Physician /
     FAQPage / Article, og:image. This is the later SEO pass and is often a wp-admin / plugin job.
     **Do not try to add or inject it**, and do not report that it is missing.
   - **Cache, Core Web Vitals and performance tuning.** Production work, set up after launch.

   If you notice any of the above missing, that is expected, say nothing and move on. When these passes
   are actually scheduled, the separate agents handle them: full WCAG (Gate 5) `accessibility-auditor`,
   technical SEO `seo-optimizer`, performance (Gate 6) `performance-tuner`.

7. **Content reconciliation.** A launch-gate item, not a nicety. Compare what the site actually says
   against `content/` and `CONTENT_CHANGELOG.md`, and report:
   - Copy live on the site that differs from the approved file in `content/`, page by page.
   - Any such difference with **no entry in `CONTENT_CHANGELOG.md` explaining it**. That is the
     finding that matters: it means the site says something nobody recorded deciding, and the
     client's Google Doc is about to be refreshed to the wrong thing.
   - Whether `content/_live/` exists and is current. **Run `prompts/export-content.md` first if it
     is missing or stale**, because that is what makes this check verified rather than
     self-reported. If it cannot be run, say so plainly and state that this check ran on the repo
     alone. Breakdance keeps live copy in the database, so without the export there is no proof.

   **Report, do not fix.** An unexplained difference is the PM's to resolve with ZilvaEdge, and
   guessing at the reason is how a wrong explanation ends up in the record.

## Report
- Grouped by the seven headings. For each finding: page, what is wrong, the fix. Mark severity:
  **must-fix before launch**, **should-fix**, or **minor**.
- Keep **expected-deferred** items (links to pages not built yet) in their own short list, so the
  scheduled passes are not counted as failures. **Page titles, meta descriptions, schema / structured
  data, and cache / performance are all out of scope** (done after the build), so do not flag them and
  do not attempt them. The accessibility signals above ARE in scope.
- End with a plain verdict: **is the site launch-ready**, and the short list of must-fix items.
- **Change nothing.** Copy fixes go into `content/{slug}.md` then to staging (the Gate 7 content
  rule); build fixes go through `review-and-changes.md`. Reconciliation gaps go to the PM, who
  runs ZilvaEdge's content reconciliation before Gate 8.
