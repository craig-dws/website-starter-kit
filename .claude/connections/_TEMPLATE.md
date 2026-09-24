# Connection: [CONNECTION NAME]

<!--
TEMPLATE for adding a connection method. Copy to .claude/connections/<connection-id>.md and fill
every section. Nothing else changes: the core .claude/CLAUDE.md is never edited to add a
connection.

Rules for this file:
- Say how EVERY capability in the core's table is done. Where this connection cannot do one, say
  who does it instead (usually a person, and exactly where they click).
- Name where the credential lives. It is never a committed file. Any tool in .claude/tools/ that
  needs it must be able to read it from that place (see .claude/tools/wp_credentials.py).
- Invent nothing. Mark anything not yet seen on a real site *(confirm)*.
- Delete this comment block when the file is filled.

Before a client build relies on this connection, prove each of these on a real staging site and
record the evidence (date, site, versions) under Status:
[ ] Connected, and the "confirm the environment" call returned the staging site's own address.
[ ] A read of one real page's stored layout.
[ ] A snapshot taken, and restored onto a throwaway page, with the result checked.
[ ] A throwaway page written, opened in the builder's editor and confirmed editable, then deleted.
[ ] One image uploaded and seen in the media library.
[ ] The cache route tested: the public page check in the core passed after a write.
[ ] Any dangerous abilities the connection exposes are listed, and denied in
    .claude/settings.json where it can be done, with the deny confirmed working after a restart.
[ ] The combinations table in START-HERE.md updated for each builder listed under Supports.
-->

[One or two sentences: what this connection is, in plain words, and what is installed where.]

**Supports:** [builders this connection can write layout for, and which it cannot, with the reason]

**Credential:** [what it is, where it lives on this machine, why that is never in the repo, and the
setup prompt]

**Status:** [proven where and when, or "unverified"]

## How each capability is done

| Capability | On this connection |
|------------|--------------------|
| Confirm the environment | |
| Read a page's layout | |
| Snapshot a page | |
| Write a page's layout | |
| Upload media | |
| Clear the cache | |
| Read the design tokens | |
| Write the design tokens | |

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| [term] | [plain words] |
