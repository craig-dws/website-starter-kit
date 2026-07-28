# Connect the MCPs (guided setup, new machine)

Paste this into Claude Code, **in this cloned site folder**, on a machine that has Claude Code but not
the site's MCP connections yet. Claude does everything it can itself and stops to prompt you only when a
step genuinely needs you: logging in to wp-admin, or restarting the app. `CONNECT.md` is the reference
detail behind every step.

---

You are setting up this build's MCP connections on a new machine. Work from `CONNECT.md` in this folder.
Do everything you can yourself with the Bash tool. When a step needs the human (a wp-admin login,
restarting Claude Code, authorising a claude.ai connector), **stop, give clear numbered instructions,
and wait** rather than guessing.

## 0. Orient and check prerequisites
- Read `CONNECT.md` and `.claude/settings.json`. **Note the exact MCP server name the permission rules
  are keyed to** (grep the `deny` list for `breakdance-wordpress`); you must reuse it verbatim in step 1.
- Check tooling with Bash and report what is missing, with the fix:
  - `node --version` and `npx --version` (the WordPress and chrome-devtools MCPs run via npx).
  - `python --version` and `python -c "import PIL, requests"` (the image-upload tool needs Pillow +
    requests: `pip install pillow requests`).
  - Chrome installed (chrome-devtools drives headless Chrome).
- Continue with what you can even if something is missing; just flag it.

## 1. Breakdance MCP (the only connection with a secret)
This connects the site so Claude can build layouts.

- **The server name MUST be exactly the one in `settings.json`** (for this build,
  `ees-dev-dwsstaging-net-au-start-website-breakdance-wordpress`). The safety deny rules that block
  `shell-exec`, `php-eval`, `wp-cli` and the rest of the Universal Abilities pack are keyed to that
  name. **A different name silently disables every one of those guards.** Read it from `settings.json`,
  do not retype it from memory.
- **Prompt the human for the Application Password** (needs a wp-admin login, you cannot do this):
  1. Log in to the staging site's wp-admin (`WP_API_URL` in `settings.json`). If you have no login, ask
     the site owner for a **WordPress admin account on the staging site** (or a second app password on
     the existing user).
  2. Open **Agent Connector > Connect** and generate **your own new** Application Password, named for you
     (e.g. "Eastwood MCP - <your name>"). **Do not reuse anyone else's password.** WordPress shows an app
     password **once** then stores only a hash, so there is nothing to copy off the site later, and a
     per-person password is **individually revocable**, which matters because this credential can reach
     the armed Universal Abilities on the server. Copy it now.
  3. Paste the password and the username it belongs to back here.
- **Then connect.** Build the working command from `CONNECT.md` step 4 with the **exact server name**
  above, the pasted username and password, and the **default (local) scope** (never `--scope project`,
  which would write the password into a committed file). **Recommended: you run it via the Bash tool** so
  the server name is exact and cannot be fat-fingered (note the password appears in this session, which
  is on the user's own machine). If they prefer to keep the secret out of the chat, give them the command
  to run in **cmd.exe, not PowerShell** (PowerShell mangles the `--` terminator).
- The site-side settings and the Universal-Abilities deny are already done: the Agent Connector toggles
  are server-side (set once, already set) and the deny rules are in the cloned `settings.json`. Nothing
  to redo; you confirm the deny is in effect after the restart in step 4.

## 2. chrome-devtools MCP (no secret)
For the Figma visual diffs and the QA auditors. Run it yourself:
```
claude mcp add -s user chrome-devtools -- npx -y chrome-devtools-mcp@latest --headless=true
```
User scope, so every build on this machine gets it.

## 3. Figma MCP (optional, only if they will read designs)
The Figma connection is the claude.ai connector: **no local secret**, authorised through the user's own
claude.ai account in connector settings. It is needed to read the reference frames (condition, treatment,
surgeon designs), not to build from components already established on the site. If `mcp__figma__*` tools
are absent when a design is needed, tell them to authorise Figma in their claude.ai connector settings.

## 4. Restart, then verify (you cannot restart the app yourself)
- Tell them to **fully quit and reopen Claude Code** (a new chat is not enough; MCP servers load at app
  start), reopening this folder, then **re-paste this prompt** so you can run the verification in the
  fresh session.
- In the fresh session, confirm and report a short green/red checklist:
  - `/mcp` shows the Breakdance server and `chrome-devtools` connected.
  - `breakdance/site-info` returns the site (Breakdance 3.0.0-beta.1, the home/header/footer ids).
  - The Breakdance **write tools** are present (`html-to-page`, `edit-post`, `insert-stylesheet`, ...).
  - The dangerous route `mcp-adapter-execute-ability` is **absent** from the tool set: proof the deny is
    applying to this server name. If it is present, the server name does not match `settings.json`,
    remove the server and reconnect with the exact name.
  - The image tool can read creds from `~/.claude.json` (a dry check; do not upload anything).
- If Breakdance tools are missing, it is almost always the native MCP not enabled
  (**Breakdance > Settings > Agents & MCP**) or a server-name mismatch. See `CONNECT.md` step 6 and the
  troubleshooting in `START-HERE.md`.

## Then
Once green, reorient with the Stage 0 resume line in `START-HERE.md` and pick up the build. **If both
machines build at the same time, claim your section in `build-log/ACTIVE.md` first** (see
`parallel-builds.md`) so the two sessions do not collide.
