# 02 — Implantable interface (guidelines §1)

**Owner:** Defne (materials, fabrication, surgery / LSE2) — _to confirm_
**Subfolders:** `calculs/` (charge density, buckling, impedance…) · `fabrication/` (process flow) · `masks/` (layout per step)

Legend: `[x]` done · `[ ] 🟡` in progress · `[ ]` missing.

## Guideline questions
- [x] Anatomical target and why → D-001
- [x] Electrode type and why this geometry fits → D-002 (penetrating flexible shanks), D-012 (combs)
- [x] Substrate / insulation material → PI-2611, 2 × 5 µm (D-002)
- [ ] 🟡 Electrode surface material and its effect on biocompatibility, CIC, **impedance** → SIROF (D-003); impedance value at 1 kHz still missing
- [ ] 🟡 Number of electrodes, geometry, dimensions, **spacing** → 256 sites (D-004); pitch blocked by conflict C1
- [x] Stimulation amplitude and feasibility with the chosen electrode → D-005 (30/40 µA, k = 0.81); human vs mouse thresholds addressed (Defne Q4)
- [ ] 🟡 Fabrication process flow: steps, **tools/machines per step**, thickness of each layer → layer table in Defne's LSE2 answers; tools per step missing
- [ ] **Device dimensions + mask layout: top-down view of each fabrication step** → `masks/` empty

## TA feedback on this part
- [ ] 🟡 Are the 8 × 8 shanks connected or inserted separately → D-012 (proposed)
- [ ] 🟡 How and when the stiffener is attached → D-013 (proposed), buckling issue C5
- [ ] 🟡 Own diagram of device layers and dimensions (not Fig. 1 of a paper) → draft in `people/defne/wip/`
- [x] Translate mouse thresholds to humans, current range → Defne Q4 (compliance voltage → 03)

## Key numbers (single source; update here)
| Quantity | Value | Source |
|---|---|---|
| Shank cross-section | 10 × 50 µm | D-002 |
| Shank length | up to 4 mm | D-002 |
| Sites | 64 shanks × 4 = 256, 1000 µm² each | D-004 |
| Pitch / footprint | **400 µm / 2.8 mm or 800 µm / 5.6 mm — C1** | DECISIONS |
| Layers | Al 100 nm (sacrificial) / PI 5 µm / Ti-Pt-Ti 20-200-20 nm / PI 5 µm / SIROF ~300 nm | Defne LSE2 |
| Charge per phase at cap | 8 nC → 800 µC/cm², k = 0.81 | D-005 |
| Critical buckling load, bare shank | 1 mN up to ~485 µm free length | Defne LSE2 (calc) |

## Open questions
- Traces for 4 sites on a 50 µm shank: only ~7 µm per side → wider shanks, elongated sites, or 2nd metal layer?
- Galvanic corrosion of Pt/SIROF during anodic Al release.
