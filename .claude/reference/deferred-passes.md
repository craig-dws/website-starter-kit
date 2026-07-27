# Deferred passes

Some work is **deliberately not finished during a page build**. It is done later, once, in a dedicated
pass, because doing it per page is either impossible over the tools or wasteful while the site is still
moving. These items are **expected-incomplete, not defects.**

**The rule the build must follow:**
- Record each deferred item **once**, in the page record under **Deferred passes**, in the row format
  below. That is all. **Do not** raise it as a follow-up, a warning, a gap, or a checklist failure,
  and do not re-explain it on every page. A reviewer seeing it should read "scheduled", not "broken".
- Verification and review **distinguish expected-deferred from a real defect.** An internal link that
  404s because its target page is not built yet is expected. A link that 404s because the slug is
  wrong is a defect. Judge by the cause, not the symptom.
- Each pass has one owner prompt or step that resolves **every** instance across the site in one go,
  working from the page records. It is not chipped away per page.

## The passes

### 1. Images not yet worked out
Pages built without decided imagery carry a **placeholder block** at the right size (see
`image-placeholder.md`), not an invented image or a collapsed slot.
- **Resolved by:** `prompts/source-images.md` (gallery first, else stock/AI, optimise, upload, swap).
- **Logged under:** Outstanding images.
- **A real defect instead of deferred:** an image slot with no placeholder and a collapsed layout, or
  an un-optimised image dropped in during the build.

### 2. Internal links to pages not built yet
Links point at the **real sitemap slugs from the moment they are built**, so navigation never has to
be rewritten later (BUILD-LOG 2026-07-26: "link to the real slugs now so the navigation does not have
to be rewritten later"). Until the target page exists, that link 404s. That is deliberate.
- **Resolved by:** simply building the remaining pages. The **review/finalise pass** then confirms
  every internal link resolves once the site is complete.
- **Logged under:** Deferred links (a count and the target slugs is enough, not prose per page).
- **A real defect instead of deferred:** a link to a slug **not in `design/sitemap.md`** (a typo or an
  invented URL). That is always a defect, build-time or not. Only a link to a real-but-unbuilt slug is
  deferred.

### 3. SEO title and meta description
The Breakdance MCP **cannot write post meta** (every registered ability is `breakdance/*`; none
touches the SEO plugin's fields, proven). So live SEO meta is a **human pass in wp-admin** via The SEO
Framework. But the build has the content and context, so **it drafts a good title and meta description
per page as it builds** and records them, so nothing is lost and the human pass is paste-only.
- **Resolved by:** `prompts/seo-meta.md` (collects the drafts, a human pastes them into The SEO
  Framework; applies them directly only if a safe post-meta route is ever confirmed).
- **Logged under:** SEO meta, carrying the drafted title and description.
- **A real defect instead of deferred:** no draft recorded (the build had everything it needed to
  write one), or a duplicated/templated title copied across pages instead of a per-page draft.

### 4. Favicon and site-wide SEO config (site-level, set once)
The MCP cannot write the WordPress Site Icon or the SEO plugin's site-wide fields, so the favicon, the
site title template (a fresh install emits a duplicated `Business - Business` title) and the missing
site description are a **human wp-admin pass**, done once for the whole site, not per page.
- **Resolved by:** `prompts/seo-meta.md` (it covers site-wide config and the favicon alongside the
  per-page meta, all in the one wp-admin sitting).
- **Logged under:** a single site-level note in `build-log/BUILD-LOG.md`, **not** repeated on every
  page record.

### 5. Draft regulated copy awaiting professional sign-off
On regulated niches (medical, dental, health), AI-drafted clinical statements and any uncertain factual
label are **draft until a qualified human approves them** before launch. This is a review gate, not a
build defect, and it does not block building the page.
- **Resolved by:** the human content/clinical sign-off at the pre-launch gate.
- **Logged under:** a **Draft copy for sign-off** line in the page record, listing the passages.
- **A real defect instead of deferred:** a drafted clinical claim presented as final, or one with no
  sign-off flag at all.

### Related, already documented: media-library binding
Images are URL-referenced because the beta MCP cannot bind media (`limitations.md`). A human binds
them in the builder for `srcset` as a batch pass. Same shape as the above: a scheduled improvement,
not a defect. Note it under Deferred passes if a page relies on it, do not re-flag it.

## How to record it (page record `build-log/pages/<slug>.md`)

Under a single **Deferred passes** section:

```
## Deferred passes (expected, resolved in a later pass — not defects)
- Images: N placeholders. See Outstanding images table. Pass: source-images.
- Links: N internal links to unbuilt pages (list the target slugs). Pass: build those pages, then link check.
- SEO meta: drafted below, to paste into The SEO Framework. Pass: seo-meta.
  - Title: <drafted title>
  - Meta description: <drafted description>
```

If a page has none of a given kind, omit that line. Keep it terse. This section is the punch-list the
deferred passes consume; it is not a list of problems.

## See also
- `image-placeholder.md`, `prompts/source-images.md` — the images pass.
- `prompts/seo-meta.md` — the SEO meta pass.
- `build-standards.md`, `build-checklist.md`, `limitations.md`.
