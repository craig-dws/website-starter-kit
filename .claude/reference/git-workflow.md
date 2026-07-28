# Git workflow (commit cadence and two-machine sync)

The `build-log/` is the durable memory of the build. **Git is the shared backup, the recovery points,
and how two machines stay in sync.** Commit often, at natural boundaries. Yes, commit after every page.

## When to commit (and push)
- **After each page or component is built and logged.** One page is a clean, reviewable unit. Commit its
  record, its content and any design or settings changes, then push. This is the main cadence.
- **After a stage boundary** (the design system, header, footer), a batch of changes, or a plan round.
- **Not mid-write.** Commit at a resting point, once the build-log entry for that unit is written, not
  half way through a page.

Why per page: it gives clean history, a recovery point if a later write goes wrong, and it is what lets
a second machine pull your work. It also keeps commits small enough to review.

## Two machines building in parallel
- **Pull before you start**, and again before each new page, so you have the other machine's work.
- **Claim your section in `build-log/ACTIVE.md`** before building (see `parallel-builds.md`). Working
  different sections keeps conflicts near zero.
- **Push as soon as a page is done**, so the other machine sees it on its next pull.
- A conflict, if it happens, will be in a build-log or content file. Keep both sides' entries; never
  discard the other machine's log lines.

## Messages
Short and specific: what the page or change is. One unit per commit where practical.

## Branches and production
- The build works on `main` for staging. If you want review before merging, branch per feature and open
  a PR; otherwise commit to `main` and push.
- **Git never touches production.** Production is reached only by the human migration step, not by a
  push. Staging is the only thing the build writes.

## Secrets
Never commit secrets. The Application Password lives in `~/.claude.json`, not the repo; `.gitignore`
already excludes `.env`, `settings.local.json` and the source image library. If a secret is ever
committed, rotate it and scrub it, do not just delete the file.
