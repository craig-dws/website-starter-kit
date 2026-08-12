# Which prompt, when

You run a build by pasting one prompt into Claude Code, in the client folder. Start at `START-HERE.md`;
this is the quick index of what each prompt is for and when to reach for it.

| Prompt | Use it when | What it does |
|--------|-------------|--------------|
| `guided-build.md` | First build, or you are new to this | Connects the site, then walks you through the whole build step by step, explaining as it goes and asking before anything risky. |
| `advanced-build.md` | Once the flow is second nature | The same build in whole stages with little narration, stopping only for real decisions and gates. |
| `connect-mcps.md` | A new machine, or someone joining the build | Connects the MCP servers (Breakdance, chrome-devtools, Figma), doing what it can and prompting you for the manual bits (the wp-admin Application Password, the restart). |
| `new-page.md` | Internal-pages phase, once the design system is locked | Builds one internal page from its reference and content, reusing the type's components. One page per chat; run several in parallel. |
| `blog.md` | Building a blog / resources / news section | Builds the single-post template and the archive listing once, as Breakdance Templates every post inherits. Templates, not one page per post. |
| `source-images.md` | After pages are built | Works through the image placeholders: client gallery first, else stock or AI, optimise, upload, swap in. |
| `seo-meta.md` | After pages are built | Gathers the per-page SEO title and meta drafts to paste into the SEO plugin, plus the favicon and site-wide config. |
| `status.md` | Any time you want to know where the build is | Read-only snapshot: page-by-page progress, plus lists of images to update, things that need you, and what is not done yet. |
| `plan-changes.md` | A client or reviewer sends feedback | Turns the feedback into a change plan: fix-now items plus standing rules so future pages inherit it. Plans, does not apply. |
| `review-and-changes.md` | After a build or stage, or to apply a punch-list | Reviews the built site against the standards, or applies changes one at a time. |
| `export-content.md` | After any session that changed copy, and before launch | Exports the live text of every page into `content/_live/` and commits it, so what the site says is in git. Breakdance keeps copy in the database, so without this there is no evidence of a heading someone changed in the UI. |
| `final-check.md` | Before launch, once pages are built | Pre-launch sweep of the whole site: broken links, spelling, grammar, consistency, house style. Reports, does not fix. |
| `triage-final-check.md` | After a final check | Turns the report into an AI fix-plan plus a tab-per-fix-type tracker (a Google Sheet you drag in) with page, URL, section, issue, fix and owner. Triages, does not fix. |

## Rough order over a project
1. **Connect** — `guided-build.md` or `advanced-build.md` (first machine), `connect-mcps.md` (each extra machine).
2. **Build** the design system, then home, header and footer.
3. **`new-page.md`** for each internal page (one per chat, parallel once the first of a type is set).
   For a **blog / resources** section use **`blog.md`** instead (templates, not one page per post).
4. **`source-images.md`**, then **`seo-meta.md`** once pages exist.
5. **`review-and-changes.md`** for sign-off, then **`export-content.md`** to put what the site
   actually says into git, then **`final-check.md`** for the pre-launch sweep, then
   **`triage-final-check.md`** to turn the report into a fix-plan and tracker.

`plan-changes.md` runs whenever client feedback arrives, and `status.md` any time you want to see where
the build stands.

See `.claude/reference/git-workflow.md` for when to commit and how two machines stay in sync.
