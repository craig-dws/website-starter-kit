# Builder: [BUILDER NAME]

<!--
TEMPLATE for adding a builder. Copy to .claude/builders/<builder-id>.md, fill every section, and
write the matching limits skill in .claude/skills/<builder-id>-limits/SKILL.md. Nothing else changes:
the core .claude/CLAUDE.md is never edited to add a builder.

Rules for this file:
- Name no connection. How Claude reaches the site belongs in a connection file.
- Invent nothing. Every fact comes from a real site, or is marked *(confirm)*.
- Keep it to what must load into every chat. Detail goes in the limits skill.
- Delete this comment block when the file is filled.

Before a client build relies on this builder, prove each of these on a real staging site and
record the evidence (date, site, version) in the limits skill:
[ ] Where a page's layout is stored, confirmed by reading a real page's stored layout.
[ ] Where the tokens live, confirmed by reading them from a real site.
[ ] A throwaway page written through at least one connection, then opened in the builder's own
    editor and confirmed editable, then deleted.
[ ] What "verified as editable" looks like when it FAILS, seen at least once, so the check below
    is known to catch it.
[ ] How the builder's own cache or compiled styling is refreshed after a write.
[ ] At least one connection file lists this builder under Supports, with its own proof done.
[ ] The row for this builder added to the combinations table in START-HERE.md.
-->

The rules for a site built in [BUILDER NAME]. They name no connection: how Claude reaches the site
is in the connection file.

Build target: [a new build target, or an existing site we work within].

## Stack
- [Platform and version, pinned. Where it runs: [HOST]]
- [Builder and version, pinned, and any paid tier]
- [Anything else that caches or compiles output, and who clears it]

## Layout
- [Where a page's layout is stored, and in what form]
- [The shared parts (templates, headers, reusable blocks) and their blast radius]
- [What must never be written directly]

## Tokens
- [Where the named colour, type and spacing values live, and how a page references them]
- [Whether they are ours to change on this kind of site]

## Verified as editable
- [The check that proves a written page is still editable in the builder, and what failure looks like]

## Protected paths (do not edit)
- [Files an agent must never write on this platform]

## Limits skill
`[builder-id]-limits`. Read it before the first write.

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| [term] | [plain words] |
