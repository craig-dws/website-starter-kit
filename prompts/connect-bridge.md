# Connect the bridge (existing-site builds only)

> **If you are Claude and this file was attached or referenced rather than pasted, these are your
> instructions. Follow them from "Start" below.** Do not ask what to do with the file.

Paste this into Claude Code, in the client folder, to connect the **third-party bridge plugin** that
lets Claude write layouts on an **Elementor or Breakdance 2.x** site. It is the setup step for
`prompts/existing-site-page.md`.

**You almost certainly do not need this.** A normal build on a Breakdance 3.0 staging site uses the
first-party connection and `prompts/connect-mcps.md`. This is only for adding a page to a site that is
already live and was built by someone else, where that connection does not exist.

## Read this before anything else

**The bridge is never installed on the client's live site.** Not to read from it, not for one small
change, not temporarily. It carries site-privileged abilities including PHP execution, and its sandbox
is not a security boundary. It goes on a throwaway local copy that gets deleted afterwards, and that is
the entire safety model. If you find yourself reasoning towards putting it on the live site because a
transfer turned fiddly, stop.

## Status: unverified

The vendor-specific steps below come from `docs/19_implementation_runbook.md`, not from a real
run-through against a local copy. Our own docs describe this plugin as very young. **Treat every step
marked "confirm" as a claim to check, and correct this file on the first real run.** Do not present it
to the operator as a settled procedure.

## Before you paste

- **A LocalWP copy of the whole site**, running. Not a settings export.
- **The licence key**, if the tier you need is paid. `docs/19_implementation_runbook.md` says not to buy
  it until the native Breakdance path has failed a write test, so check one exists before starting.
- **The wp-admin login for the copy.**

---

You are connecting the layout-write bridge to a **local copy** of a client site, so that
`prompts/existing-site-page.md` can add a page to it. You are not connecting to any live site, any
staging site or any production site.

Read `.claude/CLAUDE.md`, `CONNECT.md`, `.claude/settings.json`, the `existing-site-page` skill and
`docs/19_implementation_runbook.md` before you start.

I am a project manager, not a developer. I never run commands and I never edit code. You run everything
you can with your Bash tool. When a step genuinely needs me, which means a wp-admin login, a change in
the Local app, or restarting Claude Code, **stop, give me numbered instructions, and wait.**

## Start

1. **Establish which bridge this project binds.** The project records it, and this kit deliberately does
   not hardcode a vendor. `docs/19_implementation_runbook.md` names Novamira as the fallback binding for
   Breakdance, with Respira as the alternative. If the project has not recorded one, ask me and record
   my answer in `build-log/DECISIONS.md`.
2. **Get the local address of the copy from me** and show it back. It should be a `.local` or
   `localhost` address. **If it is a public domain, stop and say so.** That is the live site and nothing
   below may proceed against it.
3. **Check the tooling** with Bash and report anything missing with its fix: `node --version`,
   `npx --version`, `python --version`.

## The clone traps, before you touch the plugin

A copied site does not arrive ready. Deal with these first or the later steps fail in confusing ways.

1. **Application Passwords need HTTPS, or the site declared as local.** LocalWP is not HTTPS by default,
   so `wp-config.php` usually needs `define( 'WP_ENVIRONMENT_TYPE', 'local' );` followed by a **restart
   of the site in the Local app** so PHP reloads the file.
   **You cannot do this.** `wp-config.php` is a protected path, denied in `.claude/settings.json` and
   blocked by `.claude/hooks/block-protected-paths.sh`. Give me the exact line and where it goes, and
   tell me to restart the site in Local afterwards.
2. **A security plugin may be blocking Application Passwords**, which presents as an "Application
   passwords require HTTPS" error even when the site is fine. The full troubleshooting order, including
   the Admin and Site Enhancements trap that is the most common cause, is in `START-HERE.md`. Read it
   rather than guessing, and hand me the fix as wp-admin clicks.

## Install and configure the plugin (my hands, your instructions)

Give me these as numbered wp-admin steps, one at a time, and wait after each.

