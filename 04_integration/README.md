# 04 — Integration (guidelines §3)

**Owners:** Heliya (power, link) + Defne (bonding, package, surgery) — _to confirm_

Legend: `[x]` done · `[ ] 🟡` in progress · `[ ]` missing.

## Guideline questions
- [ ] 🟡 Electrical + mechanical connection interface ↔ electronics, and why it fits the electrode count → ACF vs flip-chip (C4); 8 ribbons merged (D-012)
- [x] Fully implanted or external electronics → fully implanted, Ti package, inductive link (D-011)
- [ ] 🟡 Failure points at the integration interface and mitigation → list in Defne's LSE2 docs (delamination, moisture at the bond, ribbon fatigue)
- [x] **Powering + power budget broken down per component** (incl. inductive link losses — TA) → table below; derivations in [`03_electronics/electronics_and_power.md`](../03_electronics/electronics_and_power.md#power-budget)

## TA feedback on this part
- [x] Where the receiving coil sits relative to the Ti package → D-011
- [ ] 🟡 **System block diagram with the data rate on each link and the power of each block** → numbers ready (table below, D-016, D-020); figure to draw
- [x] One package for M1 and S1, or two? → one skull-recessed Ti package for both chips (D-017; scope D-024)

## Power budget (fill here — single source)
Dissipated in the implant, all 192 M1 channels on (conservative reference). Derivation of every row:
[`03_electronics/electronics_and_power.md`](../03_electronics/electronics_and_power.md#power-budget).

| # | Block | Grasping (mW) | Worst case (mW) | Rest (mW) | Source |
|---|---|---|---|---|---|
| 1 | M1 recording front end + ADC, 192 ch (MiBMI) | 0.883 | 0.883 | 0.883 | Shaeri 2024 (measured) |
| 2 | NN decoder, 32 units: compute + weight memory | 0.016 | 0.016 | 0.005 | (calc) |
| 3 | LFP gate | 0.002 | 0.002 | 0.002 | (calc) |
| 4 | S1 recording, 64 ch (calibration only; 0.294 mW for minutes/day) | 0 | 0 | 0 | (calc) |
| 5 | Electrode mapping + pulse sequencer | 0.010 | 0.010 | 0.010 | (calc) + assumption |
| 6 | Stimulation delivered (8 / 64 sites at 100 / 300 Hz) | 0.051 | 1.229 | 0 | (calc) |
| 7 | Driver bias, 64 drivers | 0.353 | 0.353 | 0.353 | measured per driver × 2 margin |
| 8 | ASK demodulator + LSK modulator | 0.050 | 0.050 | 0.050 | measured + assumption |
| 9 | Safety monitors (POR, brownout, watchdog) | 0.005 | 0.005 | 0.005 | assumption |
| 10 | Low-voltage regulator loss, 1.2 → 1.0 V | 0.193 | 0.193 | 0.191 | (calc) |
| | **Circuit load** | **1.563** | **2.741** | **1.499** | sum |
| 11 | **Dissipated, load / η (η = 0.70 rectifier)** | **2.23** | **3.92** | **2.14** | (calc) |
| | **Daily mean (20 % grasping)** | | | **2.2** | ≤ 15 mW (D-014) |

With M1 channel selection (D-023): daily mean 0.9–1.2 mW. External headpiece: ~20 mW transmitted at
20 % coil efficiency, ~50 mW total, ~22 h on 300 mAh (estimate).
