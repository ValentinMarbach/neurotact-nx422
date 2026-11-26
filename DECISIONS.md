# Decision log

One row per design choice. **Status**: `accepted` (team agreed) · `proposed` (on the table) ·
`superseded` (replaced, keep for history). Change an accepted decision only via PR/issue.
Sources: 2-pager (`deliverables/2-pager/`), *NeuroTact: our choices and why*
(`00_admin/team-docs/`), LSE1 docs (`01_application/lse1/`), Defne's LSE2 answers
(`people/defne/wip/2026-11-20_LSE2_meeting/`).

## Open conflicts — resolve first

| # | Topic | Version A | Version B | To settle by |
|---|---|---|---|---|
| C1 | Shank pitch / footprint | 400 µm, 8×8 → 2.8 × 2.8 mm (2-pager, Defne LSE2 answers 20.11) | 800 µm, 8×8 → 5.6 mm, covers thumb + index (Valentin, 12.11; matches "32 drivers per finger" in *our choices*) | team meeting |
| C2 | Is the motor BCI part of NeuroTact? | Yes: M1 Utah + M1 chip with LFP gate + NN decoder (*our choices*, Decisions 1–3, 7) | No: NeuroTact = S1 probe + electronics + package; motor BCI is a companion system (LSE1 full explanations §1/§6, Defne LSE2 answers Q1) | confirm with Alae: only *our choices* puts the decoder in NeuroTact |
| C4 | Ribbon-to-ASIC bonding | Flip-chip (2-pager) | ACF bonding (Defne LSE2) | Defne + Heliya |
| C5 | Stiffener and insertion | PEG over the whole shank except a bare 400 µm tip, stepwise insertion (Defne LSE2 answers, Q7) | Buckling calc says a stiffened section of ~50–70 µm is needed for a 4 mm shank; shorter shanks / shuttle as options (Defne LSE2 questions) | Defne |
| C7 | Current cap and safety criterion | Cap 40 µA, safety via Shannon k = 0.81 < 1.85 (2-pager, D-005, Defne LSE2 Q4) | Hardware 0–100 µA, charge-based cap 10–12 nC/phase (~50–60 µA), 40 µA = site switch-over; Shannon out of domain, use ~4 nC/phase (Cogan 2016); 1.85 is from Cogan, not Shannon (LSE1 full explanations §3, §5) | Valentin + Defne + Heliya |
| C6 | Who decodes / where the encoder runs | On the implant (*our choices*, Decision 1) | TA: justify why the encoder must be on the implant; recalibration is the stronger argument | Alae + Heliya |

## Decisions

| ID | Date | Decision | Why (short) | Status | Source |
|---|---|---|---|---|---|
| D-001 | 2026-10 | Target = S1 hand area: Brodmann area 1 (crown) + superficial area 3b (posterior bank) | 3b is the main cutaneous area and is out of reach of Utah arrays | accepted | 2-pager §1 |
| D-002 | 2026-10 | Ultraflexible polyimide (PI-2611) penetrating shanks, ~10 × 50 µm, up to 4 mm long | Softer than Si (2.4–3.2 vs 179 GPa) → less micromotion and scarring; long enough for 3b | accepted | 2-pager §3, Defne Q2 |
| D-003 | 2026-10 | Site coating SIROF (~300 nm) on Ti/Pt/Ti (20/200/20 nm); PEDOT:PSS as backup | CIC 1–5 mC/cm², used in human Utah ICMS | accepted | 2-pager §5 |
| D-004 | 2026-11 | 64 shanks × 4 sites = 256 sites, 1000 µm² each; 64 current drivers shared through a switch matrix | 4 depths per shank reach area 1 and 3b; ~166 sites still work at 35 % failure | accepted | Defne Q5, *our choices* D6 |
| D-005 | 2026-10 | Stimulation: cathodic-first biphasic, 200 µs/phase, target 30 µA, hardware cap 40 µA | 8 nC → 800 µC/cm², Shannon k = 0.81 < 1.85 | accepted | 2-pager §5, Defne Q4 — challenged by C7 |
| D-006 | 2026-11 | Biomimetic encoder: intensity = a·force + b·onset + c·release, fitted on TouchSim | More natural, finer force with less charge (Greenspon 2023, Hobbs 2025) | proposed | *our choices* D4 — see C6 |
| D-007 | 2026-11 | Recalibration on the S1 chip: evoked response tracked daily + occasional patient reports | Works without radio; claim = less manual tuning, more stable sensations (not longer life) | proposed | *our choices* D5, Defne Q2 |
| D-008 | 2026-11 | Everything on the implant (scenario C), ~27 kb/s across the skin | Least data and radio hops | proposed | *our choices* D1 — depends on C2 |
| D-009 | 2026-11 | LFP power-threshold gate + shallow NN motor decoder on the M1 chip | Low power, accuracy first | proposed | *our choices* D2–3 — depends on C2 |
| D-010 | 2026-11 | Robot side bought: UR arm + PSYONIC Ability Hand, relay computer outside the body | Already sold together, open API | proposed | *our choices* D7 |
| D-011 | 2026-11 | Fully implanted titanium package; inductive link 13.56 MHz; receiving coil beside the package, outside the Ti case | Ti blocks the field (skin depth ~90 µm) | proposed | Defne Q3 |
| D-012 | 2026-11 | 8 separate combs of 8 shanks, ribbons merged before the ASIC | Curved cortex, avoid vessels, a failed insertion costs 8 shanks | proposed | Defne Q6 |
| D-013 | 2026-11 | PEG stiffener moulded after release, bonding and testing | PEG melts at ~60–80 °C, must follow hot steps | proposed | Defne Q7 — see C5 |
| D-015 | 2026-11 | Target population: intracortical motor-BCI users, cervical SCI (C4–C6) first; amputees without usable nerve as sub-case; implant early after injury | 0 amputees among implanted humans; amputees have EMG + nerve interfaces; S1 hand map blurs after SCI (Kikkert 2021) | accepted | LSE1 full explanations §1, §6 ("Group decision"); Defne Q1 |
| D-014 | 2026-10 | Power budget ceiling 15 mW for the implant | Thermal limit ΔT < 1 °C | accepted | *our choices* D1 |

## History of superseded decisions
_(none yet)_
