---
description: Move validated work from people/<name>/wip into a section folder
argument-hint: <file in people/…/wip> <target folder>
---
Arguments: $ARGUMENTS
1. Confirm with the user that this work was validated by the team (or by the section owner).
2. `git mv` the file to the target folder (never copy). Rename to a clear English name if needed.
3. Update the target section README: tick the relevant checkbox(es), add the link, update the key-number table.
   If the file contains numbers that contradict DECISIONS.md or another section, stop and report the conflict.
4. If it carries a design choice, add/update the row in DECISIONS.md.
5. Add to the author's `people/<name>/journal.md`: "promoted <file> → <target>".
6. Run `python3 tools/progress.py`, commit `[promote] <file> → <target>`.
