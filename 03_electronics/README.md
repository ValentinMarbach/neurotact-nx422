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
- [ ] Compliance voltage from site impedance at 40 µA (TA)
- [ ] **TA:** safety limits in hardware, independent of the algorithm (max current, charge balance, link loss)

## On-chip intelligence (TA feedback)
- [ ] Define the NN concretely: inputs, outputs, size, update rate; ops/s and power → must fit the budget
- [ ] Map TouchSim (peripheral nerve) responses to cortical stimulation patterns; per-patient adaptation
- [ ] 🟡 Justify encoder on implant vs external (C6); recalibration = stronger argument
- [ ] Drift: which recorded signal detects it, how stimulation artifacts are handled (blanking?)
- [ ] Latency budget per block (*our choices* D8 table has empty cells)

## Key numbers
| Quantity | Value | Source |
|---|---|---|
| Implant power ceiling | 15 mW | D-014 |
| Current drivers | 64 | D-004 |
| Data across the skin | ~3 kb/s out + ~24 kb/s in | *our choices* D1 |
| MiBMI reference decoder | 883 µW, 192 ch, 2.46 mm² | *our choices* |
