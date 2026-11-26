# Decision log

One row per design choice. **Status**: `accepted` (team agreed) · `proposed` (on the table) ·
`superseded` (replaced, keep for history). Change an accepted decision only via PR/issue.
Sources: 2-pager (`deliverables/2-pager/`), *NeuroTact: our choices and why*
(`00_admin/team-docs/`), LSE1 docs (`01_application/lse1/`), Defne's LSE2 answers
(`people/defne/wip/2026-11-20_LSE2_meeting/`).

## Open conflicts — resolve first

| # | Topic | Version A | Version B | To settle by |
|---|---|---|---|---|
| C1 | Shank pitch / footprint | 400 µm, 8×8 → 2.8 × 2.8 mm (2-pager, Defne LSE2 answers 20.11) | 800 µm, 8×8 → 5.6 mm, covers thumb + index (Valentin, 12.11; matches "32 drivers per finger" in *our choices*) | team meeting — **left open for now** (26 Nov) |
| C2 | Is the motor BCI part of NeuroTact? | Yes: M1 Utah + M1 chip with LFP gate + NN decoder (*our choices*, Decisions 1–3, 7) | No: NeuroTact = S1 probe + electronics + package; motor BCI is an existing separate system (Defne LSE2 answers, Q1) | ✅ **resolved 2026-11-26 → D-024** (yes, the motor BCI is part of NeuroTact) |
| C4 | Ribbon-to-ASIC bonding | Flip-chip (2-pager) | ACF bonding (Defne LSE2) | Defne + Heliya |
| C5 | Stiffener and insertion | PEG over the whole shank except a bare 400 µm tip, stepwise insertion (Defne LSE2 answers, Q7) | Buckling calc says a stiffened section of ~50–70 µm is needed for a 4 mm shank; shorter shanks / shuttle as options (Defne LSE2 questions) | Defne |
| C6 | Who decodes / where the encoder runs | On the implant (*our choices*, Decision 1) | TA: justify why the encoder must be on the implant; recalibration is the stronger argument | ✅ **resolved 2026-11-25 → D-016** (touch analysis robot-side; S1 chip maps and times pulses; M1 decoder stays on the M1 chip) |
| C7 | Current cap and safety criterion | Cap 40 µA, safety via Shannon k = 0.81 < 1.85 (2-pager, D-005, Defne LSE2 Q4) | Hardware 0–100 µA, charge-based cap 10–12 nC/phase (~50–60 µA), 40 µA = site switch-over; Shannon out of domain, use ~4 nC/phase (Cogan 2016); 1.85 is from Cogan, not Shannon (LSE1 full explanations §3, §5) | Valentin + Defne + Heliya |
| C8 | Recalibration and S1 recording | Daily: test pulses with S1 recording, daily channel re-ranking and decoder retraining (Heliya, `03_electronics/electronics_and_power.md`; D-007) | One calibration session before first use, no S1 recording (Alae, computing draft, row 1) | team meeting — changes power row 4, channel selection (D-023) and D-007 |
| C9 | Blanking link between the two chips | S1 chip signals the M1 chip to blank 1 ms of M1 recording around each pulse (Heliya) | Chips never communicate; interference ignored (Alae, row 9) | team meeting — one wire inside the package; Alae's feature already skips blanked samples |
| C10 | S1 stimulator base chip | No base chip named; requires ±4 V monopolar, active charge neutralisation (< 10 nA), DC-blocking caps (Heliya, D-018) | Cheon et al. (JSTS 2025): single 5 V supply, 4.9 V compliance (≈ ±2.45 V monopolar), passive balancing, 0.75 nC residual (Alae, row 8) | Heliya + Alae — add HV output stages to Cheon, or pick a ±4 V chip |

## Decisions

