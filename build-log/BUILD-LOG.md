# Build Log — [CLIENT]

Chronological record of build activity. Rows marked `auto` are appended by the
`build-log.sh` hook after database-affecting commands. Add `manual` rows for
snapshots, sign-offs and milestones. Newest at the bottom (append-only).

**Legend for `type`:** `snapshot` (backup taken) | `db-op` (agent DB write) |
`deploy` | `milestone` | `gate` (see GATES.md) | `note`.

| Timestamp | Actor | Type | Detail |
|-----------|-------|------|--------|
| YYYY-MM-DD HH:MM:SS | [name] | milestone | Project initialised from the website starter kit |
| YYYY-MM-DD HH:MM:SS | [name] | snapshot | Pre-build DB snapshot taken: [location / filename] |
