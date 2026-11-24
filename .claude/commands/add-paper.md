---
description: File a paper, write its note and its BibTeX entry
argument-hint: <path to PDF, DOI or URL>
---
Paper: $ARGUMENTS
1. Find the full reference (authors, year, title, journal, DOI). Key = `firstauthorYEAR` (add a/b if taken).
2. Check `05_literature/references.bib` and `05_literature/notes/` for a duplicate first.
3. Put the PDF in the best-matching `05_literature/` subfolder as `Author YEAR - Short title.pdf`.
4. Append the BibTeX entry to `05_literature/references.bib`.
5. Write `05_literature/notes/<key>.md` from `notes/_TEMPLATE.md`: key numbers with units and figure/page,
   what it supports in NeuroTact (decision IDs), limits (species, n, duration).
6. Commit `[05] add <key>`.
