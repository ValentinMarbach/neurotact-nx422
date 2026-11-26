# NeuroTact — Electronics and Power: Design Choices and Budgets

Heliya Shakeri · last updated 26 Nov 2026 · PDF export: [`NeuroTact_Electronics_and_Power.pdf`](NeuroTact_Electronics_and_Power.pdf)

## Summary

The NeuroTact electronics dissipate an estimated 2.2 mW while grasping, 3.9 mW in the worst case and 2.1 mW at rest. That is about a quarter of the 15 mW ceiling we set to keep tissue heating below 1 °C. NeuroTact is for people with tetraplegia after cervical spinal cord injury: it decodes movement from M1 to drive a robot arm and hand, and restores touch through S1. The design records from two platinum Utah arrays in M1 and stimulates through a 256-site SIROF polyimide array in S1, driven monopolarly by 64 current sources at ±4 V compliance behind DC-blocking capacitors. Both chips sit in one skull-recessed titanium package; the receiving coil lies beside it, and a single 13.56 MHz inductive link carries power and data. Touch features are computed on the robot side and sent in as one small packet every 5 ms, so the electronic part of the touch loop takes about 5–20 ms.

This section covers the electrodes, stimulator, wireless link, package and the power and latency budgets. Every number is either measured in a cited study or estimated, with the assumption stated.

## Electrodes

