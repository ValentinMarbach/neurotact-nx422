---
description: Turn raw meeting notes into a meeting file, update DECISIONS.md, list actions
argument-hint: <raw notes or path to notes>
---
Notes: $ARGUMENTS
1. Write `00_admin/meetings/YYYY-MM-DD.md` from `00_admin/meetings/_TEMPLATE.md` (English, concise).
2. For each decision: add or update a row in `DECISIONS.md` (next free D-ID, status `accepted` if the team agreed,
   else `proposed`); if it resolves a conflict C#, remove the conflict row and reference it in the decision.
   If it replaces an older decision, mark the old one `superseded`.
3. Update the affected section README checkboxes and key-number tables (link to the decision).
4. List the actions. Ask the user whether to create them as GitHub issues (`gh issue create`, label = section,
   milestone = Presentation or Report, assignee = owner).
5. Show the diff, then commit `[meeting] YYYY-MM-DD` after confirmation.
