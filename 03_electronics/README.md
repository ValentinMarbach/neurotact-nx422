# 03 — Electronics: recording, stimulation, on-chip processing (guidelines §2)

**Owners:** Heliya (circuits, power — EE) · Alae (on-chip AI, decoder/encoder, latency — CS) — _to confirm_
**Subfolders:** `recording/` · `stimulation/` · `on-chip-ai/`

**Main document (Heliya):** [`electronics_and_power.md`](electronics_and_power.md) — electrodes, stimulator,
safety and supply, wireless link, touch path, package, power budget, M1 channel selection, latency, risks.
PDF export: [`NeuroTact_Electronics_and_Power.pdf`](NeuroTact_Electronics_and_Power.pdf).
Computing side (Alae, draft): [`people/alae/NeuroTact_Computing_and_Signal_Processing.pdf`](../people/alae/NeuroTact_Computing_and_Signal_Processing.pdf).

⚠️ TA: *"since your device both records and stimulates, you must also address the recording part"*.

Legend: `[x]` done · `[ ] 🟡` in progress · `[ ]` missing.

## Recording (guidelines)
- [ ] Expected amplitude range and bandwidth (LFP, spikes, evoked responses) → gain and filter design
- [ ] DC offset and electrode drift in the design
- [ ] Sampling rate, derived from bandwidth and required SNR
- [x] On-device processing vs raw transmission; **data rate at each stage** → decoding on the M1 chip, ~3 kb/s out; touch analysed robot-side, ~13 kb/s in (one 64-bit packet / 5 ms); 80 kb/s up only during calibration (Alae) — [link section](electronics_and_power.md#wireless-power-and-data-link), D-016
- [x] Number of simultaneous channels and trade-offs (power, area, multiplexing) → 192 M1 ch (MiBMI front end, 883 µW, 2.46 mm²); 64 S1 recording ch for calibration only; M1 channel selection 16 at rest / top 96 while grasping — [channel selection](electronics_and_power.md#channel-selection-on-m1), D-023
- [ ] 🟡 Filter + ADC architecture (block diagram) and front-end trade-offs → MiBMI kept as is (Alae: 24 front ends × 8 ch, 10-bit SAR ADC each); block diagram and our own justification still to write

## Stimulation (guidelines)
- [x] Pulse parameters (amplitude, width, frequency, biphasic, timing) → D-005, 2-pager §2
- [x] Current vs voltage control and why → current-steering drivers, charge set independently of impedance — [stimulator](electronics_and_power.md#stimulator)
- [ ] 🟡 Stimulator circuit architecture (block diagram): 64 drivers + switch matrix to 256 sites → described in text (monopolar, DC-blocking caps, switch matrix); diagram missing
- [ ] 🟡 Compliance voltage from site impedance at 40 µA (TA) → current design ±4 V = 40 µA × 50 kΩ + 1.5 V + 0.5 V (fresh implant) — [stimulator](electronics_and_power.md#stimulator). To revisit: tissue access resistance 70–140 kΩ for a chronic site (LSE1 estimate, Defne) → ±7.6 V at 40 µA, ≥ ±12 V at 100 µA (`01_application/lse1/LSE1_Decisions_Full_Explanations_EN.pdf` §3) — depends on C7
- [x] **TA:** safety limits in hardware, independent of the algorithm (max current, charge balance, link loss) → 40 µA cap, DC-blocking caps, brownout off, 15 ms link-loss ramp, CRC before firing, impedance check — [safety and supply](electronics_and_power.md#safety-and-supply), D-019. LSE1 proposes a charge-based cap instead (10–12 nC/phase, 20 nC absolute, disable site if E_mc < −0.6 V; LSE1 full explanations §5) — C7

## On-chip intelligence (TA feedback)
- [ ] 🟡 Define the NN concretely: inputs, outputs, size, update rate; ops/s and power → Alae draft: ridge regression baseline (768 weights, < 0.1 µW); 32-unit network option (~110 k weights, 0.016 mW, budgeted)
- [ ] 🟡 Map TouchSim (peripheral nerve) responses to cortical stimulation patterns; per-patient adaptation → I = a·F + b·onset + c·release + d·slip, a–d per finger, threshold + max per site — [tactile section](electronics_and_power.md#tactile-features-measure-analyze-encode)
- [x] Justify encoder on implant vs external (C6) → resolved: touch analysis robot-side, S1 chip only maps and times pulses — D-016
- [ ] 🟡 Drift: which recorded signal detects it, how stimulation artifacts are handled (blanking?) → physiology: evoked response on neighbouring sites 2–5 ms after the pulse, ~2 ms blanking (LSE1 full explanations §2); electronics: 1 ms blanking of M1 around each pulse proposed; daily vs one-time calibration open — C8, C9
- [x] Latency budget per block → motor ~26 ms, touch ~5–20 ms (5 ms frame) — [latency](electronics_and_power.md#latency-budget)

## Key numbers
| Quantity | Value | Source |
|---|---|---|
| Implant power ceiling | 15 mW | D-014 |
| Implant dissipation | 2.2 mW grasping · 3.9 mW worst · 2.1 mW rest · 2.2 mW daily mean | (calc) [power budget](electronics_and_power.md#power-budget) |
| With M1 channel selection | 0.9–1.2 mW daily mean | (calc) D-023 |
| Current drivers | 64, ±4 V compliance, 40 µA cap | D-004, D-005 |
| Data across the skin | ~3 kb/s out + ~13 kb/s in (raw ≥ 100 kb/s each way) | D-016, D-020 |
| MiBMI reference front end | 883 µW, 192 ch; two chips, ~8 mm² total (2.46 mm² BMI chipset) | Shaeri 2024; EPFL news 2024 |
| Latency (electronics) | motor ~26 ms · touch ~5–20 ms | (calc) |