| ID | Date | Decision | Why (short) | Status | Source |
|---|---|---|---|---|---|
| D-001 | 2026-10 | Target = S1 hand area: Brodmann area 1 (crown) + superficial area 3b (posterior bank) | 3b is the main cutaneous area and is out of reach of Utah arrays | accepted | 2-pager §1 |
| D-002 | 2026-10 | Ultraflexible polyimide (PI-2611) penetrating shanks, ~10 × 50 µm, up to 4 mm long | Softer than Si (2.4–3.2 vs 179 GPa) → less micromotion and scarring; long enough for 3b | accepted | 2-pager §3, Defne Q2 |
| D-003 | 2026-10 | Site coating SIROF (~300 nm) on Ti/Pt/Ti (20/200/20 nm); PEDOT:PSS as backup | CIC 1–5 mC/cm², used in human Utah ICMS | accepted | 2-pager §5 |
| D-004 | 2026-11 | 64 shanks × 4 sites = 256 sites, 1000 µm² each; 64 current drivers shared through a switch matrix | 4 depths per shank reach area 1 and 3b; ~166 sites still work at 35 % failure | accepted | Defne Q5, *our choices* D6 |
| D-005 | 2026-10 | Stimulation: cathodic-first biphasic, 200 µs/phase, target 30 µA, hardware cap 40 µA | 8 nC → 800 µC/cm², Shannon k = 0.81 < 1.85 | accepted | 2-pager §5, Defne Q4 — challenged by C7 |
| D-006 | 2026-11 | Biomimetic encoder: intensity = a·force + b·onset + c·release + d·slip, fitted on TouchSim, computed robot-side (D-016) | More natural, finer force with less charge (Greenspon 2023, Hobbs 2025) | proposed | *our choices* D4 — C6 resolved by D-016 |
| D-007 | 2026-11 | Recalibration on the S1 chip: evoked response tracked daily + occasional patient reports | Works without radio; claim = less manual tuning, more stable sensations (not longer life) | proposed | *our choices* D5, Defne Q2 |
| D-009 | 2026-11 | LFP power-threshold gate + shallow NN motor decoder on the M1 chip | Low power, accuracy first | proposed | *our choices* D2–3 — in scope since D-024 |
| D-010 | 2026-11 | Robot side bought: UR arm + PSYONIC Ability Hand; a robot-side computer runs the motor loop and the touch analysis, and talks to the implant through the external headpiece (no separate relay computer) | Already sold together, open API | proposed | *our choices* D7, updated by D-016 |
| D-011 | 2026-11 | Fully implanted titanium package; inductive link 13.56 MHz; receiving coil beside the package, outside the Ti case | Ti blocks the field (skin depth ~90 µm) | proposed | Defne Q3 |
| D-012 | 2026-11 | 8 separate combs of 8 shanks, ribbons merged before the ASIC | Curved cortex, avoid vessels, a failed insertion costs 8 shanks | proposed | Defne Q6 |
| D-013 | 2026-11 | PEG stiffener moulded after release, bonding and testing | PEG melts at ~60–80 °C, must follow hot steps | proposed | Defne Q7 — see C5 |
| D-014 | 2026-10 | Power budget ceiling 15 mW for the implant | Thermal limit ΔT < 1 °C | accepted | *our choices* D1 |
| D-015 | 2026-11 | Target population: intracortical motor-BCI users, cervical SCI (C4–C6) first; amputees without usable nerve as sub-case; implant early after injury | 0 amputees among implanted humans; amputees have EMG + nerve interfaces; S1 hand map blurs after SCI (Kikkert 2021) | accepted | LSE1 full explanations §1, §6 ("Group decision"); Defne Q1 |
| D-016 | 2026-11-25 | **Touch analysis on the robot side.** A small computer beside the robot (not the UR control box: ur_rtde runs on an external computer) computes zone pressures, onset/release, slip, stiffness and the biomimetic intensity, and sends one 64-bit packet of 6 zone intensities every 5 ms (~13 kb/s) through the headpiece. The S1 chip only checks the packet, scales per site (threshold/max table in NVM), caps at 40 µA and times the pulses. M1 decoder stays on the M1 chip. | Retunable without surgery; ~13 vs 36 kb/s and 0.6 vs 1.7 ms airtime; simpler implant chip; grip reflex without implant round trip; same robustness (no link = no touch data anyway). Not chosen for chip load (< 0.1 µW either way). | accepted | Team decision 25 Nov; `03_electronics/electronics_and_power.md`; Alae's computing draft agrees — resolves C6, supersedes D-008 |
| D-017 | 2026-11 | M1 recording: two 96-ch Pt Utah arrays, MiBMI front end unchanged (192 ch, 883 µW, 65 nm; two chips, ~8 mm² total, 2.46 mm² BMI chipset); S1 chip in 0.18 µm HV CMOS; both chips in one Ti package | Measured power and area; HV process needed for ±4 V | proposed | Heliya — in scope since D-024 |
| D-018 | 2026-11 | Stimulator: 64 current-steering drivers, ±4 V compliance (40 µA × 50 kΩ + 1.5 V + 0.5 V; to revisit for chronic 70–140 kΩ access resistance, see C7), 256→64 switch matrix, **monopolar** return to a large Pt electrode on the package, 100 nF DC-blocking cap per driver | Charge set independent of impedance; single-fault DC protection (ISO 14708-3) | proposed | Heliya |
| D-019 | 2026-11 | Hardware safety independent of software: 40 µA cap, brownout/POR disables drivers, ramp to zero after 15 ms without a valid packet, CRC check before firing, on-chip impedance check (end-of-phase voltage via one shared ADC, no recording front end needed) | TA request | proposed | Heliya |
| D-020 | 2026-11 | Link: 13.56 MHz inductive, ASK down ~106 kb/s, LSK up ≥ 100 kb/s raw, half-duplex (0.6 ms down per 5 ms frame); calibration mode streams 192 features at ~80 kb/s up with touch paused; decoder weights reloaded from the headpiece at power-up (~8.3 s, ~4.2 s at 96 ch) | Airtime, not average traffic, sets latency | proposed | Heliya |
| D-021 | 2026-11 | Supply: dual-output rectifier (±4 V for drivers; 1.2 V → LDO → 1.0 V for logic), η = 0.70; regulator loss budgeted | Avoids a 4 V → 1 V linear drop (~25 % efficient) | proposed | Heliya |
| D-022 | 2026-11 | 5 ms encoder frame; touch loop ~5–20 ms in the electronics, motor loop ~26 ms | Frames, not the radio, set the delay | proposed | Heliya, Alae |
| D-023 | 2026-11 | M1 channel selection: 16 channels at rest for the LFP gate; top 96 channels (re-ranked at daily calibration) while grasping; per-channel power gating + fast-reset amplifiers | TA suggestion; daily mean 2.2 → 0.9–1.2 mW. Decoding accuracy at 96 vs 192 ch still to test (Alae) | proposed | Heliya, Alae |
| D-024 | 2026-11-26 | **Scope:** the motor BCI is part of NeuroTact — two M1 Utah arrays, the M1 chip (LFP gate + decoder) and the robot side, together with the S1 touch implant, in one system | Closed loop: decoded movement out, touch back in; answers the TA's scope question | accepted | Team decision, relayed by Heliya 26 Nov — resolves C2 |

## History of superseded decisions
| D-008 | 2026-11 | Everything on the implant (scenario C), ~27 kb/s across the skin | Least data and radio hops | superseded by D-016 (2026-11-25) | *our choices* D1 — depends on C2 |
