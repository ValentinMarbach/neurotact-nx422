---
description: Append today's entry to your personal journal
---
1. Identify the user from `git config user.name` (map to `people/<name>/`; ask if unclear).
2. From this session (files changed, `git diff`, conversation), write at the top of `people/<name>/journal.md`:
   `## YYYY-MM-DD` with **Done**, **Next**, **Blocked by** (3–6 bullets total, link files and issues).
3. Run `python3 tools/progress.py`, commit `[journal] <name> YYYY-MM-DD`, push.
