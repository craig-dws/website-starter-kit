# Docs archive

Superseded documents. Kept for provenance, not for use. Nothing here should be implemented.

| File | Status | Replaced by |
|---|---|---|
| `HANDOVER_CONTENT_SYNC_PLAN_2026-08.md` | Superseded 2026-08-08 | `../STARTER_KIT_PLAN_2026-08.md` |

The replacement keeps the draft's handover pack layout, the `CONTENT_CHANGELOG` convention and the
launch-gate reconciliation item. The substantive change is a new task K5.

The draft assumed `/content-reconcile` could read a `content/` diff to detect drift between the
Google Docs and the live site. This kit builds on WordPress and Breakdance, where page copy lives in
the `_breakdance_data` postmeta field rather than in repo files. A developer editing a heading in the
Breakdance UI leaves no git evidence, so a diff-based reconciliation would miss exactly the changes
it exists to catch, and would then refresh the Docs to something the site does not say. K5 adds a
committed live content export to `content/_live/` so reconciliation is verified rather than
self-reported. The changelog keeps its job as the record of why a change was made.
