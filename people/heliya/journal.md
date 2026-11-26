# Journal — Heliya Shakeri

Newest entry on top. Format: `## YYYY-MM-DD` then done / next / blocked.

## 2026-11-26
**Done:** Electronics and power document finished and added to `03_electronics/electronics_and_power.md` (+ PDF).
Covers electrodes, stimulator (monopolar, DC-blocking caps), hardware safety and supply (dual-output rectifier),
13.56 MHz link, robot-side touch path, package, full power budget (2.2 / 3.9 / 2.1 mW), M1 channel selection
(TA request, 0.9–1.2 mW daily mean), latency (motor ~26 ms, touch ~5–20 ms), risks, open values.
Filled the power table in `04_integration/README.md`. DECISIONS: C6 resolved → D-016 (robot-side touch analysis,
accepted), D-008 superseded, electronics decisions D-017–D-023 proposed.
**Next:** recording-chain items (amplitude/bandwidth, sampling rate, ADC block diagram); stimulator and system block
diagrams; check decoding at 96 vs 192 channels with Alae; confirm robot-side computer (UR box or PC).
**Blocked by:** C2 (is the motor BCI in scope?) — the whole M1 part of the budget depends on it.
**Later the same day:** aligned the document with Alae's computing draft and Defne's interface PDF:
robot-side program on a small computer beside the robot (not the UR control box), calibration stream
(~80 kb/s up, touch paused) added to the link, impedance check via end-of-phase voltage + shared ADC,
linear decoder first / network as upper bound, one hand-opening output, PSYONIC rate >= 200 Hz needed,
MiBMI = two chips ~8 mm2 (2.46 mm2 chipset), base-chip compliance issue written up. Added open
conflicts C8 (recalibration), C9 (blanking line), C10 (stimulator base chip) to DECISIONS.md.
**Decisions 26 Nov:** C2 resolved (motor BCI in scope, D-024), C3 resolved (tetraplegia, D-015), C1 (pitch) left open. No longer blocked by C2.
