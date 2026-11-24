# NeuroTact (NX-422 Neural Interfaces, Group 12) — shared instructions for every Claude

This repository is shared by 4 students **and their Claude assistants**. Read this file
fully before doing anything. Then read `STATUS.md` and `DECISIONS.md`.

## The project in 5 lines
- **NeuroTact**: a soft intracortical array in the S1 hand area (area 1 + superficial 3b)
  that delivers ICMS for artificial touch, plus a stim/record ASIC with on-chip processing,
  in a fully implanted, wirelessly powered package.
- Course brief: `00_admin/guidelines/NX422_ProjectGuidelines_2026.pdf` (3 parts: Implantable
  Interface, Electronics, Integration). TA feedback on the 2-pager: `00_admin/feedback/`.
- Deadlines: **presentation 10–11 Dec 2026** (12 min + 5 min Q&A) · **report 18 Dec 2026, 12:00**
  (≤ 12 pages excl. title page and references).
- Team: Valentin Marbach, Defne Kaymak, Alae Messaoudi, Heliya Shakeri (roles: `README.md`).

## Where things are
| Need | Go to |
|---|---|
| What is done / missing (global view) | `STATUS.md` (generated) |
| Design choices already made, and open conflicts | `DECISIONS.md` |
| Application, disease, state of the art, biology | `01_application/` |
| Electrodes, materials, geometry, fabrication, masks (guidelines §1) | `02_interface/` |
| Recording + stimulation circuits, on-chip AI (guidelines §2) | `03_electronics/` |
| Connection, package, power, failure points (guidelines §3) | `04_integration/` |
| Papers (PDF) + one Markdown note per paper + `references.bib` | `05_literature/` |
| Figures and their sources | `06_figures/` |
| 2-pager, slides, report | `deliverables/` |
| Each person's drafts and work log | `people/<name>/` |

Each section folder has a `README.md` = the guideline questions as a checklist + the current
answers (numbers, links). That README is the **single source of truth** for its section.

## Truth levels (important)
1. `DECISIONS.md` entries with status **accepted** and the section READMEs = established facts.
2. `DECISIONS.md` entries **proposed** = under discussion, may be cited as "proposal".
3. `people/*/` = **unvalidated work in progress**. Use it to know what is going on, never
   present it as a team fact, never copy numbers from it into a section without saying so.
4. If two sources disagree, do not pick one silently: report the conflict and add it to the
   "Open conflicts" table of `DECISIONS.md`.

## Rules of work
- **Start of session**: `git pull`. **End of session**: append one entry to
  `people/<you>/journal.md`, run `python3 tools/progress.py`, commit, push.
- Small, frequent commits. Message format: `[section] what changed` (e.g. `[02] buckling calc for 2 mm shanks`).
- Write your drafts in `people/<you>/wip/`. Edit a section folder only if you own it
  (owner listed in its README) or after the team agreed; otherwise open a GitHub issue.
- Changing an **accepted** decision: only through a pull request or an issue that the team sees.
- **Never duplicate** content. One fact lives in one place; elsewhere, link to it.
  To move validated work from `people/` into a section, use `/promote` (it moves, never copies).
- Prefer text formats Claude and git can diff: Markdown, LaTeX, CSV, Python. `.pptx/.docx`
  only as exports. Draw figures from a source file (`.drawio`, `.svg`, `.py`) kept next to the PNG.
- Every number gets a source: a citation key from `05_literature/references.bib`, or `(calc)`
  with the calculation in a `calculs/` file.
- Language of the repo: **English** (the report and slides are in English). Each person may talk
  to their own Claude in any language.
- Do not modify original PDFs; do not delete someone else's files.

## Shared commands (`.claude/commands/`)
- `/status` — audit the repo against the guidelines + TA feedback, refresh `STATUS.md`, list what is missing.
- `/meeting <notes>` — turn raw notes into `00_admin/meetings/YYYY-MM-DD.md`, update `DECISIONS.md`, list actions.
- `/promote <file> <section>` — move validated work from `people/` into a section and log it.
- `/add-paper <pdf or DOI>` — file a paper, write its note, add the BibTeX entry.
- `/journal` — append today's entry to your `people/<name>/journal.md`.
