# NeuroTact — NX-422 Neural Interfaces, Group 12 (EPFL, Fall 2026)

**Intracortical microstimulation of the somatosensory cortex for artificial tactile feedback.**
A soft polyimide penetrating array in the S1 hand area + a stimulation/recording ASIC with on-chip
processing, fully implanted and wirelessly powered.

| | |
|---|---|
| 🎤 Presentation | **10–11 Dec 2026** — 12 min + 5 min Q&A |
| 📄 Report | **18 Dec 2026, 12:00** — ≤ 12 pages excl. title + references |
| 🗓 Plan | [`00_admin/planning.md`](00_admin/planning.md) — next: **design freeze, Fri 28 Nov** |

## Progress
<!-- PROGRESS:START -->
_Updated 2026-11-26 by `tools/progress.py` — █ done ▒ in progress · missing_

| Section | Progress | Done | In progress | Missing | Owner |
|---|---|---|---|---|---|
| 🟢 [01 Application & state of the art](01_application/README.md) | `████████████` | 7/7 | 0 | 0 | Valentin (neuroscience / LSE1) |
| 🟡 [02 Implantable interface (§1)](02_interface/README.md) | `█████▒▒▒▒▒▒·` | 5/12 | 6 | 1 | Defne (materials, fabrication, surgery / LSE2) |
| 🟡 [03 Electronics (§2)](03_electronics/README.md) | `█▒▒▒▒▒······` | 1/16 | 7 | 8 | Heliya (circuits, power — EE) · Alae (on-chip AI, decoder/encoder, latency — CS) |
| 🟡 [04 Integration (§3)](04_integration/README.md) | `███▒▒▒······` | 2/7 | 2 | 3 | Heliya (power, link) + Defne (bonding, package, surgery) |
| 🔴 [06 Figures](06_figures/README.md) | `██··········` | 1/7 | 0 | 6 | everyone (each draws the figures of their section) |
| **Total** | `████▒▒▒▒····` | **16/49** | 15 | 18 | |
<!-- PROGRESS:END -->

➡️ What is missing, ranked: [`STATUS.md`](STATUS.md) · Choices and open conflicts: [`DECISIONS.md`](DECISIONS.md) · Task board: GitHub **Projects** tab

## Team
| Person | GitHub | Role (to confirm) | Owns | Page |
|---|---|---|---|---|
| Valentin Marbach | `@ValentinMarbach` | Neuroscience / biology | `01_application/` | [people/valentin](people/valentin/) |
| Defne Kaymak | `@defnekaymak` | Materials, fabrication, surgery | `02_interface/`, bonding/package | [people/defne](people/defne/) |
| Alae Messaoudi | `@alaaae` | Computation (decoder, encoder, recalibration) | `03_electronics/on-chip-ai/` | [people/alae](people/alae/) |
| Heliya Shakeri | `@HeliyaShakeri` | Electronics, power, wireless link | `03_electronics/`, power in `04_integration/` | [people/heliya](people/heliya/) |

## Map
```
00_admin/        guidelines, TA feedback, meetings, planning, team docs
01_application/  disease, target, state of the art, biology (LSE1)
02_interface/    electrodes, materials, geometry, fabrication, masks      (guidelines §1)
03_electronics/  recording, stimulation, on-chip AI                       (guidelines §2)
04_integration/  connection, package, power budget, failure points        (guidelines §3)
05_literature/   PDFs, one note per paper, references.bib
06_figures/      figure sources + exports
deliverables/    2-pager, presentation, report
people/<name>/   drafts (wip/) and work journal — not validated
```

## How to work here
1. `git pull` before you start.
2. Draft in `people/<you>/wip/`. When the team validates it → `/promote` into the right section.
3. Tick the checkboxes in the section README when an item is answered, with a link to the answer.
4. End of session: `/journal` (or write 3 lines in `people/<you>/journal.md`), `python3 tools/progress.py`, commit, push.

**With Claude Code**: open a terminal in this folder (or use claude.ai/code on this repo). Claude reads
[`CLAUDE.md`](CLAUDE.md) automatically. Commands: `/status`, `/meeting`, `/promote`, `/add-paper`, `/journal`.
**Without git**: GitHub Desktop, or drag and drop files on github.com into your `people/<you>/wip/` folder.
