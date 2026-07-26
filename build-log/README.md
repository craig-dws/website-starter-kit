# Build Log

The audit trail for this client build. It exists because **git tracks file
changes, but nothing tracks what an agent did to the WordPress database on
staging** — and that is precisely the risky, hard-to-reconstruct part of a
Breakdance build. This folder closes that gap.

## Files

| File | What it records | How it is filled |
|------|-----------------|------------------|
| `BUILD-LOG.md` | Chronological activity: DB writes, cache clears, deploys, milestones | **Auto** (the `build-log.sh` hook appends DB-affecting commands) plus manual milestone lines |
| `GATES.md` | The lifecycle gates, each with a named human owner, status, date, evidence | Manual, at each gate |
| `DECISIONS.md` | Choices made during the build and why | Manual, when a decision is made |
| `pages/` | One record per page built (Figma frame, staging URL, verification, snapshot) | Copy `pages/_TEMPLATE.md` per page |

## How the automatic logging works

`.claude/hooks/build-log.sh` runs after every Bash tool call. When the command
is a database-affecting or deploy operation (`wp breakdance ...`, `wp post ...`,
`wp db ...`, `import_settings`, `clear_cache`, `deploy`), it appends a timestamped
row to `BUILD-LOG.md`. Ordinary file edits are not logged here because git already
records them.

## What you still log by hand

- **Snapshots.** Before the first agent write, and before any risky write, record
  the snapshot in `BUILD-LOG.md` (what you backed up, where it is). The hook cannot
  take a snapshot for you; it only records the writes that follow.
- **Gate approvals.** Every gate in `GATES.md` needs a named human owner and a date.
  AI never approves a gate.
- **Milestones and decisions.** Page signed off, design system certified, UAT passed,
  launch. One line in `BUILD-LOG.md` and, for decisions, a row in `DECISIONS.md`.

## Rule of thumb

If someone asked "what did the agent change on staging, when, and who approved it?",
this folder should answer without anyone having to remember.
