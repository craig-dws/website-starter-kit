# Global blocks register

The sections that repeat across this site, and what each one becomes. Filled in by the
global blocks audit, once, **before the first page or template is built**, and approved by a
person.

**Every page and template prompt reads this before building a section.** If a section is here,
it is inserted or inherited, never rebuilt. If a section repeats and is **not** here, the build
stops and says so rather than building the duplicate.

Full reasoning, the decision rules and the thresholds are in the `global-blocks-audit` skill.

## Status

| | |
|---|---|
| Audit run on | |
| Sources read | design, `content/`, sitemap, *(and the live site on a migration)* |
| Approved by | |
| Approved on | |

## The decision, in one table

| If it appears | It becomes |
|---|---|
| On every page of one type | part of that type's **template** |
| On pages of different types, identically | a **global block** |
| On several pages with content that differs | a documented **pattern**, or a global block with dynamic fields |
| Once | **inline** |

Three or more identical appearances is a global block. Two is judgement, defaulting to a
pattern. Planned appearances count where the sitemap says so and a person confirms.

## The register

| # | Name | What it is | Appears on | Identical | Varies | Decision | Prefix | Built | Notes |
|---|------|-----------|-----------|-----------|--------|----------|--------|-------|-------|
| 1 | | | | | | | | Not yet | |

**Decision** is one of: template part (name the template), global block, pattern, inline,
rejected.

**Prefix** follows from the decision, per `.claude/reference/class-naming.md`. They are the same
call written twice, so fill both in together:

| Decision | Prefix |
|---|---|
| template part, or design system furniture | `sw-` |
| global block | `gb-` |
| pattern, reused component | `wg-` |
| inline, one page | `pg-` |
| inline, one section | `sc-` |

**Varies** is the crux. If you cannot say precisely what changes between instances, the
candidate has not been looked at closely enough. "Nothing" is a valid and useful answer.

**Built** is Not yet, Built, or Approved. A global block is built **once, on its own, before
the pages that use it**, and verified in isolation.

## Rejected candidates

Sections that were considered and are not being shared. **Keep them here with the reason**, or
the next person re-litigates it or quietly globalises it anyway.

| Name | Why it is not shared |
|------|---------------------|
| | |

## For the client handover notes

Every global block below is edited **once and changes on every page it appears on**. In a
restricted client editing mode this is rarely obvious in the interface, so the client finds out
by changing one page and altering six.

List them here, in plain words, for the handover document.

| Global block | Pages it appears on | What the client should know |
|---|---|---|
| | | |
