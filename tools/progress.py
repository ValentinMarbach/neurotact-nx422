#!/usr/bin/env python3
"""Count checklist items in each section README and write the progress table
into STATUS.md and README.md (between <!-- PROGRESS:START --> / <!-- PROGRESS:END -->).
Legend in the READMEs:  - [x] done   - [ ] 🟡 in progress   - [ ] missing
Run from anywhere:  python3 tools/progress.py
"""
import re, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECTIONS = [
    ("01 Application & state of the art", "01_application/README.md"),
    ("02 Implantable interface (§1)", "02_interface/README.md"),
    ("03 Electronics (§2)", "03_electronics/README.md"),
    ("04 Integration (§3)", "04_integration/README.md"),
    ("06 Figures", "06_figures/README.md"),
]
BOX = re.compile(r"^\s*-\s\[( |x|X)\]\s*(.*)$")

def owner(text):
    m = re.search(r"\*\*Owners?:\*\*\s*(.+)", text)
    return re.sub(r"\s*—\s*_to confirm_", "", m.group(1)).strip() if m else "?"

def bar(done, wip, total, width=12):
    if not total:
        return ""
    d = round(width * done / total); w = round(width * wip / total)
    return "█" * d + "▒" * w + "·" * max(0, width - d - w)

rows, tot = [], [0, 0, 0]
for name, rel in SECTIONS:
    text = (ROOT / rel).read_text(encoding="utf-8")
    done = wip = todo = 0
    for line in text.splitlines():
        m = BOX.match(line)
        if not m:
            continue
        if m.group(1).lower() == "x":
            done += 1
        elif "🟡" in m.group(2):
            wip += 1
        else:
            todo += 1
    n = done + wip + todo
    tot = [tot[0] + done, tot[1] + wip, tot[2] + todo]
    icon = "🟢" if n and done == n else ("🔴" if todo > n / 2 else "🟡")
    rows.append(f"| {icon} [{name}]({rel}) | `{bar(done, wip, n)}` | {done}/{n} | {wip} | {todo} | {owner(text)} |")

n = sum(tot)
table = "\n".join([
    f"_Updated {datetime.date.today().isoformat()} by `tools/progress.py` — █ done ▒ in progress · missing_",
    "",
    "| Section | Progress | Done | In progress | Missing | Owner |",
    "|---|---|---|---|---|---|",
    *rows,
    f"| **Total** | `{bar(tot[0], tot[1], n)}` | **{tot[0]}/{n}** | {tot[1]} | {tot[2]} | |",
])

for f in ("STATUS.md", "README.md"):
    p = ROOT / f
    s = p.read_text(encoding="utf-8")
    s2 = re.sub(r"(<!-- PROGRESS:START -->).*?(<!-- PROGRESS:END -->)",
                lambda m: f"{m.group(1)}\n{table}\n{m.group(2)}", s, flags=re.S)
    p.write_text(s2, encoding="utf-8")
print(table)
