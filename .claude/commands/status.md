---
description: Audit the project against the guidelines and TA feedback, refresh STATUS.md
---
1. `git pull`, then run `python3 tools/progress.py` (updates the counters in STATUS.md and README.md).
2. Read `00_admin/guidelines/NX422_ProjectGuidelines_2026.pdf`, `00_admin/feedback/*`, `DECISIONS.md`,
   every section `README.md` (01–04, 06, deliverables) and every `people/*/journal.md` (last 2 weeks).
3. For each unchecked item, check whether the answer actually exists somewhere in the repo
   (section folder, or `people/*/wip/`). If it exists in `wip/` only, say "draft exists, not promoted".
   If a box is checked but the answer is missing or weak, uncheck it and say why.
4. Rewrite only the section between `<!-- BLOCKERS:START -->` and `<!-- BLOCKERS:END -->` in `STATUS.md`:
   top 10 missing items ranked by deadline risk (`00_admin/planning.md`), each with owner and the file where it should go;
   open conflicts from DECISIONS; anyone working on the same thing as someone else.
5. Print a short summary in the user's language. Commit `[status] audit YYYY-MM-DD` only if the user agrees.
