# Connection: a third-party bridge plugin, on a disposable local copy

A third-party plugin (the "bridge") that writes layout for a builder with no first-party write
path, connected to a throwaway local copy of the client's site. Which vendor is recorded per
project in `build-log/DECISIONS.md`: Novamira is the named fallback for Breakdance, Respira the
alternative. Nothing here depends on which.

**Supports:** Elementor. Breakdance 2.x, and Breakdance 3.0 only if its native MCP fails the write
test. **Not a block theme or WPBakery**: WordPress core already writes their layout through its own
API, and a bridge would add full PHP execution reach for nothing (AI Web Design System decisions,
16 September and 1 October 2026).

**Where it runs:** only on a disposable local copy of the site, normally in LocalWP. **The bridge
is never installed on the live site**: not to read from it, not for one small change, not
temporarily. It carries site-privileged abilities including PHP execution, and its sandbox is not
a security boundary. The copy being throwaway is the whole safety model.

**Credential:** a WordPress Application Password generated on the copy, registered with
`claude mcp add` at the default local scope, so it lives in your local Claude config
(`~/.claude.json`) and never in the repo. Setup: `prompts/connect-bridge.md`, which also arms the
safety deny rule. The connection without the deny rule is the dangerous configuration.

**Status: unverified.** There has been no real run-through against a local copy yet
(`prompts/connect-bridge.md`). Every line marked *(confirm)* is a claim to check on the first real
job, and to correct here.

## How each capability is done

| Capability | On this connection |
|------------|--------------------|
| Confirm the environment | One read-only call through the bridge, showing the address the site reports. It must be a `.local` or `localhost` address. A public domain is the live site: stop |
| Read a page's layout | The bridge's read of the builder's stored layout *(confirm the ability on the installed plugin)* |
| Snapshot a page | The copy is disposable and regenerable, so a snapshot of it can be waived, recorded. On the live site a person takes a full backup before anything is moved there, never waived |
| Write a page's layout | The bridge, on the copy only, as a constrained patch of a known-good page, ranked by the builder's limits skill *(confirm)* |
| Upload media | `.claude/tools/optimize-and-upload.py` over the WordPress media REST API, reading the credential from the local Claude config. Media on the copy does not travel with a page; say which images the live site will need |
| Clear the cache | A person, in wp-admin on the copy: the builder's own cache or CSS regeneration, then any page cache |
| Read the design tokens | The bridge's read of the builder's global settings *(confirm)* |
| Write the design tokens | Never. On an existing site the tokens are not ours to change |

**Moving the page to the live site** is not a capability of this connection. A person does it,
backed up, following the steps the builder's limits skill and the `existing-site-page` skill give,
all as clicks in wp-admin.

## When the job is done
The local copy is deleted once the page is on the live site. If it is kept for any reason,
remove the bridge connection and revoke the Application Password.

## Talking to the operator
| Term | Say this instead |
|------|------------------|
| bridge | the third-party plugin that lets Claude change the layout on the local copy |
| local copy | a throwaway copy of the whole site on this computer, deleted afterwards |
| Application Password | the site login Claude uses, one per person, revocable in wp-admin |
