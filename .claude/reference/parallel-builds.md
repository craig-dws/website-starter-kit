# Parallel builds (more than one session on the same build)

You can run more than one chat on the same client build, but they share the staging database
and the repo, so they must coordinate. There is no automatic lock between chats, so use the
claim board below.

## Safe to parallelise
- **Independent page objects, once the design system is locked.** Two different pages, or a page
  and a distinct template. Each references existing tokens and classes, writes only its own post,
  and logs to its own `build-log/pages/<slug>.md`.

## Not safe in parallel
- **The shared design system:** `set-global-settings`, or adding global classes/variables with
  `insert-stylesheet` / `insert-css-variables`. These write a shared resource, serialise them to
  one session.
- **Shared repo files:** `settings.json`, `.claude/CLAUDE.md`, `build-log/BUILD-LOG.md`,
  `GATES.md`, `DECISIONS.md`. Two sessions editing the same file race. Partition, or one owns it.
- **The shared chrome** (header, footer) while either still needs global-style writes.

## The claim protocol (how a session checks if another is running)
Use `build-log/ACTIVE.md` as a cooperative claim board:
1. **At the start of a work session, read `build-log/ACTIVE.md`.**
2. If another session has claimed your intended object, or is doing global-settings work, pick
   different work or wait. **Never write global settings while another session is active.**
3. **Claim your work:** add a row, what you are building, which object/post, the time (from
   `date`), status `active`.
4. **Release when done:** set your row to `done` or remove it.
5. Treat a claim older than about 2 hours as a likely crashed session, but confirm before
   overriding it.

## Rule of thumb
Lock the design system and build the shared components first, in **one** session. Then fan out
independent pages in parallel, one session per page, each claiming its page and logging to its
own record. Do not parallelise the header and footer, they share the chrome and the global styles.

For a **set of same-type pages** (all the condition pages, all the treatment pages): build the
**first** one from its reference design in a single session, it establishes that type's shared
components and global classes. Then fan out the remaining pages of that type in parallel, they reuse
what the first established and only write their own page. A second page that needs a *new* shared
component pauses and adds it in one session, then parallel resumes.