We record M1 with two 96-channel Utah arrays with platinum tips, giving 192 recording channels. This matches the 192-channel recording front end of the [MiBMI chipset](https://x-mol.com/paper/1827401830204252160). Platinum is enough because M1 only records. In the longest human bidirectional implant, the stimulated S1 arrays had SIROF tips and the motor arrays had non-stimulated platinum tips ([Hughes et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8500669)).

We stimulate S1 through our polyimide array: 64 shanks with 4 SIROF sites each, 256 sites of about 1000 µm² (A = 10⁻⁵ cm²). At the hardware current cap of 40 µA and 200 µs per phase, the charge per phase and the charge density are:

*Q* = *I* · *t* = 40 µA × 200 µs = 8 nC = 0.008 µC  ·  *D* = *Q* / *A* = 800 µC/cm²  ·  *k* = log₁₀ *D* \[µC/cm²\] + log₁₀ *Q* \[µC\] = 2.903 − 2.097 = 0.81 < 1.85

The safety margin depends on the coating's real charge-injection capacity. SIROF on polyimide injects 1–9 mC/cm² depending on pulse width and area ([Cogan et al., 2009](https://www.pubmed.gov/18837458/)). So 0.8 mC/cm² is safe, but only 1.25× below the bottom of that range. Flexible polyimide shanks with SIROF plus PEDOT:PSS were pulsed at 2.3 mC/cm² (75 % of their maximum) for over 10 billion pulses with barely any change in impedance ([Chalmers flexible-shank study](https://research.chalmers.se/publication/540345/file/540345_Fulltext.pdf)). We therefore keep the 40 µA cap in hardware and keep PEDOT:PSS over SIROF as the fallback coating.

Shannon's limit was derived for large electrodes. For microelectrodes, McCreery and colleagues showed that charge per phase also matters, and some of their limits sit below our 8 nC. Human S1 trials, however, have stimulated at up to 100 µA × 200 µs = 20 nC per phase for years ([Hughes et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8500669)), so 8 nC is well inside clinical experience.

For the stimulator design we take a site impedance of 50 kΩ at 1 kHz. Those same flexible shanks measured 46.5 kΩ at 1 kHz on 15 × 15 µm sites. Our sites are about 4× larger, so 50 kΩ is a conservative upper value. It should be replaced by a measurement on our own sites.

## Stimulator

The S1 chip has 64 independent current-steering drivers, routed to the 256 sites through a 256-to-64 switch matrix, with ±4 V compliance. Pulses are cathodic-first and charge-balanced, at most 40 µA and 300 Hz. These limits are below the 100 µA and 300 Hz used safely in human S1 for years ([Pittsburgh ICMS adaptation study](https://pmc.ncbi.nlm.nih.gov/articles/PMC10308851)). Active charge-neutralization switches keep residual DC below 10 nA. Stimulation is monopolar: each site returns its current through a large platinum return electrode on the package, so only one site impedance appears in the compliance budget below. Bipolar stimulation between two sites would double the resistive drop.

**Base chip.** We have not yet named a published stimulator to build the S1 chip from. The candidate in the computing part, the 64-channel IC of Cheon et al. (JSTS 2025), runs from a single 5 V supply with 4.9 V compliance and passive charge balancing (0.75 nC residual per pulse). With a monopolar return at mid-supply, that gives about ±2.45 V, short of our ±4 V, and the residual is about 9 % of an 8 nC phase. It could serve as the base only with higher-voltage output stages (±4 V rails) and active charge neutralization added; otherwise we need a base chip that already meets ±4 V.

The compliance voltage has to cover three things: the drop across the site, the electrode polarization, and the driver's own headroom. For polarization we use 1.5 V, because the Pittsburgh team disabled any electrode whose interphase voltage went below −1.5 V ([Hughes et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8500669)).

*V*comp = *I*max · *Z*site + *V*pol + *V*head = 40 µA × 50 kΩ + 1.5 V + 0.5 V = 4 V

The supply delivers both phases of every pulse, so each biphasic pulse costs E = V·(2Q) = 4 V × 16 nC = 64 nJ. The stimulation power is that energy times the pulse rate, summed over active drivers:

*P*stim = *N*active · *V*comp · 2*Q* · *f*

| Case | Active sites | Rate (Hz) | Stimulation power (mW) |
| --- | --- | --- | --- |
| Typical pinch: 2 fingers × groups of 4 | 8 | 100 | 0.05 |
| Strong grasp | 8 | 300 | 0.15 |
| Worst case: all 64 drivers | 64 | 300 | 1.23 |

Stimulation power is small, even in the worst case. The real unknown is site impedance. If our sites measure 200 kΩ instead of 50 kΩ, the compliance needs to be about ±10 V and every row above grows by about 2.5×. That is still under 3.1 mW in the worst case.

### Safety and supply

**Single-fault DC protection.** Charge neutralization handles normal operation but not a failed part. Implantable stimulator standards expect that a single fault, such as a driver transistor shorted to a rail, does not drive DC into tissue. We therefore put a 100 nF ceramic DC-blocking capacitor in series with each of the 64 drivers, inside the titanium package, between the driver and the switch matrix. One 8 nC phase charges it by only 8 nC / 100 nF = 80 mV. Placing the capacitors on the driver side needs 64 parts instead of 256. The remaining risk is a switch in the matrix failing towards a rail, which 256 capacitors on the site side would also cover, at four times the board space.

**Supply rails.** The receiver is a dual-output rectifier. One output gives the ±4 V rails for the drivers directly. The other gives about 1.2 V, which a low-dropout regulator brings down to the 1.0 V used by the low-voltage circuits. Stepping 4 V down to 1.0 V with a linear regulator alone would waste three quarters of that power. The 1.2 → 1.0 V regulator wastes 0.2 / 1.2 of its input, which is row 10 of the power table. A switched-capacitor converter from 4 V, at about 80 %, would be an alternative. If the ±4 V rails came from an 80 %-efficient charge pump instead of directly from the rectifier, the worst case would rise by 1.229 / 0.8 − 1.229 = 0.31 mW of load, or 0.44 mW dissipated.

**Power loss.** The implant has no battery, so removing the headpiece or bumping the coil cuts power. A power-on reset and a brownout detector disable all 64 drivers and open the switch matrix as soon as the rectified supply drops, and stimulation restarts only after the start-up check. Separately, stimulation ramps to zero if no valid touch packet arrives for 15 ms.

**Start-up and memory.** The 1 kB site table (thresholds, maxima, groups and usable flags) is kept in non-volatile memory on the S1 chip. The decoder's 0.88 Mbit of weights sit in SRAM, which loses its content without power, so the headpiece stores them and reloads them over the 106 kb/s downlink at start-up: 0.88 Mbit / 106 kb/s ≈ 8.3 s. Stimulation and decoding stay off until both the table and the weights pass a CRC check.

**Impedance check.** The S1 chip estimates each site's impedance from its own stimulation pulses: one shared ADC behind a multiplexer samples the electrode voltage at the end of a phase, and the voltage divided by the known current gives the impedance. This needs no recording front end, so it works whether or not S1 recording is kept. Open or degraded sites are flagged and routed around by the switch matrix, and the measured values replace our 50 kΩ assumption in the compliance budget.

## Wireless power and data link

One 13.56 MHz inductive link carries both power and data. Its receiving coil sits outside the titanium package, beside it on the skull, because a metal case would block the field. The materials team notes that Wise et al. recommend carriers below 10 MHz for links of a few centimetres; we keep 13.56 MHz because the demodulators and batteryless links cited here run at it, and 6.78 MHz remains the alternative to decide with the materials team. Data going in uses amplitude-shift keying (ASK) at a raw rate of about 106 kb/s. Data coming out uses load-shift keying (LSK) at 100 kb/s or more. There is no radio inside the body. A batteryless implant already runs half-duplex 106 kb/s down and 30 kb/s up over one 13.56 MHz power link ([Sensors and Actuator Networks, 2025](https://www.mdpi.com/2224-2708/14/5/92)). Passive phase-shift keying reaches 1.35 Mb/s up over the same carrier ([UCL PPSK](https://discovery-pp.ucl.ac.uk/id/eprint/1529004/1/07569109.pdf)). So our need is well inside what has been demonstrated.

The raw bit rate matters more than the average traffic. Our average traffic is small: about 3 kb/s out (arm commands) and about 13 kb/s in (one 64-bit touch packet every 5 ms). What sets latency is how long one packet spends on air. A 64-bit packet takes 21 ms at 3 kb/s, 2.1 ms at 30 kb/s, and about 0.6 ms at 100 kb/s. We therefore specify raw rates of at least 100 kb/s each way, even though the average load is small. The one heavy stream is calibration: the M1 chip then sends all 192 channel features every 20 ms, 192 × 8 bits / 20 ms = 76.8 kb/s, about 80 kb/s with headers. This fits the 100 kb/s raw uplink because touch packets are paused during that step.

The link is half-duplex, so the two directions take turns. Each 5 ms frame holds one 0.6 ms downlink packet, and one 0.64 ms uplink packet is needed every 20 ms, so the uplink fits easily in the 4.4 ms left in a frame.

On the implant side, the rectifier and regulators set how much of the received power turns into heat. Published 13.56 MHz receivers reach 72–75 % efficiency ([references in Sci. China Inf. Sci. 2022](https://ouci.dntb.gov.ua/works/4Vg0q1Yl)). We budget η = 70 %, so the implant dissipates the circuit load divided by 0.7.

**External headpiece power.** The implant takes in at most about 3.9 mW. Coil-to-coil efficiency for a small implanted coil a few millimetres to a centimetre under the scalp is typically 10–30 %. At 20 %, the headpiece must transmit about 20 mW, or about 25 mW from its battery with an 80 %-efficient coil driver. With its microcontroller and the connection to the robot, the headpiece uses roughly 50 mW in total. A 300 mAh lithium battery (about 1.1 Wh) then lasts about 22 hours, and a 500 mAh cell about a day and a half. These are estimates; the link efficiency is the number to confirm.

## Tactile features: measure, analyze, encode

The hand measures, a program on the robot side analyzes the sensors and computes the stimulation intensity for each zone, the external headpiece forwards it through the link, and the S1 chip turns it into pulses on the right electrodes. The robot-side program runs on a small computer beside the robot, not inside the UR control box: the ur\_rtde library that sends arm commands is a client that runs on an external computer, and code inside the control box would have to be packaged as a URCap.

| Stage | Where | What it does |
| --- | --- | --- |
| Measure | PSYONIC hand and UR arm (bought) | 12 fingertip sensors on thumb and index, 6 per finger ([PSYONIC API](https://pypi.org/project/ability-hand/)); finger positions and motor current; wrist force and torque ([UR5e datasheet](https://cdn.elmark.com.pl/34833)) |
| Analyze | Robot side: small computer beside the robot | Per finger: zone pressures, contact state, onset and release, slip, optional stiffness; biomimetic intensity per zone; grip reflex on slip |
| Forward | External headpiece | One 64-bit packet per 5 ms through the 13.56 MHz link, about 13 kb/s |
| Encode and stimulate | S1 chip | Per-electrode scaling, 40 µA hardware cap, pulse timing, link-loss safety, recalibration |

Slip is flagged when, during holding, the pressure on a finger drops suddenly while its motor current stays the same (the hand still grips as hard), when the centre of pressure moves quickly across the finger's 6 sensors, or when sideways force at the wrist nears the grip force. Because the analysis runs outside the body, the wrist force costs no link bandwidth. Stiffness is the rise in force per unit of finger closure in the first \~100 ms after contact. The hand closes at a steady speed, so the onset term already tracks how fast force rises, and stiffness may come across without a new term; we test that first with foam, rubber and wooden objects.

The encoder rule gains one term: a short high-frequency burst on slip, computed within the 5 ms frame. Contact location chooses which of the finger's electrode groups receives the pulses.

*I* = *a* · *F* + *b* · onset + *c* · release + *d* · slip

### Processing on the robot side and on the S1 chip

The work is split in two. Every 5 ms frame (200 Hz), the robot-side program runs steps 1–6 and the S1 chip runs steps 7–10.

1. Robot side: read the 12 fingertip sensors, finger positions, motor current and wrist force; subtract each sensor's offset and apply its gain.
2. Sum each finger's sensors per zone (tip, middle, base: 2 sensors each) and in total.
3. Update each finger's contact state (none, onset, hold, release), with hysteresis on the contact threshold.
4. Low-pass the frame-to-frame force change: its positive part is the onset term, its negative part the release term.
5. Flag slip as above, tighten the grip at once (the reflex) and hold a burst flag for about 50 ms; optionally estimate stiffness over the first 100 ms of contact.
6. Compute the intensity per zone with the rule above, clipped to 0–1, and pack the 6 zone intensities with a header and CRC into one 64-bit packet.
7. S1 chip: check the packet's CRC. After 3 missing or corrupt frames (15 ms), stimulation ramps to zero.
8. Set each zone's pulse rate from its intensity, from about 50 Hz while holding to 300 Hz in bursts.
9. For each of the zone's 4 sites: current = threshold + intensity × (maximum − threshold), then the 40 µA hardware cap.
10. Fire all active sites together and signal the M1 chip to blank 1 ms of recording.

The coefficients a, b, c and d live in the robot-side program and are shared per finger, not set per site. They are fitted on TouchSim and adjusted with the patient's reports, so retuning them is a software update outside the body. Each site on the S1 chip stores only its threshold, maximum, group number and a usable flag, about 3 bytes, so the 256-site table takes under 1 kB of non-volatile memory. Recalibration from evoked responses updates only the thresholds and maxima.

The chip's share is the packet check and 24 electrode scalings per frame, a few thousand operations per second and well under 0.1 µW, so row 5 of the power table is unchanged. The robot side's share is trivial for any small computer.

We run the analysis on the robot side for four reasons. It is easier to retune. It sends less through the skin: about 13 kb/s instead of 36 kb/s of raw sensor values, and 0.6 ms of airtime per packet instead of 1.7 ms. It keeps the implant chip simpler, with less to verify and nothing to update after surgery. And the grip reflex can act without a round trip through the implant. It costs no robustness, because if the link drops no touch data reaches the implant wherever the analysis runs. Processing load was not the reason: on the chip the same analysis would cost under 0.1 µW.

The hand is powered from the arm side, not from the implant budget. The UR marketplace listing asks for a 12 V supply of 10 A or more ([Ability Hand for UR](https://www.universal-robots.com/marketplace/products/01tTt00000BlAFJIA3/)), which a UR5e tool flange may not provide, so a separate supply may be needed.

## Package and thermal

We put all the electronics in one skull-recessed titanium package and put no chips on the cortex. Polyimide ribbons connect the package to the M1 and S1 arrays. M1 and S1 face each other across the central sulcus, so one craniotomy reaches both, and one power-management circuit and one clock serve both chips. The receiving coil is not inside the case: a titanium shell blocks the 13.56 MHz field, so the coil lies flat on the skull beside the package, under the scalp and as close to the skin as possible. It is encapsulated on its own and enters the package through two feedthroughs.

The literature shows why no chip should sit on the cortex:

| Configuration | Power for about 1 °C rise | Source |
| --- | --- | --- |
| One 2 × 2 × 0.5 mm chip in tissue | 5.3 mW | [Silay et al., 2011](https://dx.doi.org/10.1007/s12668-011-0009-2) |
| Two such chips 10 mm apart | 9.3 mW | [Silay et al., 2011](https://dx.doi.org/10.1007/s12668-011-0009-2) |
| Chip mounted on a Utah array | 13 mW gave 1.2–1.3 °C | [Kim et al., Utah](https://collections.lib.utah.edu/dl_files/9d/e4/9de41d767090905977076379a64caa1a98416ac1.pdf) |
| Wireless cortical implant, one body / two bodies | 17.5 mW / 35 mW | [Silay et al., 2011](https://dx.doi.org/10.1007/s12668-011-0009-2) |
| Titanium skull unit | 47–81 mW | [Serrano-Amenos et al., 2023](https://doaj.org/article/aa30c8354ca8418a8cf79bf38a0b4b80) |

Our 15 mW ceiling is therefore conservative for a skull-recessed package. Our estimated 2.1–3.9 mW leaves a wide margin.

The real limit of the package is its feedthrough count, not its temperature. Keeping the switch matrix inside the package, we need about 460 hermetic feedthroughs: 192 for M1, 256 for S1, and about 10 for references, grounds and the coil. Co-fired alumina–platinum feedthroughs reach 1,000 per cm² ([Gill et al., 2013](https://www.cambridge.org/core/product/895CB985606F9C737CEA31AAE76B2F8E)), and an Al₂O₃ system reaches 20 per mm² ([PubMed 22255880](https://www.pubmed.gov/22255880/)). So 460 feedthroughs fit in about 23–46 mm², a plate about 5–7 mm on a side. One package with the switch matrix inside is therefore feasible. Moving the switch matrix out to the array would cut S1 to 64 feedthroughs, but it would put active silicon on the cortex, so we do not do it.

## Power budget

The implant dissipates about 2.2 mW while grasping, 3.9 mW in the worst case and 2.1 mW at rest, or 2.2 mW averaged over a day with 20 % grasping. Recording dominates, not stimulation or computation: the 192-channel M1 front end alone is 0.88 mW of the 1.6 mW load during a typical grasp. Rest and grasping are close, because recording and the driver bias run all the time. Each row is numbered; its calculation and source follow the table.

| # | Block | Grasping (mW) | Worst case (mW) | Rest (mW) | Basis |
| --- | --- | --- | --- | --- | --- |
| 1 | M1 recording, 192 ch | 0.883 | 0.883 | 0.883 | Measured |
| 2 | NN decoder (32-unit): compute + weight memory | 0.016 | 0.016 | 0.005 | Calculated from measured energies |
| 3 | LFP gate | 0.002 | 0.002 | 0.002 | Calculated |
| 4 | S1 recording, 64 ch (calibration only) | 0 | 0 | 0 | Scaled from row 1; 0.294 mW for a few minutes a day |
| 5 | Electrode mapping + pulse sequencer | 0.010 | 0.010 | 0.010 | Calculated + assumption |
| 6 | Stimulation delivered | 0.051 | 1.229 | 0 | Calculated |
| 7 | Driver bias, 64 drivers | 0.353 | 0.353 | 0.353 | Measured per driver, 2× margin |
| 8 | ASK demodulator + LSK modulator | 0.050 | 0.050 | 0.050 | Measured + assumption |
| 9 | Safety monitors: power-on reset, brownout, link watchdog | 0.005 | 0.005 | 0.005 | Assumption |
| 10 | Low-voltage regulator loss, 1.2 → 1.0 V | 0.193 | 0.193 | 0.191 | Calculated |
|  | **Circuit load** | **1.563** | **2.741** | **1.499** | Sum of rows 1–10 |
| 11 | **Dissipated in implant (load / 0.70)** | **2.23** | **3.92** | **2.14** | Calculated |

### How each row is calculated

**Row 1 · M1 recording.** MiBMI records 192 channels and runs a 512-channel decoder in 65 nm CMOS, consuming 883 µW in total. It is a two-chip set, a recording chip and a decoding chip, about 8 mm² together (\[EPFL\](https://actu.epfl.ch/news/an-entire-brain-machine-interface-on-a-chip-7)); the 2.46 mm² in the paper's title is the area of the BMI chipset itself ([Shaeri et al., 2024](https://x-mol.com/paper/1827401830204252160)). We charge the full 883 µW to recording alone. This over-counts, because MiBMI's own decoder is included in that figure. The front end stays on at rest, because the LFP gate needs its signal.

**Row 2 · NN decoder.** We use the shallow network of [Willsey et al., 2022](https://chestekresearch.engin.umich.edu/wp-content/uploads/sites/189/2022/11/Willseyetal_Nature_2022.pdf) with its hidden layers narrowed from 256 to 32 units (see Design risks, item 1). It keeps the time-feature layer (3 time bins → 16 features per electrode), uses 192 electrodes, and has 4 outputs (3D hand velocity and one hand-opening value: thumb and index make the pinch, the other fingers follow). The multiply-accumulates (MACs) per inference are:

*N*MAC = (192 · 3 · 16) + (16 · 192 · 32) + (32 · 32) + (32 · 32) + (32 · 4) = 9,216 + 98,304 + 1,024 + 1,024 + 128 ≈ 1.10 × 10⁵ per inference

One inference per 20 ms bin gives 5.48 × 10⁶ MAC/s. In 45 nm CMOS, an 8-bit multiply costs 0.2 pJ, an 8-bit add 0.03 pJ, and a 32-bit read from an 8 KB SRAM 5 pJ ([Horowitz, ISSCC 2014, table via MIT 6.5930](https://csg.csail.mit.edu/6.5930/lectures/L11-Advanced_Tech.pdf)). Fetching one 8-bit weight therefore costs 5 / 4 = 1.25 pJ, and one MAC about 1.5 pJ. We use 2 pJ to allow for 65 nm.

*P*compute = 5.48 × 10⁶ MAC/s × 2 pJ = 0.011 mW

The network has about 110,000 weights, which is 0.88 Mbit (0.84 Mb in binary units) at 8 bits. A 65 nm low-leakage SRAM macro leaks 12 µA per Mb at its 0.5 V retention voltage, array and periphery included ([Wang et al., Intel, JSSC 2008](https://search.isc.ac/inventory/49/1051357.htm)). That is 0.5 V × 12 µA = 6 µW per Mb, so the weight memory leaks 0.84 × 6 µW = 0.005 mW, at rest too. The total is 0.011 + 0.005 = 0.016 mW.

**Row 3 · LFP gate.** Per channel and per sample, the gate runs one biquad band-pass filter (5 multiplies, 4 adds), then squares and accumulates (1 multiply, 1 add). That is 6 multiplies and 5 adds. With 16-bit operations at 0.62 pJ per multiply and 0.18 pJ per add (45 nm; [Pedram et al.](https://ar5iv.labs.arxiv.org/html/1602.04183)), this is 4.6 pJ per sample. At 1 kS/s on 192 channels: 1.92 × 10⁵ s⁻¹ × 4.6 pJ = 0.9 µW. Doubled for 65 nm, it is 1.8 µW, about 0.002 mW.

**Row 4 · S1 recording.** From row 1, 883 µW / 192 channels = 4.6 µW per channel, an upper bound; for 64 channels, 64 × 4.6 µW = 0.294 mW. It runs only during calibration: the daily test pulses for recalibration, a few minutes a day. It is off while grasping, because recording on the same shanks during ±4 V pulses would saturate the front end. In the daily mean it is negligible.

**Row 5 · Electrode mapping and pulse sequencer.** The touch analysis runs on the robot side. The S1 chip's share is the packet check and 24 electrode scalings per 5 ms frame, a few thousand operations per second and well under 0.1 µW. The real cost is the sequencer that times pulses for 64 drivers. We allocate 10 µW for its clock and leakage, which is an assumption.

**Row 6 · Stimulation delivered.** As derived in the Stimulator section, each biphasic pulse costs 64 nJ (4 V × 2 × 8 nC). A typical grasp is 8 sites × 100 Hz × 64 nJ = 0.051 mW. The worst case is 64 × 300 Hz × 64 nJ = 1.229 mW.

**Row 7 · Driver bias.** A compact current-mode stimulator driver for 10–250 µA outputs measured 2.76 µW of quiescent power per driver, in 0.35 µm CMOS ([Toronto, ISCAS 2011](https://www.eecg.utoronto.ca/~roman/professional/pubs/pdfs/iscas11_stim.pdf)). Our drivers run from ±4 V in a different high-voltage process, so we carry them at 2× that figure, 5.52 µW. We keep all 64 drivers biased at all times: 64 × 5.52 µW = 0.353 mW in every state. As a cross-check, a complete 64-channel recording-and-stimulation IC dissipates 700 µW in a typical configuration ([Johnson et al.](https://escholarship.org/content/qt3mf489zc/qt3mf489zc_noSplash_afd59fa7f3c5c45d9cc0af7eade9c43e.pdf)). That is the same order as our S1 rows 4–7, which total 0.41 mW during a grasp.

**Row 8 · Data link circuits.** An EPFL ASK demodulator consumes 45 µW at 1.8 V and reaches about 2.7 Mb/s at 13.56 MHz ([Karimi et al., 2024](https://infoscience.epfl.ch/handle/20.500.14299/242865)), far above our 106 kb/s. The LSK modulator is a switch that detunes the coil; we allocate 5 µW for its gate drive, which is an assumption. The total is 0.050 mW, always on.

**Row 9 · Safety monitors.** A power-on reset, a brownout detector and the link watchdog are a few comparators and a counter. We allocate 5 µW for them, which is an assumption. The impedance check's shared ADC and multiplexer are included in this allocation.

**Row 10 · Low-voltage regulator.** Rows 1–3, 5, 8 and 9 run at 1.0 V from the 1.2 V output of the dual-output rectifier. That is 0.966 mW while grasping and in the worst case, and 0.955 mW at rest. A linear regulator passes the same current at 1.2 V that the load draws at 1.0 V, so it wastes (1.2 / 1.0 − 1) = 0.20 of the load: 0.20 × 0.966 = 0.193 mW and 0.20 × 0.955 = 0.191 mW. The drivers and the stimulation (rows 6 and 7) run from the ±4 V outputs directly.

**Row 11 · Receiver efficiency.** Published 13.56 MHz receivers include a 72 %-efficient passive rectifier and a receiver with 75.4 % power-conversion efficiency ([references in Sci. China Inf. Sci. 2022](https://ouci.dntb.gov.ua/works/4Vg0q1Yl)). We use η = 0.70 for the rectifier; the regulator loss is already in row 10. The lost power is dissipated in the implant too, so dissipation = load / η: 1.563 / 0.70 = 2.23 mW, 2.741 / 0.70 = 3.92 mW, and 1.499 / 0.70 = 2.14 mW.

The mean over a day with 20 % grasping is:

*P*mean = 0.2 × 2.23 mW + 0.8 × 2.14 mW ≈ 2.2 mW

### Channel selection on M1

M1 recording is the largest row: 0.883 mW, 56 % of the load while grasping and 59 % at rest. We keep all 192 electrodes implanted but power only the channels we need, in two tiers. The hardware change is per-channel power gating of the front-end amplifiers, plus a fast-reset switch on each amplifier's high-pass filter so a channel settles within about 5–20 ms of waking. Without that switch, a filter corner near 1 Hz would take hundreds of milliseconds to settle.

**Rest: 16 channels for the LFP gate.** Beta-band power (13–30 Hz) is spread widely across M1, so 16 channels spread over both arrays are enough to detect the beta drop that precedes movement. The other 176 amplifiers are off. When the gate fires, it wakes them. Because beta power starts falling 100–200 ms before movement, the 5–20 ms settling time is mostly hidden.

**Grasping: the 96 most informative channels.** During the daily calibration, the external side ranks all 192 channels by their contribution to decoding (or by spike signal-to-noise ratio), retrains the decoder on the top 96, and reloads it. Halving the input layer halves the weights, from 0.88 to 0.45 Mbit, so a reload takes 0.45 Mbit / 106 kb/s ≈ 4.2 s instead of 8.3 s, and decoder compute falls from 0.011 to 0.006 mW. Re-ranking every day lets the selection follow units as they drift or are lost over months, which is why we keep 192 physical electrodes rather than implanting fewer.

The saving depends on how much of the front end's power is shared between channels (bias, ADC, clock, digital back end), which cannot be switched off per channel. MiBMI does not publish that split. We therefore give two bounds: all of the 4.6 µW per channel can be gated, or 25 % of the front end's power is shared and stays on, which is an assumption.

| Dissipated in implant (mW) | All 192 channels (baseline) | Selection, 25 % shared | Selection, nothing shared |
| --- | --- | --- | --- |
| M1 recording at rest (16 ch) | 0.883 | 0.276 | 0.074 |
| M1 recording while grasping (96 ch) | 0.883 | 0.552 | 0.442 |
| Rest | 2.14 | 1.10 | 0.75 |
| Grasping | 2.23 | 1.65 | 1.46 |
| Worst case | 3.92 | 3.34 | 3.15 |
| Daily mean (20 % grasping) | 2.2 | 1.2 | 0.9 |

So channel selection cuts the daily mean roughly in half, mostly at rest. With 25 % shared, the 25 % share is 0.221 mW, each gated channel costs 0.883 × 0.75 / 192 = 3.45 µW, and 16 channels give 0.221 + 16 × 3.45 µW = 0.276 mW. The other rows follow the same way: replace row 1 in the load, add the smaller decoder, recompute the regulator loss in row 10 as 0.20 of the smaller low-voltage load, and divide by 0.70. With M1 gated, the 0.353 mW of driver bias becomes the largest load at rest; the drivers could be gated the same way and woken on contact, but we have not budgeted that.

One result is still to be checked: whether decoding accuracy holds with 96 channels. The offline validation of the decoder should be run at both 192 and 96 channels, and if accuracy drops, the grasping tier can use more channels at about 3.5–4.6 µW each. The main power table above stays at 192 channels as the conservative reference.

The worst case of 3.9 mW is 26 % of our 15 mW ceiling and an order of magnitude below the 47–81 mW skull-unit range. If the ±4 V rails came from an 80 %-efficient charge pump instead of directly from the rectifier, the worst case would rise by about 0.44 mW to 4.4 mW, still 29 %. The remaining risks and their fixes are in Design risks and fixes, below.

## Latency budget

We budget the two loops separately, because they answer different questions. The motor loop is how fast the arm follows intent. The touch loop is how fast the patient feels a contact. The electronics add about 26 ms to the motor loop and about 5–20 ms to the touch loop. The motor loop is dominated by its 20 ms bin, the touch loop by the 5 ms encoder frame and the wait for the next pulse, not by the radio.

| Loop | Step | Latency (ms) | Basis |
| --- | --- | --- | --- |
| Motor | M1 feature bin | 20 | Design choice (one bin) |
| Motor | Gate + NN decoder on chip | < 1 | Estimate: small network, decoder awake |
| Motor | Uplink, 64-bit packet at 100 kb/s | 0.6 | Calculated |
| Motor | External headpiece | \~1 | Assumption |
| Motor | UR arm command cycle | 2 | 500 Hz control ([UR datasheet](https://www.universal-robots.com/media/1827367/05_2023_collective_data-sheet.pdf)) |
| Motor | Hand command over UART | \~2 | A third-party ROS interface runs a 500 Hz loop ([UIUC](https://gh.r-mj.com/uiuckimlab/psyonic_hand_control)) |
| **Motor** | **Electronics total** | **\~26** | Plus mechanical motion; full hand closure takes 0.2 s ([UR marketplace](https://www.universal-robots.com/marketplace/products/01tTt00000BlAFJIA3/)); first movement after rest: see below |
| Touch | Hand pressure sampling | \~2 | Assumption, 500 Hz; at least 200 Hz is needed for 5 ms frames, and at 200 Hz this step is 5 ms (worst case 22.6 ms) |
| Touch | Robot-side analysis | \~1 | Assumption |
| Touch | External headpiece | \~1 | Assumption |
| Touch | Downlink, 64-bit packet at 106 kb/s | 0.6 | Calculated |
| Touch | Wait for next encoder frame | 0–5 | 5 ms frame |
| Touch | First pulse of the train at 100 Hz | 0–10 | Calculated |
| **Touch** | **Electronics total** | **\~5–20** | Sum: 4.6–19.6 |

_Latency chart (worst case per step): see page 12 of [`NeuroTact_Electronics_and_Power.pdf`](NeuroTact_Electronics_and_Power.pdf)._

The perceptual delay of ICMS itself is larger than our electronics. When intensity-matched, vibration on the skin was felt 48 ms faster than ICMS, although in a temporal-order task the two seemed simultaneous ([Christie et al., 2022](https://pubmed.ncbi.nlm.nih.gov/35644516/)). Stronger ICMS is perceived faster, and multi-channel ICMS gave reaction times comparable to natural touch ([David et al.](https://www.vis.caltech.edu/documents/22267/David_2022.pdf)). So we avoid adding delay: a 5 ms encoder frame throughout keeps the electronic touch delay at about 5–20 ms, or about 5–10 ms if the first pulse fires at the moment of contact.

The motor total assumes the decoder is already awake. On the first movement after rest, the LFP gate must first see beta power drop, which takes up to one smoothing window of 100–200 ms. Much of this is hidden, because beta power starts to fall before the movement itself begins, but the first grasp after a pause can still start a little late. We measure missed and late onsets when testing the gate.

## Design risks and fixes

Reviewing the design turned up five risks, and each has a fix that keeps the current architecture. The power table already includes fixes 1 and 2.

**1. Decoder memory.** A 256-unit network needs 7.35 Mbit of weights. With Intel's 0.667 µm² low-leakage memory cell ([Wang et al., Intel, JSSC 2008](https://search.isc.ac/inventory/49/1051357.htm)), the cells alone would take 4.9 mm², twice MiBMI's 2.46 mm² chipset and more than half of its 8 mm² two-chip total. We narrow the three hidden layers to 32 units. That leaves about 110,000 weights (0.88 Mbit, about 0.6 mm² of cells), costing 0.011 mW of computation and 0.005 mW of leakage. Willsey's network used 256 units, so the 32-unit version must be validated offline on recorded M1 data. The computing part starts with a linear (ridge-regression) decoder, 768 weights and under 0.1 µW, and keeps the network only if it decodes clearly better; row 2 budgets the network as the upper bound.

**2. Stimulator process.** ±4 V rails are more than 65 nm transistors tolerate. The S1 chip is therefore made in 0.18 µm high-voltage CMOS, the process used for a 16-channel stimulator with a ±20 V supply ([16-channel HV stimulator, BioMed Eng OnLine 2017](https://link.springer.com/10.1186/s12938-017-0385-0)). The M1 chip stays in 65 nm, and both dies sit in the same titanium package. The 2.76 µW driver figure came from a different process, so the budget carries it at 2×.

**3. Stimulation artifacts in M1.** Each S1 pulse appears as an artifact on the M1 channels. All active electrodes fire at the same instant, so each pulse period produces one artifact. We blank M1 for 1 ms around it: about 0.5 ms of biphasic pulse plus up to 0.4 ms of front-end recovery, which fast-recovery front ends achieve ([Hall et al., JSSC 2025](<https://bioee.ucsd.edu/papers/A%202.5%E2%80%9320%20kS:s%20In-Pixel%20Direct%20Digitization%20ECoG%20Front%20End%20With%20Submillisecond%20Stimulation%20Artifact%20Recovery%20-%20Hall%20(JSSC,%202025).pdf>)). This blanks 2 ms of each 20 ms bin at 100 Hz (10 %) and 6 ms at 300 Hz (30 %). The decoder's spike-band power is computed over the unblanked samples only and rescaled by their fraction, so every bin keeps its meaning. Artifact rejection of this kind has already been used in human closed-loop ICMS ([Weiss, 2018](https://core.ac.uk/download/158572558.pdf)). Blanking adds no latency.

**4. Headroom above perceptual threshold.** Human S1 detection thresholds started at a median of 31.5 µA at day 100 ([Hughes et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC8500669)), which leaves little room under a 40 µA cap. We keep the cap and code intensity in two other ways. One is the number of electrodes in a group, from 1 to 4. The other is pulse frequency, from 50 to 300 Hz, because detection thresholds fall as frequency rises up to about 250 Hz ([Kim et al., PNAS 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4679002)). With the PEDOT:PSS coating (about 3 mC/cm² on flexible shanks), the cap could rise to 60 µA at 1.2 mC/cm², still under 40 % of that limit.

**5. Coil field and Utah connection.** At 13.56 MHz, the safe exposure limit of 544 µW/mm² allows tens of mW into millimetre-sized implants ([Varkevisser et al., 2025](https://bioelectronics.tudelft.nl/~wout/documents/TCAS-I_2025_Varkevisser.pdf)), so our 3.9 mW worst case is well inside it. The Utah arrays are bonded to thin-film polyimide cables made in the same process as the S1 array. These replace the usual wire bundle and skull pedestal, and are owned by the materials teammate.

## Open values to confirm

| Value | Used here | Why it matters | Who |
| --- | --- | --- | --- |
| Impedance of our 1000 µm² SIROF sites | 50 kΩ at 1 kHz | Sets compliance voltage and stimulation power | Materials |
| Power of our velocity NN decoder | 0.016 mW with 32-unit hidden layers | The narrower network may lose accuracy; test it offline on recorded M1 data | Computer scientist |
| PSYONIC touch-sensor streaming rate | 500 Hz assumed; ≥ 200 Hz needed | First step of the touch loop | Electronics |
| Driver bias current per channel | 5.5 µW per driver (2× the 0.35 µm measurement) | 64× multiplier in the budget | Electronics |
| Coil-field tissue heating | Bounded: of \~20 mW sent, \~3.9 mW reaches the implant; even if the other \~16 mW were all absorbed in 10 g of scalp, SAR ≤ 1.6 W/kg, under the 2 W/kg limit | Adds to the thermal check | Electronics |

## Sources

- [Shaeri et al., MiBMI, IEEE JSSC 2024](https://x-mol.com/paper/1827401830204252160)
- [Hughes et al., SIROF and Pt arrays in human S1/M1 over 1500 days](https://pmc.ncbi.nlm.nih.gov/articles/PMC8500669)
- [Pittsburgh ICMS adaptation study (100 µA, 300 Hz limits)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10308851)
- [Cogan et al., SIROF on polyimide, J Biomed Mater Res B 2009](https://www.pubmed.gov/18837458/)
- [Chalmers, long-term stimulation through flexible polyimide shanks](https://research.chalmers.se/publication/540345/file/540345_Fulltext.pdf)
- [Silay et al., thermal analysis of a two-body cortical implant, 2011](https://dx.doi.org/10.1007/s12668-011-0009-2)
- [Kim et al., thermal impact of an active Utah array](https://collections.lib.utah.edu/dl_files/9d/e4/9de41d767090905977076379a64caa1a98416ac1.pdf)
- [Serrano-Amenos et al., skull-unit power budget, IEEE TNSRE 2023](https://doaj.org/article/aa30c8354ca8418a8cf79bf38a0b4b80)
- [Gill et al., high-density hermetic feedthroughs, MRS 2013](https://www.cambridge.org/core/product/895CB985606F9C737CEA31AAE76B2F8E)
- [Al₂O₃ high-density feedthroughs, PubMed 22255880](https://www.pubmed.gov/22255880/)
- [Batteryless implant with 13.56 MHz power and data, 2025](https://www.mdpi.com/2224-2708/14/5/92)
- [Passive phase-shift keying at 1.35 Mb/s, UCL](https://discovery-pp.ucl.ac.uk/id/eprint/1529004/1/07569109.pdf)
- [13.56 MHz power and data telemetry, Sci. China Inf. Sci. 2022](https://ouci.dntb.gov.ua/works/4Vg0q1Yl)
- [Universal Robots e-Series datasheet](https://www.universal-robots.com/media/1827367/05_2023_collective_data-sheet.pdf)
- [Ability Hand for UR arms](https://www.universal-robots.com/marketplace/products/01tTt00000BlAFJIA3/)
- [UIUC PSYONIC hand ROS interface](https://gh.r-mj.com/uiuckimlab/psyonic_hand_control)
- [Christie et al., perceived timing of ICMS, Brain Stimulation 2022](https://pubmed.ncbi.nlm.nih.gov/35644516/)
- [David et al., multi-channel ICMS reaction times](https://www.vis.caltech.edu/documents/22267/David_2022.pdf)

* [Willsey et al., shallow NN finger decoder, Nat. Commun. 2022](https://chestekresearch.engin.umich.edu/wp-content/uploads/sites/189/2022/11/Willseyetal_Nature_2022.pdf)
* [Horowitz, ISSCC 2014 energy table (via MIT 6.5930)](https://csg.csail.mit.edu/6.5930/lectures/L11-Advanced_Tech.pdf)
* [Pedram et al., Dark Memory and Accelerator-Rich System](https://ar5iv.labs.arxiv.org/html/1602.04183)
* [Wang et al., Intel 65 nm low-leakage SRAM, JSSC 2008](https://search.isc.ac/inventory/49/1051357.htm)
* [Toronto compact current-mode stimulator, ISCAS 2011](https://www.eecg.utoronto.ca/~roman/professional/pubs/pdfs/iscas11_stim.pdf)
* [Johnson et al., 64-channel neuromodulation IC](https://escholarship.org/content/qt3mf489zc/qt3mf489zc_noSplash_afd59fa7f3c5c45d9cc0af7eade9c43e.pdf)
* [Karimi et al., EPFL ASK demodulator, TCAS-II 2024](https://infoscience.epfl.ch/handle/20.500.14299/242865)
* [16-channel stimulator in 0.18 µm HV CMOS, BioMed Eng OnLine 2017](https://link.springer.com/10.1186/s12938-017-0385-0)
* [Hall et al., sub-ms stimulation artifact recovery, JSSC 2025](<https://bioee.ucsd.edu/papers/A%202.5%E2%80%9320%20kS:s%20In-Pixel%20Direct%20Digitization%20ECoG%20Front%20End%20With%20Submillisecond%20Stimulation%20Artifact%20Recovery%20-%20Hall%20(JSSC,%202025).pdf>)
* [Weiss, closed-loop BCI with ICMS and artifact rejection, 2018](https://core.ac.uk/download/158572558.pdf)
* [Kim et al., sensitivity to ICMS of primate S1, PNAS 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4679002)
* [Varkevisser et al., multichannel stimulator power, TCAS-I 2025](https://bioelectronics.tudelft.nl/~wout/documents/TCAS-I_2025_Varkevisser.pdf)

- [PSYONIC Ability Hand Python API](https://pypi.org/project/ability-hand/)
- [UR5e datasheet, force/torque sensing](https://cdn.elmark.com.pl/34833)
