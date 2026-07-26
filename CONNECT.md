# Connecting a site to Claude Code

How to connect a client's WordPress / Breakdance staging site to Claude Code. Do this
once per site, on each developer's machine. The steps are identical for every build.

## How it works, and why there is nothing to edit

The Agent Connector plugin generates a WordPress Application Password and hands you a
ready-made `claude mcp add ...` command. Running that command from the site's folder
registers the site's MCP server in your **local** Claude Code config
(`~/.claude.json`), scoped to that one project directory.

The password lives there, on your machine, **never in the repo and never in git**. That
is the whole point: one command, the secret stays local, no config files to edit and no
environment variables to juggle. Because it is scoped to the folder, each site's
connection is isolated and two sites never collide.

## Steps (repeat per site)

1. In wp-admin, open **Agent Connector > Connect** and generate the Application
   Password. It is shown once, so copy it immediately.
2. The Connect screen shows a `claude mcp add ...` command. Copy it, but expect to adjust
   it on Windows (next step).
3. Open a terminal **in this site's project folder**:
   ```
   cd "C:\DWS\Websites\<Site Folder>"
   ```
4. Run the `claude mcp add` command there, at the default scope, so the connection belongs
   to this project only.

   **Windows note, this bites everyone the first time.** Run it in **Command Prompt
   (cmd.exe), not PowerShell.** PowerShell mangles the `--` terminator, so the repeated
   `--env` options swallow the `npx` arguments and the add fails. Also drop the single
   quotes the Connect screen wraps values in, and double-quote the password. Working form:
   ```
   claude mcp add <server-name> --env WP_API_URL=<url> --env WP_API_USERNAME=<user> --env "WP_API_PASSWORD=<paste-password>" --env OAUTH_ENABLED=false -- npx -y @automattic/mcp-wordpress-remote
   ```
5. **Fully restart Claude Code before the tools appear.** `claude mcp list` may already say
   Connected, but MCP servers only load when the app starts, so a new chat is not enough.
   Quit and reopen the desktop app (or restart the CLI), reopening this folder.
6. Run `/mcp` to confirm the server is connected, then have Claude **list the tools** and
   confirm the Breakdance write tools are present (breakdance/html-to-page, create-template,
   set-global-settings, and so on). If only generic tools appear, the Breakdance native MCP
   is not enabled: turn it on at **Breakdance > Settings > Agents & MCP** and reconnect.

## The staging operating model (read once, then it never changes)

This build runs on a disposable **staging** site. We do **not** rely on the Agent
Connector's environment guards. Safety comes from process:

- Agents only ever touch the staging site, never production.
- The site stays on the staging domain for the whole build.
- At migration, the site is moved to the client domain and the **Agent Connector plugin
  and the MCP connection are removed** before it goes live. This is the step everything
  depends on.
- Least privilege (Universal Abilities off) limits what is exposed if that removal is
  ever missed.

Because of this, it does **not** matter that the site reports "production", and the
environment-based protections stay off. They are not part of our model, so do not turn
them on expecting them to help.

## Agent Connector settings (the exact toggles, every site)

Set these once, in **Agent Connector > Settings** and **Abilities**:

| Setting | State |
|---------|-------|
| Enable Agent Connector | ON |
| Universal Abilities pack | OFF |
| Disable production warning | OFF |
| Block on production environments | OFF |
| Enable domain lock | OFF |
| Log MCP events | OFF (once connected) |

Only two differ from what you will see by default, and one of them is not a simple toggle:

- **Universal Abilities** (shell, PHP eval, filesystem, WP-CLI, create-admin-login-link) is
  **active by default and reachable over MCP, and the current Agent Connector beta gives you
  no way to turn it off.** The Ability Packs tab only generates packs for your other plugins;
  the pack has no Settings switch and is not a deactivatable plugin. You cannot remove those
  abilities without deactivating Agent Connector itself, which you need. So the mitigation is
  a repo-side deny plus a recorded risk acceptance (next section). It matters because the
  local guards (hooks, settings.json deny rules) only see Write/Edit/Bash, never MCP calls,
  so these abilities bypass every guard, and shell-exec/file-write reach the whole server,
  not just this site. The `breakdance/*` tools are a separate provider, unaffected.