1. **Install and activate the bridge plugin** on the local copy. Confirm with me that the site in the
   browser address bar is the local one before I click anything.
2. **Enable its AI abilities.** A copied site normally arrives with these switched **off**.
3. **Repoint the domain lock at the local address.** This is the trap that catches people:
   `docs/19_implementation_runbook.md` records that cloning leaves the lock pointing at the **old
   domain**, so the plugin silently refuses to work. *(Confirm the setting's name and location against
   the installed plugin.)*
4. **Check safe mode** and set it for the work intended. *(Confirm.)*
5. **Generate an Application Password**, named for the person using it, under Users and then Profile.
   WordPress shows it **once**. Have me paste it and the username back here.

## Register it, and arm the guard at the same time

**Do these two together. The connection without the guard is the dangerous configuration.**

1. **Add the deny rule first, before connecting.** `.claude/reference/limitations.md` records that the
   dangerous ability pack cannot be switched off on this class of plugin, and that the mitigation is to
   deny the execute-ability route in `.claude/settings.json`. **Check whether that deny actually exists
   in this project. In the starter kit it does not**, so you are probably adding it rather than
   confirming it. Add a deny entry keyed to the exact MCP server name you are about to use, tell me in
   one plain sentence what it blocks, and show me the change.
   *(Confirm the exact permission-pattern syntax works, by checking after the restart that the
   dangerous tool is genuinely absent. Do not assume a pattern is effective because it looks right.)*
2. **Then register the server**, with the **same name verbatim**. A name that does not match the deny
   entry silently disarms the guard you just added.
   - **Local scope**, which is the default. **Never `--scope project`**, which would write the password
     into a committed file.
   - Recommended: you run the `claude mcp add` command yourself with Bash, so the name cannot be
     mistyped. If I would rather keep the password out of the chat, give me the command to run in
     **cmd.exe, not PowerShell**, which mangles the `--` terminator.
3. **Tell me to fully quit and reopen Claude Code**, then re-paste this prompt so you can verify in the
   fresh session. A new chat is not enough; MCP servers load when the app starts.

## Verify, and be strict about it

In the fresh session, report a short green or red checklist:

- `/mcp` lists the bridge as connected.
- **One read-only call returns the local copy's own data, with the local address visible in it.** This
  is the check that matters. Show me what came back. Not "it connected", but what it said its site is.
- **The dangerous execute-ability tool is absent** from the tool set. If it is present, the deny is not
  applying: the server name does not match. Remove the server and reconnect with the exact name.
- No write of any kind has been attempted.

If any line is red, say so and stop. A half-connected bridge with an unarmed guard is worse than no
connection, because the next session will assume it is safe.

## Finish

1. **Record it in `build-log/DECISIONS.md`**: which bridge, which version, the local address, the deny
   rule added, and the date.
2. **Correct this file** where reality differed from the steps above, and remove the "confirm" markers
   you have now confirmed. That is the point of the first run.
3. **Send me the report below.** Then stop. Do not start building; that is
   `prompts/existing-site-page.md`.

### The report to send me

```
## Bridge connected

Status: <Connected and verified on the local copy  |  Not connected, see below>

What it is pointed at: <the local address it reported back, in its own words>

The guard: <"Armed and verified: the dangerous ability is absent." or what is wrong.>

Needs you:
- <plain actions only I can do, or "Nothing.">

Corrections I made to this prompt: <what the real plugin did differently, or "None.">
```

Rules for the report:

- **Never report connected without having seen the local address come back from the site itself.**
- **Never report the guard armed because the deny rule is in the file.** It is armed when the dangerous
  tool is confirmed absent after a restart.
- If the plugin turns out not to support what this build needs, say so plainly. That is a real finding
  and it changes the plan, rather than something to work around quietly.

## When the job is done

The local copy is deleted when the page has been transferred and promoted. If it is kept for any reason,
**remove the bridge connection and revoke the Application Password**, the same rule as removing the
Agent Connector before a staging site goes live.

British and Australian English. No em dashes, no en dashes, no double hyphens in prose. No emojis.
