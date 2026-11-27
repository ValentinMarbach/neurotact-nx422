# LSE1 v2 (27 Nov 2026) — draft, not validated

Update of `01_application/lse1/LSE1_Decisions_{QA,Full_Explanations}_EN.pdf` (v1, 12 Nov) to the team
decisions of 27 Nov 2026. Source = `build_lse1_v2.py`; the PDFs are exports.

## What changed since v1
- **Motor side inside NeuroTact** (2 Utah arrays in M1 + M1 chip, linear decoder first); v1 called it a companion system.
- **Recalibration** = daily on-chip self-check (electrode side) + weekly threshold staircase answered through the motor BCI.
  No recording in S1, so evoked responses and the ~2 ms blanking move to "next step".
- **Artefact on M1**: filtering only, blanking as fallback (team decision; check = follow-up F5).
- **No fixed 30 µA target** (R4): per site, threshold → min(threshold + ~4 JND, cap).
- **Current cap (C7)**: LSE1 proposal unchanged (0–100 µA + 10–12 nC/phase); new compromise 0–60 µA / ~±8 V.
- **Pitch (C1)**: LSE1 recommends 800 µm (5.6 mm, thumb + index); site groups = 4 depth sites of one shank.
- New caveat: a weekly staircase does not track the > 10 µA day-to-day variation (Hughes 2021).
- Section 7 now lists sentences to correct in all team documents (S6, 2-pager, D-005, Defne's LSE2 answers, LSE1 v1).

## Calculations (calc)
- Finger spacing: 15.5 mm (D1→D5, Martuzzi 2014) / 4 intervals ≈ 3.9 mm.
- Footprint: 7 × 800 µm = 5.6 mm; 7 × 400 µm = 2.8 mm.
- Activated radius r = √(I/k), k = 1292 µA/mm² (Stoney 1968): 40 µA → 0.176 mm; 60 µA → 0.215 mm.
- Compliance: 60 µA × 140 kΩ = 8.4 V → ~±8 V; 100 µA × 70–140 kΩ = 7–14 V → ±12 V.
- Charge: Q = I × 200 µs: 60 µA → 12 nC; D = 12 nC / 10⁻⁵ cm² = 1.2 mC/cm²; k = log 1200 + log 0.012 = 3.08 − 1.92 = 1.16.
- Staircase time (assumptions: 20 trials/site, 2 s/trial): 40 s/site → 64 sites ≈ 43 min; 256 sites ≈ 2.8 h.

## To validate with
- Alae / Heliya: content of the daily self-check, staircase design and duration.
- Whole team: C1 (pitch) and C7 (current range) before the slides are frozen.