- **Log MCP events** OFF once connected (it stores raw request bodies).

Leave everything else as shipped.

## Universal Abilities cannot be disabled on this beta: the accepted procedure

There is no wp-admin switch for the Universal Abilities pack on the current Agent Connector
beta. Do not deadlock waiting for one. Harden from this repo and record the residual risk:

1. **Deny the executor.** The dangerous abilities (shell-exec, php-eval, wp-cli, the file
   tools, create-admin-login-link) are **not** exposed as individual MCP tools. They are
   reachable only through `mcp-adapter-execute-ability`, which takes an ability name as an
   argument. Denying that single meta-tool, plus `mcp-adapter-get-ability-info`, in
   `.claude/settings.json` closes the hole. Add per-ability deny entries too, pre-emptively,
   in case a future build ever surfaces them as first-class tools.
2. **Have the connected session do it.** It sees the exact tool identifiers and can verify
   the deny took effect (the denied tools drop out of its available set immediately, no
   restart needed).
3. **Record a risk-acceptance decision** in `build-log/DECISIONS.md`: the abilities remain
   armed on the server; the deny protects only this project on this machine; the residual
   risk (another MCP client or project using the Application Password) is accepted because
   the password is team-held and not in the repo, the site is disposable staging, and the
   connector is removed at migration.

Note: `search-media`, a benign read-only tool, is collateral. It was only reachable via
`execute-ability`, so denying the executor kills it too. Handle media by existing library
URLs or Breakdance's picker.

## Keep the Breakdance write tools on prompt until you have a snapshot

The deny closes the dangerous pack; it does not gate the Breakdance write tools, and you
should not allow those yet. Leave `html-to-page`, `edit-post`, `insert-stylesheet`, the
`delete-*` tools and the other write tools on **per-call prompt** until the database snapshot
exists. On a beta builder with no backup, that prompt is the last guard before an
unrecoverable write. Promote them to allow once the snapshot is done.

## Install the chrome-devtools MCP (once per machine)

The Figma visual diff and the QA auditor agents (accessibility, SEO, performance) use the
chrome-devtools MCP, which drives **headless** Chrome, with no visible browser pane. Install it
once, at user scope, so every client build gets it:

1. Install Google Chrome if it is not already on the machine.
2. In **Command Prompt (not PowerShell)** (the same `--` terminator gotcha applies), run:
   ```
   claude mcp add -s user chrome-devtools -- npx -y chrome-devtools-mcp@latest --headless=true
   ```
   The `--headless=true` runs Chrome with no visible window, which is what a build/QA context
   wants. (Drop it only if you ever need to watch the browser for debugging.)
3. **Fully restart Claude Code**, then run `/mcp` and confirm `chrome-devtools` is connected.

Without it the build can only measure rendered elements, not screenshot them for the visual
diff against Figma.

## Managing connections

- List what is registered: `claude mcp list`
- Remove a stale or duplicate one: `claude mcp remove <name>`
- If you rotate the Application Password, remove the old server and run the new
  `claude mcp add` command again.

## Rules

- Run the command from the site folder with the **default (local) scope**. Never use
  `--scope project`: that writes the password into a committed file and leaks it to git.
- One site per folder. Never reuse another site's connection.
- If an Application Password is ever exposed, revoke it in wp-admin and reconnect.

## If the Connect screen will not generate a password

See the Troubleshooting section in `START-HERE.md` (ASE "Disable Application Passwords",
LocalWP environment type, LiteSpeed HTTPS detection, wrong adapter URL).
