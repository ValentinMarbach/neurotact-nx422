# 03 — Electronics: recording, stimulation, on-chip processing (guidelines §2)

**Owners:** Heliya (circuits, power — EE) · Alae (on-chip AI, decoder/encoder, latency — CS) — _to confirm_
**Subfolders:** `recording/` · `stimulation/` · `on-chip-ai/`

⚠️ TA: *"since your device both records and stimulates, you must also address the recording part"*.

Legend: `[x]` done · `[ ] 🟡` in progress · `[ ]` missing.

## Recording (guidelines)
- [ ] Expected amplitude range and bandwidth (LFP, spikes, evoked responses) → gain and filter design
- [ ] DC offset and electrode drift in the design
- [ ] Sampling rate, derived from bandwidth and required SNR
- [ ] 🟡 On-device processing vs raw transmission; **data rate at each stage** → ~27 kb/s total in *our choices* D1, per-stage numbers missing
- [ ] 🟡 Number of simultaneous channels and trade-offs (power, area, multiplexing)
- [ ] Filter + ADC architecture (block diagram) and front-end trade-offs

## Stimulation (guidelines)
- [x] Pulse parameters (amplitude, width, frequency, biphasic, timing) → D-005, 2-pager §2
- [ ] 🟡 Current vs voltage control and why → current drivers stated, justification to write
- [ ] Stimulator circuit architecture (block diagram): 64 drivers + switch matrix to 256 sites
- [ ] 🟡 Compliance voltage → LSE1 estimate ≥ ±12 V (70–140 kΩ access, 7–14 V at 100 µA), `01_application/lse1/LSE1_Decisions_Full_Explanations_EN.pdf` §3; EE to confirm
- [ ] 🟡 **TA:** safety limits in hardware → LSE1 proposal: charge cap 10–12 nC/phase per site, 20 nC absolute, duty cycle, disable site if E_mc < −0.6 V (`01_application/lse1/LSE1_Decisions_Full_Explanations_EN.pdf` §5); link loss + EE implementation missing — see C7

## On-chip intelligence (TA feedback)
- [ ] Define the NN concretely: inputs, outputs, size, update rate; ops/s and power → must fit the budget
- [ ] Map TouchSim (peripheral nerve) responses to cortical stimulation patterns; per-patient adaptation
- [ ] 🟡 Justify encoder on implant vs external (C6); recalibration = stronger argument
- [ ] 🟡 Drift: physiology + detection signal (evoked response on neighbouring sites, 2–5 ms after pulse, ~2 ms blanking) → `01_application/lse1/LSE1_Decisions_Full_Explanations_EN.pdf` §2; algorithm/circuit side missing
- [ ] Latency budget per block (*our choices* D8 table has empty cells)

## Key numbers
| Quantity | Value | Source |
|---|---|---|
| Implant power ceiling | 15 mW | D-014 |
| Current drivers | 64 | D-004 |
| Data across the skin | ~3 kb/s out + ~24 kb/s in | *our choices* D1 |
| MiBMI reference decoder | 883 µW, 192 ch, 2.46 mm² | *our choices* |
